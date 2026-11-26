require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json({
  limit: '25mb',
  verify: (req, res, buf) => {
    req.rawBody = buf.toString('utf8');
  }
}));
app.use(express.urlencoded({ extended: true }));

// Serve static frontend files
app.use(express.static(path.join(__dirname)));

// Healthcheck & Configuration Status
const statusHandler = require('./api/status');
app.all('/api/status', statusHandler);

// Dodo Payments Gateway Endpoint
const dodoInitialize = require('./api/dodo/initialize');
app.all('/api/dodo/initialize', dodoInitialize);

// PDF Email Delivery & Payment Webhooks (Customer + karakoc.i@gmail.com)
const deliverPdf = require('./api/deliver-pdf');
const dodoWebhook = require('./api/webhooks/dodo');
const whopWebhook = require('./api/webhooks/whop');
app.all('/api/deliver-pdf', deliverPdf);
app.all('/api/webhooks/dodo', dodoWebhook);
app.all('/api/webhooks/whop', whopWebhook);

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`🚀 ChronoSpec AI Server running on port ${PORT}`);
    console.log(`🌐 Local preview: http://localhost:${PORT}`);
  });
}

module.exports = app;
