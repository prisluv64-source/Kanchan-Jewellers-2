from pathlib import Path
import re

index_path = Path('index.html')
styles_path = Path('styles.css')

html = index_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')

if 'carousel-image-cta' not in html:
    def add_hotspot(match):
        num = match.group(1)
        img = match.group(2)
        return (
            f'<div class="home-carousel-slide{(" active" if num == "1" else "")}">\n'
            f'        {img}\n'
            f'        <a href="#collections" class="carousel-image-cta carousel-image-cta-{num}" '
            f'aria-label="Open jewellery collections from banner {num}"></a>\n'
            f'      </div>'
        )

    pattern = re.compile(
        r'<div class="home-carousel-slide(?: active)?">\s*'
        r'(<img src="carousel/banner-(\d)\.webp"[^>]*>)\s*'
        r'</div>',
        re.S,
    )

    # capture order above is img then number; normalize with a second callback
    def repl(match):
        img = match.group(1)
        num = match.group(2)
        active = ' active' if num == '1' else ''
        return (
            f'<div class="home-carousel-slide{active}">\n'
            f'        {img}\n'
            f'        <a href="#collections" class="carousel-image-cta carousel-image-cta-{num}" '
            f'aria-label="Open jewellery collections from banner {num}"></a>\n'
            f'      </div>'
        )

    html, count = pattern.subn(repl, html)
    if count != 5:
        raise RuntimeError(f'Expected 5 carousel slides, found {count}')
    index_path.write_text(html, encoding='utf-8')

marker = '/* ===== CLICKABLE CAROUSEL IMAGE BUTTONS ===== */'
if marker not in css:
    css += r'''

/* ===== CLICKABLE CAROUSEL IMAGE BUTTONS ===== */
.carousel-image-cta {
  position: absolute;
  z-index: 3;
  display: block;
  cursor: pointer;
  border-radius: 12px;
  background: transparent;
}

/* Hotspot positions match the button artwork baked into each banner image. */
.carousel-image-cta-1 { left: 7.2%; top: 75.0%; width: 17.8%; height: 10.5%; }
.carousel-image-cta-2 { left: 7.0%; top: 64.5%; width: 16.5%; height: 10.0%; }
.carousel-image-cta-3 { left: 8.3%; top: 71.5%; width: 20.8%; height: 11.0%; }
.carousel-image-cta-4 { left: 6.5%; top: 63.5%; width: 19.8%; height: 10.5%; }
.carousel-image-cta-5 { left: 6.5%; top: 62.5%; width: 20.0%; height: 10.5%; }

.carousel-image-cta:focus-visible {
  outline: 2px solid rgba(255,255,255,.9);
  outline-offset: 2px;
}
'''
    styles_path.write_text(css, encoding='utf-8')

print('Carousel image button hotspots applied.')
