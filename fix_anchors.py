import re
from pathlib import Path

html = Path(r'C:\Users\bubbl\Documents\New OpenCode Project\zen_ea_tea\index.html').read_text(encoding='utf-8')

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
}

count = 0
for old, new in LINK_MAP.items():
    target = 'href="' + old + '"'
    replacement = 'href="' + new + '"'
    n = html.count(target)
    if n > 0:
        html = html.replace(target, replacement)
        count += n
        print(f"  {old} -> {new} ({n} occurrences)")

Path(r'C:\Users\bubbl\Documents\New OpenCode Project\zen_ea_tea\index.html').write_text(html, encoding='utf-8')
print(f"\nTotal anchor links updated: {count}")
