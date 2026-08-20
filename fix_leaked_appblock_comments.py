"""
fix_leaked_appblock_comments.py

Purpose:
    build_pages.py (opencode, round 2) generated every new content page by copying
    the <head>/<header> region from a source that had its HTML comment delimiters
    around Shopify's "app block"/"app snippet" markers stripped somewhere in the
    pipeline. The markers themselves (e.g. "BEGIN app block: shopify://apps/...")
    survived, but the surrounding "<!--" / "-->" did not, so they render as literal
    visible text at the very top of every page instead of being invisible comments.
    Confirmed by diffing against the correctly-commented version in index.html.

    This is a one-time repair pass across every generated page, re-wrapping each
    marker in its own "<!-- ... -->" comment. It does not touch any other content —
    the actual embedded scripts/divs between markers were never damaged, only the
    marker text itself lost its comment delimiters.

Args:
    None (operates on a fixed file list below).

Returns:
    Rewrites each file in place; prints a per-file before/after leak count.
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

# Case 1: marker already has a trailing "-->" left over (asymmetric strip) — just add
# the leading "<!--" and normalize.
RE_BEGIN_WITH_ARROW = re.compile(r"BEGIN app (block|snippet):\s*([^\n]*?)\s*-->")
RE_END_WITH_ARROW = re.compile(r"END app (block|snippet)\s*-->")

# Case 2: marker has no trailing "-->" at all — terminate at the next marker, a tag
# open, or 2+ spaces (Shopify's original formatting pads that spot).
RE_BEGIN_NO_ARROW = re.compile(
    r"BEGIN app (block|snippet):\s*([^\n<]*?)(?=\s{2,}|\n|<)"
)
RE_END_NO_ARROW = re.compile(r"END app (block|snippet)\b(?!\s*-->)")

# Case 3: other fixed-text (no variable content) comments that lost their delimiters
# the same way — found by diffing every <!--...--> comment in the correctly-commented
# index.html against these pages and checking which ones show up "naked".
FIXED_TEXT_MARKERS = [
    "A11y",
    "Back in Stock helper snippet",
    "End Back in Stock helper snippet",
    "Stamped - Begin Script",
    "Stamped - End Script",
]


def fix_fixed_text_markers(text: str) -> str:
    for marker in FIXED_TEXT_MARKERS:
        # Only re-wrap occurrences not already preceded by "<!-- " (idempotent).
        pattern = re.compile(r"(?<!<!-- )" + re.escape(marker) + r"(?!\s*-->)")
        text = pattern.sub(f"<!-- {marker} -->", text)
    return text


def fix_text(text: str) -> str:
    text = RE_BEGIN_WITH_ARROW.sub(lambda m: f"<!-- BEGIN app {m.group(1)}: {m.group(2)} -->", text)
    text = RE_END_WITH_ARROW.sub(lambda m: f"<!-- END app {m.group(1)} -->", text)
    text = RE_BEGIN_NO_ARROW.sub(lambda m: f"<!-- BEGIN app {m.group(1)}: {m.group(2)} -->", text)
    text = RE_END_NO_ARROW.sub(lambda m: f"<!-- END app {m.group(1)} -->", text)
    text = fix_fixed_text_markers(text)
    return text


def count_leaks(text: str) -> int:
    # A "leak" is a marker not immediately preceded by "<!-- ".
    leaks = 0
    for m in re.finditer(r"(BEGIN|END) app (block|snippet)", text):
        start = m.start()
        if text[max(0, start - 5):start] != "<!-- ":
            leaks += 1
    for marker in FIXED_TEXT_MARKERS:
        for m in re.finditer(re.escape(marker), text):
            start = m.start()
            if text[max(0, start - 5):start] != "<!-- ":
                leaks += 1
    return leaks


def main():
    base = Path(__file__).parent
    for name in FILES:
        path = base / name
        if not path.exists():
            print(f"{name}: SKIP (not found)")
            continue
        text = path.read_text(encoding="utf-8")
        before = count_leaks(text)
        fixed = fix_text(text)
        after = count_leaks(fixed)
        path.write_text(fixed, encoding="utf-8")
        print(f"{name}: leaks {before} -> {after}")


if __name__ == "__main__":
    main()
