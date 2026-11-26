const { test, describe, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const { OWNER_EMAIL, PRODUCTS, resolveProduct } = require('../lib/products');
const {
  resolvePdfBuffer,
  sendPurchaseDossierEmails,
  setCustomTransport,
  clearOrderStateForTest
} = require('../lib/mailer');
const {
  USDT_TRC20_WALLET,
  USDC_ERC20_WALLET,
  USDT_TRC20_CONTRACT,
  USDC_ERC20_CONTRACT,
  setCustomFetcher
} = require('../lib/verifier');

function detectRepoProductKey() {
  const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'package.json'), 'utf8'));
  if (pkg.name.includes('cabinet')) return 'cabinetscan';
  if (pkg.name.includes('chrono')) return 'chronospec';
  return 'lambospec';
}

const DEFAULT_KEY = detectRepoProductKey();
const app = require('../server');

function httpRequest(server, method, urlPath, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const addr = server.address();
    const rawBody = typeof body === 'string' ? body : (body ? JSON.stringify(body) : '');
    const req = http.request({
      hostname: '127.0.0.1',
      port: addr.port,
      path: urlPath,
      method,
      headers: {
        ...(rawBody ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(rawBody) } : {}),
        ...headers
      }
    }, (res) => {
      let data = '';
      res.on('data', c => { data += c; });
      res.on('end', () => {
        let json = null;
        try { json = JSON.parse(data); } catch { json = data; }
        resolve({ status: res.statusCode, body: json });
      });
    });
    req.on('error', reject);
    if (rawBody) req.write(rawBody);
    req.end();
  });
}

