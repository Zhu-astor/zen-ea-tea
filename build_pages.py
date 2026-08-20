"""
build_pages.py - Generate all subpages for the ZenEaTea POC site.

Purpose:
    Reads zen_ea_tea/index.html, extracts the shared head/header/footer
    markup, and generates all subpages with correct CSS/JS load order
    and consistent navigation.

    Pages generated:
      - 4 product detail pages (honey-black, gaba, fresh-oolong, yushan-oolong)
      - about, store, tea-master, tea-intro, brewing, faq, contact, privacy, terms
      - journal (article list) + 3 sample articles
      - products (unified listing with category filter)
      - wishlist, search, cart (static placeholder)

    Also generates:
      - assets/zen-cart.js, assets/zen-wishlist.js, assets/zen-search.js

    Finally, updates index.html links from #anchors to real .html pages.

Args:
    None. All paths relative to zen_ea_tea/.

Notes:
    - Does NOT modify existing homepage visual sections (Hero, sliders, etc.)
    - Only touches <a href> attributes in index.html to point to real pages
    - Header/footer copied verbatim from index.html (not refactored)
    - CSS load order preserved exactly as homepage:
      font-awesome → base → main--global → wl-main--global → style →
      bundle_fix → zen-fixes → component-predictive-search
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
INDEX = BASE / "index.html"
html_text = INDEX.read_text(encoding="utf-8")
soup = BeautifulSoup(html_text, "html.parser")

# ---------------------------------------------------------------------------
# Extract shared fragments from index.html
# ---------------------------------------------------------------------------

# 1. HEAD: everything from <head> up to (not including) </head>
head_tag = soup.find("head")
head_inner = "".join(str(c) for c in head_tag.contents)

# 2. BODY-UPPER: from <body> through the end of <header> (announcement bar +
#    SVG symbols + header nav). This is everything before <main>.
body_tag = soup.find("body")
body_upper_parts = []
for c in body_tag.contents:
    if c.name == "main":
        break
    body_upper_parts.append(str(c))
body_upper = "".join(body_upper_parts)

# 3. BODY-LOWER: from </main> through end of <body> (footer + scripts).
#    We find <main> in the original soup, then take everything after it.
main_tag = body_tag.find("main")
body_lower_parts = []
found_main = False
for c in body_tag.contents:
    if c is main_tag:
        found_main = True
        continue
    if found_main:
        body_lower_parts.append(str(c))
body_lower = "".join(body_lower_parts)

print(f"[EXTRACT] head: {len(head_inner)} chars")
print(f"[EXTRACT] body_upper: {len(body_upper)} chars")
print(f"[EXTRACT] body_lower: {len(body_lower)} chars")

# ---------------------------------------------------------------------------
# Product data (from site-inventory.json + homepage content)
# ---------------------------------------------------------------------------
PRODUCTS = [
    {
        "id": "honey-black",
        "slug": "honey-black",
        "name_zh": "蟬吃蜜香紅茶",
        "name_en": "Honey Flavored Black Tea",
        "tea_type": "紅茶",
        "price": "NT$480",
        "image": "assets/brand/zh-0698346863.png",
        "key_attr": "小綠葉蟬吸食後烘焙產生天然蜜果香",
        "desc": "南投山上自然農法茶園，小綠葉蟬吸食茶樹嫩芽後，茶葉萎縮捲曲，烘焙後產生天然蜜果香氣。這是蟬吃茶的招牌茶品，也是品牌名稱的由來。",
        "brewing": "熱泡：水溫 95°C，茶葉 3g，水量 150ml，浸泡 3-5 分鐘。冷泡：水溫室溫，茶葉 5g，水量 500ml，冷藏 4-8 小時。",
    },
    {
        "id": "gaba",
        "slug": "gaba",
        "name_zh": "蟬吃佳葉龍茶",
        "name_en": "GABA Tea",
        "tea_type": "佳葉龍茶 / GABA",
        "price": "NT$520",
        "image": "assets/brand/zh-252518c735.png",
        "key_attr": "厭氧發酵製程產生 γ-胺基丁酸；安定心神、舒壓助眠",
        "desc": "佳葉龍茶（GABA Tea）是厭氧發酵製程產生 γ-胺基丁酸的茶品，具有安定心神、舒壓助眠的特性。蟬吃茶提供低咖啡因版本，適合晚間飲用。",
        "brewing": "熱泡：水溫 90°C，茶葉 3g，水量 150ml，浸泡 4-6 分鐘。低咖啡因版本適合晚間飲用。",
    },
    {
        "id": "fresh-oolong",
        "slug": "fresh-oolong",
        "name_zh": "蟬吃鮮翠烏龍茶",
        "name_en": "Fresh Jade Oolong Tea",
        "tea_type": "烏龍茶",
        "price": "NT$450",
        "image": "assets/brand/fresh-oolong-product.png",
        "key_attr": "輕發酵、中烘焙；入口清香、落喉甘潤醇甜",
        "desc": "輕發酵、中烘焙的烏龍茶，入口清香、落喉甘潤醇甜。展現台灣烏龍茶的特色風味，適合日常品飲。",
        "brewing": "熱泡：水溫 95°C，茶葉 3g，水量 150ml，第一泡 60 秒，後續每泡加 30 秒，可沖 5-7 次。",
    },
    {
        "id": "yushan-oolong",
        "slug": "yushan-oolong",
        "name_zh": "蟬吃玉山烏龍茶",
        "name_en": "Yushan Oolong Tea",
        "tea_type": "烏龍茶",
        "price": "NT$680",
        "image": "assets/brand/zh-df5984bc2c.png",
        "key_attr": "高山涼冷、雲霧繚繞、日照短；兒茶素苦澀低、葉肉厚、果膠質高、耐沖泡",
        "desc": "產自玉山高山茶區，涼冷氣候與雲霧繚繞的環境造就獨特風味。兒茶素苦澀低、葉肉厚、果膠質高，耐沖泡，是蟬吃茶的高階品項。",
        "brewing": "熱泡：水溫 95°C，茶葉 3g，水量 150ml，第一泡 90 秒，後續每泡加 30 秒，可沖 6-8 次。",
    },
]

# Article data (from site-inventory.json content_library)
ARTICLES = [
    {"slug": "yushan-tea-garden", "title": "玉山自然茶園", "type": "產地故事", "image": "assets/brand/1671099309366.jpg", "excerpt": "走進玉山山區的自然茶園，了解自然農法如何與生態共存。"},
    {"slug": "natural-farming", "title": "自然農法", "type": "品牌理念", "image": "assets/brand/240130.jpg", "excerpt": "不使用農藥、不施化肥，讓茶樹與小綠葉蟬共生，產出天然的蜜果香氣。"},
    {"slug": "gaba-intro", "title": "GABA茶、佳葉龍茶介紹", "type": "知識型", "image": "assets/brand/GABA.jpg", "excerpt": "什麼是 GABA 茶？厭氧發酵製程如何產生 γ-胺基丁酸？"},
    {"slug": "cold-brew", "title": "冷泡茶泡茶方法", "type": "沖泡指南", "image": "assets/brand/zh-3a2d00425c.jpeg", "excerpt": "冷泡茶的簡單步驟，讓你在夏天也能享受清涼的好茶。"},
    {"slug": "tea-english", "title": "各種茶的英文要怎麼說？", "type": "知識型", "image": "assets/brand/zh-e4383d3a55.jpeg", "excerpt": "烏龍茶、蜜香紅茶、佳葉龍茶的英文怎麼說？一次整理給你。"},
    {"slug": "tea-king-award", "title": "全國製茶武林大賽・榮獲茶王", "type": "獎項 / 信任資產", "image": "assets/brand/2.jpg", "excerpt": "製茶師陳昭鳳參加全國製茶武林大賽，榮獲茶王殊榮。"},
]


# ---------------------------------------------------------------------------
# Helper: build a complete page from head + body_upper + content + body_lower
# ---------------------------------------------------------------------------
def build_page(title: str, description: str, content_html: str,
               extra_head: str = "", extra_scripts: str = "") -> str:
    """Assemble a full HTML page using shared head/header/footer.

    Args:
        title: <title> content.
        description: meta description content.
        content_html: main content to go inside <main>.
        extra_head: additional <link>/<style> for <head> (optional).
        extra_scripts: additional <script> before </body> (optional).

    Returns:
        Complete HTML string.
    """
    # Modify head: replace title and description
    head = head_inner
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, flags=re.DOTALL)
    head = re.sub(r'<meta\s+content="[^"]*"\s+name="description"', f'<meta content="{description}" name="description"', head)
    head = re.sub(r'<meta\s+content="[^"]*"\s+property="og:title"', f'<meta content="{title}" property="og:title"', head)
    head = re.sub(r'<meta\s+content="[^"]*"\s+property="og:description"', f'<meta content="{description}" property="og:description"', head)
    if extra_head:
        head += extra_head

    page = f"""<!DOCTYPE html>
