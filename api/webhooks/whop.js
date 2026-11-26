const { handleWhopWebhook } = require('../../lib/handlers');

const handler = (req, res) => handleWhopWebhook(req, res, { defaultProductKey: 'chronospec' });
handler.config = { api: { bodyParser: false } };

module.exports = handler;
module.exports.config = { api: { bodyParser: false } };
