const { handleDeliverPdf } = require('../lib/handlers');

module.exports = (req, res) => handleDeliverPdf(req, res, { defaultProductKey: 'chronospec' });
