const fs = require('fs');
const path = require('path');
const https = require('https');
const nodemailer = require('nodemailer');
const { OWNER_EMAIL, PRODUCTS } = require('./products');

const MAX_PDF_BYTES = 12 * 1024 * 1024;
const DEDUPE_FILE = path.join('/tmp', 'federal216_email_dedupe.json');
const sentOrderState = new Map();

let customTransport = null;

function setCustomTransport(fn) {
  customTransport = fn;
}

function isValidEmail(email) {
  if (!email || typeof email !== 'string') return false;
  const trimmed = email.trim();
  return /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(trimmed) && trimmed.length <= 254;
}

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function sanitizeFilename(filename, fallback) {
  const base = (filename || fallback || 'Dossier.pdf').replace(/[^a-zA-Z0-9._-]/g, '_');
  return base.toLowerCase().endsWith('.pdf') ? base : `${base}.pdf`;
}

function resolvePdfBuffer({ product, pdfBase64, filename }) {
  const safeName = sanitizeFilename(filename, product.defaultFilename);

  if (pdfBase64 && typeof pdfBase64 === 'string') {
    const clean = pdfBase64.replace(/^data:application\/pdf[^,]*;base64,/i, '').trim();
    if (clean.length > 0) {
      const buf = Buffer.from(clean, 'base64');
      if (buf.length > MAX_PDF_BYTES) {
        throw new Error(`PDF payload exceeds ${MAX_PDF_BYTES} bytes limit.`);
      }
      if (buf.length < 100 || buf.subarray(0, 4).toString('ascii') !== '%PDF') {
        throw new Error('Provided pdfBase64 is not a valid PDF document.');
      }
      return { buffer: buf, filename: safeName, source: 'client_generated' };
    }
  }

  const candidates = [
    path.resolve(__dirname, '..', product.pdfRelPath),
    path.resolve(process.cwd(), product.pdfRelPath)
  ];

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      const buf = fs.readFileSync(candidate);
      return { buffer: buf, filename: safeName, source: 'official_master_pdf' };
    }
  }

  throw new Error(`Official PDF file not found for ${product.productKey} (${product.pdfRelPath}).`);
}

function getConfiguredProvider() {
  if (customTransport) return 'custom';
  const forced = (process.env.EMAIL_PROVIDER || '').trim().toLowerCase();
  if (forced) return forced;

  const hasResend = Boolean(process.env.RESEND_API_KEY);
  const hasSmtp = Boolean(process.env.GMAIL_APP_PASSWORD || process.env.SMTP_PASS);
  const hasGas = Boolean(process.env.GAS_MAILER_URL);

  // Prefer Resend when a custom verified domain sender is explicitly configured
  if (hasResend && process.env.RESEND_FROM) return 'resend';
  // Prefer SMTP (e.g., Gmail App Password) because it delivers directly to any customer email without domain DNS setup
  if (hasSmtp) return 'smtp';
  if (hasResend) return 'resend';
  if (hasGas) return 'gas';
  return null;
}