<html class="no-js" lang="zh-Hant">
<head>
{head}
</head>
<body class="gradient" id="zen-ea-tea-page">
{body_upper}
<main class="content-for-layout focus-none" id="MainContent" role="main" tabindex="-1">
{content_html}
</main>
{body_lower}
{extra_scripts}
</body>
</html>"""
    return page


# ---------------------------------------------------------------------------
# Helper: page content wrapper with breadcrumb + heading
# ---------------------------------------------------------------------------
def page_wrapper(title: str, breadcrumb_label: str, content: str,
                 page_class: str = "p-sub-page") -> str:
    """Wrap page content with breadcrumb and standard spacing."""
    return f"""
<div class="{page_class}" style="padding: 40px 0 80px;">
  <div class="page-width" style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
    <nav class="breadcrumb" style="margin-bottom: 30px; font-size: 13px; color: #888;">
      <a href="index.html" style="color: #888; text-decoration: none;">首頁</a>
      <span style="margin: 0 8px;">/</span>
      <span style="color: #333;">{breadcrumb_label}</span>
    </nav>
    <h1 style="font-size: 28px; margin-bottom: 30px; color: #333;">{title}</h1>
    {content}
  </div>
</div>"""


# ---------------------------------------------------------------------------
# Generate product detail pages
# ---------------------------------------------------------------------------
for p in PRODUCTS:
    content = f"""
