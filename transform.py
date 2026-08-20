"""
transform.py - Rebuild the Ippodo-cloned homepage as a ZenEaTea (蟬吃茶) POC site.

Purpose:
    Load zen_ea_tea/index.html (an Ippodo clone), replace every piece of
    brand content, navigation, hero, product grid, articles, trust section,
    and footer with ZenEaTea equivalents sourced from the requirements doc
    (蟬吃茶_需求拆解_最終版.md) and the asset manifest. Preserve all Ippodo
    CSS/JS/animation structure so the visual fidelity stays high.

Args:
    None. Paths are hardcoded relative to the zen_ea_tea/ project dir.

Returns:
    Overwrites zen_ea_tea/index.html in place. Prints a section-by-section
    completion log.

Notes:
    - Hero: Ippodo uses 4 parallax-layered PNGs. M1.4.2 forbids parallax,
      so we collapse to a single static hero image (m240130.jpg) with the
      existing fade-in animation preserved.
    - Two new sections are injected (Ippodo has no equivalent):
      1) Four Homophones brand section (潺/禪/蟬/饞)
      2) Trust section (製茶師陳昭鳳・茶王・鹿鳴特優)
    - Prices are placeholder NT$ values pending FamiShop data export (M10.2).
"""

from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
HTML = BASE / "index.html"
B = "assets/brand/"

soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")

# ---------------------------------------------------------------------------
# 0. <title>, meta description, og tags
# ---------------------------------------------------------------------------
if soup.title:
    soup.title.string = "蟬吃茶 ZenEaTea | 來自南投山上的自然農法好茶"
for meta in soup.find_all("meta", attrs={"name": "description"}):
    meta["content"] = (
        "蟬吃茶 ZenEaTea，來自南投山上的自然農法茶園。"
        "小綠葉蟬吸食茶樹嫩芽，烘焙後產生天然蜜果香氣。"
        "製茶師陳昭鳳・全國製茶武林大賽茶王・鹿鳴自然生態烏龍茶大賽特優。"
    )
for meta in soup.find_all("meta", attrs={"property": "og:site_name"}):
    meta["content"] = "蟬吃茶 ZenEaTea"
for meta in soup.find_all("meta", attrs={"property": "og:title"}):
    meta["content"] = "蟬吃茶 ZenEaTea | 來自南投山上的自然農法好茶"
for meta in soup.find_all("meta", attrs={"property": "og:description"}):
    meta["content"] = "來自南投山上的自然農法茶園，製茶師陳昭鳳・茶王・鹿鳴特優。"
print("[0] title/meta done")

# ---------------------------------------------------------------------------
# 1. Announcement bar
# ---------------------------------------------------------------------------
for ann in soup.select(".announcement-bar__message"):
    ann.clear()
    ann.append(BeautifulSoup(
        "<p>製茶師陳昭鳳 ・ 全國製茶武林大賽【茶王】・ 鹿鳴自然生態烏龍茶大賽特優</p>",
        "html.parser"))
print("[1] announcement bar done")

# ---------------------------------------------------------------------------
# 2. Header logo  IPPODO -> 蟬吃茶
# ---------------------------------------------------------------------------
for a in soup.select("a.c-header__logo"):
    a.string = "蟬吃茶"
print("[2] header logo done")

