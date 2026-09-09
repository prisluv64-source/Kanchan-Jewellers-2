from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')
old = '''      <div class="location">\n        Near Dr. Dey's Hospital, Lal Bangla, Jajmau, Kanpur – 208007\n      </div>'''
new = '''      <div class="location">\n        <a href="https://maps.google.com/maps?q=H.N%2C%2BKazi%2BKhera%2C%2Bnear%2BDr.%2BDey's%2BHospital%2C%2BLal%2BBangla%2C%2BJajmau%2BSub%2BMetro%2BCity%2C%2BKanpur%2C%2BUttar%2BPradesh%2B208007%2C%2BIndia&sll=26.419236275641314,80.38961693644524" target="_blank" rel="noopener" aria-label="Open Kanchan Jewellers location in Google Maps">Near Dr. Dey's Hospital, Lal Bangla, Jajmau, Kanpur – 208007</a>\n      </div>'''
if old not in html:
    raise RuntimeError('Top address block not found')
html = html.replace(old, new, 1)
path.write_text(html, encoding='utf-8')
print('Top address linked to Google Maps.')
