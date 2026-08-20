"""
fix_nested_comment_corruption.py

Purpose:
    fix_leaked_appblock_comments.py was run twice (once for BEGIN/END app markers,
    once more after adding the FIXED_TEXT_MARKERS pass) against files that, in a couple
    of spots, hold these marker strings as JS *string literal content* rather than real
    HTML comments (e.g. `const reactTarget = \`<!-- BEGIN app snippet: ... -->\`;` — a
    JS template literal that happens to contain comment-shaped text as DATA). The regex
    passes matched that literal text as if it were an unwrapped comment and kept adding
    another "<!--"/"-->" layer around it on each run, producing runs like
    "<!-- <!-- <!-- <!-- <!-- BEGIN app snippet: ... --> --> -->" that then render as
    literal "--> --> -->" garbage text at the top of the page.

    This collapses any run of 2+ consecutive "<!--" (with only whitespace between them)
    down to one, and any run of 2+ consecutive "-->" down to one, everywhere in each
    file. Legitimate HTML never has genuinely nested comment delimiters, so this is safe
    cleanup regardless of how many times the previous script's passes stacked them.

Args:
    None (operates on the same file list as fix_leaked_appblock_comments.py).

Returns:
    Rewrites each file in place; prints a per-file before/after corruption count.
"""

import re
from pathlib import Path

FILES = [
    "about.html", "account.html", "article-cold-brew.html", "article-gaba-intro.html",
    "article-natural-farming.html", "article-tea-english.html", "article-tea-king-award.html",
    "article-yushan-tea-garden.html", "brewing.html", "cart.html", "contact.html",
    "faq.html", "journal.html", "privacy.html", "product-fresh-oolong.html",
    "product-gaba.html", "product-honey-black.html", "product-yushan-oolong.html",
    "products.html", "search.html", "store.html", "tea-master.html", "terms.html",
    "wishlist.html",
]

RE_NESTED_OPEN = re.compile(r"(?:<!--\s*){2,}")
RE_NESTED_CLOSE = re.compile(r"(?:\s*-->){2,}")


def fix_text(text: str) -> str:
    text = RE_NESTED_OPEN.sub("<!-- ", text)
    text = RE_NESTED_CLOSE.sub(" -->", text)
    return text


def count_corruption(text: str) -> int:
    return len(RE_NESTED_OPEN.findall(text)) + len(RE_NESTED_CLOSE.findall(text))


def main():
    base = Path(__file__).parent
    for name in FILES:
        path = base / name
        if not path.exists():
            print(f"{name}: SKIP (not found)")
            continue
        text = path.read_text(encoding="utf-8")
        before = count_corruption(text)
        fixed = fix_text(text)
        after = count_corruption(fixed)
        path.write_text(fixed, encoding="utf-8")
        print(f"{name}: corruption {before} -> {after}")


if __name__ == "__main__":
    main()
