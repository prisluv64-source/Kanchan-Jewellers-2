from pathlib import Path
import re

path = Path("index.html")
html = path.read_text(encoding="utf-8")
original = html

# 1) Performance: keep only the visible brand logo and first carousel banner eager.
# Everything else gets native lazy loading and async decoding.
def optimize_img(match: re.Match) -> str:
    tag = match.group(0)

    if 'class="brand-logo"' in tag:
        return tag

    if 'src="carousel/banner-1.webp"' in tag:
        if 'fetchpriority=' not in tag:
            tag = tag[:-1] + ' fetchpriority="high">'
        if 'decoding=' not in tag:
            tag = tag[:-1] + ' decoding="async">'
        return tag

    if 'loading=' not in tag:
        tag = tag[:-1] + ' loading="lazy">'
    if 'decoding=' not in tag:
        tag = tag[:-1] + ' decoding="async">'
    return tag

html = re.sub(r'<img\b[^>]*>', optimize_img, html)

# 3) Correct accessibility labels for each jewellery mega-menu.
labels = [
    "Necklaces",
    "Earrings and Jhumkas",
    "Bangles",
    "Rings",
    "Mangalsutra",
    "Chains",
    "Silver Articles",
    "Gold and Silver Coins",
]
label_pattern = re.compile(r'(<section class="category-section" aria-label=")[^"]+("\s*>)')
label_matches = list(label_pattern.finditer(html))
if len(label_matches) != len(labels):
    raise RuntimeError(f"Expected {len(labels)} mega-menu section labels, found {len(label_matches)}")

label_iter = iter(labels)
html = label_pattern.sub(lambda m: m.group(1) + next(label_iter) + m.group(2), html)
html = html.replace('<!-- ===== EARRINGS & JHUMKAS SECTION ===== -->', '<!-- ===== JEWELLERY MEGA MENU ===== -->')

# 4) Shop-by-category View all must not jump to Contact.
old_view_all = '<a href="#contact" class="view-all">View all →</a>'
new_view_all = '<a href="#collections" class="view-all">View all →</a>'
if old_view_all not in html and new_view_all not in html:
    raise RuntimeError("Shop by Category View all link not found")
html = html.replace(old_view_all, new_view_all, 1)

# 6) Security: every target=_blank anchor gets rel=noopener.
def secure_blank_link(match: re.Match) -> str:
    tag = match.group(0)
    if 'target="_blank"' in tag and not re.search(r'\brel\s*=', tag, flags=re.I):
        tag = tag.replace('target="_blank"', 'target="_blank" rel="noopener"', 1)
    return tag

html = re.sub(r'<a\b[^>]*>', secure_blank_link, html, flags=re.S)

# Sanity checks.
if 'src="carousel/banner-1.webp"' not in html or 'fetchpriority="high"' not in html:
    raise RuntimeError("First carousel banner priority optimization missing")
if '<a href="#collections" class="view-all">View all →</a>' not in html:
    raise RuntimeError("View all link fix missing")
for label in labels:
    if f'aria-label="{label}"' not in html:
        raise RuntimeError(f"Missing corrected aria-label: {label}")
for tag in re.findall(r'<a\b[^>]*target="_blank"[^>]*>', html, flags=re.S):
    if not re.search(r'\brel\s*=\s*"[^"]*noopener', tag, flags=re.I):
        raise RuntimeError(f"target=_blank link without noopener: {tag}")

if html == original:
    print("No changes needed.")
else:
    path.write_text(html, encoding="utf-8")
    lazy_count = html.count('loading="lazy"')
    print(f"Applied index audit fixes. Lazy images: {lazy_count}; mega-menu labels: {len(labels)}")
