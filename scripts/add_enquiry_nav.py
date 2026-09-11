from pathlib import Path


def replace_once(path_str, old, new):
    path = Path(path_str)
    text = path.read_text(encoding='utf-8')
    if new in text:
        print(f'{path_str}: already updated')
        return False
    if old not in text:
        raise RuntimeError(f'Expected navigation block not found in {path_str}')
    text = text.replace(old, new, 1)
    path.write_text(text, encoding='utf-8')
    print(f'{path_str}: Enquiry navigation added')
    return True

replace_once(
    'index.html',
    '      <a class="nav-direct" href="contact.html">Visit Us</a>\n',
    '      <a class="nav-direct" href="contact.html">Visit Us</a>\n      <a class="nav-direct" href="contact.html#enquiry">Enquiry</a>\n'
)

replace_once(
    'contact.html',
    '        <a href="contact.html" class="active">Visit Us</a>\n        <a class="contact-nav-whatsapp"',
    '        <a href="contact.html" class="active">Visit Us</a>\n        <a href="#enquiry">Enquiry</a>\n        <a class="contact-nav-whatsapp"'
)