# ---------------------------------------------------------------------------
# 3. PC navigation (c-gnav-pc)
# ---------------------------------------------------------------------------
gnav = soup.select_one("div.c-gnav-pc")
if gnav:
    gnav.clear()
    gnav.append(BeautifulSoup("""
<div class="c-gnav-pc__lv01 c-js--over">
  <a class="c-gnav-pc__lv01__link" href="javascript:void(0)">關於蟬吃茶</a>
  <div class="c-gnav-pc__inner">
    <ul class="c-gnav-pc__lv02">
      <li class="c-gnav-pc__lv02__item">
        <a href="#about"><img alt="" class="c-img-nav--pc border" height="190" loading="eager" src=\"""" + B + """zh-789ede0530.png" width="150"/>
        <div class="c-gnav-pc__lv02__title">品牌故事</div></a>
      </li>
      <li class="c-gnav-pc__lv02__item">
        <a href="#store"><img alt="" class="c-img-nav--pc border" height="190" loading="eager" src=\"""" + B + """240130.jpg" width="150"/>
        <div class="c-gnav-pc__lv02__title">門市資訊</div></a>
      </li>
    </ul>
  </div>
</div>
<div class="c-gnav-pc__lv01 c-js--over">
  <a class="c-gnav-pc__lv01__link" href="javascript:void(0)">茶品知識</a>
  <div class="c-gnav-pc__inner">
    <ul class="c-gnav-pc__lv02">
      <li class="c-gnav-pc__lv02__item">
        <a href="#tea-intro"><img alt="" class="c-img-nav--pc border" height="190" loading="eager" src=\"""" + B + """zh-1f0dfb5b8b.png" width="150"/>
        <div class="c-gnav-pc__lv02__title">茶品介紹</div></a>
      </li>
      <li class="c-gnav-pc__lv02__item">
        <a href="#brewing"><img alt="" class="c-img-nav--pc border" height="190" loading="eager" src=\"""" + B + """GABA.jpg" width="150"/>
        <div class="c-gnav-pc__lv02__title">沖泡指南</div></a>
      </li>
    </ul>
  </div>
</div>
<div class="c-gnav-pc__lv01 c-js--over">
  <a class="c-gnav-pc__lv01__link" href="javascript:void(0)">購物</a>
  <div class="c-gnav-pc__inner">
    <ul class="c-gnav-pc__lv03">
      <li><a href="#tea-bag"><img alt="" class="c-img-nav-category" height="58" loading="eager" src=\"""" + B + """350x200-430fbc.jpg" width="58"/><p class="c-gnav-pc__lv03__title">茶包<br/><span class="caption"></span></p></a></li>
      <li><a href="#tea-leaf"><img alt="" class="c-img-nav-category" height="58" loading="eager" src=\"""" + B + """350x200-003b9c.jpg" width="58"/><p class="c-gnav-pc__lv03__title">茶葉<br/><span class="caption"></span></p></a></li>
      <li><a href="#tea-ware"><img alt="" class="c-img-nav-category" height="58" loading="eager" src=\"""" + B + """350x200-c40400.jpg" width="58"/><p class="c-gnav-pc__lv03__title">茶具<br/><span class="caption"></span></p></a></li>
      <li><a href="#gift-set"><img alt="" class="c-img-nav-category" height="58" loading="eager" src=\"""" + B + """350x200.jpg" width="58"/><p class="c-gnav-pc__lv03__title">禮盒<br/><span class="caption"></span></p></a></li>
    </ul>
  </div>
</div>
<div class="c-gnav-pc__lv01 c-js--over">
  <a class="c-gnav-pc__lv01__link" href="javascript:void(0)">蟬茶日誌</a>
  <div class="c-gnav-pc__inner">
    <ul class="c-gnav-pc__lv02">
      <li class="c-gnav-pc__lv02__item c-gnav-pc__lv02__ochakura">
        <a class="c-gnav-pc__lv02__item-link" href="#journal">
          <img alt="" class="c-img-nav--pc border" height="190" loading="eager" src=\"""" + B + """zh-3a2d00425c.jpeg" width="150"/>
          <div class="c-gnav-pc__lv02__body">
            <p class="c-gnav-pc__lv02__title">蟬茶日誌</p>
            <p class="c-text-nav--lead">產地故事、自然農法、茶文化與沖泡知識。</p>
          </div>
        </a>
      </li>
      <li class="c-gnav-pc__lv02__item c-gnav-pc__lv02__ochakura">
        <a class="c-gnav-pc__lv02__item-link" href="#blog">
          <img alt="" class="c-img-nav--pc border" height="190" loading="eager" src=\"""" + B + """2.jpg" width="150"/>
          <div class="c-gnav-pc__lv02__body">
            <p class="c-gnav-pc__lv02__title">活動與獎項</p>
            <p class="c-text-nav--lead">全國製茶武林大賽茶王、鹿鳴自然生態烏龍茶大賽特優。</p>
          </div>
        </a>
      </li>
    </ul>
  </div>
</div>
<div class="c-gnav-pc__lv01 c-js--over">
  <a class="c-gnav-pc__lv01__link" href="#news">最新消息</a>
</div>
""", "html.parser"))
print("[3] PC nav done")

