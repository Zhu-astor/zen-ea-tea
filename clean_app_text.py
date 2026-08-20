"""Thoroughly clean ALL Shopify app text residue from subpages."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Patterns that match visible Shopify app block text
TEXT_PATTERNS = [
    r'A11y END app block',
    r'END app block',
    r'END app snippet',
    r'BEGIN app block[^<\n]*',
    r'BEGIN app snippet[^<\n]*',
    r'Back in Stock helper snippet[^<\n]*',
    r'End Back in Stock helper snippet',
    r'Stamped - Begin Script[^<\n]*',
    r'Stamped - End Script',
    r'BEGIN app block: shopify://apps/[^<\n]*',
]

for f in BASE.glob("*.html"):
    if f.name == "index.html":
        continue
    html = f.read_text(encoding="utf-8")
    original_len = len(html)

    # Remove visible text patterns (not inside script tags)
    for pat in TEXT_PATTERNS:
        html = re.sub(pat, '', html, flags=re.IGNORECASE)

    # Clean up empty comment tags left behind
    html = re.sub(r'<!--\s*-->', '', html)
    html = re.sub(r'<!--\s*<!--\s*', '<!-- ', html)

    # Remove leftover backtick artifacts
    html = re.sub(r'`;\s*', '', html)

    if len(html) != original_len:
        f.write_text(html, encoding="utf-8")
        print(f"  [cleaned] {f.name} (removed {original_len - len(html)} bytes)")
