"""Tiny teaching model; deliberately not a networked or durable Agent server."""
from decimal import Decimal, ROUND_CEILING
import hashlib
import json
import threading
import uuid


def cost_micros(input_tokens, cached_tokens, output_tokens, input_rate, cache_rate, output_rate):
    counts = (input_tokens, cached_tokens, output_tokens)
    if any(type(value) is not int or value < 0 for value in counts):
        raise ValueError("token counts must be non-negative integers")
    if cached_tokens > input_tokens:
        raise ValueError("cached tokens are included in input in this lab")
    rates = tuple(Decimal(str(value)) for value in (input_rate, cache_rate, output_rate))
    if any(not rate.is_finite() or rate < 0 for rate in rates):
        raise ValueError("rates must be finite and non-negative")
    # USD / million tokens × micro-USD / USD cancels the million factor.
    amount = ((input_tokens - cached_tokens) * rates[0]
              + cached_tokens * rates[1] + output_tokens * rates[2])
    return int(amount.to_integral_value(rounding=ROUND_CEILING))


def safe_cut(items, boundary):
    if not 0 <= boundary <= len(items):
        return False
    calls, results = {}, {}
    for index, item in enumerate(items):
        kind = item.get("type")
        if kind not in ("call", "result"):
            continue
        call_id = item.get("call_id")
        if not call_id:
            return False
        if kind == "call":
            if call_id in calls:
                return False
            calls[call_id] = index
        else:
            if call_id not in calls or call_id in results:
                return False
            results[call_id] = index
    for call_id, call_index in calls.items():
        result_index = results.get(call_id)
        if result_index is None:
            if call_index < boundary:
                return False
        elif (call_index < boundary) != (result_index < boundary):
            return False
    return True


def classify_reply(finish_reason, text="", calls=()):
    if finish_reason not in ("stop", "tool_calls"):
        return "incomplete"
    if calls:
        try:
            arguments = [json.loads(raw) for raw in calls]
        except (ValueError, TypeError):
            return "invalid"
        if any(not isinstance(value, dict) for value in arguments):
            return "invalid"
        return "tools"
    return "completed" if text.strip() else "empty"


class RequestRegistry:
    """Only demonstrates same-process atomic identity; not durable or distributed."""

    def __init__(self):
        self._lock = threading.Lock()
        self._records = {}

    def accept(self, owner, key, payload):
        if not owner or not key:
            raise ValueError("owner and request key are required")
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
        fingerprint = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        identity = (owner, key)
        with self._lock:
            existing = self._records.get(identity)
            if existing:
                previous_fingerprint, run_id = existing
                if previous_fingerprint != fingerprint:
                    raise ValueError("request key reused with a different payload")
                return run_id
            run_id = str(uuid.uuid4())
            self._records[identity] = (fingerprint, run_id)
            return run_id
