from pathlib import Path


def patch(path_str):
    path = Path(path_str)
    text = path.read_text(encoding='utf-8')
    original = text

    # Main navigation on homepage.
    text = text.replace(
        '<a class="nav-direct" href="#about">Our Story</a>',
        '<a class="nav-direct" href="about.html">Our Story</a>'
    )

    # Dedicated-page navigation/footer links that previously returned to homepage story section.
    text = text.replace(
        '<a href="index.html#about">Our Story</a>',
        '<a href="about.html">Our Story</a>'
    )

    # Any footer-style link on homepage pointing to its own story section.
    text = text.replace(
        '<a href="#about">Our Story</a>',
        '<a href="about.html">Our Story</a>'
    )

    if text == original:
        print(f'{path_str}: no matching Our Story links needed changing')
        return

    path.write_text(text, encoding='utf-8')
    print(f'{path_str}: linked Our Story to about.html')


patch('index.html')
patch('contact.html')
