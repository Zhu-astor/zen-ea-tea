"""
screenshot.py - Render zen_ea_tea/index.html headless and capture diagnostics.

Purpose:
    Load the local clone in headless Chromium, capture console errors,
    measure which animation/section elements are visible & their computed
    styles, and save full-page + section screenshots for review.

Args:
    None.

Returns:
    Writes PNGs to zen_ea_tea/_shots/ and prints a diagnostic report.
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(__file__).resolve().parent
URL = "http://localhost:8765/index.html"
OUT = BASE / "_shots"
OUT.mkdir(exist_ok=True)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()

        errors = []
        page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))

        await page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(1500)

        # Scroll through the full page before screenshotting. Playwright's
        # full_page screenshot renders the entire page in one pass without ever
        # scrolling it, so IntersectionObserver-based .js-fadetarget elements
        # below the first viewport never cross their threshold and stay at
        # opacity:0 — the resulting screenshot shows large false-negative blank
        # gaps that do not reflect what a real scrolling user sees.
        height = await page.evaluate("document.body.scrollHeight")
        y = 0
        while y < height:
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(120)
            y += 400
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(500)

        # Full page screenshot
        await page.screenshot(path=str(OUT / "full.png"), full_page=True)

        # Hero
        hero = await page.query_selector("div.p-top-hero")
        if hero:
            await hero.screenshot(path=str(OUT / "hero.png"))
            box = await hero.bounding_box()
            print(f"hero box: {box}")

        # Each top section
        sections = [
            ("shopify-section-zen-brand", "brand"),
            ("shopify-section-zen-trust", "trust"),
            ("shopify-section-template--16094548295831__261e2087-fb62-4eab-b2b5-a20fc52855d8", "feature"),
            ("shopify-section-template--16094548295831__2dc91539-1147-49b5-9f5f-1029a00f01c3", "highlight"),
            ("shopify-section-template--16094548295831__474b3010-f474-4572-92ea-73601f050045", "recipe"),
            ("shopify-section-template--16094548295831__8f977aec-4b5c-4e73-b614-c09fc4643f07", "iroiro"),
            ("shopify-section-template--16094548295831__7cbf7210-36a1-42e9-adae-8417fea07e0f", "buy"),
        ]
        for sid, name in sections:
            el = await page.query_selector(f"#{sid}")
            if el:
                await el.screenshot(path=str(OUT / f"{name}.png"))
                box = await el.bounding_box()
                vis = await el.is_visible()
                print(f"{name}: visible={vis} box={box}")
            else:
                print(f"{name}: NOT FOUND")

        # Computed style checks on key animation classes
        checks = await page.evaluate("""
() => {
  const out = {};
  const pick = (sel) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return {w: r.width, h: r.height, op: cs.opacity, tr: cs.transform, bg: cs.backgroundImage.slice(0,80), display: cs.display};
  };
  out.hero = pick('.p-top-hero');
  out.hero_item = pick('.banner-img-1');
  out.hero_ul = pick('ul.p-top-hero__image');
  out.feature = pick('.p-top-feature');
  out.swiper_feature = pick('.js-slider-feature');
  out.highlight = pick('.p-top-highlight');
  out.swiper_highlight = pick('.js-slider-highlight');
  out.fade_active = pick('.js-fadetarget.is-active');
  out.fade_any = pick('.js-fadetarget');
  out.brand_grid = pick('.zen-homophones');
  return out;
}
""")
        print("\n=== computed styles ===")
        for k, v in checks.items():
            print(f"{k}: {v}")

        # Check Swiper init
        swiper_state = await page.evaluate("""
() => {
  const out = {};
  document.querySelectorAll('.swiper-container').forEach((el, i) => {
    out['swiper_'+i] = {cls: el.className, children: el.querySelectorAll('.swiper-slide').length, width: el.getBoundingClientRect().width};
  });
  if (window.Swiper) out.Swiper_loaded = true;
  if (window.Rellax) out.Rellax_loaded = true;
  return out;
}
""")
        print("\n=== swiper state ===")
        for k, v in swiper_state.items():
            print(f"{k}: {v}")

        print(f"\n=== {len(errors)} console errors/warnings ===")
        for e in errors[:20]:
            print(e)

        await browser.close()


asyncio.run(main())
