from pathlib import Path
from io import BytesIO
import time

import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path('carousel')
OUT.mkdir(exist_ok=True)

W, H = 2560, 1000

SLIDES = [
    {
        'url': 'https://images.pexels.com/photos/5043048/pexels-photo-5043048.jpeg?auto=compress&cs=tinysrgb&w=2560',
        'eyebrow': 'TIMELESS CRAFTSMANSHIP',
        'title': 'Jewellery for\nEvery Story',
        'body': "From everyday elegance to life's special moments,\nfind pieces that celebrate you.",
        'button': 'Discover Collection',
        'theme': (56, 31, 19),
        'accent': (228, 181, 92),
    },
    {
        'url': 'https://images.pexels.com/photos/35137273/pexels-photo-35137273.jpeg?auto=compress&cs=tinysrgb&w=2560',
        'eyebrow': 'FESTIVE COLLECTION',
        'title': 'Moments Shine\nBrighter',
        'body': 'Timeless designs for celebrations, traditions\nand every moment worth remembering.',
        'button': 'Explore Festive',
        'theme': (14, 49, 36),
        'accent': (225, 185, 91),
    },
    {
        'url': 'https://images.pexels.com/photos/7419598/pexels-photo-7419598.jpeg?auto=compress&cs=tinysrgb&w=2560',
        'eyebrow': 'GIFTS OF LOVE',
        'title': 'Celebrate\nEvery Bond',
        'body': 'Thoughtful jewellery for weddings, anniversaries\nand all the people who make life brighter.',
        'button': 'Find the Perfect Gift',
        'theme': (102, 27, 49),
        'accent': (243, 191, 199),
    },
    {
        'url': 'https://images.pexels.com/photos/15871502/pexels-photo-15871502.jpeg?auto=compress&cs=tinysrgb&w=2560',
        'eyebrow': 'BRILLIANCE COLLECTION',
        'title': 'Brilliance in\nEvery Detail',
        'body': 'Refined pieces crafted to bring a quiet sparkle\nto everyday style and special occasions.',
        'button': 'Discover Brilliance',
        'theme': (12, 35, 62),
        'accent': (191, 211, 235),
    },
    {
        'url': 'https://images.pexels.com/photos/32077588/pexels-photo-32077588.jpeg?auto=compress&cs=tinysrgb&w=2560',
        'eyebrow': 'MODERN CLASSICS',
        'title': 'More Than\nJewellery',
        'body': 'A reflection of your story, your style\nand every beautiful milestone ahead.',
        'button': "See What's New",
        'theme': (75, 14, 37),
        'accent': (224, 176, 98),
    },
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140 Safari/537.36'
}

SERIF_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANS_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def font(path, size):
    return ImageFont.truetype(path, size=size)


def fetch_image(url):
    last = None
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=35)
            r.raise_for_status()
            return Image.open(BytesIO(r.content)).convert('RGB')
        except Exception as exc:
            last = exc
            time.sleep(2 + attempt)
    raise RuntimeError(f'Could not download {url}: {last}')


def cover(im, size):
    tw, th = size
    scale = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))


def draw_round_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def build_slide(spec, index):
    photo = cover(fetch_image(spec['url']), (W, H))
    photo = photo.filter(ImageFilter.GaussianBlur(radius=0.25))

    # Add a mild warm/colored tint so each slide has a distinct premium palette.
    tint = Image.new('RGB', (W, H), spec['theme'])
    photo = Image.blend(photo, tint, 0.10)

    # Dark/colored gradient from left to transparent right.
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = overlay.load()
    tr, tg, tb = spec['theme']
    for x in range(W):
        t = x / W
        if t < 0.50:
            alpha = int(245 - (t / 0.50) * 70)
        elif t < 0.76:
            alpha = int(175 * (1 - (t - 0.50) / 0.26))
        else:
            alpha = 0
        if alpha <= 0:
            continue
        for y in range(H):
            px[x, y] = (tr, tg, tb, alpha)

    canvas = photo.convert('RGBA')
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)

    white = (252, 249, 244, 255)
    soft = (231, 226, 220, 255)
    accent = (*spec['accent'], 255)
    button_text = (28, 24, 20, 255)

    x = 165
    y = 145

    eyebrow_font = font(SANS_BOLD, 34)
    title_font = font(SERIF_BOLD, 112)
    body_font = font(SANS, 37)
    button_font = font(SANS_BOLD, 31)

    # Eyebrow pill.
    eyebrow_box = draw.textbbox((0, 0), spec['eyebrow'], font=eyebrow_font)
    ew = eyebrow_box[2] - eyebrow_box[0]
    eh = eyebrow_box[3] - eyebrow_box[1]
    draw_round_rect(draw, (x - 20, y - 12, x + ew + 24, y + eh + 20), 26, (*spec['theme'], 205))
    draw.text((x, y), spec['eyebrow'], font=eyebrow_font, fill=accent)

    y += 112
    draw.multiline_text((x, y), spec['title'], font=title_font, fill=white, spacing=4)
    title_bbox = draw.multiline_textbbox((x, y), spec['title'], font=title_font, spacing=4)
    y = title_bbox[3] + 34

    draw.multiline_text((x, y), spec['body'], font=body_font, fill=soft, spacing=14)
    body_bbox = draw.multiline_textbbox((x, y), spec['body'], font=body_font, spacing=14)
    y = body_bbox[3] + 55

    btn_bbox = draw.textbbox((0, 0), spec['button'], font=button_font)
    bw = btn_bbox[2] - btn_bbox[0] + 86
    bh = 78
    draw_round_rect(draw, (x, y, x + bw, y + bh), 20, accent)
    draw.text((x + 35, y + 20), spec['button'], font=button_font, fill=button_text)
    draw.text((x + bw - 42, y + 16), '›', font=font(SANS_BOLD, 39), fill=button_text)

    # Subtle inner frame for premium finish.
    draw.rounded_rectangle((24, 24, W - 24, H - 24), radius=36, outline=(255, 255, 255, 35), width=2)

    out = OUT / f'banner-{index}.webp'
    canvas.convert('RGB').save(out, 'WEBP', quality=94, method=6)
    print(f'Created {out} ({out.stat().st_size / 1024:.1f} KB)')


for i, slide in enumerate(SLIDES, 1):
    build_slide(slide, i)

print('UHD carousel banners generated at 2560x1000.')
