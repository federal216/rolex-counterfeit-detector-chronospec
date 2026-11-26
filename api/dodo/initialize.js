const https = require('https');
const { isAllowedReturnUrl } = require('../../lib/handlers');

const LIVE_API_KEY = process.env.DODO_PAYMENTS_LIVE_KEY || 'dodo_live_xNuMmrRTOkHMLZY7.pEQXFVs-wu2XLVkeKX7xvdvcH9v71jbN6FdtMEyTPzCJLR0j';
const LIVE_PRODUCT_ID = process.env.DODO_LIVE_PRODUCT_ID || 'pdt_0Nsi1qHuRLnD6c4NmHyfK';

const TEST_API_KEY = process.env.DODO_PAYMENTS_TEST_KEY || 'dodo_test_0_u-P96zqKPvQVU1.lwM9WJvPchJR4POMqkT0iVuHclz9ul4Jfbf8Jd_-JJZSuM4Q';
const TEST_PRODUCT_ID = process.env.DODO_TEST_PRODUCT_ID || 'pdt_0Nsi1qHuRLnD6c4NmHyfK';

function createCheckoutSession(host, apiKey, productId, email, buyerName, returnUrl) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      product_cart: [{ product_id: productId, quantity: 1 }],
      customer: { email, name: buyerName },
      return_url: returnUrl,
      metadata: {
        app: 'chronospec',
        product: 'ChronoSpec AI VIP Rolex Dossier',
        customer_email: email,
        timestamp: Date.now().toString()
      }
    });

    const options = {
      hostname: host,
      port: 443,
      path: '/checkouts',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ statusCode: res.statusCode, data: json });
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

module.exports = async (req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ status: 'failed', reason: 'Method Not Allowed' });

  try {
    const { email = 'collector@chronospec.ai', buyerName = 'Horological Collector', returnUrl: clientReturnUrl } = req.body || {};

    const host = req.headers['x-forwarded-host'] || req.headers.host || 'chronospec.ai';
    const protocol = req.headers['x-forwarded-proto'] || 'https';
    const returnUrl = isAllowedReturnUrl(clientReturnUrl)
      ? clientReturnUrl
      : (process.env.DODO_RETURN_URL || `${protocol}://${host}/?status=success&paid=true&dodo_paid=true`);

    // 1. First attempt: Live Mode API
    let liveResult = null;
    try {
      liveResult = await createCheckoutSession(
        'live.dodopayments.com',
        LIVE_API_KEY,
        LIVE_PRODUCT_ID,
        email,
        buyerName,
        returnUrl
      );
    } catch (err) {
      console.warn('Live mode request network error:', err.message);
    }

    if (liveResult && liveResult.statusCode >= 200 && liveResult.statusCode < 300 && liveResult.data.checkout_url) {
      console.log('✅ Live Dodo Payments Checkout session created for ChronoSpec');
      return res.json({
        status: 'success',
        mode: 'live',
        sessionId: liveResult.data.session_id,
        checkoutUrl: liveResult.data.checkout_url
      });
    }

    // 2. Fallback to verified Test Mode session
    console.log('Live mode not active yet, falling back to verified Test Mode session...');
    const testResult = await createCheckoutSession(
      'test.dodopayments.com',
      TEST_API_KEY,
      TEST_PRODUCT_ID,
      email,
      buyerName,
      returnUrl
    );

    if (testResult && testResult.statusCode >= 200 && testResult.statusCode < 300 && testResult.data.checkout_url) {
      return res.json({
        status: 'success',
        mode: 'test',
        sessionId: testResult.data.session_id,
        checkoutUrl: testResult.data.checkout_url
      });
    }

    // Fallback if both failed
    return res.status(400).json({
      status: 'failed',
      reason: testResult?.data?.message || 'Failed to create Dodo checkout session'
    });

  } catch (err) {
    console.error('Server error on Dodo initialize:', err);
    res.status(500).json({ status: 'failed', reason: err.message });
  }
};