function postJsonHttps(targetUrl, headers, payloadObj) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(targetUrl);
    const body = JSON.stringify(payloadObj);

    const req = https.request({
      hostname: parsed.hostname,
      port: parsed.port || 443,
      path: `${parsed.pathname}${parsed.search}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        ...headers
      }
    }, (res) => {
      let raw = '';
      res.on('data', chunk => { raw += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(raw || '{}'));
          } catch {
            resolve({ raw });
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${raw.slice(0, 400)}`));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function dispatchSingleEmail({ to, subject, html, text, filename, pdfBuffer, replyTo, brandName }) {
  const provider = getConfiguredProvider();
  if (!provider) {
    throw new Error(
      'Email transport is not configured. Set GMAIL_APP_PASSWORD (or SMTP_PASS + SMTP_USER) or RESEND_API_KEY in environment variables.'
    );
  }

  if (provider === 'custom' && customTransport) {
    return customTransport({ to, subject, html, text, filename, pdfBuffer, replyTo, brandName });
  }

  if (provider === 'smtp') {
    const host = process.env.SMTP_HOST || 'smtp.gmail.com';
    const port = parseInt(process.env.SMTP_PORT || '465', 10);
    const secure = process.env.SMTP_SECURE ? process.env.SMTP_SECURE === 'true' : port === 465;
    const user = (process.env.SMTP_USER || OWNER_EMAIL).trim();
    const pass = (process.env.GMAIL_APP_PASSWORD || process.env.SMTP_PASS || '').replace(/\s+/g, '');
    const fromAddr = process.env.EMAIL_FROM || `${brandName} <${user}>`;

    const transporter = nodemailer.createTransport({
      host,
      port,
      secure,
      auth: { user, pass }
    });

    const info = await transporter.sendMail({
      from: fromAddr,
      to,
      replyTo: replyTo || OWNER_EMAIL,
      subject,
      text,
      html,
      attachments: [
        {
          filename,
          content: pdfBuffer,
          contentType: 'application/pdf'
        }
      ]
    });

    return { provider: 'smtp', messageId: info.messageId };
  }

  if (provider === 'resend') {
    const apiKey = process.env.RESEND_API_KEY;
    const fromAddr = process.env.RESEND_FROM || process.env.EMAIL_FROM || `${brandName} <onboarding@resend.dev>`;

    const result = await postJsonHttps(
      'https://api.resend.com/emails',
      { Authorization: `Bearer ${apiKey}` },
      {
        from: fromAddr,
        to: [to],
        reply_to: replyTo || OWNER_EMAIL,
        subject,
        html,
        text,
        attachments: [
          {
            filename,
            content: pdfBuffer.toString('base64')
          }
        ]
      }
    );

    return { provider: 'resend', messageId: result.id };
  }

  if (provider === 'gas') {
    const gasUrl = process.env.GAS_MAILER_URL;
    const result = await postJsonHttps(
      gasUrl,
      {},
      {
        secret: process.env.GAS_MAILER_SECRET || '',
        to,
        replyTo: replyTo || OWNER_EMAIL,
        subject,
        html,
        text,
        filename,
        pdfBase64: pdfBuffer.toString('base64')
      }
    );
    return { provider: 'gas', result };
  }

  throw new Error(`Unsupported EMAIL_PROVIDER: ${provider}`);
}

