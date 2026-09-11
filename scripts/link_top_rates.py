from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')
original = html

# Wrap the dynamic top-bar IBJA rate text in an in-page link without touching
# the actual rate markup that scripts/update_rates.py updates.
pattern = re.compile(
    r'(<div class="rates">\s*<span class="rate-dot"></span>\s*)'
    r'(IBJA Rate:\s*<strong>Gold 22K [^<]+</strong>\s*&nbsp;•&nbsp;\s*<strong>Silver [^<]+</strong>)'
    r'(\s*</div>)',
    re.S,
)

if 'class="top-rate-link"' not in html:
    html, count = pattern.subn(
        r'\1<a class="top-rate-link" href="#ibjaRates" aria-label="View full IBJA gold and silver rates">\2</a>\3',
        html,
        count=1,
    )
    if count != 1:
        raise RuntimeError('Could not locate top-bar IBJA rate block')

css = '''\n    html {\n      scroll-behavior: smooth;\n    }\n\n    .top-rate-link {\n      color: inherit;\n      text-decoration: none;\n      cursor: pointer;\n    }\n\n    .top-rate-link:hover,\n    .top-rate-link:focus-visible {\n      text-decoration: underline;\n      text-underline-offset: 3px;\n    }\n\n    #ibjaRates {\n      scroll-margin-top: 110px;\n    }\n'''

if '.top-rate-link {' not in html:
    marker = '  </style>'
    if marker not in html:
        raise RuntimeError('Could not locate inline style closing tag')
    html = html.replace(marker, css + '\n' + marker, 1)

if html == original:
    print('Top rate link already present; no changes needed.')
else:
    path.write_text(html, encoding='utf-8')
    print('Linked top-bar IBJA rates to #ibjaRates with smooth scrolling.')
