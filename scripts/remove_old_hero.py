from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

pattern = re.compile(
    r'\n\s*<!-- Hero Section -->\s*\n\s*<section class="hero">.*?</section>\s*\n\s*(?=<!-- Shop by Category -->)',
    re.S,
)

new_html, count = pattern.subn('\n\n    ', html, count=1)
if count != 1:
    raise RuntimeError(f'Expected exactly one old hero section, found {count}')

path.write_text(new_html, encoding='utf-8')
print('Old hero section removed; Shop by Category now follows carousel.')