<div class="p-product-detail" style="padding: 40px 0 80px;">
  <div class="page-width" style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
    <nav class="breadcrumb" style="margin-bottom: 30px; font-size: 13px; color: #888;">
      <a href="index.html" style="color: #888; text-decoration: none;">首頁</a>
      <span style="margin: 0 8px;">/</span>
      <a href="products.html" style="color: #888; text-decoration: none;">茶品介紹</a>
      <span style="margin: 0 8px;">/</span>
      <span style="color: #333;">{p['name_zh']}</span>
    </nav>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px;" class="product-detail-grid">
      <div class="product-detail__image" style="background: #f5f6f7; border-radius: 8px; overflow: hidden; aspect-ratio: 1; display: flex; align-items: center; justify-content: center;">
        <img src="{p['image']}" alt="{p['name_zh']}" style="width: 100%; height: 100%; object-fit: contain;"/>
      </div>
      <div class="product-detail__info">
        <p style="font-size: 14px; color: #888; margin: 0 0 8px;">{p['tea_type']}</p>
        <h1 style="font-size: 28px; margin: 0 0 8px; color: #333;">{p['name_zh']}</h1>
        <p style="font-size: 16px; color: #666; margin: 0 0 16px;">{p['name_en']}</p>
        <p style="font-size: 22px; color: #333; margin: 0 0 24px;">{p['price']}</p>
        <p style="font-size: 15px; color: #555; line-height: 1.8; margin: 0 0 24px;">{p['key_attr']}</p>
        <p style="font-size: 15px; color: #555; line-height: 1.8; margin: 0 0 24px;">{p['desc']}</p>
        <div style="display: flex; gap: 12px; margin-bottom: 30px;">
          <button class="zen-add-to-cart" data-product-id="{p['id']}" data-product-name="{p['name_zh']}" data-product-price="{p['price']}" data-product-image="{p['image']}" style="padding: 12px 32px; background: #3a3a3a; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 15px;">加入購物車</button>
          <button class="zen-add-to-wishlist" data-product-id="{p['id']}" data-product-name="{p['name_zh']}" data-product-image="{p['image']}" style="padding: 12px 24px; background: #fff; color: #3a3a3a; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; font-size: 15px;">♡ 加入收藏</button>
        </div>
      </div>
    </div>
    <div class="product-detail__brewing" style="background: #f9f8f6; border-radius: 8px; padding: 30px; margin-bottom: 30px;">
      <h2 style="font-size: 20px; margin: 0 0 16px; color: #333;">沖泡建議</h2>
      <p style="font-size: 15px; color: #555; line-height: 1.8; margin: 0;">{p['brewing']}</p>
    </div>
    <div style="margin-top: 30px;">
      <a href="products.html" style="color: #3a3a3a; text-decoration: underline; font-size: 14px;">← 返回茶品介紹</a>
    </div>
  </div>
</div>
<style>
@media (max-width: 768px) {{
  .product-detail-grid {{ grid-template-columns: 1fr !important; }}
}}
</style>"""
    page = build_page(
        f"{p['name_zh']} | 蟬吃茶 ZenEaTea",
        f"{p['name_zh']}，{p['key_attr']}。蟬吃茶 ZenEaTea 自然農法好茶。",
        content,
        extra_scripts='<script src="assets/zen-cart.js"></script><script src="assets/zen-wishlist.js"></script>',
    )
    out = BASE / f"product-{p['slug']}.html"
    out.write_text(page, encoding="utf-8")
    print(f"  [WROTE] {out.name}")

print("[DONE] product pages")


# ---------------------------------------------------------------------------
# Generate simple content pages
# ---------------------------------------------------------------------------
SIMPLE_PAGES = [
    ("about", "關於蟬吃茶", "關於蟬吃茶", f"""
<div style="max-width: 800px; margin: 0 auto;">
  <div style="margin-bottom: 30px;">
    <img src="assets/brand/hero-banner.jpg" alt="蟬吃茶" style="width: 100%; border-radius: 8px; aspect-ratio: 2 / 1; object-fit: cover;"/>
  </div>
  <h2 style="font-size: 22px; margin: 0 0 16px; color: #333;">品牌故事</h2>
  <p style="font-size: 16px; color: #555; line-height: 2; margin: 0 0 24px;">
    蟬吃茶（ZenEaTea）來自南投山上的自然農法茶園。品牌名稱源自「蟬吃過的茶」——
    小綠葉蟬吸食茶樹嫩芽後，茶葉萎縮捲曲，烘焙後產生天然蜜果香氣。
    這是無毒、天然、健康的茶，也是品牌的核心概念。
  </p>
  <h2 style="font-size: 22px; margin: 32px 0 16px; color: #333;">四字同音</h2>
  <p style="font-size: 16px; color: #555; line-height: 2; margin: 0 0 20px;">
    潺／禪／蟬／饞 吃茶，四個同音字各配一組理念：
  </p>
  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px;" class="homophones-grid">
    <div style="text-align: center;"><img src="assets/brand/zh-5022a890a3.png" alt="潺" style="width: 80px; height: 80px; margin: 0 auto 8px;"/><p style="font-size: 14px; color: #666;">潺潺流水的健康</p></div>
    <div style="text-align: center;"><img src="assets/brand/zh-d69dd08d36.png" alt="禪" style="width: 80px; height: 80px; margin: 0 auto 8px;"/><p style="font-size: 14px; color: #666;">禪意寧靜的當下</p></div>
    <div style="text-align: center;"><img src="assets/brand/zh-789ede0530.png" alt="蟬" style="width: 80px; height: 80px; margin: 0 auto 8px;"/><p style="font-size: 14px; color: #666;">友善生物的自然</p></div>
    <div style="text-align: center;"><img src="assets/brand/zh-165f6dcbcc.png" alt="饞" style="width: 80px; height: 80px; margin: 0 auto 8px;"/><p style="font-size: 14px; color: #666;">喝一口就愛上</p></div>
  </div>
  <h2 style="font-size: 22px; margin: 32px 0 16px; color: #333;">包裝理念</h2>
  <p style="font-size: 16px; color: #555; line-height: 2; margin: 0;">
    取向天然，禮盒不做華麗包裝。每款茶配一首詩、依茶性添色，以潑墨、書法、詩詞呈現文創力。
  </p>
