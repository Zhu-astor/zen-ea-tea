"""
fix_all_links_everywhere.py

Purpose:
    build_pages.py copies the shared header/nav markup from index.html into every
    subpage at generation time. The anchor-link fixes (fix_anchor_links.py,
    update_links.py) were only ever run against index.html itself, so every subpage's
    OWN copy of the header still has the pre-fix #anchor / absolute-Shopify-path hrefs
    baked in — clicking "茶包" from the dropdown while ON product-honey-black.html,
    for example, does nothing, because that page's header still says href="#tea-bag"
    instead of href="tea-bag.html".

    This applies the exact same href replacements to every *.html file in the project
    (index.html included, safe to re-run — idempotent since it only replaces the exact
    old attribute string, which stops matching once replaced).

Args:
    None.

Returns:
    Rewrites every *.html file in place where changes are found; prints a per-file
    replacement count.
"""

from pathlib import Path

BASE = Path(__file__).resolve().parent

LINK_MAP = {
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
    '/cart': 'cart.html',
    '/account': 'account.html',
    '/pages/wishlist': 'wishlist.html',
    '/pages/store-locator': 'store.html',
    '/search': 'search.html',
    '/blogs/news': 'journal.html',
    '/blogs/recipe': 'journal.html',
    '/blogs/story': 'journal.html',
    '/products/gyokuro441032': 'product-honey-black.html',
}

TOP_LEVEL_VOID = {
    ('href="javascript:void(0)">關於蟬吃茶</a>'): 'href="about.html">關於蟬吃茶</a>',
    ('href="javascript:void(0)">茶品知識</a>'): 'href="tea-intro.html">茶品知識</a>',
    ('href="javascript:void(0)">購物</a>'): 'href="products.html">購物</a>',
    ('href="javascript:void(0)">蟬茶日誌</a>'): 'href="journal.html">蟬茶日誌</a>',
}

total_files = 0
total_replacements = 0

for path in sorted(BASE.glob("*.html")):
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    file_count = 0

    for old, new in LINK_MAP.items():
        old_attr = f'href="{old}"'
        new_attr = f'href="{new}"'
        n = text.count(old_attr)
        if n:
            text = text.replace(old_attr, new_attr)
            file_count += n

    for old_frag, new_frag in TOP_LEVEL_VOID.items():
        n = text.count(old_frag)
        if n:
            text = text.replace(old_frag, new_frag)
            file_count += n

    if text != original:
        path.write_text(text, encoding="utf-8")
        total_files += 1
        total_replacements += file_count
        print(f"{path.name}: {file_count} link(s) fixed")

print(f"\n{total_files} files touched, {total_replacements} total replacements")
