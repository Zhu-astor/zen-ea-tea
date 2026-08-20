"""
cleanup_scripts.py - Remove Shopify-residual scripts/modules that block
Ippodo's own bundle.js from initializing Swiper and fade animations.

Purpose:
    The cloned index.html still references ~20 Shopify CDN scripts that
    were not downloaded (404). Under HTTP, these 404s don't block CORS,
    but the <script type="module"> entries invoke import() chains that
    throw and can interrupt the document's module-loading queue, delaying
    or suppressing bundle.js execution.

    This script strips every <script> and <link> that points to a Shopify
    runtime asset (CDN, ESM modules, storefront, klaviyo, pandectes,
    promolayer, swym, back-in-stock, etc.) while preserving:
      - jquery-3.6.3.min.js
      - global.js
      - bundle.js
      - vendor.bundle.js
      - is_touch_device.js
      - scripts.js (footer sections)
      - wish-list-button.js / wish-list-notification.js (UI)
      - predictive-search.js
      - cart-notification.js
      - section-footer.css and other Ippodo CSS

Args:
    None.

Returns:
    Overwrites index.html in place. Reports what was removed.
"""

from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
HTML = BASE / "index.html"
soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")

KEEP_SUBSTR = (
    "jquery", "global.js", "bundle.js", "vendor.bundle", "is_touch_device",
    "scripts.js", "wish-list-button", "wish-list-notification",
    "predictive-search", "cart-notification",
)
KEEP_LINK_SUBSTR = (
    "section-footer", "component-", "disclosure", "newsletter",
    "main--global", "wl-main", "bundle_fix", "predictive-search",
    "cart-notification", "search", "font-awesome",
)

removed_scripts = []
removed_links = []

for s in list(soup.find_all("script")):
    src = s.get("src", "")
    typ = s.get("type", "")
    # inline module scripts (Shopify runtime config) — remove
    if not src and typ == "module":
        removed_scripts.append(f"inline module ({(s.string or '')[:50].strip()})")
        s.decompose()
        continue
    if not src:
        continue
    if src in ("", "#"):
        continue
    # Shopify CDN + ESM + third-party — remove unless in keep list
    if any(k in src for k in KEEP_SUBSTR):
        continue
    # drop Shopify domain scripts and 404-prone ESM
    removed_scripts.append(src)
    s.decompose()

for lk in list(soup.find_all("link", rel=lambda v: v and "stylesheet" in v)):
    href = lk.get("href", "")
    if not href:
        continue
    if any(k in href for k in KEEP_LINK_SUBSTR):
        continue
    removed_links.append(href)
    lk.decompose()

# Also remove <link rel="preconnect/dns-prefetch"> to external hosts
for lk in list(soup.find_all("link", rel=lambda v: v and ("preconnect" in v or "dns-prefetch" in v))):
    href = lk.get("href", "")
    if href.startswith("http"):
        removed_links.append(f"[preconnect] {href}")
        lk.decompose()

# Remove inline scripts that reference Shopify globals (window.routes, etc.) but KEEP IPPODO global
for s in list(soup.find_all("script")):
    if not s.get("src") and s.string:
        if "window.routes" in s.string or "swym" in s.string.lower():
            removed_scripts.append(f"inline ({s.string[:60].strip()})")
            s.decompose()
        elif "IPPODO" in s.string and "shopUrl" not in s.string:
            # keep IPPODO global var definition — bundle.js depends on it
            continue

HTML.write_text(str(soup), encoding="utf-8")

print(f"Removed {len(removed_scripts)} scripts:")
for r in removed_scripts:
    print(f"  - {r}")
print(f"\nRemoved {len(removed_links)} links:")
for r in removed_links:
    print(f"  - {r}")
print(f"\nWrote {HTML} ({HTML.stat().st_size} bytes)")