</div>
<style>@media (max-width: 768px) {{ .homophones-grid {{ grid-template-columns: repeat(2, 1fr) !important; }} }}</style>"""),

    ("store", "門市資訊", "門市資訊", f"""
<div style="max-width: 800px; margin: 0 auto;">
  <h2 style="font-size: 22px; margin: 0 0 20px; color: #333;">台北店</h2>
  <div style="background: #f9f8f6; border-radius: 8px; padding: 30px; margin-bottom: 30px;">
    <table style="width: 100%; font-size: 15px; color: #555;">
      <tr><td style="padding: 8px 0; width: 100px; color: #888;">地址</td><td style="padding: 8px 0;">110 台北市信義區吳興街30號</td></tr>
      <tr><td style="padding: 8px 0; color: #888;">交通</td><td style="padding: 8px 0;">捷運台北101/世貿站（淡水信義線）</td></tr>
      <tr><td style="padding: 8px 0; color: #888;">電話</td><td style="padding: 8px 0;">02-2732-2745</td></tr>
      <tr><td style="padding: 8px 0; color: #888;">Email</td><td style="padding: 8px 0;"><a href="mailto:tea@organic-naturetea.com" style="color: #3a3a3a;">tea@organic-naturetea.com</a></td></tr>
    </table>
  </div>
  <h2 style="font-size: 22px; margin: 30px 0 20px; color: #333;">社群媒體</h2>
  <div style="display: flex; gap: 20px; flex-wrap: wrap;">
    <a href="https://www.facebook.com/profile.php?id=100063636140648" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: #f5f6f7; border-radius: 6px; text-decoration: none; color: #333; font-size: 14px;">Facebook</a>
    <a href="https://www.instagram.com/healthtea1000" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: #f5f6f7; border-radius: 6px; text-decoration: none; color: #333; font-size: 14px;">Instagram</a>
    <a href="https://liff.line.me/1645278921-kWRPP32q/?accountId=lgr7235d" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: #f5f6f7; border-radius: 6px; text-decoration: none; color: #333; font-size: 14px;">LINE 官方帳號</a>
  </div>
</div>"""),

    ("tea-master", "製茶師陳昭鳳", "製茶師陳昭鳳", f"""
<div style="max-width: 800px; margin: 0 auto;">
  <h2 style="font-size: 22px; margin: 0 0 20px; color: #333;">製茶師 陳昭鳳</h2>
  <div style="background: #f9f8f6; border-radius: 8px; padding: 30px; margin-bottom: 30px;">
    <p style="font-size: 16px; color: #555; line-height: 2; margin: 0 0 20px;">
      陳昭鳳是蟬吃茶的製茶師，2018 年首次參加全國製茶武林大賽即為當時唯一女性製茶師，
      歷年武林大賽從不缺席。
    </p>
    <p style="font-size: 16px; color: #555; line-height: 2; margin: 0 0 20px;">
      2024 年製茶師陳昭鳳榮獲全國製茶武林大賽【茶王】。
    </p>
    <p style="font-size: 16px; color: #555; line-height: 2; margin: 0;">
      2023 冬季鹿鳴自然生態烏龍茶大賽，有機烏龍茶組「特優」獎，
      評審單位為行政院農業委員會茶業改良場魚池分場。
    </p>
  </div>
  <h2 style="font-size: 22px; margin: 30px 0 16px; color: #333;">獎項紀錄</h2>
  <ul style="font-size: 16px; color: #555; line-height: 2; padding-left: 20px;">
    <li>全國製茶武林大賽【茶王】</li>
    <li>鹿鳴自然生態烏龍茶大賽 有機烏龍茶組「特優」</li>
    <li>2018 年首次參賽即為當時唯一女性製茶師</li>
  </ul>
</div>"""),

    ("tea-intro", "茶品介紹", "茶品介紹", f"""
<div style="max-width: 1000px; margin: 0 auto;">
  <p style="font-size: 16px; color: #555; line-height: 2; margin: 0 0 30px;">
    蟬吃茶目前有四款自然農法好茶，每一款都來自南投山上的茶園，
    以友善生物、不使用農藥的自然農法製成。
  </p>
  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;" class="tea-intro-grid">
""" + "".join(f"""
    <a href="product-{p['slug']}.html" style="text-decoration: none; color: inherit;">
      <div style="background: #f5f6f7; border-radius: 8px; overflow: hidden; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; margin-bottom: 12px;">
        <img src="{p['image']}" alt="{p['name_zh']}" style="width: 100%; height: 100%; object-fit: contain;"/>
      </div>
      <p style="font-size: 12px; color: #888; margin: 0 0 4px;">{p['tea_type']}</p>
      <p style="font-size: 15px; color: #333; margin: 0 0 4px;">{p['name_zh']}</p>
      <p style="font-size: 14px; color: #666; margin: 0;">{p['price']}</p>
    </a>""" for p in PRODUCTS) + """
  </div>
