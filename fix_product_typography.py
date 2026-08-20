"""
fix_product_typography.py

Purpose:
    The 4 product detail pages use hand-rolled inline styles for the category label,
    product name (h1), and price — a generic sans-serif look with none of Ippodo's real
    typography (goudy-old-style serif headings, the site's real color palette). Real
    classes for exactly these three elements already exist in the scraped
    main--global.css and render correctly elsewhere on the site:
      .a-tag--type01        — pill-shaped category label chip
      .a-heading--type10    — large serif product-name heading
      .a-text-price--type01 — price text styling

    This swaps the inline-styled category/h1/price elements for these real classes on
    all 4 product pages. Companion fix to fix_button_styling.py, which did the same for
    the add-to-cart/wishlist buttons.

Args:
    None (operates on the fixed file list below).

Returns:
    Rewrites each file in place; prints a per-file replacement count.
"""

import re
from pathlib import Path

FILES = [
    "product-honey-black.html", "product-gaba.html",
    "product-fresh-oolong.html", "product-yushan-oolong.html",
]

RE_TAG = re.compile(r'<p style="font-size: 14px; color: #888; margin: 0 0 8px;">([^<]*)</p>')
RE_H1 = re.compile(r'<h1 style="font-size: 28px; margin: 0 0 8px; color: #333;">([^<]*)</h1>')
RE_PRICE = re.compile(r'<p style="font-size: 22px; color: #333; margin: 0 0 24px;">([^<]*)</p>')


def fix_text(text: str) -> str:
    text = RE_TAG.sub(r'<p class="a-tag--type01">\1</p>', text)
    text = RE_H1.sub(r'<h1 class="a-heading--type10">\1</h1>', text)
    text = RE_PRICE.sub(r'<p class="a-text-price--type01">\1</p>', text)
    return text


def main():
    base = Path(__file__).parent
    for name in FILES:
        path = base / name
        if not path.exists():
            print(f"{name}: SKIP (not found)")
            continue
        text = path.read_text(encoding="utf-8")
        tag_n = len(RE_TAG.findall(text))
        h1_n = len(RE_H1.findall(text))
        price_n = len(RE_PRICE.findall(text))
        fixed = fix_text(text)
        path.write_text(fixed, encoding="utf-8")
        print(f"{name}: tag={tag_n} h1={h1_n} price={price_n}")


if __name__ == "__main__":
    main()
