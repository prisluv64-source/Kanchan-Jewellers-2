from pathlib import Path

html_path = Path('contact.html')
css_path = Path('contact-page.css')

html = html_path.read_text(encoding='utf-8')
css = css_path.read_text(encoding='utf-8')

faq_html = '''

      <section class="contact-faq-section" id="faq">
        <div class="contact-page-section-head contact-faq-head">
          <p class="eyebrow">FAQ</p>
          <h2>Frequently Asked Questions</h2>
        </div>

        <div class="contact-faq-list">
          <details class="contact-faq-item" open>
            <summary>Is all your gold hallmarked?</summary>
            <div class="contact-faq-answer">
              <p>Yes. Every gold piece carries the BIS hallmark with HUID. Silver articles are 92.5 sterling.</p>
            </div>
          </details>

          <details class="contact-faq-item">
            <summary>Do you accept old gold in exchange?</summary>
            <div class="contact-faq-answer">
              <p>Bring your old gold to the showroom for assessment. Our team can check its purity and weight and explain the exchange value and applicable terms before you decide.</p>
            </div>
          </details>

          <details class="contact-faq-item">
            <summary>Can you make a custom design?</summary>
            <div class="contact-faq-answer">
              <p>Custom-design requirements can be discussed at the showroom. Share a reference, photo or idea with us and our team can guide you on the design, metal, approximate weight and feasibility.</p>
            </div>
          </details>

          <details class="contact-faq-item">
            <summary>How are prices decided?</summary>
            <div class="contact-faq-answer">
              <p>Jewellery pricing depends on the prevailing gold or silver rate, purity, net metal weight, making charges, design or stone value where applicable, and taxes. The final breakup is explained at the time of purchase.</p>
            </div>
          </details>
        </div>
      </section>
'''

if 'class="contact-faq-section"' not in html:
    marker = '      </section>    </section>\n  </main>'
    if marker in html:
        html = html.replace(marker, '      </section>' + faq_html + '    </section>\n  </main>', 1)
    else:
        marker = '    </section>\n  </main>'
        if marker not in html:
            raise RuntimeError('Could not find contact main closing marker')
        html = html.replace(marker, faq_html + '    </section>\n  </main>', 1)
    html_path.write_text(html, encoding='utf-8')
    print('FAQ section added to contact.html')
else:
    print('FAQ section already present')

faq_css = '''

/* ===== CONTACT FAQ ===== */
.contact-faq-section {
  margin-top: 72px;
  padding-top: 8px;
}

.contact-faq-head {
  max-width: 760px;
  margin-bottom: 26px;
}

.contact-faq-list {
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 14px 38px rgba(52, 20, 30, .06);
}

.contact-faq-item {
  border-bottom: 1px solid var(--border);
}

.contact-faq-item:last-child {
  border-bottom: 0;
}

.contact-faq-item summary {
  position: relative;
  padding: 23px 64px 23px 24px;
  cursor: pointer;
  list-style: none;
  color: var(--primary);
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.45rem;
  font-weight: 700;
  line-height: 1.2;
  transition: background .2s ease, color .2s ease;
}

.contact-faq-item summary::-webkit-details-marker {
  display: none;
}

.contact-faq-item summary::after {
  content: '+';
  position: absolute;
  top: 50%;
  right: 24px;
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  transform: translateY(-50%);
  border-radius: 50%;
  background: #f4ead5;
  color: var(--primary);
  font-family: Inter, sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  transition: transform .2s ease, background .2s ease;
}

.contact-faq-item[open] summary {
  background: #fffaf3;
}

.contact-faq-item[open] summary::after {
  content: '−';
  background: var(--primary);
  color: #fff;
}

.contact-faq-answer {
  padding: 0 64px 23px 24px;
  background: #fffaf3;
}

.contact-faq-answer p {
  max-width: 900px;
  margin: 0;
  color: var(--text-light);
  font-size: .84rem;
  line-height: 1.75;
}

@media (max-width: 720px) {
  .contact-faq-section {
    margin-top: 56px;
  }

  .contact-faq-item summary {
    padding: 19px 56px 19px 18px;
    font-size: 1.25rem;
  }

  .contact-faq-item summary::after {
    right: 18px;
    width: 30px;
    height: 30px;
  }

  .contact-faq-answer {
    padding: 0 18px 20px;
  }
}
'''

if '/* ===== CONTACT FAQ ===== */' not in css:
    css = css.rstrip() + faq_css + '\n'
    css_path.write_text(css, encoding='utf-8')
    print('FAQ styles added to contact-page.css')
else:
    print('FAQ styles already present')