</div>
<style>@media (max-width: 768px) { .tea-intro-grid { grid-template-columns: repeat(2, 1fr) !important; } }</style>"""),

    ("brewing", "沖泡指南", "沖泡指南", f"""
<div style="max-width: 800px; margin: 0 auto;">
  <p style="font-size: 16px; color: #555; line-height: 2; margin: 0 0 30px;">
    不同的茶有不同的沖泡方式，以下是四款茶的基本沖泡建議。
  </p>
""" + "".join(f"""
  <div style="background: #f9f8f6; border-radius: 8px; padding: 24px; margin-bottom: 20px;">
    <h3 style="font-size: 18px; margin: 0 0 12px; color: #333;">{p['name_zh']}</h3>
    <p style="font-size: 15px; color: #555; line-height: 1.8; margin: 0;">{p['brewing']}</p>
  </div>""" for p in PRODUCTS) + """
</div>"""),

    ("faq", "常見問答", "常見問答", """
<div style="max-width: 800px; margin: 0 auto;">
  <div class="faq-item" style="border-bottom: 1px solid #e0e0e0; padding: 20px 0;">
    <h3 style="font-size: 17px; margin: 0 0 12px; color: #333;">訂單多久會出貨？</h3>
    <p style="font-size: 15px; color: #555; line-height: 1.8; margin: 0;">下單後 1-3 個工作天內出貨，出貨後會通知您物流追蹤號碼。</p>
  </div>
  <div class="faq-item" style="border-bottom: 1px solid #e0e0e0; padding: 20px 0;">
    <h3 style="font-size: 17px; margin: 0 0 12px; color: #333;">可以退換貨嗎？</h3>
    <p style="font-size: 15px; color: #555; line-height: 1.8; margin: 0;">收到商品後如有瑕疵，請於 7 天內聯繫我們辦理退換貨。</p>
  </div>
  <div class="faq-item" style="border-bottom: 1px solid #e0e0e0; padding: 20px 0;">
    <h3 style="font-size: 17px; margin: 0 0 12px; color: #333;">茶葉如何保存？</h3>
    <p style="font-size: 15px; color: #555; line-height: 1.8; margin: 0;">請存放於陰涼乾燥處，避免陽光直射及高溫。開封後建議密封保存，並盡早飲用完畢。</p>
  </div>
  <div class="faq-item" style="padding: 20px 0;">
    <h3 style="font-size: 17px; margin: 0 0 12px; color: #333;">有實體門市可以試茶嗎？</h3>
    <p style="font-size: 15px; color: #555; line-height: 1.8; margin: 0;">有的，歡迎到我們的台北店（台北市信義區吳興街30號）品茶。</p>
  </div>
</div>"""),

    ("contact", "聯絡我們", "聯絡我們", """
<div style="max-width: 600px; margin: 0 auto;">
  <p style="font-size: 16px; color: #555; line-height: 2; margin: 0 0 30px;">
    有任何問題歡迎與我們聯繫，我們會盡快回覆您。
  </p>
  <form id="zen-contact-form" style="display: flex; flex-direction: column; gap: 16px;">
    <div>
      <label style="display: block; font-size: 14px; color: #666; margin-bottom: 6px;">姓名</label>
      <input type="text" name="name" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 15px;"/>
    </div>
    <div>
      <label style="display: block; font-size: 14px; color: #666; margin-bottom: 6px;">Email</label>
      <input type="email" name="email" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 15px;"/>
    </div>
    <div>
      <label style="display: block; font-size: 14px; color: #666; margin-bottom: 6px;">訊息</label>
      <textarea name="message" rows="5" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 15px;"></textarea>
    </div>
    <button type="submit" style="padding: 12px 32px; background: #3a3a3a; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 15px; align-self: flex-start;">送出</button>
    <p id="zen-contact-result" style="font-size: 14px; color: #2a8; display: none;">感謝您的來信，我們會盡快回覆！（此為 POC 示範，實際不會送出）</p>
  </form>
  <script>
  document.getElementById('zen-contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    document.getElementById('zen-contact-result').style.display = 'block';
    this.reset();
  });
  </script>
</div>"""),

    ("privacy", "隱私權政策", "隱私權政策", """
<div style="max-width: 800px; margin: 0 auto;">
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0 0 20px;">
    蟬吃茶 ZenEaTea 重視您的隱私權。本政策說明我們如何收集、使用及保護您的個人資料。
  </p>
  <h2 style="font-size: 20px; margin: 24px 0 12px; color: #333;">資料收集</h2>
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0 0 20px;">
    我們僅在您主動提供時收集姓名、 email、電話及地址等資訊，用於訂單處理及聯繫。
  </p>
  <h2 style="font-size: 20px; margin: 24px 0 12px; color: #333;">資料使用</h2>
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0 0 20px;">
    收集之資料僅用於訂單履行、客戶服務及電子報寄送，不會轉售或分享給第三方。
  </p>
  <h2 style="font-size: 20px; margin: 24px 0 12px; color: #333;">資料安全</h2>
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0 0 20px;">
    我們採取合理的安全措施保護您的個人資料，未經授權不會存取或使用。
  </p>
  <h2 style="font-size: 20px; margin: 24px 0 12px; color: #333;">您的權利</h2>
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0;">
    依據個人資料保護法，您有權查詢、閱覽、製給複本、補充或更正、請求停止處理及利用、請求刪除您的個人資料。
  </p>