# ---------------------------------------------------------------------------
# 4. SP navigation (c-gnav-sp__lv01 groups)
# ---------------------------------------------------------------------------
sp_nav = soup.select_one("div.c-gnav-sp > div.c-gnav-sp--open")
if sp_nav:
    # keep logo & top icons; replace the lv01 lists
    for ul in sp_nav.select("ul.c-gnav-sp__lv01"):
        ul.decompose()
    # also remove lang list
    for ul in sp_nav.select("ul.c-gnav-lang"):
        ul.decompose()
    insert_after = sp_nav.select_one("div.c-gnav-sp__search-container")
    new_nav = BeautifulSoup("""
<ul class="c-gnav-sp__lv01">
  <li class="c-gnav-sp__lv01__title"><a href="#about">品牌故事</a></li>
  <li class="c-gnav-sp__lv01__title"><a href="#store">門市資訊</a></li>
</ul>
<ul class="c-gnav-sp__lv01">
  <li class="c-gnav-sp__lv01__title"><a href="#tea-intro">茶品介紹</a></li>
  <li class="c-gnav-sp__lv01__title"><a href="#brewing">沖泡指南</a></li>
</ul>
<ul class="c-gnav-sp__lv01">
  <li><span class="c-gnav-sp__lv01__title">購物</span>
    <ul class="c-gnav-sp__lv02">
      <li><a href="#tea-bag"><img alt="" class="c-img-nav-category" height="40" src=\"""" + B + """350x200-430fbc.jpg" width="42"/><span class="c-gnav-sp__lv02__title">茶包<br/><span class="caption"></span></span></a></li>
      <li><a href="#tea-leaf"><img alt="" class="c-img-nav-category" height="40" src=\"""" + B + """350x200-003b9c.jpg" width="42"/><span class="c-gnav-sp__lv02__title">茶葉<br/><span class="caption"></span></span></a></li>
      <li><a href="#tea-ware"><img alt="" class="c-img-nav-category" height="40" src=\"""" + B + """350x200-c40400.jpg" width="42"/><span class="c-gnav-sp__lv02__title">茶具<br/><span class="caption"></span></span></a></li>
      <li><a href="#gift-set"><img alt="" class="c-img-nav-category" height="40" src=\"""" + B + """350x200.jpg" width="42"/><span class="c-gnav-sp__lv02__title">禮盒<br/><span class="caption"></span></span></a></li>
    </ul>
  </li>
</ul>
<ul class="c-gnav-sp__lv01">
  <li class="c-gnav-sp__lv01__title"><a href="#journal">蟬茶日誌</a></li>
  <li class="c-gnav-sp__lv01__title"><a href="#blog">活動與獎項</a></li>
</ul>
<ul class="c-gnav-sp__lv01">
  <li class="c-gnav-sp__lv01__title"><a href="#news">最新消息</a></li>
</ul>
<ul class="c-gnav-sp__lv01">
  <li class="c-gnav-sp__lv01__title"><a href="#contact">聯絡我們</a></li>
  <li class="c-gnav-sp__lv01__title"><a href="#faq">常見問答</a></li>
</ul>
""", "html.parser")
    sp_nav.append(new_nav)
print("[4] SP nav done")

# ---------------------------------------------------------------------------
# 5. Hero - collapse 4 parallax layers into single static image
# ---------------------------------------------------------------------------
hero = soup.select_one("div.p-top-hero")
if hero:
    # remove the video-open button
    for btn in hero.select("a.p-top-video-open"):
        btn.decompose()
    hero_ul = hero.select_one("ul.p-top-hero__image")
    if hero_ul:
        hero_ul.clear()
        hero_ul.append(BeautifulSoup(
            '<li class="js-fadetarget is-active"><div class="p-top-hero__item banner-img-1 p-top-hero__item--main"></div></li>',
            "html.parser"))
