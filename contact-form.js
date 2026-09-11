(() => {
  const form = document.getElementById('enquiryForm');
  if (!form) return;

  const submitBtn = form.querySelector('.enquiry-submit-btn');
  const errorEl = form.querySelector('.enquiry-form-error');
  const modal = document.getElementById('enquirySuccessModal');
  const closeBtn = document.getElementById('enquirySuccessClose');
  const defaultBtnText = submitBtn ? submitBtn.textContent : 'Submit Enquiry';

  const showError = (message) => {
    if (errorEl) errorEl.textContent = message || '';
  };

  const openSuccess = () => {
    if (!modal) return;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    closeBtn?.focus();
  };

  const closeSuccess = () => {
    if (!modal) return;
    modal.hidden = true;
    document.body.style.overflow = '';
  };

  closeBtn?.addEventListener('click', closeSuccess);

  modal?.addEventListener('click', (event) => {
    if (event.target === modal) closeSuccess();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modal && !modal.hidden) closeSuccess();
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    showError('');

    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const payload = {
      name: String(data.get('name') || '').trim(),
      phone: String(data.get('phone') || '').trim(),
      interest: String(data.get('interest') || '').trim(),
      occasion: String(data.get('occasion') || '').trim(),
      preferredVisit: String(data.get('preferredVisit') || '').trim(),
      message: String(data.get('message') || '').trim(),
      website: String(data.get('website') || '').trim()
    };

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Submitting…';
    }

    try {
      const response = await fetch('/api/enquiry', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      let result = null;
      try {
        result = await response.json();
      } catch (_) {
        result = null;
      }

      if (!response.ok || !result?.ok) {
        throw new Error(result?.message || 'Unable to submit enquiry');
      }

      form.reset();
      openSuccess();
    } catch (error) {
      console.error('Enquiry submission failed:', error);
      showError('We could not submit your enquiry right now. Please try again in a moment or call us at +91 98396 38670.');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = defaultBtnText;
      }
    }
  });
})();
