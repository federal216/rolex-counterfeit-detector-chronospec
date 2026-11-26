const crypto = require('crypto');
const https = require('https');

const USDT_TRC20_WALLET = 'TUzD8hJcCsdjPZaS1man4vLAufiqzYpKWi';
const USDC_ERC20_WALLET = '0x45824b71c98b4922723be312fa6fc8af6be0e090';
const USDT_TRC20_CONTRACT = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t';
const USDC_ERC20_CONTRACT = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48';

const DODO_LIVE_KEY = process.env.DODO_PAYMENTS_LIVE_KEY || 'dodo_live_xNuMmrRTOkHMLZY7.pEQXFVs-wu2XLVkeKX7xvdvcH9v71jbN6FdtMEyTPzCJLR0j';
const DODO_TEST_KEY = process.env.DODO_PAYMENTS_TEST_KEY || 'dodo_test_0_u-P96zqKPvQVU1.lwM9WJvPchJR4POMqkT0iVuHclz9ul4Jfbf8Jd_-JJZSuM4Q';

let customFetcher = null;

function setCustomFetcher(fn) {
  customFetcher = fn;
}

function getJsonHttps(urlStr, headers = {}) {
  if (customFetcher) {
    return customFetcher(urlStr, headers);
  }
  return new Promise((resolve, reject) => {
    const parsed = new URL(urlStr);
    const req = https.request({
      hostname: parsed.hostname,
      port: parsed.port || 443,
      path: `${parsed.pathname}${parsed.search}`,
      method: 'GET',
      headers: {
        'User-Agent': 'Federal216-Delivery-Verifier/1.0',
        Accept: 'application/json',
        ...headers
      }
    }, (res) => {
      let raw = '';
      res.on('data', chunk => { raw += chunk; });
      res.on('end', () => {
        let data = null;
        try { data = JSON.parse(raw || '{}'); } catch { data = { raw }; }
        resolve({ statusCode: res.statusCode, data });
      });
    });
    req.on('error', reject);
    req.end();
  });
}

function readRawRequestBody(req) {
  if (typeof req.rawBody === 'string') return Promise.resolve(req.rawBody);
  if (Buffer.isBuffer(req.rawBody)) return Promise.resolve(req.rawBody.toString('utf8'));
  if (typeof req.body === 'string') return Promise.resolve(req.body);
  if (req.body && typeof req.body === 'object' && Object.keys(req.body).length > 0) {
    return Promise.resolve(JSON.stringify(req.body));
  }
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => { raw += chunk; });
    req.on('end', () => resolve(raw));
    req.on('error', reject);
  });
}

function safeTimingEqual(a, b) {
  const bufA = Buffer.from(String(a));
  const bufB = Buffer.from(String(b));
  if (bufA.length !== bufB.length) return false;
  return crypto.timingSafeEqual(bufA, bufB);
}

function getHeaderCaseInsensitive(headers, name) {
  if (!headers || typeof headers !== 'object') return undefined;
  if (headers[name] !== undefined) return headers[name];
  const target = name.toLowerCase();
  for (const key of Object.keys(headers)) {
    if (key.toLowerCase() === target) return headers[key];
  }
  return undefined;
}

function verifyStandardWebhookHmac({ rawBody, webhookId, webhookTs, webhookSig, candidateKeys }) {
  if (!webhookId || !webhookTs || !webhookSig) {
    return { verified: false, reason: 'missing_signature_headers' };
  }
  const signedContent = `${webhookId}.${webhookTs}.${rawBody}`;
  const parts = String(webhookSig).split(/\s+/).filter(Boolean);
  for (const keyBytes of candidateKeys) {
    const expected = crypto.createHmac('sha256', keyBytes).update(signedContent).digest('base64');
    for (const part of parts) {
      const commaIdx = part.indexOf(',');
      const sig = commaIdx >= 0 ? part.slice(commaIdx + 1).trim() : part.trim();
      if (sig && safeTimingEqual(sig, expected)) {
        return { verified: true };
      }
    }
  }
  return { verified: false, reason: 'signature_mismatch' };
}