describe(`${DEFAULT_KEY} PDF email delivery & verification`, () => {
  let server;
  let sentEmails = [];

  beforeEach(async () => {
    sentEmails = [];
    clearOrderStateForTest();
    setCustomTransport(async (msg) => {
      sentEmails.push(msg);
      return { provider: 'mock', messageId: `msg_${sentEmails.length}` };
    });
    setCustomFetcher(null);
    delete process.env.DODO_WEBHOOK_SECRET;
    delete process.env.WHOP_WEBHOOK_SECRET;
    delete process.env.WHOP_API_KEY;
    delete process.env.DELIVERY_TEST_TOKEN;

    await new Promise(resolve => {
      server = app.listen(0, '127.0.0.1', resolve);
    });
  });

  afterEach(async () => {
    setCustomTransport(null);
    setCustomFetcher(null);
    if (server) {
      await new Promise(resolve => server.close(resolve));
    }
  });

  test('resolves product catalog and owner email correctly', () => {
    assert.equal(OWNER_EMAIL, 'karakoc.i@gmail.com');
    const prod = resolveProduct({ defaultKey: DEFAULT_KEY });
    assert.equal(prod.productKey, DEFAULT_KEY);
    const { buffer } = resolvePdfBuffer({ product: prod });
    assert.equal(buffer.subarray(0, 4).toString('ascii'), '%PDF');
    assert.ok(buffer.length > 10000, 'Expected real 10-page PDF > 10KB');
  });

  test('rejects invalid custom pdfBase64 and accepts valid %PDF base64', () => {
    const prod = PRODUCTS[DEFAULT_KEY];
    assert.throws(() => resolvePdfBuffer({
      product: prod,
      pdfBase64: Buffer.from('not-a-pdf').toString('base64')
    }));

    const fakePdf = Buffer.from('%PDF-1.4\n' + '0'.repeat(200) + '\n%%EOF');
    const res = resolvePdfBuffer({
      product: prod,
      pdfBase64: `data:application/pdf;base64,${fakePdf.toString('base64')}`,
      filename: 'Custom Test.pdf'
    });
    assert.equal(res.source, 'client_generated');
    assert.equal(res.filename, 'Custom_Test.pdf');
  });

  test('sends PDF to both customer and karakoc.i@gmail.com with idempotency and partial-retry recovery', async () => {
    let failFirstCustomer = true;
    setCustomTransport(async (msg) => {
      if (failFirstCustomer && msg.to === 'buyer@example.com') {
        failFirstCustomer = false;
        throw new Error('Transient customer SMTP error');
      }
      sentEmails.push(msg);
      return { provider: 'mock', messageId: `ok_${sentEmails.length}` };
    });

    const first = await sendPurchaseDossierEmails({
      product: PRODUCTS[DEFAULT_KEY],
      customerEmail: 'buyer@example.com',
      buyerName: 'Test Buyer',
      paymentMethod: 'dodo',
      transactionId: 'TXN_RETRY_1'
    });
    assert.equal(first.customerSent, false);
    assert.equal(first.ownerSent, true);
    assert.equal(sentEmails.length, 1);
    assert.equal(sentEmails[0].to, 'karakoc.i@gmail.com');

    // Retry should send ONLY to customer, without duplicating owner email
    const second = await sendPurchaseDossierEmails({
      product: PRODUCTS[DEFAULT_KEY],
      customerEmail: 'buyer@example.com',
      buyerName: 'Test Buyer',
      paymentMethod: 'dodo',
      transactionId: 'TXN_RETRY_1'
    });
    assert.equal(second.ok, true);
    assert.equal(second.customerSent, true);
    assert.equal(second.ownerSent, true);
    assert.equal(sentEmails.length, 2);
    assert.equal(sentEmails[1].to, 'buyer@example.com');
    assert.equal(sentEmails[1].pdfBuffer.subarray(0, 4).toString('ascii'), '%PDF');

    // Third call is fully deduplicated
    const third = await sendPurchaseDossierEmails({
      product: PRODUCTS[DEFAULT_KEY],
      customerEmail: 'buyer@example.com',
      paymentMethod: 'dodo',
      transactionId: 'TXN_RETRY_1'
    });
    assert.equal(third.deduplicated, true);
    assert.equal(sentEmails.length, 2);
  });

  test('GET /api/status reports online and karakoc.i@gmail.com', async () => {
    const res = await httpRequest(server, 'GET', '/api/status');
    assert.equal(res.status, 200);
    assert.equal(res.body.status, 'online');
    assert.equal(res.body.ownerEmail, 'karakoc.i@gmail.com');
  });

  test('POST /api/deliver-pdf rejects unverified payments', async () => {
    const res = await httpRequest(server, 'POST', '/api/deliver-pdf', {
      productKey: DEFAULT_KEY,
      customerEmail: 'buyer@example.com',
      paymentMethod: 'crypto',
      transactionId: 'deadbeef12345678'
    });
    assert.equal(res.status, 402);
    assert.equal(sentEmails.length, 0);
  });

  test('POST /api/deliver-pdf delivers Dodo verified purchase to customer + owner', async () => {
    setCustomFetcher(async (url) => {
      if (url.includes('/payments/pay_dodo_ok')) {
        return {
          statusCode: 200,
          data: {
            payment_id: 'pay_dodo_ok',
            status: 'succeeded',
            total_amount: Math.round(PRODUCTS[DEFAULT_KEY].priceUsd * 100),
            currency: 'USD',
            customer: { email: 'dodo.buyer@example.com', name: 'Dodo Buyer' },
            metadata: { app: DEFAULT_KEY }
          }
        };
      }
      return { statusCode: 404, data: {} };
    });

    const res = await httpRequest(server, 'POST', '/api/deliver-pdf', {
      productKey: DEFAULT_KEY,
      paymentMethod: 'dodo',
      paymentId: 'pay_dodo_ok'
    });

    assert.equal(res.status, 200);
    assert.equal(res.body.ok, true);
    assert.equal(res.body.customerSent, true);
    assert.equal(res.body.ownerSent, true);
    assert.deepEqual(sentEmails.map(e => e.to).sort(), ['dodo.buyer@example.com', 'karakoc.i@gmail.com']);
    assert.equal(sentEmails[0].pdfBuffer.subarray(0, 4).toString('ascii'), '%PDF');
    assert.equal(sentEmails[1].pdfBuffer.subarray(0, 4).toString('ascii'), '%PDF');
  });

  test('POST /api/deliver-pdf verifies USDT TRC20 on TronGrid and emails both recipients', async () => {
    const txHash = 'a'.repeat(64);
    setCustomFetcher(async (url) => {
      if (url.includes('api.trongrid.io/v1/accounts/')) {
        return {
          statusCode: 200,
          data: {
            data: [{
              transaction_id: txHash,
              to: USDT_TRC20_WALLET,
              contract_address: USDT_TRC20_CONTRACT,
              value: String(Math.round(PRODUCTS[DEFAULT_KEY].priceUsd * 1e6))
            }]
          }
        };
      }
      return { statusCode: 200, data: { data: [] } };
    });

    const res = await httpRequest(server, 'POST', '/api/deliver-pdf', {
      productKey: DEFAULT_KEY,
      customerEmail: 'crypto.buyer@example.com',
      paymentMethod: 'crypto',
      network: 'usdt',
      transactionId: txHash
    });

    assert.equal(res.status, 200);
    assert.equal(res.body.ok, true);
    assert.deepEqual(sentEmails.map(e => e.to).sort(), ['crypto.buyer@example.com', 'karakoc.i@gmail.com']);
  });

  test('POST /api/deliver-pdf verifies USDC ERC20 on Blockscout and emails both recipients', async () => {
    const txHash = '0x' + 'b'.repeat(64);
    setCustomFetcher(async (url) => {
      if (url.includes('eth.blockscout.com/api/v2/transactions/')) {
        return {
          statusCode: 200,
          data: {
            items: [{
              transaction_hash: txHash,
              token: { address_hash: USDC_ERC20_CONTRACT },
              to: { hash: USDC_ERC20_WALLET },
              total: { decimals: '6', value: String(Math.round(PRODUCTS[DEFAULT_KEY].priceUsd * 1e6)) }
            }]
          }
        };
      }
      return { statusCode: 404, data: {} };
    });

    const res = await httpRequest(server, 'POST', '/api/deliver-pdf', {
      productKey: DEFAULT_KEY,
      customerEmail: 'usdc.buyer@example.com',
      paymentMethod: 'crypto',
      network: 'usdc',
      transactionId: txHash
    });

    assert.equal(res.status, 200);
    assert.equal(res.body.ok, true);
    assert.deepEqual(sentEmails.map(e => e.to).sort(), ['karakoc.i@gmail.com', 'usdc.buyer@example.com']);
  });

  test('POST /api/webhooks/dodo verifies Standard Webhooks signature and delivers PDF to both', async () => {
    const rawSecret = Buffer.from('test-dodo-webhook-secret-key').toString('base64');
    process.env.DODO_WEBHOOK_SECRET = `whsec_${rawSecret}`;

    const payload = JSON.stringify({
      type: 'payment.succeeded',
      data: {
        payment_id: 'pay_wh_dodo_1',
        status: 'succeeded',
        total_amount: Math.round(PRODUCTS[DEFAULT_KEY].priceUsd * 100),
        currency: 'USD',
        customer: { email: 'dodo.webhook@example.com', name: 'Webhook Customer' },
        metadata: { app: DEFAULT_KEY }
      }
    });

    const whId = 'msg_12345';
    const whTs = String(Math.floor(Date.now() / 1000));
    const sig = crypto
      .createHmac('sha256', Buffer.from(rawSecret, 'base64'))
      .update(`${whId}.${whTs}.${payload}`)
      .digest('base64');

    const badRes = await httpRequest(server, 'POST', '/api/webhooks/dodo', payload, {
      'webhook-id': whId,
      'webhook-timestamp': whTs,
      'webhook-signature': 'v1,invalid'
    });
    assert.equal(badRes.status, 401);

    const okRes = await httpRequest(server, 'POST', '/api/webhooks/dodo', payload, {
      'webhook-id': whId,
      'webhook-timestamp': whTs,
      'webhook-signature': `v1,${sig}`
    });
    assert.equal(okRes.status, 200);
    assert.equal(okRes.body.ok, true);
    assert.deepEqual(sentEmails.map(e => e.to).sort(), ['dodo.webhook@example.com', 'karakoc.i@gmail.com']);
  });

  test('POST /api/webhooks/whop verifies HMAC signature and delivers PDF to both', async () => {
    const secret = 'test-whop-secret';
    process.env.WHOP_WEBHOOK_SECRET = secret;

    const payload = JSON.stringify({
      action: 'payment.succeeded',
      data: {
        id: 'pay_whop_999',
        final_amount: PRODUCTS[DEFAULT_KEY].priceUsd,
        currency: 'usd',
        user: { email: 'whop.buyer@example.com', name: 'Whop VIP' }
      }
    });

    const sig = crypto.createHmac('sha256', secret).update(payload).digest('hex');

    const badRes = await httpRequest(server, 'POST', '/api/webhooks/whop', payload, {
      'x-whop-signature': 'wrong_sig'
    });
    assert.equal(badRes.status, 401);

    const okRes = await httpRequest(server, 'POST', '/api/webhooks/whop', payload, {
      'x-whop-signature': sig
    });
    assert.equal(okRes.status, 200);
    assert.equal(okRes.body.ok, true);
    assert.deepEqual(sentEmails.map(e => e.to).sort(), ['karakoc.i@gmail.com', 'whop.buyer@example.com']);
  });

  test('HTML index.html inline scripts compile cleanly and contain delivery hooks', () => {
    const htmlPath = path.join(__dirname, '..', 'index.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    assert.ok(html.includes('/api/deliver-pdf'), 'index.html must call /api/deliver-pdf');
    assert.ok(html.includes('karakoc.i@gmail.com'), 'index.html must reference owner email');

    const scriptRegex = /<script(?![^>]*type="application\/ld\+json")(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
    let match;
    let count = 0;
    while ((match = scriptRegex.exec(html)) !== null) {
      count++;
      new vm.Script(match[1], { filename: `index.html#script-${count}` });
    }
    assert.ok(count > 0, 'Expected at least one inline script block');
  });
});
