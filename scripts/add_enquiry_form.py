from pathlib import Path

path = Path('contact.html')
html = path.read_text(encoding='utf-8')

css_link = '  <link rel="stylesheet" href="contact-form.css">\n'
if 'contact-form.css' not in html:
    html = html.replace(
        '  <link rel="stylesheet" href="contact-page.css">\n',
        '  <link rel="stylesheet" href="contact-page.css">\n' + css_link,
        1,
    )

form_markup = r'''
      <section class="enquiry-section" id="enquiry">
        <div class="enquiry-section-head">
          <p class="eyebrow">Send an Enquiry</p>
          <h2>Tell us what you are looking for</h2>
        </div>

        <div class="enquiry-layout">
          <aside class="enquiry-intro">
            <p class="enquiry-kicker">Kanchan Jewellers</p>
            <h3>We’ll help you plan your jewellery visit.</h3>
            <p>Share a few details and our showroom team will receive your enquiry privately. You stay on this page — WhatsApp will not open on your device.</p>

            <div class="enquiry-points">
              <div class="enquiry-point">
                <span>✦</span>
                <div><strong>Personal response</strong><small>We can guide you according to jewellery type, occasion and visit preference.</small></div>
              </div>
              <div class="enquiry-point">
                <span>☎</span>
                <div><strong>Easy follow-up</strong><small>Leave your mobile number so our team can get in touch with you.</small></div>
              </div>
              <div class="enquiry-point">
                <span>⌖</span>
                <div><strong>Showroom assistance</strong><small>Tell us what you want to see and we can prepare better for your visit.</small></div>
              </div>
            </div>
          </aside>

          <div class="enquiry-form-card">
            <form class="enquiry-form" id="enquiryForm" novalidate>
              <div class="enquiry-form-grid">
                <div class="enquiry-field">
                  <label for="enquiryName">Your Name *</label>
                  <input id="enquiryName" name="name" type="text" autocomplete="name" minlength="2" maxlength="80" required placeholder="Enter your name">
                </div>

                <div class="enquiry-field">
                  <label for="enquiryPhone">Mobile Number *</label>
                  <input id="enquiryPhone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="18" required placeholder="e.g. 9839638670">
                </div>

                <div class="enquiry-field">
                  <label for="enquiryInterest">Interested In *</label>
                  <select id="enquiryInterest" name="interest" required>
                    <option value="">Select jewellery</option>
                    <option>Necklaces</option>
                    <option>Earrings & Jhumkas</option>
                    <option>Bangles</option>
                    <option>Rings</option>
                    <option>Mangalsutra</option>
                    <option>Chains</option>
                    <option>Bridal Jewellery</option>
                    <option>Silver Articles</option>
                    <option>Gold & Silver Coins</option>
                    <option>Other Jewellery</option>
                  </select>
                </div>

                <div class="enquiry-field">
                  <label for="enquiryOccasion">Occasion</label>
                  <select id="enquiryOccasion" name="occasion">
                    <option value="">Select occasion</option>
                    <option>Wedding</option>
                    <option>Engagement</option>
                    <option>Festival</option>
                    <option>Anniversary</option>
                    <option>Gifting</option>
                    <option>Daily Wear</option>
                    <option>Other</option>
                  </select>
                </div>

                <div class="enquiry-field full">
                  <label for="enquiryVisit">Preferred Visit Date & Time</label>
                  <input id="enquiryVisit" name="preferredVisit" type="datetime-local">
                </div>

                <div class="enquiry-field full">
                  <label for="enquiryMessage">Message</label>
                  <textarea id="enquiryMessage" name="message" maxlength="500" placeholder="Tell us about the design, budget range or anything you would like us to know..."></textarea>
                </div>

                <div class="enquiry-honeypot" aria-hidden="true">
                  <label for="enquiryWebsite">Website</label>
                  <input id="enquiryWebsite" name="website" type="text" tabindex="-1" autocomplete="off">
                </div>
              </div>

              <p class="enquiry-form-note">By submitting this enquiry, you agree that Kanchan Jewellers may contact you about this request. Your WhatsApp app will not be opened by this form.</p>

              <div class="enquiry-submit-row">
                <button class="enquiry-submit-btn" type="submit">Submit Enquiry</button>
                <p class="enquiry-form-error" role="alert" aria-live="polite"></p>
              </div>
            </form>
          </div>
        </div>
      </section>

      <div class="enquiry-success-modal" id="enquirySuccessModal" hidden role="dialog" aria-modal="true" aria-labelledby="enquirySuccessTitle">
        <div class="enquiry-success-card">
          <div class="enquiry-success-icon">✓</div>
          <h3 id="enquirySuccessTitle">Enquiry submitted successfully!</h3>
          <p>Thank you for contacting Kanchan Jewellers. We have received your enquiry and will get in touch with you shortly.</p>
          <button class="enquiry-success-close" id="enquirySuccessClose" type="button">Done</button>
        </div>
      </div>
'''

if 'id="enquiryForm"' not in html:
    needle = '      </section>\n    </section>\n  </main>'
    if needle not in html:
        raise RuntimeError('Could not find insertion point after Plan Your Visit section')
    html = html.replace(
        needle,
        '      </section>\n' + form_markup + '    </section>\n  </main>',
        1,
    )

script_tag = '  <script src="contact-form.js" defer></script>\n'
if 'contact-form.js' not in html:
    needle = '  <script>\n    const yearEl = document.getElementById(\'year\');'
    if needle not in html:
        raise RuntimeError('Could not find footer script insertion point')
    html = html.replace(needle, script_tag + needle, 1)

path.write_text(html, encoding='utf-8')
print('Enquiry form, stylesheet and script links added to contact.html')
