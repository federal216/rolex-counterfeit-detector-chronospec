const { OWNER_EMAIL, resolveProduct } = require('./products');
const { isValidEmail, sendPurchaseDossierEmails, getConfiguredProvider } = require('./mailer');
const {
  readRawRequestBody,
  verifyDodoWebhookSignature,
  verifyWhopWebhookSignature,
  verifyDodoPayment,
  verifyWhopPayment,
  verifyDeliveryProof
} = require('./verifier');

function setCorsHeaders(res) {
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');
}

function buildMetadataSummary(meta) {
  if (!meta || typeof meta !== 'object') return '';
  const parts = [];
  if (meta.model) parts.push(`Model: ${meta.model}`);
  if (meta.reference) parts.push(`Reference: ${meta.reference}`);
  if (meta.summary) parts.push(String(meta.summary));
  return parts.join(' | ');
}

function isAllowedReturnUrl(urlStr) {
  if (!urlStr || typeof urlStr !== 'string') return false;
  try {
    const parsed = new URL(urlStr);
    if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') return false;
    const host = parsed.hostname.toLowerCase();
    return (
      host === 'federal216.github.io' ||
      host === 'hseenglish.app' ||
      host === 'localhost' ||
      host === '127.0.0.1' ||
      host.endsWith('.vercel.app') ||
      host.endsWith('lambospec.ai') ||
      host.endsWith('cabinetscan.ai') ||
      host.endsWith('chronospec.ai')
    );
  } catch {
    return false;
  }
}

async function parseJsonFromRequest(req) {
  if (req.body && typeof req.body === 'object' && !Buffer.isBuffer(req.body)) {
    return { rawBody: req.rawBody || JSON.stringify(req.body), body: req.body };
  }
  const rawBody = await readRawRequestBody(req);
  const body = rawBody ? JSON.parse(rawBody) : {};
  return { rawBody, body };
}

async function handleDeliverPdf(req, res, { defaultProductKey }) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method Not Allowed' });

  try {
    const { body } = await parseJsonFromRequest(req);
    const {
      productKey,
      customerEmail,
      buyerName,
      paymentMethod,
      paymentId,
      sessionId,
      transactionId,
      network,
      pdfBase64,
      filename,
      summaryText,
      testToken
    } = body || {};

    const product = resolveProduct({ productKey, defaultKey: defaultProductKey });

    const proof = await verifyDeliveryProof({
      paymentMethod,
      paymentId,
      sessionId,
      transactionId,
      network,
      testToken,
      product
    });

    if (!proof.verified) {
      return res.status(402).json({
        ok: false,
        error: proof.reason || 'Payment proof could not be verified.'
      });
    }

    const finalProduct = proof.productId || proof.planId || proof.metadata
      ? resolveProduct({
          productKey,
          productId: proof.productId,
          planId: proof.planId,
          metadata: proof.metadata,
          defaultKey: product.productKey
        })
      : product;

    const finalEmail = isValidEmail(customerEmail) ? customerEmail.trim() : proof.customerEmail;
    if (!isValidEmail(finalEmail)) {
      return res.status(400).json({
        ok: false,
        error: 'A valid customer email address is required to deliver the PDF dossier.'
      });
    }

    const result = await sendPurchaseDossierEmails({
      product: finalProduct,
      customerEmail: finalEmail,
      buyerName: buyerName || proof.buyerName || 'VIP Client',
      paymentMethod: paymentMethod || 'checkout',
      transactionId: proof.transactionId || transactionId || paymentId || sessionId || `TXN-${Date.now()}`,
      amountLabel: proof.amountLabel,
      pdfBase64,
      filename,
      summaryText: summaryText || buildMetadataSummary(proof.metadata)
    });

    const statusCode = result.ok ? 200 : 500;
    return res.status(statusCode).json(result);
  } catch (err) {
    console.error('Deliver PDF error:', err);
    return res.status(500).json({ ok: false, error: err.message || 'Internal delivery error' });
  }
}

