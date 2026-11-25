require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static frontend files
app.use(express.static(path.join(__dirname)));

// Healthcheck & Configuration Status
app.get('/api/status', (req, res) => {
  res.json({
    status: 'online',
    service: 'ChronoSpec AI',
    priceUsd: '89.00',
    gateways: {
      dodo: true,
      whop: true,
      crypto: true
    }
  });
});

// Dodo Payments Gateway Endpoint
const dodoInitialize = require('./api/dodo/initialize');
app.all('/api/dodo/initialize', dodoInitialize);

app.listen(PORT, () => {
  console.log(`🚀 ChronoSpec AI Server running on port ${PORT}`);
  console.log(`🌐 Local preview: http://localhost:${PORT}`);
});
