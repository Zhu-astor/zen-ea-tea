"""
fix_round3.py — Fix all issues reported in round 3.

1. Rename "茶品知識" → "茶知識" in index.html + all subpages
2. Fix shopping section grid (4 items in one row)
3. Add announcement bar background image (bg-announcement.png)
4. Clean Shopify app block text from all subpages
5. Ensure consistent image sizes (object-fit: cover, fixed aspect ratios)
6. Fix header icon rendering (add explicit width/height for icons)
7. Set body/section background to match Ippodo's beige
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 1. Fix index.html
# ---------------------------------------------------------------------------
idx_path = BASE / "index.html"
html = idx_path.read_text(encoding="utf-8")

# 1a. Rename 茶品知識 → 茶知識
html = html.replace("茶品知識", "茶知識")
print("[1] Renamed 茶品知識 → 茶知識")

idx_path.write_text(html, encoding="utf-8")

# ---------------------------------------------------------------------------
# 2. Fix all subpages: rename + clean Shopify app blocks
# ---------------------------------------------------------------------------
for f in BASE.glob("*.html"):
    if f.name == "index.html":
        continue
    html = f.read_text(encoding="utf-8")
    changed = False

    # Rename
    if "茶品知識" in html:
        html = html.replace("茶品知識", "茶知識")
        changed = True

    # Clean Shopify app block comments that render as visible text
    # These are HTML comments that somehow ended up as visible text
    patterns = [
        r'<!--\s*<!--\s*BEGIN app block: shopify://apps/[^>]*?END app block\s*-->\s*-->',
        r'BEGIN app block: shopify://apps/[^<]*?END app block',
        r'BEGIN app snippet: [^<]*?END app snippet',
        r'BEGIN app block: shopify://apps/pandectes-gdpr/[^<]*',
        r'BEGIN app block: shopify://apps/klaviyo-email-marketing-sms/[^<]*',
        r'BEGIN app block: shopify://apps/helium-customer-fields/[^<]*',
        r'BEGIN app block: shopify://apps/microsoft-clarity/[^<]*',
    ]
    for pat in patterns:
        new_html = re.sub(pat, "", html, flags=re.DOTALL | re.IGNORECASE)
        if new_html != html:
            html = new_html
            changed = True

    # Also clean any remaining "BEGIN app" / "END app" text nodes
    html = re.sub(r'BEGIN app (block|snippet):[^\n]*\n?', '', html)
    html = re.sub(r'END app (block|snippet)\s*-->', '-->', html)

    if changed:
        f.write_text(html, encoding="utf-8")
        print(f"  [fixed] {f.name}")

print("[2] Subpages cleaned")

# ---------------------------------------------------------------------------
# 3. Update zen-fixes.css with all visual fixes
# ---------------------------------------------------------------------------
css_path = BASE / "assets" / "zen-fixes.css"
css = css_path.read_text(encoding="utf-8")

# Add new fixes at the end
new_fixes = """

/* ===== Round 3 fixes ===== */

/* Announcement bar: use Ippodo's bg-announcement.png like the real site */
.announcement-bar {
  background-image: url(assets/bg-announcement.png) !important;
  background-repeat: repeat-x !important;
  background-size: auto 100% !important;
  background-color: #f5f0e8 !important;
}

/* Body background: warm beige to match Ippodo's site tone */
body {
  background-color: #faf8f5 !important;
}

/* Header icons: ensure they have explicit dimensions and show */
.c-unav-pc .c-icon--search,
.c-unav-sp .c-icon--search,
.c-unav-sp-fix .c-icon--search {
  width: 20px !important;
  height: 20px !important;
  display: inline-block !important;
  background: url(assets/icon-search.svg) center no-repeat !important;
  background-size: contain !important;
}
.c-unav-pc .c-icon--shop,
.c-unav-sp .c-icon--shop {
  width: 20px !important;
  height: 20px !important;
  display: inline-block !important;
  background: url(assets/icon-shop.svg) center no-repeat !important;
  background-size: contain !important;
}

/* Shopping section: force 4 columns, prevent wrapping */
@media (min-width: 769px) {
  .p-top-buy__nav {
    grid-template-columns: repeat(4, 1fr) !important;
    max-width: 877px !important;
    margin: 0 auto !important;
    gap: 20px !important;
  }
  .p-top-buy__item {
    width: 100% !important;
  }
}

/* Ensure all shopping category icons are uniform squares */
.p-top-buy__image {
  width: 100% !important;
  aspect-ratio: 1 / 1 !important;
  object-fit: cover !important;
  object-position: center !important;
  border-radius: 8px;
}

/* Feature slider: uniform square images */
.o-feature-list__item img.a-image {
  display: block !important;
  width: 100% !important;
  aspect-ratio: 1 / 1 !important;
  object-fit: cover !important;
  object-position: center !important;
}

/* Recipe slider: uniform 3:2 images */
.p-top-recipe__item img.p-top-recipe__image,
.p-top-recipe__item .p-top-recipe__image {
  display: block !important;
  width: 100% !important;
  aspect-ratio: 3 / 2 !important;
  object-fit: cover !important;
  object-position: center !important;
}

/* Story/Iroiro slider: uniform 3:2 images */
.p-top-iroiro__item > a > img {
  display: block !important;
  width: 100% !important;
  aspect-ratio: 3 / 2 !important;
  object-fit: cover !important;
  object-position: center !important;
}

/* Product cards in highlight slider: already handled by main--global.css
   padding-top:124% trick, but ensure images fill properly */
.m-product-card__image img {
  object-fit: cover !important;
  object-position: center !important;
}

/* Nav cards (關於蟬吃茶 / 茶品介紹 / 門市與活動): uniform 4:5 portrait */
.o-card-nav__image img {
  display: block !important;
  width: 100% !important;
  aspect-ratio: 4 / 5 !important;
  object-fit: cover !important;
  object-position: center !important;
}

/* Brand homophones section: uniform square icons */
.zen-homophones img {
  display: block !important;
  width: 100% !important;
  max-width: 140px !important;
  aspect-ratio: 1 / 1 !important;
  object-fit: contain !important;
  object-position: center !important;
  margin: 0 auto 12px !important;
}

/* Trust section cards: uniform height */
#shopify-section-zen-trust .js-fadetarget {
  min-height: 160px;
  display: flex !important;
  flex-direction: column;
  justify-content: center;
}
"""

if "Round 3 fixes" not in css:
    css += new_fixes
    css_path.write_text(css, encoding="utf-8")
    print("[3] zen-fixes.css updated with round 3 fixes")
else:
    print("[3] zen-fixes.css already has round 3 fixes")

# ---------------------------------------------------------------------------
# 4. Add zen-fixes.css and zen-fixes.js to all subpages (if missing)
# ---------------------------------------------------------------------------
for f in BASE.glob("*.html"):
    if f.name == "index.html":
        continue
    html = f.read_text(encoding="utf-8")
    changed = False

    # Add zen-fixes.css if missing
    if "zen-fixes.css" not in html and "assets/zen-fixes.css" not in html:
        html = html.replace("</head>", '<link href="assets/zen-fixes.css" rel="stylesheet"/>\n</head>')
        changed = True

    # Add zen-fixes.js if missing
    if "zen-fixes.js" not in html and "assets/zen-fixes.js" not in html:
        html = html.replace("</body>", '<script src="assets/zen-fixes.js"></script>\n</body>')
        changed = True

    if changed:
        f.write_text(html, encoding="utf-8")
        print(f"  [css/js added] {f.name}")

print("[4] zen-fixes.css/js linked in all subpages")

print("\n=== ALL ROUND 3 FIXES APPLIED ===")