function buildCustomerEmail({ product, buyerName, paymentMethod, transactionId, amountLabel, summaryText }) {
  const safeBrand = escapeHtml(product.brandName);
  const safeName = escapeHtml(buyerName || 'Valued Client');
  const safeTx = escapeHtml(transactionId || 'VERIFIED');
  const safeMethod = escapeHtml((paymentMethod || 'Online Checkout').toUpperCase());
  const safeAmount = escapeHtml(amountLabel || `$${product.priceUsd.toFixed(2)} USD`);
  const safeSummary = summaryText ? `<p style="margin:12px 0;padding:12px;background:#f8fafc;border-left:4px solid ${product.accentHex};color:#334155;font-size:13px;">${escapeHtml(summaryText)}</p>` : '';

  const subject = `${product.brandName} — Your Official 10-Page PDF Dossier (Ref: ${transactionId || 'CONFIRMED'})`;

  const html = `
    <div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;margin:0 auto;background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;">
      <div style="background:#0f172a;padding:24px;border-bottom:4px solid ${product.accentHex};">
        <div style="color:${product.accentHex};font-size:11px;font-weight:bold;letter-spacing:1.5px;text-transform:uppercase;">Official Digital Delivery</div>
        <h1 style="color:#ffffff;margin:6px 0 0;font-size:22px;">${safeBrand}</h1>
      </div>
      <div style="padding:24px;color:#1e293b;line-height:1.6;font-size:14px;">
        <p>Hello <strong>${safeName}</strong>,</p>
        <p>Thank you for your purchase! Your official <strong>${escapeHtml(product.dossierTitle)}</strong> is attached directly to this email as a PDF file.</p>
        ${safeSummary}
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:16px;margin:18px 0;font-size:13px;">
          <div><strong>Product:</strong> ${escapeHtml(product.dossierTitle)}</div>
          <div><strong>Amount Paid:</strong> ${safeAmount}</div>
          <div><strong>Payment Method:</strong> ${safeMethod}</div>
          <div><strong>Transaction Reference:</strong> <code>${safeTx}</code></div>
        </div>
        <p>You can download and save the attached PDF immediately. For concierge support or questions, reply to this email or contact <a href="mailto:${escapeHtml(product.supportEmail)}">${escapeHtml(product.supportEmail)}</a> or <a href="mailto:${escapeHtml(OWNER_EMAIL)}">${escapeHtml(OWNER_EMAIL)}</a>.</p>
        <p style="margin-top:24px;font-size:12px;color:#64748b;">&copy; 2026 ${safeBrand} · <a href="${escapeHtml(product.liveUrl)}">${escapeHtml(product.liveUrl)}</a></p>
      </div>
    </div>
  `;

  const text = [
    `${product.brandName} — Official PDF Dossier Delivery`,
    '',
    `Hello ${buyerName || 'Valued Client'},`,
    `Thank you for your purchase! Your ${product.dossierTitle} is attached to this email as a PDF.`,
    summaryText ? `\nDetails: ${summaryText}` : '',
    '',
    `Product: ${product.dossierTitle}`,
    `Amount Paid: ${amountLabel || `$${product.priceUsd.toFixed(2)} USD`}`,
    `Payment Method: ${(paymentMethod || 'Online Checkout').toUpperCase()}`,
    `Transaction Reference: ${transactionId || 'VERIFIED'}`,
    '',
    `Support: ${product.supportEmail} | ${OWNER_EMAIL}`,
    `Portal: ${product.liveUrl}`
  ].filter(Boolean).join('\n');

  return { subject, html, text };
}