# replace the inline <style> block that sets banner-img-1..4
for style in soup.find_all("style"):
    txt = style.string or ""
    if "banner-img-1" in txt and "mainvisual" in txt:
        style.string = """
  @media (min-width: 769px){.banner-img-1{
        background-image: url(""" + B + """m240130.jpg);
        background-size: cover; background-position: center;
      }}
  @media (max-width: 768px){.banner-img-1{
          background-image: url(""" + B + """m240130.jpg);
          background-size: cover; background-position: center;
        }}
"""
print("[5] hero done")

# ---------------------------------------------------------------------------
# 6. Feature slider - 4 tea feature cards
# ---------------------------------------------------------------------------
feat = soup.select_one("div.p-top-feature")
if feat:
    wrap = feat.select_one("div.p-top-feature__list.swiper-wrapper")
    if wrap:
        wrap.clear()
        items = [
            ("#honey-black", B + "zh-0698346863.png", "蟬吃蜜香紅茶 — 小綠葉蟬的天然蜜果香"),
            ("#gaba", B + "zh-252518c735.png", "蟬吃佳葉龍茶 — 厭氧發酵・安定心神"),
            ("#fresh-oolong", B + "zh-1f0dfb5b8b.png", "蟬吃鮮翠烏龍茶 — 輕發酵中烘焙・清香甘潤"),
            ("#yushan-oolong", B + "zh-df5984bc2c.png", "蟬吃玉山烏龍茶 — 高山雲霧・葉厚耐泡"),
        ]
        for href, img, title in items:
            wrap.append(BeautifulSoup(
                f'<div class="o-feature-list__item swiper-slide"><a href="{href}"><img alt="" class="a-image" src="{img}"/><p class="o-feature-list__item-title">{title}</p></a></div>',
                "html.parser"))
print("[6] feature slider done")

# ---------------------------------------------------------------------------
# 7. Best Sellers -> 蟬吃茶嚴選 (4 product cards)
# ---------------------------------------------------------------------------
hl = soup.select_one("div.o-product-list--slider.p-top-highlight")
if hl:
    title_el = hl.select_one("h3.o-product-list__title")
    if title_el:
        title_el.string = "蟬吃茶嚴選"
    ul = hl.select_one("ul.p-top-highlight__list")
    if ul:
        ul.clear()
        products = [
            ("#honey-black", B + "zh-0698346863.png", "蜜香紅茶", "蟬吃蜜香紅茶 25g 袋", "NT$480"),
            ("#gaba", B + "zh-252518c735.png", "佳葉龍茶", "蟬吃佳葉龍茶 25g 袋", "NT$520"),
            ("#fresh-oolong", B + "zh-1f0dfb5b8b.png", "烏龍茶", "蟬吃鮮翠烏龍茶 25g 袋", "NT$450"),
            ("#yushan-oolong", B + "zh-df5984bc2c.png", "烏龍茶", "蟬吃玉山烏龍茶 25g 袋", "NT$680"),
        ]
        for href, img, cat, name, price in products:
            ul.append(BeautifulSoup(
                f'''<li class="p-top-highlight__item o-product-list__item swiper-slide js-fadetarget">
<div class="m-product-card js-product-card">
<a class="m-product-card__image" href="{href}"><img alt="{name}" class="a-image-product--type01" src="{img}"/></a>
<div class="m-product-card__body">
<p class="m-product-card__category">{cat}</p>
<div class="m-product-card__name"><a class="a-link-product--type01" href="{href}"><div>{name}</div></a></div>
<p class="m-product-card__price a-text-price--type01">{price}</p>
</div></div></li>''',
                "html.parser"))
print("[7] best sellers done")