/**
 * Verifies Standard Webhooks signature used by Dodo Payments.
 */
function verifyDodoWebhookSignature({ rawBody, headers, secret }) {
  if (!secret) return { verified: false, reason: 'no_secret' };
  const webhookId = getHeaderCaseInsensitive(headers, 'webhook-id');
  const webhookTs = getHeaderCaseInsensitive(headers, 'webhook-timestamp');
  const webhookSig = getHeaderCaseInsensitive(headers, 'webhook-signature');
  const cleanSecret = secret.startsWith('whsec_') ? secret.slice(6) : secret;
  return verifyStandardWebhookHmac({
    rawBody,
    webhookId,
    webhookTs,
    webhookSig,
    candidateKeys: [Buffer.from(cleanSecret, 'base64')]
  });
}

/**
 * Verifies Whop webhook signature (`webhook-id`/`webhook-timestamp`/`webhook-signature` Standard Webhooks for `ws_` secrets, or legacy `x-whop-signature` / `whop-signature`).
 */
function verifyWhopWebhookSignature({ rawBody, headers, secret }) {
  if (!secret) return { verified: false, reason: 'no_secret' };
  const webhookId = getHeaderCaseInsensitive(headers, 'webhook-id');
  const webhookTs = getHeaderCaseInsensitive(headers, 'webhook-timestamp');
  const stdSig = getHeaderCaseInsensitive(headers, 'webhook-signature');

  if (webhookId && webhookTs && stdSig) {
    const candidateKeys = [Buffer.from(secret, 'utf8')];
    if (secret.startsWith('whsec_')) {
      candidateKeys.push(Buffer.from(secret.slice(6), 'base64'));
    }
    return verifyStandardWebhookHmac({
      rawBody,
      webhookId,
      webhookTs,
      webhookSig: stdSig,
      candidateKeys
    });
  }

  const sigHeader =
    getHeaderCaseInsensitive(headers, 'x-whop-signature') ||
    getHeaderCaseInsensitive(headers, 'whop-signature') ||
    stdSig;
  if (!sigHeader) return { verified: false, reason: 'missing_whop_signature' };

  const hexDigest = crypto.createHmac('sha256', secret).update(rawBody).digest('hex');
  const b64Digest = crypto.createHmac('sha256', secret).update(rawBody).digest('base64');

  const candidates = String(sigHeader)
    .split(/[,\s]+/)
    .map(s => s.replace(/^sha256=/i, '').replace(/^v1=/i, '').trim())
    .filter(Boolean);

  for (const cand of candidates) {
    if (safeTimingEqual(cand, hexDigest) || safeTimingEqual(cand, b64Digest)) {
      return { verified: true };
    }
  }
  return { verified: false, reason: 'signature_mismatch' };
}

async function verifyDodoPayment({ paymentId, sessionId }) {
  const hosts = [
    { host: 'live.dodopayments.com', key: DODO_LIVE_KEY, mode: 'live' },
    { host: 'test.dodopayments.com', key: DODO_TEST_KEY, mode: 'test' }
  ];

  for (const { host, key, mode } of hosts) {
    if (!key) continue;
    if (paymentId) {
      try {
        const res = await getJsonHttps(`https://${host}/payments/${encodeURIComponent(paymentId)}`, {
          Authorization: `Bearer ${key}`
        });
        if (res.statusCode >= 200 && res.statusCode < 300 && res.data) {
          const st = String(res.data.status || '').toLowerCase();
          if (st === 'succeeded' || st === 'paid' || st === 'completed') {
            return {
              verified: true,
              mode,
              transactionId: res.data.payment_id || paymentId,
              customerEmail: res.data.customer?.email || null,
              buyerName: res.data.customer?.name || null,
              productId: res.data.product_cart?.[0]?.product_id || null,
              metadata: res.data.metadata || {},
              totalAmountCents: res.data.total_amount ?? null,
              amountLabel: res.data.total_amount
                ? `${(Number(res.data.total_amount) / 100).toFixed(2)} ${res.data.currency || 'USD'}`
                : null
            };
          }
        }
      } catch {
        // Try next mode
      }
    }

    if (sessionId) {
      try {
        const res = await getJsonHttps(`https://${host}/checkouts/${encodeURIComponent(sessionId)}`, {
          Authorization: `Bearer ${key}`
        });
        if (res.statusCode >= 200 && res.statusCode < 300 && res.data) {
          const payStatus = String(res.data.payment_status || res.data.status || '').toLowerCase();
          if (res.data.payment_id) {
            const nested = await verifyDodoPayment({ paymentId: res.data.payment_id });
            if (nested.verified) return nested;
          }
          if (payStatus === 'succeeded' || payStatus === 'paid' || payStatus === 'completed') {
            return {
              verified: true,
              mode,
              transactionId: res.data.payment_id || res.data.session_id || sessionId,
              customerEmail: res.data.customer_email || res.data.customer?.email || null,
              buyerName: res.data.customer_name || res.data.customer?.name || null,
              productId: res.data.product_cart?.[0]?.product_id || null,
              metadata: res.data.metadata || {}
            };
          }
        }
      } catch {
        // Try next mode
      }
    }
  }

  return { verified: false, reason: 'Dodo payment not found or not succeeded.' };
}