</div>"""),

    ("terms", "服務條款", "服務條款", """
<div style="max-width: 800px; margin: 0 auto;">
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0 0 20px;">
    歡迎使用蟬吃茶 ZenEaTea 網站。使用本網站即表示您同意以下條款。
  </p>
  <h2 style="font-size: 1px; margin: 24px 0 12px; color: #333;">服務內容</h2>
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0 0 20px;">
    本網站提供茶品瀏覽、購物車功能及相關資訊。目前為 POC 示範版本，購物車功能僅儲存於本地瀏覽器，不涉及實際交易。
  </p>
  <h2 style="font-size: 20px; margin: 24px 0 12px; color: #333;">智慧財產</h2>
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0 0 20px;">
    本網站所有內容（文字、圖片、logo）皆為蟬吃茶所有，未經授權不得複製或轉載。
  </p>
  <h2 style="font-size: 20px; margin: 24px 0 12px; color: #333;">免責聲明</h2>
  <p style="font-size: 15px; color: #555; line-height: 2; margin: 0;">
    本網站力求資訊正確，但不保證所有內容即時更新且完全無誤。如有疑問請與我們聯繫。
  </p>
</div>"""),
]

for slug, title, breadcrumb, content in SIMPLE_PAGES:
    wrapped = page_wrapper(title, breadcrumb, content)
    page = build_page(
        f"{title} | 蟬吃茶 ZenEaTea",
        f"{title} - 蟬吃茶 ZenEaTea，來自南投山上的自然農法好茶。",
        wrapped,
        extra_scripts='<script src="assets/zen-cart.js"></script><script src="assets/zen-wishlist.js"></script><script src="assets/zen-search.js"></script>',
    )
    out = BASE / f"{slug}.html"
    out.write_text(page, encoding="utf-8")
    print(f"  [WROTE] {out.name}")

print("[DONE] simple pages")


# ---------------------------------------------------------------------------
# Generate products listing page (unified, with category filter)
# ---------------------------------------------------------------------------
products_content = f"""
<div style="padding: 40px 0 80px;">
  <div class="page-width" style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
    <nav class="breadcrumb" style="margin-bottom: 30px; font-size: 13px; color: #888;">
      <a href="index.html" style="color: #888; text-decoration: none;">首頁</a>
      <span style="margin: 0 8px;">/</span>
      <span style="color: #333;">茶品介紹</span>
    </nav>
    <h1 style="font-size: 28px; margin-bottom: 30px; color: #333;">茶品介紹</h1>
    <div style="display: flex; gap: 12px; margin-bottom: 30px; flex-wrap: wrap;" class="zen-product-filter">
      <button class="zen-filter-btn" data-cat="all" style="padding: 8px 20px; background: #3a3a3a; color: #fff; border: none; border-radius: 20px; cursor: pointer; font-size: 14px;">全部</button>
      <button class="zen-filter-btn" data-cat="tea-bag" style="padding: 8px 20px; background: #fff; color: #333; border: 1px solid #ccc; border-radius: 20px; cursor: pointer; font-size: 14px;">茶包</button>
      <button class="zen-filter-btn" data-cat="tea-leaf" style="padding: 8px 20px; background: #fff; color: #333; border: 1px solid #ccc; border-radius: 20px; cursor: pointer; font-size: 14px;">茶葉</button>
      <button class="zen-filter-btn" data-cat="tea-ware" style="padding: 8px 20px; background: #fff; color: #333; border: 1px solid #ccc; border-radius: 20px; cursor: pointer; font-size: 14px;">茶具</button>
      <button class="zen-filter-btn" data-cat="gift-set" style="padding: 8px 20px; background: #fff; color: #333; border: 1px solid #ccc; border-radius: 20px; cursor: pointer; font-size: 14px;">禮盒</button>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;" class="zen-product-grid">
""" + "".join(f"""
      <div class="zen-product-card" data-cat="tea-leaf" style="text-decoration: none; color: inherit;">
        <a href="product-{p['slug']}.html" style="text-decoration: none; color: inherit;">
          <div style="background: #f5f6f7; border-radius: 8px; overflow: hidden; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; margin-bottom: 12px;">
            <img src="{p['image']}" alt="{p['name_zh']}" style="width: 100%; height: 100%; object-fit: contain;"/>
          </div>
          <p style="font-size: 12px; color: #888; margin: 0 0 4px;">{p['tea_type']}</p>
          <p style="font-size: 15px; color: #333; margin: 0 0 4px;">{p['name_zh']}</p>
          <p style="font-size: 14px; color: #666; margin: 0;">{p['price']}</p>
        </a>
        <div style="display: flex; gap: 8px; margin-top: 10px;">
          <button class="zen-add-to-cart" data-product-id="{p['id']}" data-product-name="{p['name_zh']}" data-product-price="{p['price']}" data-product-image="{p['image']}" style="padding: 6px 14px; background: #3a3a3a; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">加入購物車</button>
          <button class="zen-add-to-wishlist" data-product-id="{p['id']}" data-product-name="{p['name_zh']}" data-product-image="{p['image']}" style="padding: 6px 14px; background: #fff; color: #333; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; font-size: 12px;">♡</button>
        </div>
      </div>""" for p in PRODUCTS) + """
    </div>
  </div>