# ---------------------------------------------------------------------------
# 8. Recipe section -> 品茗搭配 (knowledge articles)
# ---------------------------------------------------------------------------
recipe = soup.select_one("div.p-top-recipe")
if recipe:
    logo_el = recipe.select_one("h2.p-top-recipe__logo")
    if logo_el:
        logo_el.string = "品茗筆記"
    title_en = recipe.select_one("div.p-top-recipe__title-en")
    if title_en:
        title_en.string = "Tea Notes"
    lead = recipe.select_one("p.p-top-recipe__text-en")
    if lead:
        lead.string = "從產地故事、自然農法到沖泡知識，走進蟬吃茶的茶世界。"
    ul = recipe.select_one("ul.p-top-recipe__list")
    if ul:
        ul.clear()
        arts = [
            ("#journal", B + "1671099309366.jpg", "玉山自然茶園", "#產地故事"),
            ("#journal", B + "GABA.jpg", "GABA茶、佳葉龍茶介紹", "#知識型"),
            ("#journal", B + "zh-3a2d00425c.jpeg", "吃茶去 — 茶文化", "#茶文化"),
        ]
        for href, img, title, tag in arts:
            ul.append(BeautifulSoup(
                f'''<li class="p-top-recipe__item m-blog--recipe swiper-slide js-fadetarget">
<a href="{href}"><img alt="" class="p-top-recipe__image a-image" src="{img}"/></a>
<div class="m-blog__body">
<a class="m-blog__title">{title}</a>
<div class="m-blog__tag"><div><a class="a-tag--type03" href="{href}">{tag}</a></div></div>
</div></li>''',
                "html.parser"))
    btn = recipe.select_one("a.p-top-recipe__button")
    if btn:
        btn.string = "查看更多"
print("[8] recipe -> tea notes done")

# ---------------------------------------------------------------------------
# 9. iroiro section -> 蟬茶日誌 stories
# ---------------------------------------------------------------------------
iro = soup.select_one("div.p-top-iroiro")
if iro:
    h = iro.select_one("h2.p-top-iroiro__heading-en")
    if h:
        h.string = "蟬茶日誌・活動與獎項"
    p = iro.select_one("p.p-top-iroiro__lead")
    if p:
        p.string = "製茶師陳昭鳳的故事、自然農法的堅持、茶文化與活動紀實。"
    ul = iro.select_one("ul.p-top-iroiro__list")
    if ul:
        ul.clear()
        stories = [
            ("#blog", B + "2.jpg", "活動與獎項", "全國製茶武林大賽・榮獲茶王"),
            ("#journal", B + "zh-e4383d3a55.jpeg", "知識型", "各種茶的英文要怎麼說？"),
            ("#journal", B + "240130.jpg", "品牌理念", "蟬吃茶用心製作一杯好茶"),
        ]
        for href, img, ep, title in stories:
            ul.append(BeautifulSoup(
                f'''<li class="p-top-iroiro__item m-blog--iroiro swiper-slide js-fadetarget">
<a href="{href}"><img alt="" src="{img}"/>
<div class="m-blog__body"><div class="m-blog__episode">{ep}</div><p class="m-blog__title">{title}</p></div></a></li>''',
                "html.parser"))
    btn = iro.select_one("a.p-top-iroiro__button")
    if btn:
        btn.string = "查看更多"
print("[9] iroiro -> journal done")

# ---------------------------------------------------------------------------
# 10. Buy section -> 購物指南 (4 categories)
# ---------------------------------------------------------------------------
buy = soup.select_one("div.p-top-buy")
if buy:
    hero_img = buy.select_one("img.a-image")
    if hero_img:
        hero_img["src"] = B + "zh-0698346863.png"
        hero_img["alt"] = "購物"
    title_jp = buy.select_one("h2.p-top-buy__title")
    if title_jp:
        title_jp.string = "選購"
    title_en = buy.select_one("div.p-top-buy__title-en")
    if title_en:
        title_en.string = "Shopping"
    txt = buy.select_one("p.p-top-buy__text-en")
    if txt:
        txt.string = "四款自然農法好茶，從蜜香紅茶到玉山烏龍，每一口都是南投山上的風土。"
    ul = buy.select_one("ul.p-top-buy__nav")
    if ul:
        ul.clear()
        cats = [
            ("#tea-bag", B + "350x200-430fbc.jpg", "茶包"),
            ("#tea-leaf", B + "350x200-003b9c.jpg", "茶葉"),
            ("#tea-ware", B + "350x200-c40400.jpg", "茶具"),
            ("#gift-set", B + "350x200.jpg", "禮盒"),
        ]
        for href, img, name in cats:
            ul.append(BeautifulSoup(
                f'''<li class="p-top-buy__item js-fadetarget">
<a href="{href}"><img alt="" class="p-top-buy__image" src="{img}"/>
<div class="p-top-buy__name">{name}</div></a></li>''',
                "html.parser"))
