"""Clean leaked Shopify JS ONLY from subpages, NOT index.html.
The leaked code is a broken template literal from Customer Fields app
that starts with `; and const $forms. It's between cf-preload spans
and the zen scripts at the bottom."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

for f in BASE.glob("*.html"):
    if f.name == "index.html":
        continue
    html = f.read_text(encoding="utf-8")
    original_len = len(html)

    # Only clean if cf-preload-item exists (indicates leaked JS)
    if 'cf-preload-item' not in html:
        continue

    # Find the last legitimate HTML before the leaked JS
    # The leaked block starts after a broken backtick and contains
    # "const $forms" - remove from the first backtick+semicolon to
    # the next <script src="assets/zen or </body>
    html = re.sub(
        r'`;\s*\n\s*const \$forms.*?(?=<script src="assets/zen|</body>)',
        '',
        html,
        flags=re.DOTALL
    )

    # Remove the cf-preload divs themselves (they're Shopify app remnants)
    html = re.sub(
        r'<div[^>]*class="cf-preload[^"]*"[^>]*>.*?</div>\s*<!--\s*-->`;',
        '',
        html,
        flags=re.DOTALL
    )

    # Clean any remaining backtick+semicolon artifacts
    html = re.sub(r'<!--\s*-->`;', '', html)

    if len(html) != original_len:
        f.write_text(html, encoding="utf-8")
        print(f"  [cleaned] {f.name} (removed {original_len - len(html)} bytes)")
    else:
        print(f"  [no change] {f.name}")
