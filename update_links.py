"""
update_links.py — Update index.html links from #anchors to real .html pages.

Purpose:
    Replaces all dead anchor links and Shopify routes in index.html with
    links to the newly generated subpages. Does NOT touch any visual
    sections, CSS, or JS — only href attributes.

Args:
    None.
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
INDEX = BASE / "index.html"
html = INDEX.read_text(encoding="utf-8")

# Link mapping: old href -> new href
LINK_MAP = {
    # Anchor links -> real pages
    '#about': 'about.html',
    '#store': 'store.html',
    '#tea-master': 'tea-master.html',
    '#tea-intro': 'tea-intro.html',
    '#brewing': 'brewing.html',
    '#faq': 'faq.html',
    '#contact': 'contact.html',
    '#privacy': 'privacy.html',
    '#terms': 'terms.html',
    '#journal': 'journal.html',
    '#news': 'news.html',
    '#blog': 'journal.html',
    '#tea-bag': 'tea-bag.html',
    '#tea-leaf': 'tea-leaf.html',
    '#tea-ware': 'tea-ware.html',
    '#gift-set': 'gift-set.html',
    '#honey-black': 'product-honey-black.html',
    '#gaba': 'product-gaba.html',
    '#fresh-oolong': 'product-fresh-oolong.html',
    '#yushan-oolong': 'product-yushan-oolong.html',

    # Shopify routes -> real pages
    '/cart': 'cart.html',
    '/account': 'account.html',
    '/pages/wishlist': 'wishlist.html',
    '/pages/store-locator': 'store.html',
    '/search': 'search.html',
    '/blogs/news': 'journal.html',
    '/blogs/recipe': 'journal.html',
    '/blogs/story': 'journal.html',
    '/products/gyokuro441032': 'product-honey-black.html',

    # Ippodo language links -> remove (single language POC)
    'https://www.ippodo-tea.co.jp/': '#',
    'https://ippodotea.com': '#',
    'https://global.ippodo-tea.co.jp/': 'index.html',
}

count = 0
for old, new in LINK_MAP.items():
    # Match href="old" or href='old' (case insensitive, but href is lowercase in HTML)
    pattern = 'href="' + re.escape(old) + '"'
    replacement = 'href="' + new + '"'
    new_html, n = re.subn(re.escape(pattern), replacement, html)
    if n > 0:
        html = new_html
        count += n
        print(f"  {old} -> {new} ({n} occurrences)")

INDEX.write_text(html, encoding="utf-8")
print(f"\nTotal links updated: {count}")

# Also add zen-cart.js, zen-wishlist.js, zen-search.js to index.html
# (before </body>)
html = INDEX.read_text(encoding="utf-8")
zen_scripts = '<script src="assets/zen-cart.js"></script>\n<script src="assets/zen-wishlist.js"></script>\n<script src="assets/zen-search.js"></script>\n'
if 'zen-cart.js' not in html:
    html = html.replace('</body>', zen_scripts + '</body>')
    INDEX.write_text(html, encoding="utf-8")
    print("Added zen-cart.js, zen-wishlist.js, zen-search.js to index.html")
else:
    print("zen-cart.js already referenced in index.html")
