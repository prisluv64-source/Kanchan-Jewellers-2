from pathlib import Path
import re

index_path = Path('index.html')
styles_path = Path('styles.css')
html = index_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')

footer_html = r'''  <!-- Footer -->
  <footer class="site-footer">
    <div class="footer-shell">

      <div class="footer-cta">
        <div class="footer-cta-copy">
          <strong>Get festive offers &amp; new designs on WhatsApp</strong>
          <span>Festive offers, new arrivals and today's jewellery rate — straight from our showroom.</span>
        </div>
        <a href="https://wa.me/919839638670?text=Hi%20Kanchan%20Jewellers%2C%20please%20send%20me%20latest%20offers%20and%20new%20designs." target="_blank" rel="noopener" class="footer-whatsapp-cta">
          <svg viewBox="0 0 32 32" aria-hidden="true">
            <path d="M16.004 2.002c-7.732 0-14 6.268-14 14 0 2.465.643 4.86 1.863 6.975L2 30l7.22-1.89A13.93 13.93 0 0 0 16.004 30c7.732 0 14-6.268 14-14s-6.268-14-14-14zm0 25.5a11.47 11.47 0 0 1-5.86-1.605l-.42-.25-4.28 1.12 1.14-4.17-.27-.43A11.47 11.47 0 0 1 4.5 16c0-6.35 5.15-11.5 11.5-11.5S27.5 9.65 27.5 16 22.35 27.5 16 27.5z"/>
            <path d="M22.15 19.35c-.3-.15-1.78-.88-2.05-.98-.28-.1-.48-.15-.68.15-.2.3-.78.98-.96 1.18-.18.2-.35.22-.65.08-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.78-1.68-2.08-.18-.3-.02-.46.13-.6.14-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.38-.02-.52-.08-.15-.68-1.63-.93-2.23-.24-.58-.5-.5-.68-.5h-.58c-.2 0-.52.08-.8.38-.28.3-1.05 1.03-1.05 2.5s1.08 2.9 1.23 3.1c.15.2 2.12 3.23 5.15 4.53 1.92.83 2.67.9 3.63.76.58-.09 1.78-.73 2.03-1.43.25-.7.25-1.3.18-1.43-.08-.12-.28-.2-.58-.35z"/>
          </svg>
          Get updates on WhatsApp
        </a>
      </div>

      <div class="footer-grid">
        <div class="footer-column footer-about">
          <a href="#top" class="footer-logo-row">
            <img src="logo-kj.jpg" alt="Kanchan Jewellers" loading="lazy" decoding="async">
            <div>
              <strong>Kanchan</strong>
              <span>Jewellers</span>
            </div>
          </a>
          <p>Timeless gold, silver and diamond jewellery with warm personal service for every celebration.</p>
          <div class="footer-mini-badge">✦ Jewellery chosen with care</div>
        </div>

        <div class="footer-column">
          <h3>Quick Links</h3>
          <nav class="footer-nav" aria-label="Footer quick links">
            <a href="#top">Home</a>
            <a href="#collections">All Jewellery</a>
            <a href="#featured">Bridal</a>
            <a href="#about">Our Story</a>
            <a href="#contact">Visit Us</a>
          </nav>
        </div>

        <div class="footer-column">
          <h3>Categories</h3>
          <nav class="footer-nav" aria-label="Footer jewellery categories">
            <a href="#collections">Necklaces</a>
            <a href="#collections">Earrings &amp; Jhumkas</a>
            <a href="#collections">Bangles</a>
            <a href="#collections">Rings</a>
            <a href="#collections">Mangalsutra</a>
            <a href="#collections">Chains</a>
            <a href="#collections">Silver Articles</a>
            <a href="#collections">Gold &amp; Silver Coins</a>
          </nav>
        </div>

        <div class="footer-column footer-contact">
          <h3>Contact</h3>
          <div class="footer-contact-item">
            <span class="footer-contact-icon">⌖</span>
            <div>
              <span>H.N., Kazi Khera, near Dr. Dey's Hospital, Lal Bangla, Jajmau, Kanpur – 208007</span>
              <a href="https://maps.google.com/maps?q=H.N%2C%2BKazi%2BKhera%2C%2Bnear%2BDr.%2BDey's%2BHospital%2C%2BLal%2BBangla%2C%2BJajmau%2BSub%2BMetro%2BCity%2C%2BKanpur%2C%2BUttar%2BPradesh%2B208007" target="_blank" rel="noopener">Get Directions →</a>
            </div>
          </div>
          <div class="footer-contact-item">
            <span class="footer-contact-icon">☎</span>
            <a href="tel:+919839638670">+91 98396 38670</a>
          </div>
          <div class="footer-contact-item">
            <span class="footer-contact-icon">◷</span>
            <span>Tue–Sun: 10:00 AM – 10:00 PM<br>Mon: 11:00 AM – 10:00 PM</span>
          </div>
          <div class="footer-contact-item">
            <span class="footer-contact-icon">◎</span>
            <a href="https://www.instagram.com/kanchanjewellersvipin/" target="_blank" rel="noopener">@kanchanjewellersvipin</a>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="footer-bottom-inner">
        <p>© <span id="year"></span> Kanchan Jewellers. All rights reserved.</p>
        <div class="footer-trust-badges" aria-label="Store values">
          <span>✦ Personal Assistance</span>
          <span>◇ Elegant Designs</span>
          <span>₹ Transparent Pricing</span>
        </div>
      </div>
    </div>
  </footer>'''

