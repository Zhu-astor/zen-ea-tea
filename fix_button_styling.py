"""
fix_button_styling.py

Purpose:
    The add-to-cart / add-to-wishlist buttons on product pages and the listing page
    were built with hand-rolled inline styles (gray #3a3a3a box, 4px corners, generic
    sans-serif) instead of Ippodo's own button system, which already exists in the
    scraped main--global.css: .a-button--type01 (base: pill shape via border-radius:
    50-60px, goudy-old-style serif font, generous padding) combined with .a-button--
    brown (filled, #93806f bg / white text, #ba876a on hover — the site's real CTA
    color) or .a-button--gray (outline, #4e4e4e border, same #ba876a hover) for the
    secondary action. These classes are already used correctly elsewhere on the site
    (e.g. the "查看更多" buttons on index.html use a-button--type01 a-button--gray).

    This strips the inline style="..." attribute from every zen-add-to-cart /
    zen-add-to-wishlist button (inline styles always beat stylesheet rules regardless
    of specificity, so the real classes would otherwise have no visible effect) and
    adds the matching real classes. The JS hook classes (zen-add-to-cart /
    zen-add-to-wishlist, used by zen-cart.js / zen-wishlist.js's event listeners) are
    left untouched.

Args:
    None (operates on the fixed file list below).

Returns:
    Rewrites each file in place; prints a per-file replacement count.
"""

import re
from pathlib import Path

FILES = [
    "product-honey-black.html", "product-gaba.html", "product-fresh-oolong.html",
    "product-yushan-oolong.html", "products.html",
]

RE_CART_BTN = re.compile(
    r'<button class="zen-add-to-cart"([^>]*?)\s+style="[^"]*"([^>]*)>'
)
RE_WISHLIST_BTN = re.compile(
    r'<button class="zen-add-to-wishlist"([^>]*?)\s+style="[^"]*"([^>]*)>'
)


def fix_text(text: str) -> str:
    text = RE_CART_BTN.sub(
        r'<button class="zen-add-to-cart a-button--type01 a-button--brown"\1\2>', text
    )
    text = RE_WISHLIST_BTN.sub(
        r'<button class="zen-add-to-wishlist a-button--type01 a-button--gray"\1\2>', text
    )
    return text


def main():
    base = Path(__file__).parent
    for name in FILES:
        path = base / name
        if not path.exists():
            print(f"{name}: SKIP (not found)")
            continue
        text = path.read_text(encoding="utf-8")
        cart_before = len(RE_CART_BTN.findall(text))
        wish_before = len(RE_WISHLIST_BTN.findall(text))
        fixed = fix_text(text)
        path.write_text(fixed, encoding="utf-8")
        print(f"{name}: cart buttons fixed={cart_before}, wishlist buttons fixed={wish_before}")


if __name__ == "__main__":
    main()
