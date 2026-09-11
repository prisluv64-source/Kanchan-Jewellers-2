from pathlib import Path

path = Path('about-page.css')
css = path.read_text(encoding='utf-8')

old_grid = '''.about-story-section,\n.about-editorial-section {\n  max-width: 1240px;\n  margin: 0 auto;\n  padding: 110px 28px;\n  display: grid;\n  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);\n  gap: clamp(48px, 7vw, 100px);\n  align-items: center;\n}\n\n.about-story-media {\n  position: relative;\n  min-height: 580px;\n}\n\n.about-story-media img {\n  width: 100%;\n  height: 580px;\n  object-fit: cover;\n  display: block;\n  border-radius: 28px 28px 90px 28px;\n  box-shadow: 0 28px 70px rgba(75, 20, 33, 0.16);\n}\n'''

new_grid = '''.about-story-section,\n.about-editorial-section {\n  max-width: 1320px;\n  margin: 0 auto;\n  padding: 110px 28px;\n  display: grid;\n  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);\n  gap: clamp(48px, 6vw, 88px);\n  align-items: center;\n}\n\n.about-story-media {\n  position: relative;\n  min-height: 0;\n}\n\n.about-story-media img {\n  width: 100%;\n  height: auto;\n  object-fit: contain;\n  display: block;\n  border-radius: 28px 28px 90px 28px;\n  box-shadow: 0 28px 70px rgba(75, 20, 33, 0.16);\n}\n'''

if old_grid not in css:
    raise RuntimeError('Expected desktop story image CSS block not found')
css = css.replace(old_grid, new_grid, 1)

old_mobile = '''  .about-story-media,\n  .about-story-media img {\n    min-height: 420px;\n    height: 420px;\n  }\n'''
new_mobile = '''  .about-story-media {\n    min-height: 0;\n  }\n\n  .about-story-media img {\n    min-height: 0;\n    height: auto;\n  }\n'''

if old_mobile not in css:
    raise RuntimeError('Expected mobile story image CSS block not found')
css = css.replace(old_mobile, new_mobile, 1)

path.write_text(css, encoding='utf-8')
print('About story image now displays uncropped at its natural aspect ratio.')
