"""
Removes script blocks that make real network requests to Ippodo Tea's / Shopify's
live production infrastructure (analytics beacons, CDN-hosted polyfills, a hotlinked
promo video). These are leftover boilerplate from the pristine Shopify clone and are
not used by any of this site's actual functionality (cart/wishlist/search are handled
by the separate zen-*.js files). Run once before making the repo/site public.
"""
import re
import glob

PATTERNS = [
    # Shopify "trekkie" analytics loader — unconditionally fetches and runs a real
    # analytics script from global.ippodo-tea.co.jp on every page load.
    re.compile(r'<script class="analytics">.*?</script>\s*', re.DOTALL),
    # Autosizes/performance polyfill — conditionally injects a script tag pointing at
    # global.ippodo-tea.co.jp for older browsers.
    re.compile(r'<script>\(function \(\) \{var userAgent = navigator\.userAgent;.*?</script>\s*', re.DOTALL),
    # Site-abandonment sendBeacon — fires on pagehide to monorail-edge.shopifysvc.com
    # with Ippodo's real shop_id.
    re.compile(r'<script>\(function\(\)\{if \("sendBeacon" in navigator.*?</script>\s*', re.DOTALL),
    # Accelerated-checkout / portable-wallets loader cluster (3 scripts).
    re.compile(r'<script data-source-attribution="shopify\.dynamic_checkout\.[a-z_.]+">.*?</script>\s*', re.DOTALL),
    # Hero video modal — hotlinks a real promo video from global.ippodo-tea.co.jp/cdn.
    re.compile(
        r'<div class="shopify-section" id="shopify-section-header-video">.*?'
        r'<div class="p-top-video__close" id="js-top-video-close">close</div>\s*</div></div>\s*',
        re.DOTALL,
    ),
]

total_removed = 0
for path in glob.glob('*.html'):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    original = text
    file_removed = 0
    for pattern in PATTERNS:
        text, n = pattern.subn('', text)
        file_removed += n
    if text != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'{path}: removed {file_removed} block(s)')
        total_removed += file_removed

print(f'Total blocks removed: {total_removed}')
