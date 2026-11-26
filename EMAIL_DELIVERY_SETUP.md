# Automatic PDF Email Delivery Setup (Customer + karakoc.i@gmail.com)

All purchase flows (**Dodo Payments**, **Whop**, **USDT TRC20 / USDC ERC20 Crypto**, and **PayTR**) are wired to send the PDF dossier to **both** the customer's email and `karakoc.i@gmail.com`.

Because GitHub Pages (`federal216.github.io`, `hseenglish.app`) hosts static files only, live email delivery requires deploying the included Node.js / Vercel Serverless API (`api/`) with SMTP or Resend credentials.

## 1. Deploy Backend (`vercel.json` is already included)
Deploy the repository to Vercel (free Hobby tier works):
- Endpoints exposed automatically:
  - `POST /api/deliver-pdf` (verifies Dodo payment or Crypto TxID on-chain, then emails PDF to customer + `karakoc.i@gmail.com`)
  - `POST /api/webhooks/dodo` (Dodo Payments `payment.succeeded` webhook -> emails PDF to customer + `karakoc.i@gmail.com`)
  - `POST /api/webhooks/whop` (Whop `payment.succeeded` / `membership.went_valid` webhook -> emails PDF to customer + `karakoc.i@gmail.com`)
  - `POST /api/dodo/initialize` (creates Dodo Checkout sessions with customer email & allowed redirect URL)
  - `GET /api/status` (shows `emailConfigured: true/false`)

## 2. Set Environment Variables (Vercel Project Settings -> Environment Variables)

### Option A: Gmail SMTP (Fastest, sends to any customer email)
1. Enable 2-Step Verification on your Google account (`karakoc.i@gmail.com`).
2. Create an App Password at Google Account -> Security -> App Passwords.
3. Set in Vercel:
   - `OWNER_EMAIL=karakoc.i@gmail.com`
   - `SMTP_USER=karakoc.i@gmail.com`
   - `GMAIL_APP_PASSWORD=<16-character app password>`

### Option B: Resend API (with a verified custom domain)
- `OWNER_EMAIL=karakoc.i@gmail.com`
- `RESEND_API_KEY=re_...`
- `RESEND_FROM=Support <noreply@yourdomain.com>`

## 3. Configure Payment Gateways (Guaranteed Delivery Even If Buyer Closes Browser)
- **Dodo Payments Dashboard -> Webhooks**:
  - Endpoint URL: `https://<your-vercel-app>.vercel.app/api/webhooks/dodo`
  - Subscribe to: `payment.succeeded`, `checkout.session.completed`
  - Copy Signing Secret into Vercel env var: `DODO_WEBHOOK_SECRET=whsec_...`
- **Whop Dashboard -> Webhooks**:
  - Endpoint URL: `https://<your-vercel-app>.vercel.app/api/webhooks/whop`
  - Subscribe to: `payment.succeeded`, `membership.went_valid`
  - Copy Secret into Vercel env var: `WHOP_WEBHOOK_SECRET=...`

## 4. Connect GitHub Pages Frontend to Vercel API (For Crypto & Dynamic Dodo Sessions)
In `index.html`, set `window.FEDERAL216_API_BASE = 'https://<your-vercel-app>.vercel.app'` (or store `localStorage.setItem('FEDERAL216_API_BASE', 'https://<your-vercel-app>.vercel.app')`) if serving the UI from `federal216.github.io` / `hseenglish.app`. When visiting the Vercel URL directly, same-origin `/api/*` works with zero changes.
