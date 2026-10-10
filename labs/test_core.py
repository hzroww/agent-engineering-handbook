import concurrent.futures
import threading
import unittest

from core import RequestRegistry, classify_reply, cost_micros, safe_cut


class CostTests(unittest.TestCase):
    def test_cached_tokens_are_not_counted_twice(self):
        self.assertEqual(cost_micros(10000, 6000, 1000, "2", "0.5", "8"), 19000)

    def test_zero_usage_is_zero(self):
        self.assertEqual(cost_micros(0, 0, 0, "2", "0.5", "8"), 0)

    def test_invalid_usage_is_not_silently_billed(self):
        for counts in [(-1, 0, 0), (2, 3, 0), (0, 0, -1), (1.5, 0, 0)]:
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                cost_micros(*counts, "2", "0.5", "8")

    def test_nonfinite_or_negative_rates_are_rejected(self):
        for rate in ["NaN", "Infinity", "-2"]:
            with self.subTest(rate=rate), self.assertRaises(ValueError):
                cost_micros(2, 0, 1, rate, "0", "1")

    def test_rounding_is_explicit_ceiling_to_micro_unit(self):
        self.assertEqual(cost_micros(1, 0, 0, "0.5", "0", "1"), 1)


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"type": "message"},
            {"type": "call", "call_id": "c1"},
            {"type": "result", "call_id": "c1"},
            {"type": "message"},
        ]

    def test_cannot_split_call_from_result(self):
        self.assertFalse(safe_cut(self.items, 2))

    def test_whole_exchange_can_be_summarized(self):
        self.assertTrue(safe_cut(self.items, 3))

    def test_whole_exchange_can_be_retained(self):
        self.assertTrue(safe_cut(self.items, 1))

    def test_orphan_result_is_never_a_valid_history(self):
        self.assertFalse(safe_cut([{"type": "result", "call_id": "missing"}], 0))

    def test_duplicate_result_is_invalid(self):
        items = self.items + [{"type": "result", "call_id": "c1"}]
        self.assertFalse(safe_cut(items, 0))

    def test_result_before_call_is_invalid(self):
        self.assertFalse(safe_cut(list(reversed(self.items)), 0))

    def test_unfinished_call_is_not_summarized(self):
        items = [{"type": "call", "call_id": "pending"}]
        self.assertTrue(safe_cut(items, 0))
        self.assertFalse(safe_cut(items, 1))

    def test_boundary_outside_history_is_invalid(self):
        self.assertFalse(safe_cut(self.items, 20))


class ReplyTests(unittest.TestCase):
    def test_length_is_incomplete_even_if_text_exists(self):
        self.assertEqual(classify_reply("length", text="partial"), "incomplete")

    def test_unfinished_json_does_not_execute(self):
        self.assertEqual(classify_reply("tool_calls", calls=['{"q":']), "invalid")

    def test_complete_call_can_continue(self):
        self.assertEqual(classify_reply("tool_calls", calls=['{"q":"test"}']), "tools")

    def test_normal_text_is_completed(self):
        self.assertEqual(classify_reply("stop", text="answer"), "completed")

    def test_empty_reply_is_failure(self):
        self.assertEqual(classify_reply("stop"), "empty")

    def test_json_array_is_not_tool_argument_object(self):
        self.assertEqual(classify_reply("tool_calls", calls=["[]"]), "invalid")

    def test_unknown_finish_reason_is_not_success(self):
        self.assertEqual(classify_reply("mystery", text="answer"), "incomplete")


class IdempotencyTests(unittest.TestCase):
    def test_retry_returns_original_run(self):
        registry = RequestRegistry()
        first = registry.accept("u1", "k", {"q": "one"})
        self.assertEqual(registry.accept("u1", "k", {"q": "one"}), first)

    def test_same_key_with_changed_payload_conflicts(self):
        registry = RequestRegistry()
        registry.accept("u1", "k", {"q": "one"})
        with self.assertRaises(ValueError):
            registry.accept("u1", "k", {"q": "two"})

    def test_users_do_not_share_request_identity(self):
        registry = RequestRegistry()
        self.assertNotEqual(
            registry.accept("u1", "k", {"q": "one"}),
            registry.accept("u2", "k", {"q": "one"}),
        )

    def test_key_order_is_not_semantic_difference(self):
        registry = RequestRegistry()
        first = registry.accept("u1", "k", {"a": 1, "b": 2})
        self.assertEqual(registry.accept("u1", "k", {"b": 2, "a": 1}), first)

    def test_payload_mutation_cannot_change_existing_fingerprint(self):
        registry = RequestRegistry()
        payload = {"q": "one"}
        registry.accept("u1", "k", payload)
        payload["q"] = "two"
        with self.assertRaises(ValueError):
            registry.accept("u1", "k", payload)

    def test_simultaneous_duplicates_create_only_one_run(self):
        registry = RequestRegistry()
        barrier = threading.Barrier(8)
        def submit(_):
            barrier.wait(timeout=5)
            return registry.accept("u1", "k", {"q": "one"})
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            runs = list(pool.map(submit, range(8)))
        self.assertEqual(len(set(runs)), 1)

    def test_empty_identity_is_rejected(self):
        for owner, key in [("", "k"), ("u", "")]:
            with self.subTest(owner=owner), self.assertRaises(ValueError):
                RequestRegistry().accept(owner, key, {"q": "one"})


if __name__ == "__main__":
    unittest.main()

