"""
strip_shopify_app_blocks.py

Purpose:
    The previous repair passes (fix_leaked_appblock_comments.py,
    fix_nested_comment_corruption.py) restored the HTML comment delimiters around
    Shopify's "app block"/"app snippet" markers, but that only fixes the *visible
    text* symptom. The actual embedded scripts between those markers (Shopify
    checkout captcha, "Customer Fields" third-party form embed, Klaviyo, Back in
    Stock, Stamped reviews, ...) are still live code that expects a real Shopify
    storefront: it calls out to Shopify/third-party APIs that don't exist for this
    static offline site ("Failed to fetch" in the console), and at least one of them
    is now throwing "Unexpected end of input" — a genuine JS syntax error, most
    likely from a legacy document.write()-based loader that, on our offline pages,
    ends up blanking the entire rendered document instead of silently failing.

    None of this is needed for the POC. This removes each full
    "<!-- BEGIN app (block|snippet): ... --> ... <!-- END app (block|snippet) -->"
    span (including whatever markup/script sits between the markers) rather than
    continuing to patch the comment delimiters around code that shouldn't run here
    at all. Also removes the similarly dead "Back in Stock helper snippet" and
    "Stamped - Begin/End Script" blocks.

Args:
    None (operates on every *.html file in the project directory).

Returns:
    Rewrites each file in place; prints a per-file removed-block count.
"""

import re
from pathlib import Path

RE_APP_BLOCK = re.compile(
    r"<!--\s*BEGIN app (block|snippet):.*?-->.*?<!--\s*END app \1\s*-->",
    re.S,
)
# swymVersion/swymCustomCss/swymSnippet snippets have no matching END for their own
# name (they nest inside the outer app block instead) — the RE_APP_BLOCK pass above
# already consumes them as part of their enclosing block, so no separate pass needed.

RE_BACK_IN_STOCK = re.compile(
    r"<!--\s*Back in Stock helper snippet\s*-->.*?<!--\s*End Back in Stock helper snippet\s*-->",
    re.S,
)
RE_STAMPED = re.compile(
    r"<!--\s*Stamped - Begin Script\s*-->.*?<!--\s*Stamped - End Script\s*-->",
    re.S,
)


def fix_text(text: str) -> tuple[str, int]:
    count = 0
    for pattern in (RE_APP_BLOCK, RE_BACK_IN_STOCK, RE_STAMPED):
        count += len(pattern.findall(text))
        text = pattern.sub("", text)
    return text, count


def main():
    base = Path(__file__).parent
    for path in sorted(base.glob("*.html")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        fixed, count = fix_text(text)
        if count:
            path.write_text(fixed, encoding="utf-8")
        print(f"{path.name}: removed {count} block(s)")


if __name__ == "__main__":
    main()