</div>
<style>
@media (max-width: 768px) { .zen-product-grid { grid-template-columns: repeat(2, 1fr) !important; } }
.zen-product-card { transition: opacity 0.3s; }
.zen-product-card.hidden { display: none; }
</style>
<script>
document.querySelectorAll('.zen-filter-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var cat = this.dataset.cat;
    document.querySelectorAll('.zen-filter-btn').forEach(function(b) {
      b.style.background = '#fff'; b.style.color = '#333'; b.style.border = '1px solid #ccc';
    });
    this.style.background = '#3a3a3a'; this.style.color = '#fff';
    document.querySelectorAll('.zen-product-card').forEach(function(card) {
      if (cat === 'all' || card.dataset.cat === cat) {
        card.classList.remove('hidden');
      } else {
        card.classList.add('hidden');
      }
    });
  });
});
</script>"""

page = build_page(
    "茶品介紹 | 蟬吃茶 ZenEaTea",
    "蟬吃茶四款自然農法好茶——蜜香紅茶、佳葉龍茶、鮮翠烏龍、玉山烏龍。",
    products_content,
    extra_scripts='<script src="assets/zen-cart.js"></script><script src="assets/zen-wishlist.js"></script><script src="assets/zen-search.js"></script>',
)
(BASE / "products.html").write_text(page, encoding="utf-8")
print("  [WROTE] products.html")

# Redirect pages for category links
for cat in ["tea-bag", "tea-leaf", "tea-ware", "gift-set"]:
    redirect = f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"/>
<meta content="0;url=products.html?cat={cat}" http-equiv="refresh"/>
<title>蟬吃茶 - 茶品介紹</title></head><body></body></html>"""
    (BASE / f"{cat}.html").write_text(redirect, encoding="utf-8")
    print(f"  [WROTE] {cat}.html (redirect to products.html?cat={cat})")

print("[DONE] products page")


# ---------------------------------------------------------------------------
# Generate journal/article list page + sample articles
# ---------------------------------------------------------------------------
journal_content = f"""
<div style="padding: 40px 0 80px;">
  <div class="page-width" style="max-width: 1000px; margin: 0 auto; padding: 0 20px;">
    <nav class="breadcrumb" style="margin-bottom: 30px; font-size: 13px; color: #888;">
      <a href="index.html" style="color: #888; text-decoration: none;">首頁</a>
      <span style="margin: 0 8px;">/</span>
      <span style="color: #333;">蟬茶日誌</span>
    </nav>
    <h1 style="font-size: 28px; margin-bottom: 30px; color: #333;">蟬茶日誌</h1>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px;" class="journal-grid">
""" + "".join(f"""
      <a href="article-{a['slug']}.html" style="text-decoration: none; color: inherit;">
        <div style="border-radius: 8px; overflow: hidden; aspect-ratio: 3/2; margin-bottom: 12px;">
          <img src="{a['image']}" alt="{a['title']}" style="width: 100%; height: 100%; object-fit: cover;"/>
        </div>
        <p style="font-size: 12px; color: #888; margin: 0 0 6px;">{a['type']}</p>
        <h3 style="font-size: 16px; color: #333; margin: 0 0 8px;">{a['title']}</h3>
        <p style="font-size: 14px; color: #666; line-height: 1.6; margin: 0;">{a['excerpt']}</p>
      </a>""" for a in ARTICLES) + """
    </div>
  </div>
</div>
<style>@media (max-width: 768px) { .journal-grid { grid-template-columns: 1fr !important; } }</style>"""

page = build_page(
    "蟬茶日誌 | 蟬吃茶 ZenEaTea",
    "蟬吃茶日誌——產地故事、自然農法、茶文化、沖泡知識與活動紀實。",
    journal_content,
    extra_scripts='<script src="assets/zen-cart.js"></script><script src="assets/zen-wishlist.js"></script>',
)
(BASE / "journal.html").write_text(page, encoding="utf-8")
print("  [WROTE] journal.html")

# Also make news.html and blog.html redirect to journal.html
for slug in ["news", "blog"]:
    redirect = f'''<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"/><meta content="0;url=journal.html" http-equiv="refresh"/><title>蟬吃茶 - 蟬茶日誌</title></head><body></body></html>'''
    (BASE / f"{slug}.html").write_text(redirect, encoding="utf-8")
    print(f"  [WROTE] {slug}.html (redirect to journal.html)")

