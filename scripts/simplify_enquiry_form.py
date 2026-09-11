from pathlib import Path
import re

path = Path('contact.html')
html = path.read_text(encoding='utf-8')

replacements = {
    "Share a few details and our showroom team will receive your enquiry privately. You stay on this page — WhatsApp will not open on your device.":
        "Share a few details, then continue to WhatsApp. Your enquiry will be prepared automatically — just review it and tap Send.",
    "By submitting this enquiry, you agree that Kanchan Jewellers may contact you about this request. Your WhatsApp app will not be opened by this form.":
        "On submit, WhatsApp will open with your enquiry details already filled in. Review the message and tap Send to contact Kanchan Jewellers.",
    ">Submit Enquiry</button>": ">Continue on WhatsApp</button>",
}

for old, new in replacements.items():
    if old not in html:
        raise RuntimeError(f'Missing expected text: {old[:60]}')
    html = html.replace(old, new, 1)

pattern = re.compile(r'\n\s*<div class="enquiry-success-modal".*?</div>\n\s*</div>\n(?=\s*</section>\n\s*</main>)', re.S)
html, count = pattern.subn('', html, count=1)
if count != 1:
    raise RuntimeError(f'Expected to remove one success modal, removed {count}')

path.write_text(html, encoding='utf-8')
print('Simplified enquiry form for WhatsApp handoff.')
