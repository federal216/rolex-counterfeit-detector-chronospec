const OWNER_EMAIL = (process.env.OWNER_EMAIL || 'karakoc.i@gmail.com').trim();

const PRODUCTS = {
  lambospec: {
    productKey: 'lambospec',
    brandName: 'LamboSpec AI',
    dossierTitle: 'LamboSpec AI — 10-Page Supercar Forensic & Negotiation Dossier',
    priceUsd: 79.0,
    pdfRelPath: 'sample_report.pdf',
    defaultFilename: 'LamboSpec_10Page_Master_Dossier.pdf',
    supportEmail: 'lamborginichallenge2026@gmail.com',
    liveUrl: 'https://federal216.github.io/',
    accentHex: '#f97316',
    dodoProductIds: ['pdt_0NsdaQ7P6h6NjAauG3k4P', 'pdt_0NsdXpb0AXJ8AeTfGANYe'],
    whopIds: ['lambospec-ai-vip-pre-purchase-dossier']
  },
  cabinetscan: {
    productKey: 'cabinetscan',
    brandName: 'CabinetScan AI',
    dossierTitle: 'CabinetScan AI — 10-Page Clinical Pharmacokinetic Safety Dossier',
    priceUsd: 99.0,
    pdfRelPath: 'sample_cabinetscan_dossier.pdf',
    defaultFilename: 'CabinetScan_10Page_Master_Clinical_Dossier.pdf',
    supportEmail: 'support@cabinetscan.ai',
    liveUrl: 'https://federal216.github.io/cabinetscan/',
    accentHex: '#10b981',
    dodoProductIds: ['pdt_0Nsi1itVeozy7gIIA0y'],
    whopIds: ['plan_ikEY1bP1Pk7di']
  },
  chronospec: {
    productKey: 'chronospec',
    brandName: 'ChronoSpec AI',
    dossierTitle: 'ChronoSpec AI — 10-Page Horological Forensic Appraisal Dossier',
    priceUsd: 89.0,
    pdfRelPath: 'sample_chronospec_dossier.pdf',
    defaultFilename: 'ChronoSpec_10Page_Forensic_Dossier.pdf',
    supportEmail: 'karakoc.i@gmail.com',
    liveUrl: 'https://federal216.github.io/rolex-counterfeit-detector-chronospec/',
    accentHex: '#d4af37',
    dodoProductIds: ['pdt_0Nsi1qHuRLnD6c4NmHyfK'],
    whopIds: ['chronospec-ai-vip-watch-appraisal-dossier']
  }
};

function normalizeProductKey(raw) {
  if (!raw || typeof raw !== 'string') return null;
  const val = raw.trim().toLowerCase();
  if (val.includes('lambo')) return 'lambospec';
  if (val.includes('cabinet')) return 'cabinetscan';
  if (val.includes('chrono') || val.includes('rolex')) return 'chronospec';
  return PRODUCTS[val] ? val : null;
}

function resolveProduct({ productKey, productId, planId, metadata, amountUsd, defaultKey = 'cabinetscan' } = {}) {
  const fromKey = normalizeProductKey(productKey) || normalizeProductKey(metadata?.app) || normalizeProductKey(metadata?.product);
  if (fromKey && PRODUCTS[fromKey]) return PRODUCTS[fromKey];

  if (planId) {
    const matchWhop = Object.values(PRODUCTS).find(p =>
      p.whopIds.some(id => id.toLowerCase() === String(planId).toLowerCase())
    );
    if (matchWhop) return matchWhop;
    const fromPlanName = normalizeProductKey(String(planId));
    if (fromPlanName && PRODUCTS[fromPlanName]) return PRODUCTS[fromPlanName];
  }

  if (productId) {
    if (productId === 'pdt_0Nsi1itVeozy7gIIA0y') return PRODUCTS.cabinetscan;
    if (productId === 'pdt_0Nsi1qHuRLnD6c4NmHyfK') return PRODUCTS.chronospec;
    if (PRODUCTS[defaultKey]?.dodoProductIds.includes(productId)) {
      return PRODUCTS[defaultKey];
    }
    const matchDodo = Object.values(PRODUCTS).find(p => p.dodoProductIds.includes(productId));
    if (matchDodo) return matchDodo;
  }

  if (typeof amountUsd === 'number' && !Number.isNaN(amountUsd)) {
    if (Math.abs(amountUsd - 99) < 0.5) return PRODUCTS.cabinetscan;
    if (Math.abs(amountUsd - 89) < 0.5) return PRODUCTS.chronospec;
    if (Math.abs(amountUsd - 79) < 0.5) return PRODUCTS.lambospec;
  }

  return PRODUCTS[defaultKey] || PRODUCTS.cabinetscan;
}

module.exports = {
  OWNER_EMAIL,
  PRODUCTS,
  normalizeProductKey,
  resolveProduct
};