print("[10] buy section done")

# ---------------------------------------------------------------------------
# 11. News section -> 最新消息
# ---------------------------------------------------------------------------
news = soup.select_one("div.p-top-news")
if news:
    h = news.select_one("h2.p-top-news__heading")
    if h:
        h.string = "最新消息"
    ul = news.select_one("ul.p-top-news__list")
    if ul:
        ul.clear()
        items = [
            ("2026-08-13", "蟬吃茶 AI 形象購物官網 POC 上線"),
            ("2024-01-30", "製茶師陳昭鳳・全國製茶武林大賽榮獲茶王"),
            ("2023-12-15", "2023 冬季鹿鳴自然生態烏龍茶大賽・特優"),
            ("2023-10-01", "園遊會×草地茶席活動紀實"),
        ]
        for date, title in items:
            ul.append(BeautifulSoup(
                f'''<li class="p-top-news__item"><a href="#news">
<div class="p-top-news__date"><time datetime="{date}">{date}</time></div>
<h3 class="p-top-news__title">{title}</h3></a></li>''',
                "html.parser"))
    btn = news.select_one("a.p-top-news__button")
    if btn:
        btn.string = "查看更多"
print("[11] news done")

# ---------------------------------------------------------------------------
# 12. Others section -> 品牌故事 cards (About / Tea / Events)
# ---------------------------------------------------------------------------
oth = soup.select_one("div.p-top-others")
if oth:
    nav = oth.select_one("nav.o-card-nav")
    if nav:
        nav.clear()
        cards = [
            ("#about", B + "zh-789ede0530.png", "關於蟬吃茶"),
            ("#tea-intro", B + "zh-1f0dfb5b8b.png", "茶品介紹"),
            ("#store", B + "240130.jpg", "門市與活動"),
        ]
        for href, img, title in cards:
            nav.append(BeautifulSoup(
                f'''<a class="p-top-others-nav__item js-fadetarget o-card-nav__link" href="{href}">
<div class="o-card-nav__image"><img alt="{title}" src="{img}"/></div>
<div class="o-card-nav__content"><span class="o-card-nav__title">{title}</span></div></a>''',
                "html.parser"))
print("[12] others done")

# ---------------------------------------------------------------------------
# 13. Footer - links, social, copyright, newsletter
# ---------------------------------------------------------------------------
# Footer link blocks
for fb in soup.select(".footer-block__details-content"):
    fb.decompose()
footer_top = soup.select_one("div.footer__content-top")
if footer_top:
    blocks = footer_top.select("div.footer-block")
    for b in blocks:
        b.decompose()
    footer_top.clear()
    footer_top.append(BeautifulSoup("""
<div class="footer__blockswrapper grid grid--1-col grid--2-col grid--4-col-tablet">
<div class="footer-block grid__item footer-block--menu"><ul class="footer-block__details-content list-unstyled">
<li class="m-accordion--type01 js-accordion footer-accordion"><div class="footer-link01 js-accordion-trigger">關於蟬吃茶<i class="a-icon--accordion--type01 m-accordion__icon c-links-unit__arrow"></i></div>
<ul class="footer-link-child js-accordion-content">
<li class="level2"><a href="#about">品牌故事</a></li>
<li class="level2"><a href="#store">門市資訊</a></li>
<li class="level2"><a href="#tea-master">製茶師陳昭鳳</a></li>
</ul></li></ul></div>
<div class="footer-block grid__item footer-block--menu"><ul class="footer-block__details-content list-unstyled">
<li class="m-accordion--type01 js-accordion footer-accordion"><div class="footer-link01 js-accordion-trigger">茶品知識<i class="a-icon--accordion--type01 m-accordion__icon c-links-unit__arrow"></i></div>
<ul class="footer-link-child js-accordion-content">
<li class="level2"><a href="#tea-intro">茶品介紹</a></li>
<li class="level2"><a href="#brewing">沖泡指南</a></li>
</ul></li></ul></div>
<div class="footer-block grid__item footer-block--menu"><ul class="footer-block__details-content list-unstyled">
<li class="m-accordion--type01 js-accordion footer-accordion"><div class="footer-link01 js-accordion-trigger">購物<i class="a-icon--accordion--type01 m-accordion__icon c-links-unit__arrow"></i></div>
<ul class="footer-link-child js-accordion-content">
<li class="level2"><a href="#tea-bag">茶包</a></li>
<li class="level2"><a href="#tea-leaf">茶葉</a></li>
<li class="level2"><a href="#tea-ware">茶具</a></li>
<li class="level2"><a href="#gift-set">禮盒</a></li>
</ul></li></ul></div>
<div class="footer-block grid__item footer-block--menu"><ul class="footer-block__details-content list-unstyled">
<li class="m-accordion--type01 js-accordion footer-accordion"><div class="footer-link01 js-accordion-trigger">客服<i class="a-icon--accordion--type01 m-accordion__icon c-links-unit__arrow"></i></div>
<ul class="footer-link-child js-accordion-content">
<li class="level2"><a href="#faq">常見問答</a></li>
<li class="level2"><a href="#contact">聯絡我們</a></li>
<li class="level2"><a href="https://liff.line.me/1645278921-kWRPP32q/?accountId=lgr7235d">LINE 官方帳號</a></li>
</ul></li></ul></div>
</div>
""", "html.parser"))