html, count = re.subn(
    r'  <!-- Footer -->\s*<footer>.*?</footer>',
    footer_html,
    html,
    count=1,
    flags=re.S,
)
if count != 1:
    raise RuntimeError('Could not locate existing footer HTML')

footer_css = r'''/* ========== PREMIUM FOOTER ========== */
.site-footer {
  margin-top: 62px;
  padding: 0;
  background: #211f22;
  color: #f7f1e8;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.footer-shell {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px 42px;
}

.footer-cta {
  position: relative;
  transform: translateY(-34px);
  margin: 0 auto -4px;
  max-width: 980px;
  min-height: 82px;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  border: 1px solid rgba(232, 213, 163, 0.18);
  border-radius: 16px;
  background: linear-gradient(135deg, #5c1a3a, #6d2850);
  box-shadow: 0 16px 34px rgba(0, 0, 0, 0.24);
}

.footer-cta-copy strong {
  display: block;
  margin-bottom: 3px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.35rem;
  line-height: 1.1;
  color: #fffaf2;
}

.footer-cta-copy span {
  display: block;
  color: rgba(255, 255, 255, 0.72);
  font-size: 0.75rem;
}

.footer-whatsapp-cta {
  flex: 0 0 auto;
  min-height: 40px;
  padding: 9px 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  border-radius: 9px;
  background: #25d366;
  color: #fff;
  font-size: 0.76rem;
  font-weight: 700;
  transition: var(--transition);
}

.footer-whatsapp-cta svg {
  width: 17px;
  height: 17px;
  fill: currentColor;
}

.footer-whatsapp-cta:hover {
  background: #1daf52;
  transform: translateY(-1px);
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.25fr 0.75fr 0.9fr 1.3fr;
  gap: 54px;
  align-items: start;
  padding-top: 16px;
}

.footer-column h3 {
  margin: 0 0 14px;
  color: #fffaf2;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.05rem;
  font-weight: 700;
}

.footer-logo-row {
  display: inline-flex;
  align-items: center;
  gap: 11px;
  margin-bottom: 16px;
}

.footer-logo-row img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(232, 213, 163, 0.65);
}

.footer-logo-row strong,
.footer-logo-row span {
  display: block;
  line-height: 1;
}

.footer-logo-row strong {
  color: #f4d487;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.34rem;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}

.footer-logo-row span {
  margin-top: 3px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.64rem;
  text-transform: uppercase;
  letter-spacing: 1.8px;
}

.footer-about > p {
  max-width: 290px;
  margin: 0 0 16px;
  color: rgba(255, 255, 255, 0.68);
  font-size: 0.76rem;
  line-height: 1.7;
}

.footer-mini-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;
  border: 1px solid rgba(193, 151, 63, 0.3);
  border-radius: 999px;
  background: rgba(92, 26, 58, 0.24);
  color: #e8d5a3;
  font-size: 0.66rem;
  font-weight: 600;
}

.footer-nav {
  display: grid;
  gap: 9px;
}

.footer-nav a {
  width: fit-content;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.75rem;
  transition: var(--transition);
}

.footer-nav a:hover {
  color: #f4d487;
  transform: translateX(2px);
}

.footer-contact {
  min-width: 0;
}

.footer-contact-item {
  display: grid;
  grid-template-columns: 18px 1fr;
  gap: 8px;
  align-items: start;
  margin-bottom: 11px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.72rem;
  line-height: 1.55;
}

.footer-contact-icon {
  color: #d7a7c0;
  line-height: 1.4;
}

.footer-contact-item a {
  color: rgba(255, 255, 255, 0.78);
  transition: var(--transition);
}

.footer-contact-item a:hover {
  color: #f4d487;
}

.footer-contact-item div > a {
  display: inline-block;
  margin-top: 2px;
  color: #e8d5a3;
  font-size: 0.68rem;
  font-weight: 600;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: #181719;
}

.footer-bottom-inner {
  max-width: 1280px;
  min-height: 54px;
  margin: 0 auto;
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.site-footer .footer-bottom p {
  margin: 0;
  width: auto;
  text-align: left;
  color: rgba(255, 255, 255, 0.48);
  font-size: 0.68rem;
  opacity: 1;
}

.footer-trust-badges {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 7px;
  flex-wrap: wrap;
}

.footer-trust-badges span {
  padding: 4px 9px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.035);
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.62rem;
  line-height: 1;
}

@media (max-width: 980px) {
  .footer-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 36px 42px;
  }
}

@media (max-width: 680px) {
  .site-footer {
    margin-top: 52px;
  }

  .footer-shell {
    padding: 0 16px 34px;
  }

  .footer-cta {
    transform: translateY(-26px);
    margin-bottom: 0;
    padding: 18px;
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }

  .footer-whatsapp-cta {
    width: 100%;
  }

  .footer-grid {
    grid-template-columns: 1fr;
    gap: 28px;
  }

  .footer-bottom-inner {
    padding: 16px;
    flex-direction: column;
    align-items: flex-start;
  }

  .footer-trust-badges {
    justify-content: flex-start;
  }
}'''

css, count = re.subn(
    r'/\* ========== FOOTER ========== \*/.*?(?=/\* ========== FLOATING WHATSAPP ========== \*/)',
    footer_css + '\n\n',
    css,
    count=1,
    flags=re.S,
)
if count != 1:
    raise RuntimeError('Could not locate existing footer CSS')

index_path.write_text(html, encoding='utf-8')
styles_path.write_text(css, encoding='utf-8')
print('Premium screenshot-style footer applied.')