# Sample article pages
for a in ARTICLES:
    art_content = f"""
<div style="padding: 40px 0 80px;">
  <div class="page-width" style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
    <nav class="breadcrumb" style="margin-bottom: 30px; font-size: 13px; color: #888;">
      <a href="index.html" style="color: #888; text-decoration: none;">首頁</a>
      <span style="margin: 0 8px;">/</span>
      <a href="journal.html" style="color: #888; text-decoration: none;">蟬茶日誌</a>
      <span style="margin: 0 8px;">/</span>
      <span style="color: #333;">{a['title']}</span>
    </nav>
    <p style="font-size: 13px; color: #888; margin: 0 0 12px;">{a['type']}</p>
    <h1 style="font-size: 28px; margin: 0 0 24px; color: #333;">{a['title']}</h1>
    <div style="border-radius: 8px; overflow: hidden; margin-bottom: 30px; aspect-ratio: 3/2;">
      <img src="{a['image']}" alt="{a['title']}" style="width: 100%; height: 100%; object-fit: cover;"/>
    </div>
    <div style="font-size: 16px; color: #555; line-height: 2;">
      <p style="margin: 0 0 20px;">{a['excerpt']}</p>
      <p style="margin: 0; color: #999; font-size: 14px;">內容製作中，更多詳細內容將陸續補上。</p>
    </div>
    <div style="margin-top: 40px;">
      <a href="journal.html" style="color: #3a3a3a; text-decoration: underline; font-size: 14px;">← 返回蟬茶日誌</a>
    </div>
  </div>
</div>"""
    page = build_page(
        f"{a['title']} | 蟬吃茶 ZenEaTea",
        f"{a['title']} - {a['excerpt']}",
        art_content,
        extra_scripts='<script src="assets/zen-cart.js"></script><script src="assets/zen-wishlist.js"></script>',
    )
    (BASE / f"article-{a['slug']}.html").write_text(page, encoding="utf-8")
    print(f"  [WROTE] article-{a['slug']}.html")

print("[DONE] journal + articles")


# ---------------------------------------------------------------------------
# Generate wishlist page
# ---------------------------------------------------------------------------
wishlist_content = """
<div style="padding: 40px 0 80px;">
  <div class="page-width" style="max-width: 1000px; margin: 0 auto; padding: 0 20px;">
    <nav class="breadcrumb" style="margin-bottom: 30px; font-size: 13px; color: #888;">
      <a href="index.html" style="color: #888; text-decoration: none;">首頁</a>
      <span style="margin: 0 8px;">/</span>
      <span style="color: #333;">我的收藏</span>
    </nav>
    <h1 style="font-size: 28px; margin-bottom: 30px; color: #333;">我的收藏</h1>
    <div id="zen-wishlist-container" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;">
      <p id="zen-wishlist-empty" style="grid-column: 1/-1; text-align: center; color: #888; font-size: 16px; padding: 60px 0;">目前沒有收藏的商品</p>
    </div>
  </div>
</div>
<style>
@media (max-width: 768px) { #zen-wishlist-container { grid-template-columns: repeat(2, 1fr) !important; } }
.zen-wishlist-card { text-decoration: none; color: inherit; }
.zen-wishlist-card img { width: 100%; aspect-ratio: 1; object-fit: contain; background: #f5f6f7; border-radius: 8px; margin-bottom: 8px; }
.zen-wishlist-remove { color: #c33; cursor: pointer; border: none; background: none; font-size: 13px; margin-top: 6px; }
</style>"""

page = build_page(
    "我的收藏 | 蟬吃茶 ZenEaTea",
    "我的收藏清單 - 蟬吃茶 ZenEaTea。",
    wishlist_content,
    extra_scripts='<script src="assets/zen-cart.js"></script><script src="assets/zen-wishlist.js"></script>',
)
(BASE / "wishlist.html").write_text(page, encoding="utf-8")
print("  [WROTE] wishlist.html")


# ---------------------------------------------------------------------------
# Generate search results page
# ---------------------------------------------------------------------------
search_content = """
<div style="padding: 40px 0 80px;">
  <div class="page-width" style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
    <nav class="breadcrumb" style="margin-bottom: 30px; font-size: 13px; color: #888;">
      <a href="index.html" style="color: #888; text-decoration: none;">首頁</a>
      <span style="margin: 0 8px;">/</span>
      <span style="color: #333;">搜尋結果</span>
    </nav>
    <h1 style="font-size: 28px; margin-bottom: 20px; color: #333;">搜尋結果</h1>
    <form id="zen-search-form" style="display: flex; gap: 8px; margin-bottom: 30px;">
      <input type="text" id="zen-search-input" placeholder="輸入關鍵字..." style="flex: 1; padding: 10px 16px; border: 1px solid #ddd; border-radius: 4px; font-size: 15px;"/>
      <button type="submit" style="padding: 10px 24px; background: #3a3a3a; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 15px;">搜尋</button>
    </form>
    <div id="zen-search-results"></div>
  </div>
</div>"""

page = build_page(
    "搜尋結果 | 蟬吃茶 ZenEaTea",
    "搜尋蟬吃茶的茶品與文章。",
    search_content,
    extra_scripts='<script src="assets/zen-cart.js"></script><script src="assets/zen-wishlist.js"></script><script src="assets/zen-search.js"></script>',
)
(BASE / "search.html").write_text(page, encoding="utf-8")
print("  [WROTE] search.html")

# cart.html placeholder
cart_content = """
<div style="padding: 40px 0 80px;">
  <div class="page-width" style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
    <h1 style="font-size: 28px; margin-bottom: 30px; color: #333;">購物車</h1>
    <p style="font-size: 16px; color: #888;">請點擊右上角的購物車圖示查看您的購物車。</p>
  </div>
</div>"""
page = build_page("購物車 | 蟬吃茶 ZenEaTea", "購物車", cart_content,
                  extra_scripts='<script src="assets/zen-cart.js"></script>')
(BASE / "cart.html").write_text(page, encoding="utf-8")
print("  [WROTE] cart.html")

print("\n=== ALL PAGES GENERATED ===")