# Social links
sns = soup.select_one("nav.c-footer-sns")
if sns:
    sns.clear()
    sns.append(BeautifulSoup("""
<ul class="c-footer-sns__list">
<li class="c-footer-sns__item c-footer-sns__facebook"><a href="https://www.facebook.com/profile.php?id=100063636140648" rel="noopener noreferrer" target="_blank"><i class="c-icon--facebook c-icon"></i><span class="c-footer-sns__text">蟬吃茶</span></a></li>
<li class="c-footer-sns__item c-footer-sns__instagram"><a href="https://www.instagram.com/healthtea1000" rel="noopener noreferrer" target="_blank"><i class="c-icon--instagram c-icon"></i><span class="c-footer-sns__text">@healthtea1000</span></a></li>
</ul>
""", "html.parser"))

# Copyright + logo
copy = soup.select_one("p.c-footer__copyright")
if copy:
    copy.string = "© 2026 蟬吃茶 ZenEaTea"
footer_logo = soup.select_one("a.c-footer__logo img")
if footer_logo:
    footer_logo["src"] = B + "1670492324156.jpg"
    footer_logo["alt"] = "蟬吃茶"

# Newsletter title
nl_title = soup.select_one("h3.c-newsletter__title")
if nl_title:
    nl_title.string = "訂閱電子報"
nl_input = soup.select_one("input.c-newsletter__input")
if nl_input:
    nl_input["placeholder"] = "請輸入 email"
nl_btn = soup.select_one("button.c-newsletter__button")
if nl_btn:
    nl_btn.string = "訂閱"
# privacy label
for lab in soup.select("label.a-label-checkbox--type02"):
    lab.clear()
    lab.append(BeautifulSoup(
        '我同意 <a class="a-link--type01" href="#privacy">隱私權政策</a> 與 <a class="a-link--type01" href="#terms">服務條款</a>',
        "html.parser"))
# bottom lang links & terms
for fl in soup.select("ul.c-footer__links--terms"):
    fl.clear()
    fl.append(BeautifulSoup(
        '<li><a href="#privacy">隱私權政策</a></li><li><a href="#terms">服務條款</a></li>',
        "html.parser"))
# remove the lang switcher at bottom
for btn in soup.select("div.c-footer__button"):
    btn.decompose()
print("[13] footer done")

# ---------------------------------------------------------------------------
# 14. Inject two new sections: Four Homophones + Trust
#     Insert after the hero section, before feature slider.
#     We insert as new <div class="shopify-section"> wrappers so the
#     existing CSS layout rhythm is preserved.
# ---------------------------------------------------------------------------
main = soup.select_one("main#MainContent")
hero_section = soup.select_one("#shopify-section-template--16094548295831__995f922e-2572-4102-b57f-f2200dd0b391")

