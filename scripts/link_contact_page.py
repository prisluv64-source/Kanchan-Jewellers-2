from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

old = 'href="#contact"'
count = html.count(old)
if count < 1:
    raise RuntimeError('No #contact links found in index.html')

html = html.replace(old, 'href="contact.html"')
path.write_text(html, encoding='utf-8')
print(f'Updated {count} Visit Us/contact links to contact.html')