async function handleDodoWebhook(req, res, { defaultProductKey }) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method Not Allowed' });

  try {
    const { rawBody, body: event } = await parseJsonFromRequest(req);
    const webhookSecret = process.env.DODO_WEBHOOK_SECRET;

    if (webhookSecret) {
      const sigCheck = verifyDodoWebhookSignature({
        rawBody,
        headers: req.headers || {},
        secret: webhookSecret
      });
      if (!sigCheck.verified) {
        return res.status(401).json({ ok: false, error: `Invalid Dodo webhook signature: ${sigCheck.reason}` });
      }
    }

    const eventType = String(event?.type || event?.event_type || '').toLowerCase();
    const data = event?.data || event || {};
    const status = String(data.status || '').toLowerCase();

    const isSuccessEvent =
      eventType === 'payment.succeeded' ||
      eventType === 'checkout.session.completed' ||
      (!eventType && status === 'succeeded');

    if (!isSuccessEvent) {
      return res.status(200).json({ ok: true, ignored: true, eventType: eventType || status || 'unknown' });
    }

    const paymentId = data.payment_id || data.id || null;
    const sessionId = data.session_id || data.checkout_session_id || null;

    // Always corroborate against Dodo API when secret isn't set (and to retrieve full metadata)
    let apiProof = { verified: false };
    if (paymentId || sessionId) {
      apiProof = await verifyDodoPayment({ paymentId, sessionId });
    }

    if (!webhookSecret && !apiProof.verified) {
      return res.status(401).json({
        ok: false,
        error: 'Unverified Dodo webhook: set DODO_WEBHOOK_SECRET or send a valid payment_id.'
      });
    }

    const metadata = { ...(data.metadata || {}), ...(apiProof.metadata || {}) };
    const product = resolveProduct({
      productId: apiProof.productId || data.product_cart?.[0]?.product_id,
      metadata,
      defaultKey: defaultProductKey
    });

    const customerEmail = apiProof.customerEmail || data.customer?.email || null;
    const buyerName = apiProof.buyerName || data.customer?.name || 'VIP Client';
    const txId = apiProof.transactionId || paymentId || sessionId || `DODO-${Date.now()}`;
    const amountLabel = apiProof.amountLabel || (
      data.total_amount ? `${(Number(data.total_amount) / 100).toFixed(2)} ${data.currency || 'USD'}` : null
    );

    const result = await sendPurchaseDossierEmails({
      product,
      customerEmail,
      buyerName,
      paymentMethod: 'dodo',
      transactionId: txId,
      amountLabel,
      summaryText: buildMetadataSummary(metadata)
    });

    return res.status(result.ownerSent ? 200 : 500).json(result);
  } catch (err) {
    console.error('Dodo webhook error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
}

async function handleWhopWebhook(req, res, { defaultProductKey }) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method Not Allowed' });

  try {
    const { rawBody, body: event } = await parseJsonFromRequest(req);
    const webhookSecret = process.env.WHOP_WEBHOOK_SECRET;

    if (webhookSecret) {
      const sigCheck = verifyWhopWebhookSignature({
        rawBody,
        headers: req.headers || {},
        secret: webhookSecret
      });
      if (!sigCheck.verified) {
        return res.status(401).json({ ok: false, error: `Invalid Whop webhook signature: ${sigCheck.reason}` });
      }
    }

    const action = String(event?.action || event?.type || event?.event || '').toLowerCase();
    const data = event?.data || event || {};
    const validActions = ['payment.succeeded', 'membership.went_valid', 'membership.activated', 'invoice.paid'];

    if (action && !validActions.includes(action)) {
      return res.status(200).json({ ok: true, ignored: true, action });
    }

    const txId = data.id || data.payment_id || data.membership_id || null;

    let apiProof = { verified: false };
    if (!webhookSecret) {
      if (!process.env.WHOP_API_KEY) {
        return res.status(503).json({
          ok: false,
          error: 'WHOP_WEBHOOK_SECRET or WHOP_API_KEY must be configured to verify Whop webhooks.'
        });
      }
      apiProof = await verifyWhopPayment({
        paymentId: data.payment_id || (String(txId || '').startsWith('pay_') ? txId : null),
        membershipId: data.membership_id || (String(txId || '').startsWith('mem_') ? txId : null)
      });
      if (!apiProof.verified) {
        return res.status(401).json({ ok: false, error: 'Unverified Whop event.' });
      }
    }

    const customerEmail =
      apiProof.customerEmail ||
      data.user?.email ||
      data.email ||
      data.customer?.email ||
      data.member?.email ||
      null;
    const buyerName =
      apiProof.buyerName ||
      data.user?.name ||
      data.user?.username ||
      data.customer?.name ||
      'Whop VIP Client';

    const product = resolveProduct({
      planId: apiProof.planId || data.plan_id || data.plan?.id || data.product?.slug,
      productId: data.product_id || data.product?.id,
      metadata: data.metadata,
      defaultKey: defaultProductKey
    });

    const amountVal = data.final_amount || data.subtotal || data.amount;
    const amountLabel = amountVal
      ? `$${(Number(amountVal) > 500 ? Number(amountVal) / 100 : Number(amountVal)).toFixed(2)} ${(data.currency || 'USD').toUpperCase()}`
      : null;

    const result = await sendPurchaseDossierEmails({
      product,
      customerEmail,
      buyerName,
      paymentMethod: 'whop',
      transactionId: txId || `WHOP-${Date.now()}`,
      amountLabel,
      summaryText: buildMetadataSummary(data.metadata)
    });

    return res.status(result.ownerSent ? 200 : 500).json(result);
  } catch (err) {
    console.error('Whop webhook error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
}

function handleStatus(req, res, { defaultProductKey }) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();
  const product = resolveProduct({ defaultKey: defaultProductKey });
  const provider = getConfiguredProvider();
  return res.json({
    status: 'online',
    active: true,
    service: product.brandName,
    productKey: product.productKey,
    priceUsd: product.priceUsd.toFixed(2),
    ownerEmail: OWNER_EMAIL,
    emailConfigured: Boolean(provider),
    emailProvider: provider || 'unconfigured',
    gateways: {
      dodo: true,
      whop: true,
      crypto: true,
      paytr: product.productKey === 'lambospec'
    }
  });
}

module.exports = {
  setCorsHeaders,
  isAllowedReturnUrl,
  handleDeliverPdf,
  handleDodoWebhook,
  handleWhopWebhook,
  handleStatus
};
