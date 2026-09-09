from pathlib import Path
import re

index_path = Path('index.html')
styles_path = Path('styles.css')
html = index_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')

new_block = '''      <div class="header-actions">
        <a href="tel:+919839638670" class="action-btn" aria-label="Call Kanchan Jewellers">
          <svg class="action-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 5.25c0-.83.67-1.5 1.5-1.5h2.09c.65 0 1.23.42 1.43 1.04l.86 2.57c.17.51.05 1.07-.32 1.46l-1.4 1.47a12.02 12.02 0 0 0 5.8 5.8l1.47-1.4c.39-.37.95-.49 1.46-.32l2.57.86c.62.2 1.04.78 1.04 1.43v2.09c0 .83-.67 1.5-1.5 1.5h-.75C10.13 20.25 3.75 13.87 3.75 6v-.75Z"/>
          </svg>
          <span>Call</span>
        </a>

        <a href="https://wa.me/919839638670" target="_blank" rel="noopener" class="action-btn whatsapp" aria-label="WhatsApp Kanchan Jewellers">
          <svg class="action-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 11.5a8.25 8.25 0 0 1-12.2 7.25L3.75 20.25l1.5-4.3A8.25 8.25 0 1 1 20.25 11.5Z"/>
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.5 8.25c.45 2.9 2.35 4.8 5.25 5.25"/>
          </svg>
          <span>WhatsApp</span>
        </a>

        <a href="#contact" class="action-btn" aria-label="Visit Kanchan Jewellers store">
          <svg class="action-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21s6-5.05 6-11a6 6 0 1 0-12 0c0 5.95 6 11 6 11Z"/>
            <circle cx="12" cy="10" r="2.25"/>
          </svg>
          <span>Visit Store</span>
        </a>
      </div>'''

pattern = re.compile(r'      <div class="header-actions">.*?      </div>\n\n      <button class="menu-btn"', re.S)
replacement = new_block + '\n\n      <button class="menu-btn"'
html2, count = pattern.subn(replacement, html, count=1)
if count != 1:
    raise RuntimeError(f'Expected one header-actions block, found {count}')
index_path.write_text(html2, encoding='utf-8')

if '.action-svg {' not in css:
    anchor = '''.action-icon {
  font-size: 1.15rem;
  line-height: 1;
}
'''
    addition = anchor + '''\n.action-svg {
  width: 21px;
  height: 21px;
  display: block;
  flex: 0 0 auto;
}\n'''
    if anchor not in css:
        raise RuntimeError('Could not find action-icon CSS anchor')
    css = css.replace(anchor, addition, 1)
    styles_path.write_text(css, encoding='utf-8')

print('Header action icons restored.')
