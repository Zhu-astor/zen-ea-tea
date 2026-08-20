"""Remove leaked Shopify JS code from all subpages.
The code appears as visible text between a broken template literal
backtick and the next valid HTML. It starts with `cf-preload-item`
or `const $forms` and extends until the next valid closing tag."""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

for f in BASE.glob("*.html"):
    html = f.read_text(encoding="utf-8")
    original_len = len(html)

    # Pattern 1: Remove broken template literal blocks containing Shopify JS
    # These start with `-->` + backtick + JS code and end before a valid HTML tag
    # The leaked code is between the last legitimate HTML and </body>
    # It typically starts with "`;" or "`;" followed by JS code

    # Find and remove the leaked JS block
    # Pattern: everything from "`;\n      const $forms" to just before the zen scripts or </body>
    patterns = [
        # Pattern: backtick + semicolon + JS code until next <script or </body
        r'`;\s*\n\s*const \$forms.*?(?=<script|</body)',
        # Pattern: cf-preload divs + backtick + JS
        r'</div><!--\s*-->`;\s*\n\s*const \$forms.*?(?=<script|</body)',
        # Broader: any text node starting with `; or const $forms
        r'`;\s*\n.*?const \$forms.*?(?=<script src="assets/zen|</body>)',
    ]

    for pat in patterns:
        html = re.sub(pat, '', html, flags=re.DOTALL)

    # Also remove any remaining "const $forms" blocks outside script tags
    # Find the pattern: text that starts with JS keywords and is NOT inside a script tag
    # Simple approach: remove everything between `cf-preload-item` span and the first <script> after it
    if 'cf-preload-item' in html:
        # Find the cf-preload block and remove everything until the next <script> or </div></body>
        html = re.sub(
            r'<span class="cf-preload-button cf-preload-item"></span>\s*</div>\s*</div>.*?(?=<script src="assets/zen|</body>)',
            '</span>\n  </div>\n</div>\n',
            html,
            flags=re.DOTALL
        )

    # Remove any remaining leaked JS function definitions outside script tags
    # These look like: function isIgnored($form) { ... } etc.
    if 'function isIgnored' in html:
        # Remove blocks starting with common JS patterns that are outside script tags
        html = re.sub(r'`;\s*const \$forms.*?(?=<script|</body)', '', html, flags=re.DOTALL)

    # Clean up: remove the backtick + semicolon that precedes leaked code
    html = re.sub(r'<!--\s*-->`;', '', html)

    if len(html) != original_len:
        f.write_text(html, encoding="utf-8")
        print(f"  [cleaned] {f.name} (removed {original_len - len(html)} bytes)")
