from pathlib import Path

index_path = Path('index.html')
styles_path = Path('styles.css')
html = index_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')

section = r'''

    <!-- IBJA Gold & Silver Rates -->
    <section class="ibja-rates-section" id="ibjaRates" aria-labelledby="ibjaRatesTitle">
      <div class="ibja-rates-head">
        <div>
          <p class="ibja-kicker"><span class="ibja-live-dot"></span> IBJA INDIA RATE</p>
          <h2 id="ibjaRatesTitle">Today's Gold &amp; Silver Rate</h2>
        </div>
        <a class="ibja-source-link" href="https://ibjarates.com/" target="_blank" rel="noopener">
          ↗ IBJA rate as on <span id="ibja-rate-date">09 Sep 2026</span>
        </a>
      </div>

      <div class="ibja-rate-grid">
        <article class="ibja-rate-card" data-rate-key="gold999">
          <h3>Gold 24K <span>(999)</span></h3>
          <div class="ibja-main-rate"><strong id="ibja-gold999-main">₹1,53,486</strong><span>per 10 g</span></div>
          <p><span id="ibja-gold999-gram">₹15,349</span> per g</p>
        </article>

        <article class="ibja-rate-card" data-rate-key="gold916">
          <h3>Gold 22K <span>(916)</span></h3>
          <div class="ibja-main-rate"><strong id="ibja-gold916-main">₹1,40,593</strong><span>per 10 g</span></div>
          <p><span id="ibja-gold916-gram">₹14,059</span> per g</p>
        </article>

        <article class="ibja-rate-card" data-rate-key="gold750">
          <h3>Gold 18K <span>(750)</span></h3>
          <div class="ibja-main-rate"><strong id="ibja-gold750-main">₹1,15,115</strong><span>per 10 g</span></div>
          <p><span id="ibja-gold750-gram">₹11,512</span> per g</p>
        </article>

        <article class="ibja-rate-card silver" data-rate-key="silver999">
          <h3>Silver <span>(999)</span></h3>
          <div class="ibja-main-rate"><strong id="ibja-silver999-main">₹2,35,249</strong><span>per kg</span></div>
          <p><span id="ibja-silver999-gram">₹235</span> per g</p>
        </article>
      </div>

      <div class="ibja-rates-foot">
        <p>IBJA benchmark rates for reference only. Rates are exclusive of 3% GST and making charges; final showroom price may vary.</p>
        <a href="https://wa.me/919839638670?text=Hi%20Kanchan%20Jewellers%2C%20please%20share%20today%27s%20jewellery%20rate." target="_blank" rel="noopener" class="ibja-whatsapp-btn">◉ &nbsp; Ask today's rate on WhatsApp</a>
      </div>
    </section>
'''

if 'id="ibjaRates"' not in html:
    anchor = '\n    <!-- Editorial Strip -->'
    if anchor not in html:
        raise RuntimeError('Editorial Strip anchor not found in index.html')
    html = html.replace(anchor, section + anchor, 1)
    index_path.write_text(html, encoding='utf-8')

css_block = r'''

/* ========== IBJA GOLD & SILVER RATES ========== */
.ibja-rates-section {
  max-width: 1280px;
  margin: 18px auto 42px;
  padding: 30px 32px 26px;
  border: 1px solid rgba(193, 151, 63, 0.28);
  border-radius: 22px;
  background:
    radial-gradient(circle at top right, rgba(193, 151, 63, 0.12), transparent 34%),
    linear-gradient(135deg, #4a142f 0%, #5c1a3a 58%, #3d1026 100%);
  color: #fff;
  box-shadow: 0 18px 45px rgba(61, 16, 38, 0.16);
}

.ibja-rates-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 22px;
}

.ibja-kicker {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
  color: #f0cf82;
  font-size: 0.73rem;
  font-weight: 700;
  letter-spacing: 1.5px;
}

.ibja-live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #36d66b;
  box-shadow: 0 0 0 4px rgba(54, 214, 107, 0.11);
}

.ibja-rates-section h2 {
  margin: 0;
  color: #fffaf2;
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2rem, 3vw, 2.7rem);
  line-height: 1.05;
}

.ibja-source-link {
  flex: 0 0 auto;
  color: #e8d5a3;
  font-size: 0.78rem;
  opacity: 0.9;
  transition: var(--transition);
}

.ibja-source-link:hover {
  color: #fff;
  opacity: 1;
}

.ibja-rate-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.ibja-rate-card {
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

.ibja-rates-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  margin-top: 20px;
}

.ibja-rates-foot p {
  margin: 0;
  max-width: 760px;
  color: rgba(255,255,255,0.72);
  font-size: 0.75rem;
}

.ibja-whatsapp-btn {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 17px;
  border-radius: 12px;
  background: #25d366;
  color: #fff;
  font-size: 0.77rem;
  font-weight: 600;
  box-shadow: 0 8px 20px rgba(37, 211, 102, 0.18);
  transition: var(--transition);
}

.ibja-whatsapp-btn:hover {
  background: #1dae52;
  transform: translateY(-1px);
}

@media (max-width: 980px) {
  .ibja-rate-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 680px) {
  .ibja-rates-section {
    margin: 12px 10px 30px;
    padding: 22px 16px 18px;
    border-radius: 16px;
  }

  .ibja-rates-head,
  .ibja-rates-foot {
    align-items: flex-start;
    flex-direction: column;
    gap: 12px;
  }

  .ibja-rate-grid {
    grid-template-columns: 1fr;
  }

  .ibja-whatsapp-btn {
    width: 100%;
  }
}
'''

if '/* ========== IBJA GOLD & SILVER RATES ========== */' not in css:
    styles_path.write_text(css.rstrip() + css_block + '\n', encoding='utf-8')

print('IBJA rate section and matching styles added.')
