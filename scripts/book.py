"""Build the single-volume Markdown from the hand-edited sources."""
from pathlib import Path
import argparse
import re
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")


def render_book(sources, root):
    toc, sections = [], []
    for source in sources:
        relative = source.relative_to(root)
        anchor = relative.with_suffix("").as_posix().replace("/", "-")
        content = source.read_text(encoding="utf8")
        title = content.splitlines()[0].removeprefix("# ")
        toc.append(f"- [{title}](#{anchor})")
        lines, in_code = [], False
        for line in content.splitlines():
            if line.startswith("```"):
                in_code = not in_code
            elif not in_code:
                if line.startswith("#"):
                    line = "#" + line
                def rebase(match):
                    target = match.group(2)
                    parsed = urlsplit(target)
                    if parsed.scheme or target.startswith("#"):
                        return match.group(0)
                    resolved = (source.parent / unquote(parsed.path)).resolve()
                    rebased = resolved.relative_to(root.resolve()).as_posix()
                    if parsed.fragment:
                        rebased += "#" + parsed.fragment
                    return f"{match.group(1)}({rebased})"
                line = LINK.sub(rebase, line)
            lines.append(line)
        sections.append(f'<a id="{anchor}"></a>\n\n' + "\n".join(lines))
    header = (
        "# Agent 工程学习手册｜单文件总册\n\n"
        "本文件由分章资料机械合并生成。请编辑 chapters、appendices 或 labs/README.md，"
        "再运行 python3 scripts/book.py。阅读边界与公开参考见附录E。\n\n"
        "## 目录\n\n"
    )
    return header + "\n".join(toc) + "\n\n---\n\n" + "\n\n---\n\n".join(sections) + "\n"


def check_markdown(path, root):
    errors, in_code = [], False
    for number, line in enumerate(path.read_text(encoding="utf8").splitlines(), 1):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for match in LINK.finditer(line):
            target = match.group(2)
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            local = (path.parent / unquote(parsed.path)).resolve()
            if not local.is_relative_to(root.resolve()) or not local.exists():
                errors.append(f"{path.name}:{number}: unresolved local link: {target}")
    if in_code:
        errors.append(f"{path.name}: unclosed code fence")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify without writing")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sources = sorted((root / "chapters").glob("*.md"))
    sources += sorted((root / "appendices").glob("*.md"))
    sources += [root / "labs" / "README.md"]
    result = render_book(sources, root)
    book = root / "BOOK.md"
    if not args.check:
        book.write_text(result, encoding="utf8")
    errors = []
    if not book.exists() or book.read_text(encoding="utf8") != result:
        errors.append("BOOK.md is out of date; run python3 scripts/book.py")
    for document in sources + [root / "README.md", book]:
        if document.exists():
            errors.extend(check_markdown(document, root))
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Verified {len(sources)} source documents; merged book has {len(result):,} characters.")
