from pathlib import Path

path = Path('styles.css')
css = path.read_text(encoding='utf-8')

old = '''.ibja-rate-card {
  min-width: 0;
  padding: 20px 20px 17px;
  border: 1px solid rgba(232, 213, 163, 0.28);
  border-radius: 16px;
  background: rgba(255, 251, 245, 0.075);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
  backdrop-filter: blur(4px);
}

.ibja-rate-card h3 {
  margin: 0 0 11px;
  color: #fff;
  font-size: 0.9rem;
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 600;
}

.ibja-rate-card h3 span {
  color: #e8d5a3;
  font-weight: 500;
}

.ibja-main-rate {
  display: flex;
  align-items: baseline;
  gap: 8px;
  min-width: 0;
}

.ibja-main-rate strong {
  color: #f4d487;
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(1.75rem, 2.4vw, 2.2rem);
  line-height: 1;
  white-space: nowrap;
}

.ibja-main-rate span,
.ibja-rate-card p {
  color: rgba(255,255,255,0.72);
  font-size: 0.72rem;
}

.ibja-rate-card p {
  margin: 7px 0 0;
}

.ibja-rate-card p span {
  color: #fff3d1;
}
'''

new = '''.ibja-rate-card {
  min-width: 0;
  padding: 20px 20px 17px;
  border: 1px solid rgba(193, 151, 63, 0.42);
  border-radius: 16px;
  background: var(--bg);
  box-shadow: 0 10px 24px rgba(61, 16, 38, 0.16);
  transition: var(--transition);
}

.ibja-rate-card:hover {
  transform: translateY(-3px);
  border-color: rgba(193, 151, 63, 0.72);
  box-shadow: 0 14px 30px rgba(61, 16, 38, 0.22);
}

.ibja-rate-card h3 {
  margin: 0 0 11px;
  color: var(--primary-dark);
  font-size: 0.9rem;
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 700;
}

.ibja-rate-card h3 span {
  color: var(--gold);
  font-weight: 600;
}

.ibja-main-rate {
  display: flex;
  align-items: baseline;
  gap: 8px;
  min-width: 0;
}

.ibja-main-rate strong {
  color: var(--primary);
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(1.75rem, 2.4vw, 2.2rem);
  font-weight: 700;
  line-height: 1;
  white-space: nowrap;
}

.ibja-main-rate span,
.ibja-rate-card p {
  color: var(--text-light);
  font-size: 0.72rem;
}

.ibja-rate-card p {
  margin: 7px 0 0;
}

.ibja-rate-card p span {
  color: var(--primary-dark);
  font-weight: 600;
}
'''

if old not in css:
    raise RuntimeError('Expected IBJA rate card CSS block not found')

css = css.replace(old, new, 1)
path.write_text(css, encoding='utf-8')
print('IBJA rate cards restyled with website background.')