function buildOwnerEmail({ product, customerEmail, buyerName, paymentMethod, transactionId, amountLabel, summaryText }) {
  const safeBrand = escapeHtml(product.brandName);
  const safeCustEmail = escapeHtml(customerEmail || 'Not provided');
  const safeName = escapeHtml(buyerName || 'VIP Client');
  const safeTx = escapeHtml(transactionId || 'VERIFIED');
  const safeMethod = escapeHtml((paymentMethod || 'Online Checkout').toUpperCase());
  const safeAmount = escapeHtml(amountLabel || `$${product.priceUsd.toFixed(2)} USD`);
  const timestamp = new Date().toISOString();

  const subject = `[${product.brandName}] YENİ SATIN ALIM (${amountLabel || `$${product.priceUsd.toFixed(2)}`}) — ${customerEmail || 'Müşteri'} | Ref: ${transactionId || 'OK'}`;

  const html = `
    <div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;margin:0 auto;background:#ffffff;border:1px solid #cbd5e1;border-radius:12px;overflow:hidden;">
      <div style="background:#064e3b;padding:20px;border-bottom:4px solid ${product.accentHex};">
        <div style="color:#a7f3d0;font-size:11px;font-weight:bold;letter-spacing:1.5px;text-transform:uppercase;">Satış Bildirimi & PDF Arşiv Kopyası</div>
        <h2 style="color:#ffffff;margin:6px 0 0;font-size:20px;">${safeBrand} — Yeni Satın Alım</h2>
      </div>
      <div style="padding:22px;color:#0f172a;font-size:14px;line-height:1.6;">
        <p>Merhaba İbrahim, <strong>${safeBrand}</strong> üzerinden yeni bir satın alım gerçekleşti. Müşteriye iletilen PDF dosyası ekte senin için de gönderildi.</p>
        <table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:13px;">
          <tr><td style="padding:8px;border:1px solid #e2e8f0;background:#f8fafc;"><strong>Ürün</strong></td><td style="padding:8px;border:1px solid #e2e8f0;">${escapeHtml(product.dossierTitle)}</td></tr>
          <tr><td style="padding:8px;border:1px solid #e2e8f0;background:#f8fafc;"><strong>Müşteri E-posta</strong></td><td style="padding:8px;border:1px solid #e2e8f0;">${safeCustEmail}</td></tr>
          <tr><td style="padding:8px;border:1px solid #e2e8f0;background:#f8fafc;"><strong>Müşteri Adı</strong></td><td style="padding:8px;border:1px solid #e2e8f0;">${safeName}</td></tr>
          <tr><td style="padding:8px;border:1px solid #e2e8f0;background:#f8fafc;"><strong>Ödeme Yöntemi</strong></td><td style="padding:8px;border:1px solid #e2e8f0;">${safeMethod}</td></tr>
          <tr><td style="padding:8px;border:1px solid #e2e8f0;background:#f8fafc;"><strong>Tutar</strong></td><td style="padding:8px;border:1px solid #e2e8f0;">${safeAmount}</td></tr>
          <tr><td style="padding:8px;border:1px solid #e2e8f0;background:#f8fafc;"><strong>İşlem / TxID</strong></td><td style="padding:8px;border:1px solid #e2e8f0;"><code>${safeTx}</code></td></tr>
          <tr><td style="padding:8px;border:1px solid #e2e8f0;background:#f8fafc;"><strong>Tarih (UTC)</strong></td><td style="padding:8px;border:1px solid #e2e8f0;">${timestamp}</td></tr>
        </table>
        ${summaryText ? `<p style="padding:10px;background:#f1f5f9;border-radius:6px;font-size:12px;"><strong>Sipariş Detayı:</strong> ${escapeHtml(summaryText)}</p>` : ''}
      </div>
    </div>
  `;

  const text = [
    `[${product.brandName}] YENI SATIN ALIM`,
    `Urun: ${product.dossierTitle}`,
    `Musteri E-posta: ${customerEmail || 'Belirtilmedi'}`,
    `Musteri Adi: ${buyerName || 'VIP Client'}`,
    `Odeme Yontemi: ${(paymentMethod || 'Online Checkout').toUpperCase()}`,
    `Tutar: ${amountLabel || `$${product.priceUsd.toFixed(2)} USD`}`,
    `Islem Ref / TxID: ${transactionId || 'VERIFIED'}`,
    `Tarih (UTC): ${timestamp}`,
    summaryText ? `Detay: ${summaryText}` : '',
    '',
    'Musteriye gonderilen PDF dosyasi bu e-postaya da eklenmistir.'
  ].filter(Boolean).join('\n');

  return { subject, html, text };
}

function loadOrderState(key) {
  if (sentOrderState.has(key)) return sentOrderState.get(key);
  try {
    if (fs.existsSync(DEDUPE_FILE)) {
      const parsed = JSON.parse(fs.readFileSync(DEDUPE_FILE, 'utf8') || '{}');
      if (parsed[key]) {
        sentOrderState.set(key, parsed[key]);
        return parsed[key];
      }
    }
  } catch {
    // Non-fatal in read-only or ephemeral environments
  }
  return null;
}

function saveOrderState(key, state) {
  sentOrderState.set(key, state);
  try {
    let existing = {};
    if (fs.existsSync(DEDUPE_FILE)) {
      existing = JSON.parse(fs.readFileSync(DEDUPE_FILE, 'utf8') || '{}');
    }
    existing[key] = state;
    // Keep file bounded to last 500 transactions
    const keys = Object.keys(existing);
    if (keys.length > 500) {
      for (const oldKey of keys.slice(0, keys.length - 500)) {
        delete existing[oldKey];
      }
    }
    fs.writeFileSync(DEDUPE_FILE, JSON.stringify(existing));
  } catch {
    // Non-fatal
  }
}

function clearOrderStateForTest() {
  sentOrderState.clear();
  try {
    if (fs.existsSync(DEDUPE_FILE)) fs.unlinkSync(DEDUPE_FILE);
  } catch {
    // ignore
  }
}

