"""Apply Claude Code's manual fixes to rebuilt index.html"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
INDEX = BASE / "index.html"
html = INDEX.read_text(encoding="utf-8")

# 1. Add IPPODO.global before bundle.js
html = html.replace(
    '<script defer="defer" src="assets/is_touch_device.js"></script>\n<script defer="defer" src="assets/bundle.js"></script>',
    '<script>var IPPODO = IPPODO || {}; IPPODO.global = 1;</script>\n<script defer="defer" src="assets/is_touch_device.js"></script>\n<script defer="defer" src="assets/bundle.js"></script>'
)

# 2. Add Swiper CDN + manual init + zen-fixes.css/js after bundle.js
html = html.replace(
    '<script defer="defer" src="assets/vendor.bundle.js"></script>',
    """<script defer="defer" src="assets/vendor.bundle.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@6/swiper-bundle.min.css"/>
<script src="https://cdn.jsdelivr.net/npm/swiper@6/swiper-bundle.min.js"></script>
<link href="assets/zen-fixes.css" rel="stylesheet"/>
<script>
window.addEventListener('load', function () {
  if (typeof Swiper === 'undefined') { console.error('Swiper CDN failed'); return; }
  function init(el, opts) {
    if (!el || el.swiper) return;
    try { new Swiper(el, opts); } catch (e) { console.warn('swiper fail', el && el.className, e); }
  }
  document.querySelectorAll('.js-slider-feature').forEach(function (el) {
    init(el, { spaceBetween: 10, slidesPerView: 1.4, centeredSlides: true, loop: true, speed: 400, autoplay: { delay: 4000 }, breakpoints: { 769: { slidesPerView: 3 } } });
  });
  document.querySelectorAll('.js-slider-highlight').forEach(function (el) {
    init(el, { slidesPerView: 2, grabCursor: true, breakpoints: { 769: { slidesPerView: 4 } }, scrollbar: { el: el.parentElement.querySelector('.js-slider-highlight__scrollbar') || '.js-slider-highlight__scrollbar', draggable: true } });
  });
  document.querySelectorAll('.js-slider-recipe').forEach(function (el) {
    init(el, { slidesPerView: 1.2, spaceBetween: 20, breakpoints: { 769: { slidesPerView: 3 } } });
  });
  document.querySelectorAll('.js-slider-story').forEach(function (el) {
    init(el, { slidesPerView: 1.2, spaceBetween: 20, breakpoints: { 769: { slidesPerView: 3 } } });
  });
  console.log('Swiper init done, containers:', document.querySelectorAll('.swiper-container').length);
  var fadeEls = document.querySelectorAll('.js-fadetarget');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) en.target.classList.add('is-active'); });
    }, { threshold: 0.1 });
    fadeEls.forEach(function (el) { io.observe(el); });
  } else {
    fadeEls.forEach(function (el) { el.classList.add('is-active'); });
  }
});
</script>
<script src="assets/zen-fixes.js"></script>
<script src="assets/zen-cart.js"></script>
<script src="assets/zen-wishlist.js"></script>
<script src="assets/zen-search.js"></script>"""
)

# 3. Fix hero image to hero-banner.jpg
html = html.replace(
    'background-image: url(assets/mainvisual-back_5d948aa7-b685-42ee-9164-e56ec5b58b8c_1900x.png);',
    'background-image: url(assets/brand/hero-banner.jpg);'
)
html = html.replace(
    'background-image: url(assets/mainvisual-ippodo_8b242456-3786-4a02-997e-1fcb288d79cb_1900x.png);',
    'background-image: url(assets/brand/hero-banner.jpg);'
)
html = html.replace(
    'background-image: url(assets/mainvisual-front01_b676baa7-a2a9-4cb3-83cf-8f8e14502c54_1900x.png);',
    ''
)
html = html.replace(
    'background-image: url(assets/mainvisual-front02_98d7f787-eaac-48b9-ae58-a27505b2275f_1900x.png);',
    ''
)
html = html.replace(
    'background-image: url(assets/mainvisual-back-sp_74c74b64-3a24-4ff5-9294-f4d0e86e4338_1000x.png);',
    'background-image: url(assets/brand/hero-banner.jpg);'
)
html = html.replace(
    'background-image: url(assets/mainvisual-sp-white_61ccf750-2131-45d3-b4ab-1fc48f505d0d_1000x.png);',
    'background-image: url(assets/brand/hero-banner.jpg);'
)
html = html.replace(
    'background-image: url(assets/mainvisual-front-sp_1d605a90-1433-49c1-82a1-ad28661da035_1000x.png);',
    ''
)

# 4. Fix fresh-oolong product image
html = html.replace(
    'assets/zh-1f0dfb5b8b.png',
    'assets/brand/fresh-oolong-product.png'
)

# 5. Rename 茶品知識 → 茶知識
html = html.replace('茶品知識', '茶知識')

INDEX.write_text(html, encoding="utf-8")
print(f"Applied all fixes. Size: {len(html)} chars")
