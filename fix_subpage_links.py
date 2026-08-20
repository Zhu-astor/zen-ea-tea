"""Fix links in all subpages — same mapping as update_links.py"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

LINK_MAP = {
    '/cart': 'cart.html',
    '/account': 'account.html',
    '/pages/wishlist': 'wishlist.html',
    '/pages/store-locator': 'store.html',
    '/search': 'search.html',
    '/blogs/news': 'journal.html',
    '/blogs/recipe': 'journal.html',
    '/blogs/story': 'journal.html',
    '/products/gyokuro441032': 'product-honey-black.html',
    'https://www.ippodo-tea.co.jp/': '#',
    'https://ippodotea.com': '#',
    'https://global.ippodo-tea.co.jp/': 'index.html',
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
}

total = 0
for f in BASE.glob("*.html"):
    if f.name == "index.html":
        continue
    html = f.read_text(encoding="utf-8")
    changed = False
    for old, new in LINK_MAP.items():
        target = 'href="' + old + '"'
        replacement = 'href="' + new + '"'
        if target in html:
            n = html.count(target)
            html = html.replace(target, replacement)
            total += n
            changed = True
    if changed:
        f.write_text(html, encoding="utf-8")
        print(f"  Fixed: {f.name}")

print(f"\nTotal links fixed in subpages: {total}")
