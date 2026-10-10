import tempfile
import unittest
from pathlib import Path

from scripts.book import check_markdown, render_book


class BookTests(unittest.TestCase):
    def test_render_keeps_content_and_uses_unique_chapter_anchors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapter = root / "chapters" / "01-demo.md"
            chapter.parent.mkdir()
            chapter.write_text("# 示例\n\n解释。\n", encoding="utf8")
            result = render_book([chapter], root)
            self.assertIn('id="chapters-01-demo"', result)
            self.assertIn("解释。", result)
            self.assertIn("#chapters-01-demo", result)

    def test_render_rebases_relative_links_in_merged_book(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapter = root / "chapters" / "01-demo.md"
            chapter.parent.mkdir()
            chapter.write_text("# 示例\n\n[练习](../labs/README.md)\n", encoding="utf8")
            self.assertIn("[练习](labs/README.md)", render_book([chapter], root))

    def test_missing_local_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("# 示例\n\n[bad](missing.md)\n", encoding="utf8")
            self.assertTrue(check_markdown(path, root))

    def test_unclosed_code_fence_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("# 示例\n\n```python\nx=1\n", encoding="utf8")
            self.assertTrue(check_markdown(path, root))

    def test_valid_document_with_external_link_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("# 示例\n\n[规范](https://example.com/a)\n", encoding="utf8")
            self.assertEqual(check_markdown(path, root), [])


if __name__ == "__main__":
    unittest.main()

