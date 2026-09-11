const jsonResponse = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  }
});

const clean = (value, max = 180) => String(value ?? '')
  .replace(/[\u0000-\u001F\u007F]/g, ' ')
  .trim()
  .slice(0, max);

export async function onRequestPost(context) {
  const { request, env } = context;

  const contentType = request.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    return jsonResponse({ ok: false, message: 'Invalid request.' }, 415);
  }

  let body;
  try {
    body = await request.json();
  } catch (_) {
    return jsonResponse({ ok: false, message: 'Invalid request.' }, 400);
  }

  // Honeypot: silently accept obvious bot submissions without sending anything.
  if (clean(body.website, 120)) {
    return jsonResponse({ ok: true });
  }

  const name = clean(body.name, 80);
  const phone = clean(body.phone, 24);
  const interest = clean(body.interest, 80);
  const occasion = clean(body.occasion, 80) || 'Not specified';
  const preferredVisit = clean(body.preferredVisit, 80) || 'Not specified';
  const message = clean(body.message, 500) || 'No additional message';

  const phoneDigits = phone.replace(/\D/g, '');
  if (name.length < 2 || phoneDigits.length < 10 || phoneDigits.length > 15 || !interest) {
    return jsonResponse({ ok: false, message: 'Please check the required fields.' }, 400);
  }

  const token = env.WHATSAPP_TOKEN;
  const phoneNumberId = env.WHATSAPP_PHONE_NUMBER_ID;
  const recipient = String(env.WHATSAPP_RECIPIENT || '').replace(/\D/g, '');
  const templateName = env.WHATSAPP_TEMPLATE_NAME;
  const templateLanguage = env.WHATSAPP_TEMPLATE_LANGUAGE || 'en_US';
  const graphVersion = env.META_GRAPH_VERSION || 'v23.0';

  if (!token || !phoneNumberId || !recipient || !templateName) {
    console.error('WhatsApp enquiry service is missing required environment variables.');
    return jsonResponse({ ok: false, message: 'Enquiry service is not configured yet.' }, 503);
  }

  const payload = {
    messaging_product: 'whatsapp',
    recipient_type: 'individual',
    to: recipient,
    type: 'template',
    template: {
      name: templateName,
      language: { code: templateLanguage },
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: name },
            { type: 'text', text: phone },
            { type: 'text', text: interest },
            { type: 'text', text: occasion },
            { type: 'text', text: preferredVisit },
            { type: 'text', text: message }
          ]
        }
      ]
    }
  };

  let metaResponse;
  try {
    metaResponse = await fetch(`https://graph.facebook.com/${graphVersion}/${phoneNumberId}/messages`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
  } catch (error) {
    console.error('WhatsApp API network error:', error);
    return jsonResponse({ ok: false, message: 'Could not submit enquiry right now.' }, 502);
  }

  const responseText = await metaResponse.text();

  if (!metaResponse.ok) {
    console.error('WhatsApp API error:', metaResponse.status, responseText.slice(0, 800));
    return jsonResponse({ ok: false, message: 'Could not submit enquiry right now.' }, 502);
  }

  let metaData = null;
  try {
    metaData = JSON.parse(responseText);
  } catch (_) {
    metaData = null;
  }

  if (!metaData?.messages?.[0]?.id) {
    console.error('WhatsApp API returned no message id:', responseText.slice(0, 800));
    return jsonResponse({ ok: false, message: 'Could not confirm enquiry submission.' }, 502);
  }

  return jsonResponse({ ok: true });
}

export function onRequest(context) {
  if (context.request.method === 'POST') {
    return onRequestPost(context);
  }

  return jsonResponse({ ok: false, message: 'Method not allowed.' }, 405);
}
