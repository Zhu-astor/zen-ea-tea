"""
regression_check.py — Full-site regression verification with Playwright.

Purpose:
    Loads every page via HTTP, scrolls through each to trigger fade-in
    animations (per rule 1.6), screenshots desktop + mobile widths,
    checks for JS errors, verifies all links point to real files,
    and reports per-page results using the 5-point acceptance checklist.

Args:
    None. Uses http://localhost:8765/

Returns:
    Writes screenshots to _regression/ and prints a structured report.
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(__file__).resolve().parent
BASE_URL = "http://localhost:8765/"
OUT = BASE / "_regression"
OUT.mkdir(exist_ok=True)

PAGES = [
    ("index.html", "首頁"),
    ("product-honey-black.html", "蜜香紅茶"),
    ("product-gaba.html", "佳葉龍茶"),
    ("product-fresh-oolong.html", "鮮翠烏龍"),
    ("product-yushan-oolong.html", "玉山烏龍"),
    ("about.html", "關於蟬吃茶"),
    ("store.html", "門市資訊"),
    ("tea-master.html", "製茶師陳昭鳳"),
    ("tea-intro.html", "茶品介紹"),
    ("brewing.html", "沖泡指南"),
    ("faq.html", "常見問答"),
    ("contact.html", "聯絡我們"),
    ("privacy.html", "隱私權政策"),
    ("terms.html", "服務條款"),
    ("products.html", "商品列表"),
    ("journal.html", "蟬茶日誌"),
    ("wishlist.html", "我的收藏"),
    ("search.html", "搜尋"),
    ("cart.html", "購物車"),
]


async def check_page(page, filename, label):
    """Run 5-point checklist on a single page."""
    result = {"page": filename, "label": label, "checks": {}}

    url = BASE_URL + filename
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
    except Exception as e:
        result["checks"]["1_load"] = f"FAIL: {e}"
        return result

    await page.wait_for_timeout(2000)

    # Scroll through entire page to trigger IntersectionObserver fade-ins
    scroll_height = await page.evaluate("document.body.scrollHeight")
    for y in range(0, scroll_height + 500, 300):
        await page.evaluate(f"window.scrollTo(0, {y})")
        await page.wait_for_timeout(100)
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(500)

    # Check 1: Screenshot (desktop)
    await page.screenshot(path=str(OUT / f"desktop_{filename.replace('.html', '.png')}"))
    result["checks"]["1_screenshot"] = "OK"

    # Check 2: Image dimensions — flag any img with extreme aspect ratios
    img_issues = await page.evaluate("""
() => {
  const issues = [];
  document.querySelectorAll('img').forEach(function(img) {
    if (!img.complete || img.naturalWidth === 0) return;
    var r = img.naturalWidth / img.naturalHeight;
    var rendered = img.getBoundingClientRect();
    if (rendered.width < 10 || rendered.height < 10) {
      issues.push({src: img.src.slice(-40), w: Math.round(rendered.width), h: Math.round(rendered.height), issue: 'tiny'});
    }
    if (r > 5 || r < 0.2) {
      issues.push({src: img.src.slice(-40), ratio: r.toFixed(1), issue: 'extreme_aspect'});
    }
  });
  return issues;
}
""")
    result["checks"]["2_images"] = "OK" if len(img_issues) == 0 else f"WARN: {img_issues[:3]}"

    # Check 3: JS errors
    result["checks"]["3_errors"] = "OK" if len(errors) == 0 else f"{len(errors)} errors: {errors[:3]}"

    # Check 4: All links point to real files
    links = await page.evaluate("""
() => {
  return Array.from(document.querySelectorAll('a[href]')).map(function(a) {
    return a.getAttribute('href');
  }).filter(function(h) {
    return h && !h.startsWith('http') && !h.startsWith('mailto:') && !h.startsWith('tel:') && !h.startsWith('#') && !h.startsWith('javascript:');
  });
}
""")
    broken = []
    for link in set(links):
        if link in ("", ".") or link.startswith("data:"):
            continue
        # Remove query params
        clean = link.split("?")[0].split("#")[0]
        if not clean:
            continue
        filepath = BASE / clean
        if not filepath.exists() and clean != "index.html":
            broken.append(link)
    result["checks"]["4_links"] = "OK" if len(broken) == 0 else f"BROKEN: {broken[:5]}"

    # Check 5: Mobile width (375px)
    await page.set_viewport_size({"width": 375, "height": 812})
    await page.wait_for_timeout(500)
    await page.screenshot(path=str(OUT / f"mobile_{filename.replace('.html', '.png')}"))
    mobile_issues = await page.evaluate("""
() => {
  var issues = [];
  // Check for horizontal overflow
  if (document.body.scrollWidth > window.innerWidth + 5) {
    issues.push('horizontal_overflow: ' + document.body.scrollWidth + 'px > ' + window.innerWidth + 'px');
  }
  return issues;
}
""")
    result["checks"]["5_mobile"] = "OK" if len(mobile_issues) == 0 else f"ISSUES: {mobile_issues}"

    # Reset viewport
    await page.set_viewport_size({"width": 1440, "height": 900})

    return result


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()

        results = []
        for filename, label in PAGES:
            print(f"\n--- Checking {label} ({filename}) ---")
            r = await check_page(page, filename, label)
            results.append(r)
            for check_name, check_result in r["checks"].items():
                status = "[OK]" if "OK" in str(check_result) else "[FAIL]" if "FAIL" in str(check_result) else "[WARN]"
                print(f"  {status} {check_name}: {check_result}")

        await browser.close()

        # Summary
        print("\n" + "=" * 60)
        print("REGRESSION SUMMARY")
        print("=" * 60)
        ok = 0
        warn = 0
        fail = 0
        for r in results:
            for v in r["checks"].values():
                if "OK" in str(v):
                    ok += 1
                elif "FAIL" in str(v):
                    fail += 1
                else:
                    warn += 1
        print(f"Total checks: {ok + warn + fail}  |  OK: {ok}  |  WARN: {warn}  |  FAIL: {fail}")
        print(f"Screenshots saved to: {OUT}")


asyncio.run(main())
