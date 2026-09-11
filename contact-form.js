(() => {
  const form = document.getElementById('enquiryForm');
  if (!form) return;

  const WHATSAPP_NUMBER = '919839638670';
  const errorEl = form.querySelector('.enquiry-form-error');

  const showError = (message) => {
    if (errorEl) errorEl.textContent = message || '';
  };

  const formatVisit = (value) => {
    if (!value) return 'Not specified';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    showError('');

    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const name = String(data.get('name') || '').trim();
    const phone = String(data.get('phone') || '').trim();
    const interest = String(data.get('interest') || '').trim();
    const occasion = String(data.get('occasion') || '').trim() || 'Not specified';
    const preferredVisit = formatVisit(String(data.get('preferredVisit') || '').trim());
    const customerMessage = String(data.get('message') || '').trim() || 'No additional message';

    const phoneDigits = phone.replace(/\D/g, '');
    if (name.length < 2 || phoneDigits.length < 10 || phoneDigits.length > 15 || !interest) {
      showError('Please check your name, mobile number and jewellery interest.');
      return;
    }

    const message = [
      '*New Website Enquiry - Kanchan Jewellers*',
      '',
      `Name: ${name}`,
      `Mobile: ${phone}`,
      `Interested In: ${interest}`,
      `Occasion: ${occasion}`,
      `Preferred Visit: ${preferredVisit}`,
      '',
      `Message: ${customerMessage}`
    ].join('\n');

    const whatsappUrl = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
    const popup = window.open(whatsappUrl, '_blank', 'noopener');

    if (!popup) {
      window.location.href = whatsappUrl;
    }
  });
})();