new_sections_html = """
<div class="shopify-section" id="shopify-section-zen-brand">
<div class="p-top-iroiro" style="padding:80px 0 40px;">
<h2 class="p-top-iroiro__heading-en" style="text-align:center; margin-bottom:12px;">潺・禪・蟬・饞 吃茶</h2>
<p class="p-top-iroiro__lead" style="text-align:center; max-width:680px; margin:0 auto 40px;">四個同音字，四種喝茶的理由。潺潺流水的健康、禪意寧靜的當下、友善生物的自然、喝一口就愛上的饞。</p>
<div style="max-width:960px; margin:0 auto; display:grid; grid-template-columns:repeat(4,1fr); gap:24px;" class="zen-homophones">
""" + "".join(f'''<div class="js-fadetarget" style="text-align:center;">
<img alt="{ch}吃茶" src="{B}{img}" style="width:100%; max-width:140px; height:auto; margin:0 auto 12px; display:block;"/>
<h3 style="font-size:18px; margin:0 0 6px;">{ch}吃茶</h3>
<p style="font-size:13px; color:#666; line-height:1.6; margin:0;">{theme}</p>
</div>''' for ch, img, theme in [
    ("潺", "zh-5022a890a3.png", "好喝、自然健康、心靈寧靜；如潺潺流水涓涓不息"),
    ("禪", "zh-d69dd08d36.png", "寧靜、專注地感受當下"),
    ("蟬", "zh-789ede0530.png", "友善生物、大地及自己；純樸、自然、健康"),
    ("饞", "zh-165f6dcbcc.png", "喝一口就令人愛上"),
]) + """
</div>
</div>
</div>
<div class="shopify-section" id="shopify-section-zen-trust">
<div class="p-top-buy" id="tea-master" style="padding:60px 0 80px;">
<div class="p-top-buy__heading-en"><h2 class="p-top-buy__title">信任</h2><div class="p-top-buy__titlearea-en">
<div class="p-top-buy__title-en">Our Trust</div><p class="p-top-buy__text-en">製茶師陳昭鳳・全國製茶武林大賽【茶王】・鹿鳴自然生態烏龍茶大賽有機烏龍茶組「特優」・行政院農委會茶業改良場魚池分場評審。</p></div></div>
<div style="max-width:960px; margin:32px auto 0; display:grid; grid-template-columns:repeat(3,1fr); gap:24px;">
<div class="js-fadetarget" style="text-align:center; padding:24px; border:1px solid #e0d6cc; border-radius:8px;">
<h3 style="font-size:16px; margin:0 0 8px;">製茶師 陳昭鳳</h3><p style="font-size:13px; color:#666; line-height:1.6; margin:0;">2018 年首次參賽即為當時唯一女性製茶師，歷年武林大賽從不缺席。</p></div>
<div class="js-fadetarget" style="text-align:center; padding:24px; border:1px solid #e0d6cc; border-radius:8px;">
<h3 style="font-size:16px; margin:0 0 8px;">全國製茶武林大賽 茶王</h3><p style="font-size:13px; color:#666; line-height:1.6; margin:0;">2024 年製茶師陳昭鳳榮獲全國製茶武林大賽【茶王】。</p></div>
<div class="js-fadetarget" style="text-align:center; padding:24px; border:1px solid #e0d6cc; border-radius:8px;">
<h3 style="font-size:16px; margin:0 0 8px;">鹿鳴自然生態烏龍茶大賽 特優</h3><p style="font-size:13px; color:#666; line-height:1.6; margin:0;">2023 冬季有機烏龍茶組「特優」，評審單位：茶業改良場魚池分場。</p></div>
</div>
</div>
</div>
"""

if main and hero_section:
    hero_section.insert_after(BeautifulSoup(new_sections_html, "html.parser"))
print("[14] brand + trust sections injected")

# ---------------------------------------------------------------------------
# 15. Favicon
# ---------------------------------------------------------------------------
for link in soup.find_all("link", rel="icon"):
    link["href"] = B + "favicon.png"
print("[15] favicon done")

# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------
HTML.write_text(str(soup), encoding="utf-8")
print(f"\nDONE -> {HTML}  ({HTML.stat().st_size} bytes)")
