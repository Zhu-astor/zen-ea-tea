"""Targeted verification of user-reported issues"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()

        # 1. Check homepage
        await page.goto("http://localhost:8765/index.html", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(3000)
        # scroll
        for y in range(0, 6000, 300):
            await page.goto("http://localhost:8765/index.html", wait_until="domcontentloaded", timeout=20000)
            break

        results = await page.evaluate("""
() => {
  const out = {};
  // Check nav text
  out.nav = [];
  document.querySelectorAll('.c-gnav-pc__lv01__link').forEach(function(el) {
    out.nav.push(el.textContent.trim());
  });
  // Check announcement bar bg
  var ann = document.querySelector('.announcement-bar');
  if (ann) {
    var cs = getComputedStyle(ann);
    out.announcement = { bg: cs.backgroundColor, bgImage: cs.backgroundImage.slice(0, 80) };
  }
  // Check shopping grid
  var buyNav = document.querySelector('.p-top-buy__nav');
  if (buyNav) {
    var cs = getComputedStyle(buyNav);
    out.shopping = { gridCols: cs.gridTemplateColumns, childCount: buyNav.children.length };
    var r = buyNav.getBoundingClientRect();
    out.shopping.width = r.width;
    out.shopping.height = r.height;
    // Check each item
    out.shoppingItems = [];
    buyNav.querySelectorAll('.p-top-buy__item').forEach(function(item) {
      var r = item.getBoundingClientRect();
      var img = item.querySelector('img');
      var imgR = img ? img.getBoundingClientRect() : null;
      out.shoppingItems.push({
        w: Math.round(r.width), h: Math.round(r.height),
        top: Math.round(r.top),
        imgW: imgR ? Math.round(imgR.width) : 0,
        imgH: imgR ? Math.round(imgR.height) : 0
      });
    });
  }
  // Check header icons
  out.icons = [];
  document.querySelectorAll('.c-unav-pc .c-icon, .c-unav-pc img.image--favorite').forEach(function(el) {
    var r = el.getBoundingClientRect();
    var cs = getComputedStyle(el);
    out.icons.push({
      tag: el.tagName, cls: el.className.slice(0, 30),
      w: Math.round(r.width), h: Math.round(r.height),
      bg: cs.backgroundImage.slice(0, 50),
      display: cs.display
    });
  });
  // Check section backgrounds
  out.sections = {};
  ['.p-top-feature', '.p-top-highlight', '.p-top-recipe', '.p-top-iroiro', '.p-top-buy', '.p-top-news', '.p-top-others'].forEach(function(sel) {
    var el = document.querySelector(sel);
    if (el) {
      var cs = getComputedStyle(el);
      out.sections[sel] = { bg: cs.backgroundColor };
    }
  });
  return out;
}
""")
        import json
        print("=== HOMEPAGE ===")
        print(json.dumps(results, indent=2, ensure_ascii=False))

        # 2. Check products.html for Shopify text
        await page.goto("http://localhost:8765/products.html", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        body_text = await page.evaluate("document.body.innerText.slice(0, 500)")
        print("\n=== PRODUCTS.HTML first 500 chars ===")
        print(body_text)

        # 3. Mobile overflow check
        await page.set_viewport_size({"width": 375, "height": 812})
        await page.goto("http://localhost:8765/index.html", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        overflow = await page.evaluate("document.body.scrollWidth")
        print(f"\n=== MOBILE (375px) scrollWidth: {overflow}px ===")

        await browser.close()

asyncio.run(main())