async function verifyWhopPayment({ paymentId, membershipId }) {
  const apiKey = process.env.WHOP_API_KEY;
  if (!apiKey) {
    return { verified: false, reason: 'WHOP_API_KEY not configured on server; Whop webhook handles automatic delivery.' };
  }
  const targetId = paymentId || membershipId;
  if (!targetId) return { verified: false, reason: 'Missing Whop payment/membership ID.' };

  const endpoints = paymentId
    ? [`https://api.whop.com/api/v5/company/payments/${encodeURIComponent(paymentId)}`]
    : [`https://api.whop.com/api/v5/company/memberships/${encodeURIComponent(membershipId)}`];

  for (const url of endpoints) {
    try {
      const res = await getJsonHttps(url, { Authorization: `Bearer ${apiKey}` });
      if (res.statusCode >= 200 && res.statusCode < 300 && res.data) {
        const valid = Boolean(res.data.valid) || ['paid', 'succeeded', 'active', 'completed'].includes(
          String(res.data.status || res.data.substatus || '').toLowerCase()
        );
        if (valid) {
          return {
            verified: true,
            transactionId: res.data.id || targetId,
            customerEmail: res.data.user?.email || res.data.email || null,
            buyerName: res.data.user?.name || res.data.user?.username || null,
            planId: res.data.plan_id || res.data.plan?.id || null
          };
        }
      }
    } catch {
      // ignore
    }
  }

  return { verified: false, reason: 'Whop payment/membership not verified.' };
}