async function sendPurchaseDossierEmails({
  product,
  productKey,
  customerEmail,
  buyerName = 'VIP Client',
  paymentMethod = 'checkout',
  transactionId,
  amountLabel,
  pdfBase64,
  filename,
  summaryText = ''
}) {
  const resolvedProduct = product || PRODUCTS[productKey] || PRODUCTS.cabinetscan;
  const normalizedCustomer = isValidEmail(customerEmail) ? customerEmail.trim() : null;
  const txKey = transactionId ? String(transactionId).trim() : null;
  const dedupeKey = txKey ? `${resolvedProduct.productKey}:${txKey}:${(normalizedCustomer || 'no_cust').toLowerCase()}` : null;

  const priorState = dedupeKey ? loadOrderState(dedupeKey) : null;
  if (priorState && (!normalizedCustomer || priorState.customerSent) && priorState.ownerSent) {
    return {
      ok: true,
      deduplicated: true,
      customerSent: priorState.customerSent,
      ownerSent: priorState.ownerSent,
      customerEmail: normalizedCustomer,
      ownerEmail: OWNER_EMAIL,
      filename: priorState.filename || resolvedProduct.defaultFilename
    };
  }

  const { buffer: pdfBuffer, filename: finalFilename, source: pdfSource } = resolvePdfBuffer({
    product: resolvedProduct,
    pdfBase64,
    filename
  });

  const nextState = {
    customerSent: priorState?.customerSent || false,
    ownerSent: priorState?.ownerSent || false,
    filename: finalFilename,
    updatedAt: new Date().toISOString()
  };

  const errors = [];
  const tasks = [];

  if (normalizedCustomer && !nextState.customerSent) {
    const custMail = buildCustomerEmail({
      product: resolvedProduct,
      buyerName,
      paymentMethod,
      transactionId: txKey || 'VERIFIED',
      amountLabel,
      summaryText
    });
    tasks.push(
      dispatchSingleEmail({
        to: normalizedCustomer,
        subject: custMail.subject,
        html: custMail.html,
        text: custMail.text,
        filename: finalFilename,
        pdfBuffer,
        replyTo: OWNER_EMAIL,
        brandName: resolvedProduct.brandName
      }).then((res) => {
        nextState.customerSent = true;
        return { role: 'customer', res };
      })
    );
  } else if (!normalizedCustomer) {
    errors.push('Customer email missing or invalid; sent owner archive copy only.');
  }

  if (!nextState.ownerSent) {
    const ownerMail = buildOwnerEmail({
      product: resolvedProduct,
      customerEmail: normalizedCustomer,
      buyerName,
      paymentMethod,
      transactionId: txKey || 'VERIFIED',
      amountLabel,
      summaryText
    });
    tasks.push(
      dispatchSingleEmail({
        to: OWNER_EMAIL,
        subject: ownerMail.subject,
        html: ownerMail.html,
        text: ownerMail.text,
        filename: finalFilename,
        pdfBuffer,
        replyTo: normalizedCustomer || OWNER_EMAIL,
        brandName: resolvedProduct.brandName
      }).then((res) => {
        nextState.ownerSent = true;
        return { role: 'owner', res };
      })
    );
  }

  const settled = await Promise.allSettled(tasks);
  for (const item of settled) {
    if (item.status === 'rejected') {
      errors.push(item.reason?.message || String(item.reason));
    }
  }

  if (dedupeKey && (nextState.customerSent || nextState.ownerSent)) {
    saveOrderState(dedupeKey, nextState);
  }

  const ok = Boolean(nextState.ownerSent && (!normalizedCustomer || nextState.customerSent));
  return {
    ok,
    deduplicated: false,
    customerSent: nextState.customerSent,
    ownerSent: nextState.ownerSent,
    customerEmail: normalizedCustomer,
    ownerEmail: OWNER_EMAIL,
    filename: finalFilename,
    pdfSource,
    errors
  };
}

module.exports = {
  OWNER_EMAIL,
  isValidEmail,
  resolvePdfBuffer,
  getConfiguredProvider,
  sendPurchaseDossierEmails,
  setCustomTransport,
  clearOrderStateForTest
};