async function verifyCryptoTransaction({ network, txHash, minUsd = 70 }) {
  const cleanHash = String(txHash || '').trim();
  if (!/^(0x)?[a-fA-F0-9]{16,128}$/.test(cleanHash)) {
    return { verified: false, reason: 'Invalid blockchain transaction hash format.' };
  }

  const net = String(network || '').toLowerCase();
  const isUsdc = net.includes('usdc') || net.includes('erc20') || cleanHash.startsWith('0x');

  if (!isUsdc) {
    // USDT TRC20 verification via TronGrid
    const accUrl = `https://api.trongrid.io/v1/accounts/${USDT_TRC20_WALLET}/transactions/trc20?limit=40&contract_address=${USDT_TRC20_CONTRACT}&only_to=true&order_by=block_timestamp,desc`;
    const res = await getJsonHttps(accUrl);
    const list = res?.data?.data || [];
    const match = list.find(tx =>
      String(tx.transaction_id || '').toLowerCase() === cleanHash.toLowerCase() &&
      String(tx.to || '').toLowerCase() === USDT_TRC20_WALLET.toLowerCase()
    );
    if (match) {
      const amount = parseInt(match.value, 10) / 1e6;
      if (amount >= minUsd - 0.5) {
        return {
          verified: true,
          network: 'USDT TRC20',
          transactionId: match.transaction_id,
          amountLabel: `${amount.toFixed(2)} USDT (TRC20)`
        };
      }
      return { verified: false, reason: `USDT amount (${amount.toFixed(2)}) is below required $${minUsd}.` };
    }

    // Fallback: direct transaction events lookup
    const txUrl = `https://api.trongrid.io/v1/transactions/${encodeURIComponent(cleanHash)}/events`;
    const evRes = await getJsonHttps(txUrl);
    const events = evRes?.data?.data || [];
    for (const ev of events) {
      if (
        String(ev.contract_address || '').toLowerCase() === USDT_TRC20_CONTRACT.toLowerCase() &&
        ev.event_name === 'Transfer' &&
        String(ev.result?.to || '').toLowerCase() === USDT_TRC20_WALLET.toLowerCase()
      ) {
        const amount = parseInt(ev.result.value, 10) / 1e6;
        if (amount >= minUsd - 0.5) {
          return {
            verified: true,
            network: 'USDT TRC20',
            transactionId: cleanHash,
            amountLabel: `${amount.toFixed(2)} USDT (TRC20)`
          };
        }
      }
    }
    return { verified: false, reason: 'TRC20 USDT transaction not found on-chain for our receiving wallet.' };
  }

  // USDC ERC20 verification via Blockscout
  const txTransfersUrl = `https://eth.blockscout.com/api/v2/transactions/${encodeURIComponent(cleanHash)}/token-transfers`;
  const res = await getJsonHttps(txTransfersUrl);
  const items = res?.data?.items || [];
  for (const item of items) {
    const isUsdcToken = String(item.token?.address_hash || '').toLowerCase() === USDC_ERC20_CONTRACT.toLowerCase();
    const isOurWallet = String(item.to?.hash || '').toLowerCase() === USDC_ERC20_WALLET.toLowerCase();
    if (isUsdcToken && isOurWallet && item.total) {
      const decimals = parseInt(item.total.decimals || '6', 10);
      const amount = parseFloat(item.total.value) / Math.pow(10, decimals);
      if (amount >= minUsd - 0.5) {
        return {
          verified: true,
          network: 'USDC ERC20',
          transactionId: cleanHash,
          amountLabel: `${amount.toFixed(2)} USDC (ERC20)`
        };
      }
      return { verified: false, reason: `USDC amount (${amount.toFixed(2)}) is below required $${minUsd}.` };
    }
  }

  return { verified: false, reason: 'ERC20 USDC transaction not found on-chain for our receiving wallet.' };
}

async function verifyDeliveryProof({ paymentMethod, paymentId, sessionId, transactionId, network, testToken, product }) {
  if (testToken && process.env.DELIVERY_TEST_TOKEN && safeTimingEqual(testToken, process.env.DELIVERY_TEST_TOKEN)) {
    return {
      verified: true,
      transactionId: transactionId || `TEST-${Date.now()}`,
      amountLabel: `$${product.priceUsd.toFixed(2)} USD (Test)`
    };
  }

  const method = String(paymentMethod || '').toLowerCase();
  if (method === 'dodo') {
    return verifyDodoPayment({ paymentId: paymentId || transactionId, sessionId });
  }
  if (method === 'crypto') {
    return verifyCryptoTransaction({
      network: network || 'usdt',
      txHash: transactionId,
      minUsd: product.priceUsd
    });
  }
  if (method === 'whop') {
    return verifyWhopPayment({ paymentId: paymentId || transactionId, membershipId: sessionId });
  }

  return { verified: false, reason: 'Unsupported or unverified payment method.' };
}

module.exports = {
  USDT_TRC20_WALLET,
  USDC_ERC20_WALLET,
  USDT_TRC20_CONTRACT,
  USDC_ERC20_CONTRACT,
  setCustomFetcher,
  readRawRequestBody,
  verifyDodoWebhookSignature,
  verifyWhopWebhookSignature,
  verifyDodoPayment,
  verifyWhopPayment,
  verifyCryptoTransaction,
  verifyDeliveryProof
};
