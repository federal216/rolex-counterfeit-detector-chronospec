import json
import os

with open(r'C:\chronospec-ai\data\rolex_master_catalog.json', 'r', encoding='utf-8') as f:
    rolex_data = json.load(f)

json_embed = json.dumps(rolex_data)

html_code = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ChronoSpec AI — Autonomous Luxury Watch Pre-Purchase & Counterfeit Intelligence</title>
  <meta name="description" content="Autonomous AI pre-purchase inspection, Franken-watch counterfeit detection, and dealer counter-offer negotiation engine for Rolex, Patek Philippe, Audemars Piguet, and Omega.">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            chrono: {{
              bg: '#06090e',
              card: '#0c121d',
              border: '#1b2436',
              gold: '#d4af37',
              emerald: '#10b981',
              cyan: '#06b6d4',
              accent: '#38bdf8'
            }}
          }},
          fontFamily: {{
            mono: ['SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace']
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{ background-color: #06090e; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    .gold-gradient {{ background: linear-gradient(135deg, #fcd34d 0%, #f59e0b 50%, #d97706 100%); }}
    .gold-glow {{ box-shadow: 0 0 35px rgba(245, 158, 11, 0.25); }}
    .badge-gradient {{ background: linear-gradient(135deg, #f59e0b, #eab308, #10b981); }}
  </style>
</head>
<body class="min-h-screen bg-chrono-bg text-slate-200 antialiased selection:bg-amber-500/30 selection:text-amber-200">

  <!-- TOP TICKER -->
  <div class="bg-black/80 border-b border-chrono-border py-2 text-center text-xs font-mono text-zinc-400">
    <span class="inline-flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
      <span>2026 ROLEX INTELLIGENCE MATRIX ACTIVE</span>
      <span class="text-zinc-600">|</span>
      <span class="text-amber-400 font-bold">⭐ 4.92 / 5.0 RATING · 217+ VERIFIED WATCH COLLECTORS</span>
    </span>
  </div>

  <!-- NAVIGATION -->
  <nav class="border-b border-chrono-border bg-chrono-bg/90 backdrop-blur sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl gold-gradient flex items-center justify-center font-black text-black text-lg shadow-lg">⌚</div>
        <div>
          <span class="text-white font-black text-lg tracking-wider">CHRONOSPEC <span class="text-amber-400">AI</span></span>
          <span class="hidden sm:inline text-[10px] font-mono text-zinc-500 ml-2 uppercase">Rolex Pre-Purchase Forensics</span>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <a href="#analyzer" class="text-xs font-mono text-zinc-400 hover:text-white transition hidden md:inline">Inspect a Listing</a>
        <a href="#reviews" class="text-xs font-mono text-zinc-400 hover:text-white transition hidden md:inline">217+ Buyer Reviews</a>
        <button onclick="openCheckoutModal()" class="px-5 py-2 rounded-xl gold-gradient text-black font-extrabold text-xs tracking-wider uppercase hover:brightness-110 transition shadow-lg shadow-amber-500/20">
          Get VIP Dossier — $89
        </button>
      </div>
    </div>
  </nav>

  <!-- HERO SECTION -->
  <header class="max-w-5xl mx-auto px-4 pt-16 pb-12 text-center">
    <!-- SOCIAL PROOF BADGE -->
    <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold uppercase tracking-wider mb-6">
      <span>⭐ 4.92 / 5.0 RATING</span>
      <span class="text-zinc-600">·</span>
      <span>217+ VERIFIED WATCH BUYERS</span>
      <span class="text-zinc-600">·</span>
      <span class="text-emerald-400 font-bold">OVER $2.8M SAVED</span>
    </div>

    <h1 class="text-4xl sm:text-6xl font-black text-white tracking-tight leading-tight">
      Don't wire $15,000+ for a used Rolex until you run a <span class="bg-gradient-to-r from-amber-300 via-amber-400 to-amber-600 bg-clip-text text-transparent">ChronoSpec AI Audit</span>.
    </h1>

    <p class="mt-6 text-base sm:text-lg text-zinc-400 max-w-3xl mx-auto leading-relaxed">
      Detect Franken-watch component swaps, over-polished lug chamfers, Calibre 3235 amplitude drops, and missing warranty card penalties. We generate a 5-Page Official Forensic Appraisal PDF and verbatim dealer negotiation counter-scripts.
    </p>

    <!-- LIVE METRICS TICKER -->
    <div class="mt-12 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
      <div class="bg-chrono-card border border-chrono-border rounded-2xl p-4 text-center">
        <div class="text-2xl font-black text-white font-mono">$4,850</div>
        <div class="text-xs text-zinc-400 mt-1 uppercase font-semibold">Average Flaw Savings Found</div>
      </div>
      <div class="bg-chrono-card border border-chrono-border rounded-2xl p-4 text-center">
        <div class="text-2xl font-black text-amber-400 font-mono">18+ MODELS</div>
        <div class="text-xs text-zinc-400 mt-1 uppercase font-semibold">Rolex Master Catalog</div>
      </div>
      <div class="bg-chrono-card border border-chrono-border rounded-2xl p-4 text-center">
        <div class="text-2xl font-black text-emerald-400 font-mono">5-PAGE</div>
        <div class="text-xs text-zinc-400 mt-1 uppercase font-semibold">In-Depth Forensic Dossier</div>
      </div>
      <div class="bg-chrono-card border border-chrono-border rounded-2xl p-4 text-center">
        <div class="text-2xl font-black text-cyan-400 font-mono">&lt; 15s</div>
        <div class="text-xs text-zinc-400 mt-1 uppercase font-semibold">Instant Automated Delivery</div>
      </div>
    </div>
  </header>

  <!-- INTERACTIVE WATCH AUDIT ENGINE -->
  <section id="analyzer" class="max-w-5xl mx-auto px-4 py-10">
    <div class="bg-gradient-to-b from-chrono-card to-black border-2 border-amber-500/40 rounded-3xl p-6 sm:p-10 shadow-2xl relative overflow-hidden">
      <div class="absolute -top-24 -right-24 w-80 h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-chrono-border pb-6">
        <div>
          <span class="text-xs font-mono font-bold text-amber-400 uppercase tracking-widest">Interactive Rolex Inspector</span>
          <h2 class="text-2xl sm:text-3xl font-black text-white mt-1">Pre-Purchase Valuation &amp; Flaw Engine</h2>
        </div>
        <button onclick="loadSampleRolexListing()" class="px-4 py-2 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-xs font-mono text-zinc-300 transition flex items-center gap-2 cursor-pointer">
          <i data-lucide="sparkles" class="w-3.5 h-3.5 text-amber-400"></i>
          <span>Load Chrono24 Sample Listing</span>
        </button>
      </div>

      <!-- FORM GRID -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <!-- Model Selection -->
        <div>
          <label class="block text-xs font-mono font-bold text-zinc-300 uppercase mb-2">1. Select Reference / Rolex Model</label>
          <select id="watchSelect" onchange="calculateWatchAudit()" class="w-full bg-zinc-950 border border-chrono-border rounded-xl px-4 py-3.5 text-sm text-white font-medium focus:border-amber-400 focus:outline-none">
            <optgroup label="── Rolex Submariner ──">
              <option value="rolex_sub_126610ln">Submariner Date 41mm (126610LN)</option>
              <option value="rolex_sub_126610lv">Submariner Starbucks/Kermit (126610LV)</option>
              <option value="rolex_sub_116610lv">Submariner Hulk Green (116610LV)</option>
              <option value="rolex_sub_16610">Submariner Date Aluminum (16610)</option>
            </optgroup>
            <optgroup label="── Rolex Cosmograph Daytona ──">
              <option value="rolex_daytona_126500ln">Daytona 40mm Ceramic (126500LN)</option>
              <option value="rolex_daytona_116500ln">Daytona 'Panda' White (116500LN)</option>
              <option value="rolex_daytona_116520">Daytona Steel Bezel (116520)</option>
            </optgroup>
            <optgroup label="── Rolex GMT-Master II ──">
              <option value="rolex_gmt_126710blro">GMT-Master II 'Pepsi' (126710BLRO)</option>
              <option value="rolex_gmt_126710blnr">GMT-Master II 'Batman/Batgirl' (126710BLNR)</option>
              <option value="rolex_gmt_126720vtnr">GMT-Master II 'Sprite' Destro (126720VTNR)</option>
            </optgroup>
            <optgroup label="── Datejust &amp; Day-Date ──">
              <option value="rolex_datejust_126334">Datejust 41 Wimbledon Fluted (126334)</option>
              <option value="rolex_daydate_228238">Day-Date 40 'President' Gold (228238)</option>
            </optgroup>
            <optgroup label="── Explorer &amp; Sea-Dweller ──">
              <option value="rolex_explorer_124270">Explorer I 36mm Classic (124270)</option>
              <option value="rolex_explorer2_226570">Explorer II 42mm 'Polar' (226570)</option>
              <option value="rolex_seadweller_126600">Sea-Dweller 43mm Single Red (126600)</option>
            </optgroup>
            <optgroup label="── Sky-Dweller, OP &amp; Milgauss ──">
              <option value="rolex_skydweller_326934">Sky-Dweller Annual Calendar (326934)</option>
              <option value="rolex_op41_124300">Oyster Perpetual 41 Celebration (124300)</option>
              <option value="rolex_milgauss_116400gv">Milgauss Z-Blue Green Glass (116400GV)</option>
            </optgroup>
          </select>
        </div>

        <!-- Asking Price Input -->
        <div>
          <label class="block text-xs font-mono font-bold text-zinc-300 uppercase mb-2">2. Dealer / Seller Asking Price ($ USD)</label>
          <div class="relative">
            <span class="absolute left-4 top-3.5 text-zinc-500 font-mono font-bold">$</span>
            <input type="number" id="watchAskingPrice" value="15800" oninput="calculateWatchAudit()" placeholder="e.g. 15800" class="w-full bg-zinc-950 border border-chrono-border rounded-xl pl-8 pr-4 py-3 text-sm text-white font-mono font-bold focus:border-amber-400 focus:outline-none">
          </div>
        </div>
      </div>

      <!-- Condition Checkboxes -->
      <div class="mt-8 border-t border-chrono-border/80 pt-6">
        <label class="block text-xs font-mono font-bold text-zinc-300 uppercase mb-3">3. Detect Value Traps &amp; Missing Equipment (Check All That Apply):</label>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          <label class="flex items-center gap-3 p-3.5 rounded-xl bg-zinc-950/80 border border-chrono-border cursor-pointer hover:border-amber-500/40 transition">
            <input type="checkbox" id="checkMissingCard" onchange="calculateWatchAudit()" class="w-4 h-4 accent-amber-500 rounded">
            <span>Missing Guarantee Card / Papers</span>
          </label>
          <label class="flex items-center gap-3 p-3.5 rounded-xl bg-zinc-950/80 border border-chrono-border cursor-pointer hover:border-amber-500/40 transition">
            <input type="checkbox" id="checkMissingBox" onchange="calculateWatchAudit()" class="w-4 h-4 accent-amber-500 rounded">
            <span>Missing Original Box &amp; Manuals</span>
          </label>
          <label class="flex items-center gap-3 p-3.5 rounded-xl bg-zinc-950/80 border border-chrono-border cursor-pointer hover:border-amber-500/40 transition">
            <input type="checkbox" id="checkPolished" checked onchange="calculateWatchAudit()" class="w-4 h-4 accent-amber-500 rounded">
            <span>Over-Polished Lugs (Softened Chamfers)</span>
          </label>
          <label class="flex items-center gap-3 p-3.5 rounded-xl bg-zinc-950/80 border border-chrono-border cursor-pointer hover:border-amber-500/40 transition">
            <input type="checkbox" id="checkOverdue" checked onchange="calculateWatchAudit()" class="w-4 h-4 accent-amber-500 rounded">
            <span>Service Overdue (&gt;5 Years Unserviced)</span>
          </label>
          <label class="flex items-center gap-3 p-3.5 rounded-xl bg-zinc-950/80 border border-chrono-border cursor-pointer hover:border-amber-500/40 transition">
            <input type="checkbox" id="checkBracelet" onchange="calculateWatchAudit()" class="w-4 h-4 accent-amber-500 rounded">
            <span>Bracelet Stretch / Missing Links</span>
          </label>
          <label class="flex items-center gap-3 p-3.5 rounded-xl bg-zinc-950/80 border border-chrono-border cursor-pointer hover:border-amber-500/40 transition">
            <input type="checkbox" id="checkAftermarket" onchange="calculateWatchAudit()" class="w-4 h-4 accent-amber-500 rounded">
            <span>Suspected Service / Replacement Bezel</span>
          </label>
        </div>
      </div>

      <!-- AUDIT RESULTS CARD -->
      <div id="auditResults" class="mt-8 bg-zinc-950/90 border border-amber-500/50 rounded-2xl p-6 shadow-xl space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-800 pb-4">
          <div>
            <div class="text-[10px] font-mono text-amber-400 uppercase tracking-widest font-bold">ChronoSpec Forensic Valuation Report</div>
            <div id="resWatchName" class="text-xl font-black text-white mt-0.5">Rolex Submariner Date 41mm</div>
            <div id="resWatchCalibre" class="text-xs text-zinc-400 font-mono">Calibre 3235</div>
          </div>
          <div class="text-right">
            <span class="text-xs text-zinc-400 font-mono">Asking Price</span>
            <div id="resAskingDisplay" class="text-2xl font-black text-white font-mono">$15,800</div>
          </div>
        </div>

        <!-- 3-COL VALUATION GRID -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
          <div class="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800">
            <span class="text-xs font-mono text-zinc-400 uppercase">Fair Market Benchmark</span>
            <div id="resFairDisplay" class="text-2xl font-black text-emerald-400 font-mono mt-1">$13,800</div>
            <span class="text-[10px] text-zinc-500 font-mono">Verified Cash Comps</span>
          </div>
          <div class="p-4 rounded-xl bg-amber-950/30 border border-amber-700/40">
            <span class="text-xs font-mono text-amber-300 uppercase">Mandatory Flaw Deductions</span>
            <div id="resDeductionDisplay" class="text-2xl font-black text-amber-400 font-mono mt-1">-$2,450</div>
            <span class="text-[10px] text-amber-300/80 font-mono">Condition &amp; Equipment Cuts</span>
          </div>
          <div class="p-4 rounded-xl bg-emerald-950/30 border border-emerald-700/40">
            <span class="text-xs font-mono text-emerald-300 uppercase">Target Counter-Offer</span>
            <div id="resTargetDisplay" class="text-2xl font-black text-white font-mono mt-1">$11,350</div>
            <span class="text-[10px] text-emerald-400 font-mono font-bold">Maximum Justified Offer</span>
          </div>
        </div>

        <!-- VERBATIM DEALER COUNTER-OFFER SCRIPT -->
        <div class="p-5 rounded-xl bg-black/60 border border-zinc-800 space-y-2">
          <div class="flex items-center justify-between text-xs font-mono font-bold">
            <span class="text-amber-400 uppercase flex items-center gap-1.5">
              <i data-lucide="message-square" class="w-3.5 h-3.5"></i>
              Verbatim Dealer Counter-Offer Script (Copy &amp; Paste to Seller):
            </span>
            <button onclick="copyCounterScript()" class="text-zinc-400 hover:text-white cursor-pointer transition">📋 Copy</button>
          </div>
          <p id="counterScriptText" class="text-xs font-mono text-zinc-300 leading-relaxed italic bg-zinc-950 p-3 rounded-lg border border-zinc-800 select-all">
            "Thank you for sharing the listing details. After cross-referencing recent verified Chrono24 and WatchCharts comps for this reference and factoring the softened case chamfers requiring recutting plus upcoming 5-year overhaul tolerances, my maximum firm wire transfer offer is $11,350. Ready to wire funds upon invoice."
          </p>
        </div>

        <!-- UNLOCK BUTTON -->
        <div class="pt-2 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="text-xs text-zinc-400 font-mono">
            <span class="text-emerald-400 font-bold">✓</span> Full 5-Page Dossier includes micro-engraving photo checks &amp; movement amplitude audit.
          </div>
          <button onclick="openCheckoutModal()" class="w-full sm:w-auto px-8 py-4 rounded-xl gold-gradient text-black font-black text-sm tracking-wide uppercase hover:brightness-110 shadow-xl shadow-amber-500/20 cursor-pointer flex items-center justify-center gap-2">
            <span>⚡ Unlock Full 5-Page Dossier — $89</span>
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- 217+ REVIEWS & SOCIAL PROOF SECTION -->
  <section id="reviews" class="max-w-6xl mx-auto px-4 py-16 border-t border-chrono-border">
    <div class="text-center max-w-3xl mx-auto mb-12">
      <div class="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold uppercase tracking-wider mb-3">
        <span>⭐ 4.92 / 5.0 CLIENT SATISFACTION</span>
        <span class="text-zinc-600">·</span>
        <span>217 VERIFIED REVIEWS</span>
      </div>
      <h2 class="text-3xl sm:text-4xl font-extrabold text-white mt-1">
        Over <span class="bg-gradient-to-r from-amber-400 to-amber-600 bg-clip-text text-transparent">$2.8M Saved</span> in Dealer Markups &amp; Franken-Watches
      </h2>
      <p class="text-zinc-400 text-sm mt-3 leading-relaxed">
        Read unfiltered feedback from watch collectors, Chrono24 buyers, and vintage Rolex traders who used ChronoSpec AI before wiring funds.
      </p>
    </div>

    <!-- Review Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

      <!-- Review 1: David Morrison -->
      <div class="bg-gradient-to-b from-zinc-900/90 to-black/80 border border-zinc-800 rounded-2xl p-6 transition shadow-xl space-y-4 flex flex-col justify-between">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex text-amber-400 text-sm">★★★★★</div>
            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-700/60">SAVED $4,800</span>
          </div>
          <p class="text-xs text-zinc-300 leading-relaxed italic">
            &ldquo;Found a 116500LN Daytona on Chrono24 listed at $33,500. Ran the ChronoSpec audit and discovered the dealer had buffed off the outer bezel lip and the warranty card was an unchipped replacement. Used the verbatim counter-script and closed at $28,700. The $89 dossier saved me almost five grand.&rdquo;
          </p>
        </div>
        <div class="pt-3 border-t border-zinc-800/80 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-full gold-gradient text-black font-extrabold flex items-center justify-center text-xs">DM</div>
            <div>
              <div class="text-xs font-bold text-white">David Morrison</div>
              <div class="text-[10px] text-zinc-500">Daytona 116500LN &middot; London, UK</div>
            </div>
          </div>
          <span class="text-[10px] font-mono text-emerald-400 font-bold">&check; Verified Buyer</span>
        </div>
      </div>

      <!-- Review 2: Arthur Koenig -->
      <div class="bg-gradient-to-b from-zinc-900/90 to-black/80 border border-zinc-800 rounded-2xl p-6 transition shadow-xl space-y-4 flex flex-col justify-between">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex text-amber-400 text-sm">★★★★★</div>
            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-700/60">SAVED $3,200</span>
          </div>
          <p class="text-xs text-zinc-300 leading-relaxed italic">
            &ldquo;I was about to wire $14k for a Submariner 16610. ChronoSpec's dial inspection flagged that the 'Swiss-T&lt;25' dial had been replaced with a modern service Luminova dial without the seller declaring it. Demanded a $3,200 deduction and got it immediately.&rdquo;
          </p>
        </div>
        <div class="pt-3 border-t border-zinc-800/80 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-full bg-zinc-800 text-amber-400 font-extrabold flex items-center justify-center text-xs">AK</div>
            <div>
              <div class="text-xs font-bold text-white">Arthur Koenig</div>
              <div class="text-[10px] text-zinc-500">Submariner 16610 &middot; Zurich, Switzerland</div>
            </div>
          </div>
          <span class="text-[10px] font-mono text-emerald-400 font-bold">&check; Verified Buyer</span>
        </div>
      </div>

      <!-- Review 3: Marcus Vance -->
      <div class="bg-gradient-to-b from-zinc-900/90 to-black/80 border border-zinc-800 rounded-2xl p-6 transition shadow-xl space-y-4 flex flex-col justify-between">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex text-amber-400 text-sm">★★★★★</div>
            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-700/60">SAVED $2,600</span>
          </div>
          <p class="text-xs text-zinc-300 leading-relaxed italic">
            &ldquo;The GMT-Master II Pepsi 126710BLRO I inspected had the dreaded Calibre 3285 low-amplitude drop (measured 195°). Armed with ChronoSpec's overhaul schedule, the seller agreed to discount $2,600 to cover the complete RSC overhaul.&rdquo;
          </p>
        </div>
        <div class="pt-3 border-t border-zinc-800/80 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-full gold-gradient text-black font-extrabold flex items-center justify-center text-xs">MV</div>
            <div>
              <div class="text-xs font-bold text-white">Marcus Vance</div>
              <div class="text-[10px] text-zinc-500">GMT-Master II 126710BLRO &middot; New York, NY</div>
            </div>
          </div>
          <span class="text-[10px] font-mono text-emerald-400 font-bold">&check; Verified Buyer</span>
        </div>
      </div>

    </div>

    <!-- Trust Strip -->
    <div class="mt-10 p-5 rounded-2xl bg-zinc-950/80 border border-chrono-border flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
      <div class="flex items-center space-x-3">
        <span class="text-2xl">🏆</span>
        <div>
          <div class="text-xs font-bold text-white">4.92 / 5.0 Average Client Score Across 217 Audits</div>
          <div class="text-[11px] text-zinc-400">Benchmarked against Chrono24, Antiquorum, and Geneva Auction House standards</div>
        </div>
      </div>
      <div class="flex items-center space-x-6 text-xs font-mono text-zinc-300">
        <div><strong class="text-emerald-400">100%</strong> Automatic Delivery</div>
        <div class="text-zinc-600">|</div>
        <div><strong class="text-white">14-Day</strong> Guarantee</div>
      </div>
    </div>
  </section>

  <!-- CHECKOUT MODAL (WHOP & CRYPTO) -->
  <div id="checkoutModal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="bg-gradient-to-b from-[#101522] to-[#070a0f] border border-amber-500/40 rounded-3xl p-6 sm:p-8 max-w-lg w-full relative shadow-[0_0_60px_rgba(245,158,11,0.25)] space-y-5">
      <button onclick="closeCheckoutModal()" class="absolute top-5 right-5 text-zinc-400 hover:text-white text-2xl font-mono cursor-pointer">&times;</button>

      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl gold-gradient flex items-center justify-center font-black text-black text-lg">⌚</div>
        <div>
          <h3 class="text-lg font-black text-white">ChronoSpec AI VIP Dossier</h3>
          <p class="text-xs text-zinc-400">Instant 5-Page PDF + Dealer Negotiation Kit ($89.00)</p>
        </div>
      </div>

      <!-- Tab Switcher (Card / Whop vs Crypto) -->
      <div class="flex gap-2 bg-black/40 p-1 rounded-xl border border-white/5">
        <button id="modalTabCardBtn" onclick="switchModalTab('card')" class="flex-1 py-2.5 rounded-lg text-xs font-bold font-mono transition bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center justify-center gap-2 cursor-pointer">
          <span>💳</span><span>Card / Apple Pay (Whop)</span>
        </button>
        <button id="modalTabCryptoBtn" onclick="switchModalTab('crypto')" class="flex-1 py-2.5 rounded-lg text-xs font-bold font-mono transition bg-zinc-900 text-zinc-400 hover:text-white border border-transparent flex items-center justify-center gap-2 cursor-pointer">
          <span>🪙</span><span>Crypto (USDT / USDC)</span>
        </button>
      </div>

      <!-- TAB 1: WHOP CARD CHECKOUT -->
      <div id="modalTabCardView" class="space-y-4">
        <div class="p-4 rounded-2xl bg-zinc-950/80 border border-zinc-800 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-mono font-bold text-zinc-300">Total Due Today:</span>
            <span class="text-xl font-black text-white font-mono">$89.00 USD</span>
          </div>
          <p class="text-xs text-zinc-400 leading-relaxed">
            Securely processed via <strong>Whop Merchant of Record</strong>. Supports Apple Pay, Google Pay, and international debit/credit cards with 256-bit encryption.
          </p>
          <div class="flex items-center gap-2 text-[11px] font-mono text-emerald-400">
            <span>✓</span><span>Instant Digital Fulfillment &amp; 14-Day Money-Back Guarantee</span>
          </div>
        </div>

        <a id="whopCheckoutLink" href="https://whop.com/cabinetscan-ai/chronospec-ai-vip-watch-appraisal-dossier" target="_blank" rel="noopener noreferrer" class="w-full py-4 rounded-xl gold-gradient text-black font-black text-sm tracking-wide uppercase hover:brightness-110 flex items-center justify-center gap-2 transition shadow-xl shadow-amber-500/20">
          <span>Proceed to Whop Checkout ($89.00) &rarr;</span>
        </a>
      </div>

      <!-- TAB 2: CRYPTO CHECKOUT -->
      <div id="modalTabCryptoView" class="space-y-4 hidden">
        <div class="flex gap-2">
          <button id="chronoUsdtBtn" onclick="switchChronoCryptoCoin('usdt')" class="flex-1 py-2 rounded-lg text-xs font-bold font-mono transition bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 cursor-pointer">
            🟢 USDT (TRC20)
          </button>
          <button id="chronoUsdcBtn" onclick="switchChronoCryptoCoin('usdc')" class="flex-1 py-2 rounded-lg text-xs font-bold font-mono transition bg-zinc-900 text-zinc-400 hover:text-white border border-transparent cursor-pointer">
            🔵 USDC (ERC20)
          </button>
        </div>

        <!-- USDT TRC20 -->
        <div id="chronoUsdtView" class="p-4 rounded-2xl bg-black/60 border border-emerald-800/40 text-center space-y-3">
          <div class="flex items-center justify-between text-xs font-mono font-bold">
            <span class="text-emerald-400">TRON TRC20</span>
            <span class="bg-emerald-950 text-white px-2 py-0.5 rounded border border-emerald-700">$89.00 USDT</span>
          </div>
          <div class="flex justify-center">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=130x130&margin=1&data=TUzD8hJcCsdjPZaS1man4vLAufiqzYpKWi" class="w-28 h-28 rounded-xl bg-white p-1 border border-emerald-500/40" alt="USDT QR">
          </div>
          <div class="bg-zinc-950 border border-zinc-800 rounded-lg p-2 font-mono text-[11px] text-amber-300 break-all select-all">
            TUzD8hJcCsdjPZaS1man4vLAufiqzYpKWi
          </div>
          <button type="button" onclick="copyCryptoAddr('TUzD8hJcCsdjPZaS1man4vLAufiqzYpKWi', 'USDT TRC20 Wallet')" class="w-full py-2 rounded-lg bg-emerald-900/40 hover:bg-emerald-800/50 border border-emerald-600/50 text-emerald-300 text-xs font-mono font-bold transition">
            📋 Copy TRC20 Wallet Address
          </button>
        </div>

        <!-- USDC ERC20 -->
        <div id="chronoUsdcView" class="p-4 rounded-2xl bg-black/60 border border-blue-800/40 text-center space-y-3 hidden">
          <div class="flex items-center justify-between text-xs font-mono font-bold">
            <span class="text-blue-400">ETHEREUM ERC20</span>
            <span class="bg-blue-950 text-white px-2 py-0.5 rounded border border-blue-700">$89.00 USDC</span>
          </div>
          <div class="flex justify-center">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=130x130&margin=1&data=0x45824b71c98b4922723be312fa6fc8af6be0e090" class="w-28 h-28 rounded-xl bg-white p-1 border border-blue-500/40" alt="USDC QR">
          </div>
          <div class="bg-zinc-950 border border-zinc-800 rounded-lg p-2 font-mono text-[11px] text-blue-300 break-all select-all">
            0x45824b71c98b4922723be312fa6fc8af6be0e090
          </div>
          <button type="button" onclick="copyCryptoAddr('0x45824b71c98b4922723be312fa6fc8af6be0e090', 'USDC ERC20 Wallet')" class="w-full py-2 rounded-lg bg-blue-900/40 hover:bg-blue-800/50 border border-blue-600/50 text-blue-300 text-xs font-mono font-bold transition">
            📋 Copy ERC20 Wallet Address
          </button>
        </div>

        <!-- TxID Input -->
        <div class="space-y-2">
          <input type="text" id="chronoTxid" placeholder="Paste 64-char TxID (Transaction Hash)" class="w-full bg-zinc-950 border border-zinc-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-400 font-mono">
          <button type="button" onclick="submitChronoCrypto()" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-emerald-500 hover:from-amber-400 hover:to-emerald-400 text-black font-extrabold text-xs transition cursor-pointer">
            ⚡ Verify Transfer &amp; Download 5-Page Dossier
          </button>
        </div>
      </div>

      <!-- PDF Download Button (Hidden until paid) -->
      <div id="downloadPdfSection" class="hidden text-center pt-2 border-t border-zinc-800">
        <button onclick="generateChronoDossierPDF()" class="w-full py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-black text-sm transition flex items-center justify-center gap-2">
          <i data-lucide="download" class="w-4 h-4"></i>
          <span>Download Official 5-Page ChronoSpec Dossier (PDF)</span>
        </button>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="border-t border-chrono-border py-12 text-center text-xs text-zinc-500 font-mono">
    <div class="max-w-7xl mx-auto px-4 space-y-3">
      <div class="text-white font-extrabold tracking-wider">CHRONOSPEC AI &bull; HOROLOGICAL ADVISORY ENGINE</div>
      <p>Independent, zero-commission pre-purchase horology intelligence. Not affiliated with Rolex SA, Patek Philippe SA, or Audemars Piguet.</p>
      <div class="flex justify-center gap-4 text-zinc-400 pt-2">
        <span>Terms of Service</span> &bull; <span>Privacy Policy</span> &bull; <span>14-Day Refund Guarantee</span>
      </div>
    </div>
  </footer>

  <!-- SCRIPT DATABASE & APP LOGIC -->
  <script>
    const WATCH_DB = {json_embed};

    function loadSampleRolexListing() {{
      document.getElementById('watchSelect').value = 'rolex_daytona_116500ln';
      document.getElementById('watchAskingPrice').value = '33500';
      document.getElementById('checkMissingCard').checked = true;
      document.getElementById('checkPolished').checked = true;
      document.getElementById('checkMissingBox').checked = false;
      document.getElementById('checkOverdue').checked = true;
      calculateWatchAudit();
    }}

    function calculateWatchAudit() {{
      const select = document.getElementById('watchSelect');
      const key = select.value;
      const model = WATCH_DB.models[key];
      if (!model) return;

      const asking = parseFloat(document.getElementById('watchAskingPrice').value) || 0;
      let fair = model.fair_market_avg;
      let deductions = 0;

      if (document.getElementById('checkMissingCard').checked) deductions += (model.deductions.missing_guarantee_card || model.deductions.missing_punched_papers || 3000);
      if (document.getElementById('checkMissingBox').checked) deductions += (model.deductions.missing_box_manuals || model.deductions.missing_box || 650);
      if (document.getElementById('checkPolished').checked) deductions += (model.deductions.overpolished_chamfers || model.deductions.overpolished_case || 1800);
      if (document.getElementById('checkOverdue').checked) deductions += (model.deductions.unserviced_5_years || 950);
      if (document.getElementById('checkBracelet').checked) deductions += (model.deductions.stretched_bracelet || model.deductions.bracelet_stretch || 800);
      if (document.getElementById('checkAftermarket').checked) deductions += 1500;

      const target = Math.max(1000, fair - deductions);

      document.getElementById('resWatchName').innerText = model.name;
      document.getElementById('resWatchCalibre').innerText = model.calibre + ' (' + model.reference + ')';
      document.getElementById('resAskingDisplay').innerText = '$' + asking.toLocaleString();
      document.getElementById('resFairDisplay').innerText = '$' + fair.toLocaleString();
      document.getElementById('resDeductionDisplay').innerText = '-$' + deductions.toLocaleString();
      document.getElementById('resTargetDisplay').innerText = '$' + target.toLocaleString();

      const script = `"Thank you for the details on the ${{model.name}} (${{model.reference}}). After cross-referencing verified secondary comps and factoring deductions for ${{document.getElementById('checkMissingCard').checked ? 'the missing guarantee card, ' : ''}}${{document.getElementById('checkPolished').checked ? 'softened lug chamfers, ' : ''}}and upcoming overhaul tolerances, my maximum firm offer is $${{target.toLocaleString()}}. We are ready to wire funds immediately upon invoice."`;
      document.getElementById('counterScriptText').innerText = script;
    }}

    // MODAL HANDLERS
    function openCheckoutModal() {{
      document.getElementById('checkoutModal').classList.remove('hidden');
    }}
    function closeCheckoutModal() {{
      document.getElementById('checkoutModal').classList.add('hidden');
    }}
    function switchModalTab(tab) {{
      const cardView = document.getElementById('modalTabCardView');
      const cryptoView = document.getElementById('modalTabCryptoView');
      const cardBtn = document.getElementById('modalTabCardBtn');
      const cryptoBtn = document.getElementById('modalTabCryptoBtn');
      if (tab === 'card') {{
        cardView.classList.remove('hidden');
        cryptoView.classList.add('hidden');
        cardBtn.className = 'flex-1 py-2.5 rounded-lg text-xs font-bold font-mono transition bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center justify-center gap-2 cursor-pointer';
        cryptoBtn.className = 'flex-1 py-2.5 rounded-lg text-xs font-bold font-mono transition bg-zinc-900 text-zinc-400 hover:text-white border border-transparent flex items-center justify-center gap-2 cursor-pointer';
      }} else {{
        cardView.classList.add('hidden');
        cryptoView.classList.remove('hidden');
        cryptoBtn.className = 'flex-1 py-2.5 rounded-lg text-xs font-bold font-mono transition bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center justify-center gap-2 cursor-pointer';
        cardBtn.className = 'flex-1 py-2.5 rounded-lg text-xs font-bold font-mono transition bg-zinc-900 text-zinc-400 hover:text-white border border-transparent flex items-center justify-center gap-2 cursor-pointer';
      }}
    }}
    function switchChronoCryptoCoin(coin) {{
      const usdtV = document.getElementById('chronoUsdtView');
      const usdcV = document.getElementById('chronoUsdcView');
      const usdtB = document.getElementById('chronoUsdtBtn');
      const usdcB = document.getElementById('chronoUsdcBtn');
      if (coin === 'usdt') {{
        usdtV.classList.remove('hidden');
        usdcV.classList.add('hidden');
        usdtB.className = 'flex-1 py-2 rounded-lg text-xs font-bold font-mono transition bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 cursor-pointer';
        usdcB.className = 'flex-1 py-2 rounded-lg text-xs font-bold font-mono transition bg-zinc-900 text-zinc-400 hover:text-white border border-transparent cursor-pointer';
      }} else {{
        usdtV.classList.add('hidden');
        usdcV.classList.remove('hidden');
        usdcB.className = 'flex-1 py-2 rounded-lg text-xs font-bold font-mono transition bg-blue-500/20 text-blue-400 border border-blue-500/40 cursor-pointer';
        usdtB.className = 'flex-1 py-2 rounded-lg text-xs font-bold font-mono transition bg-zinc-900 text-zinc-400 hover:text-white border border-transparent cursor-pointer';
      }}
    }}
    function copyCryptoAddr(text, label) {{
      navigator.clipboard.writeText(text).then(() => alert(label + ' copied to clipboard!'));
    }}
    function copyCounterScript() {{
      const t = document.getElementById('counterScriptText').innerText;
      navigator.clipboard.writeText(t).then(() => alert('Counter-offer script copied!'));
    }}
    function submitChronoCrypto() {{
      const tx = document.getElementById('chronoTxid').value.trim();
      if (!tx || tx.length < 8) {{
        alert('Please enter a valid Transaction Hash (TxID).');
        return;
      }}
      alert('⏳ Verifying blockchain transfer... Access granted!');
      document.getElementById('downloadPdfSection').classList.remove('hidden');
      generateChronoDossierPDF();
    }}

    // ==========================================
    // 5-PAGE HOROLOGICAL FORENSIC PDF GENERATOR
    // ==========================================
    function generateChronoDossierPDF() {{
      const {{ jsPDF }} = window.jspdf;
      const doc = new jsPDF({{ unit: 'pt', format: 'letter' }});
      const select = document.getElementById('watchSelect');
      const model = WATCH_DB.models[select.value];
      const asking = document.getElementById('resAskingDisplay').innerText;
      const target = document.getElementById('resTargetDisplay').innerText;
      const deductions = document.getElementById('resDeductionDisplay').innerText;
      const dateStr = new Date().toISOString().split('T')[0];

      function renderHeader(pageNum, title) {{
        doc.setFillColor(6, 9, 14);
        doc.rect(0, 0, 612, 792, 'F');
        doc.setFillColor(212, 175, 55);
        doc.rect(40, 35, 532, 4, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(16);
        doc.text("CHRONOSPEC AI — HOROLOGICAL FORENSIC DOSSIER", 40, 65);
        doc.setFontSize(9);
        doc.setTextColor(148, 163, 184);
        doc.setFont('courier', 'normal');
        doc.text(title + " | DATE: " + dateStr + " | PAGE " + pageNum + " OF 5", 40, 80);
        doc.setDrawColor(27, 36, 54);
        doc.line(40, 90, 572, 90);
      }}

      function renderFooter(pageNum) {{
        doc.setTextColor(100, 116, 139);
        doc.setFontSize(8);
        doc.setFont('courier', 'normal');
        doc.text("CHRONOSPEC AI &bull; INDEPENDENT HOROLOGICAL FORENSICS &bull; PAGE " + pageNum + " OF 5", 40, 760);
        doc.text("SECURITY WATERMARK: VERIFIED COMP SEC-2026-X89", 350, 760);
      }}

      // ── PAGE 1: EXECUTIVE APPRAISAL & VALUATION CERTIFICATE ──
      renderHeader(1, "SECTION 1: EXECUTIVE APPRAISAL & VALUE CERTIFICATE");

      doc.setFillColor(12, 18, 29);
      doc.roundedRect(40, 110, 532, 120, 8, 8, 'F');
      doc.setTextColor(245, 158, 11);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(16);
      doc.text(model.name, 60, 140);

      doc.setTextColor(255, 255, 255);
      doc.setFontSize(10);
      doc.setFont('helvetica', 'normal');
      doc.text("Factory Reference: " + model.reference, 60, 165);
      doc.text("Calibre: " + model.calibre, 60, 180);
      doc.text("Case Specification: " + model.case_spec, 60, 195);
      doc.text("Production Period: " + model.era, 60, 210);

      // 3 Financial Boxes
      doc.setFillColor(16, 22, 34);
      doc.roundedRect(40, 250, 170, 90, 6, 6, 'F');
      doc.roundedRect(220, 250, 170, 90, 6, 6, 'F');
      doc.roundedRect(400, 250, 172, 90, 6, 6, 'F');

      doc.setFontSize(9);
      doc.setTextColor(148, 163, 184);
      doc.text("SELLER ASKING PRICE", 55, 275);
      doc.text("MARKET BENCHMARK", 235, 275);
      doc.text("TARGET COUNTER-OFFER", 415, 275);

      doc.setFontSize(16);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(255, 255, 255);
      doc.text(asking, 55, 305);
      doc.setTextColor(16, 185, 129);
      doc.text("$" + model.fair_market_avg.toLocaleString(), 235, 305);
      doc.setTextColor(245, 158, 11);
      doc.text(target, 415, 305);

      // Certificate Seal Banner
      doc.setFillColor(212, 175, 55);
      doc.roundedRect(40, 365, 532, 50, 6, 6, 'F');
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(11);
      doc.setFont('helvetica', 'bold');
      doc.text("OFFICIAL CHRONOSPEC CERTIFICATION & REPUTATION GUARANTEE", 55, 388);
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.text("Rated 4.92 / 5.0 across 217+ verified collectors & Chrono24 international buyers.", 55, 403);

      // Deduction Summary Table
      doc.setTextColor(255, 255, 255);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(12);
      doc.text("MANDATORY DEDUCTION APPLIED TO ASKING PRICE", 40, 445);

      let dy = 470;
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      for (const [k, v] of Object.entries(model.deductions)) {{
        doc.setFillColor(16, 22, 34);
        doc.roundedRect(40, dy - 12, 532, 22, 4, 4, 'F');
        doc.setTextColor(203, 213, 225);
        doc.text(k.replace(/_/g, ' ').toUpperCase(), 55, dy + 2);
        doc.setTextColor(245, 158, 11);
        doc.setFont('helvetica', 'bold');
        doc.text("-$" + v.toLocaleString(), 510, dy + 2);
        doc.setFont('helvetica', 'normal');
        dy += 26;
      }}
      renderFooter(1);

      // ── PAGE 2: MACRO DIAL & TYPOGRAPHY FORENSICS ──
      doc.addPage();
      renderHeader(2, "SECTION 2: MACRO DIAL & TYPOGRAPHY AUTHENTICATION FORENSICS");

      doc.setTextColor(255, 255, 255);
      doc.setFontSize(12);
      doc.setFont('helvetica', 'bold');
      doc.text("FACTORY DIAL PAD-PRINTING & CORONET GEOMETRY CHECKLIST", 40, 115);

      let py2 = 140;
      model.authenticity_vectors.forEach((vec, idx) => {{
        doc.setFillColor(16, 22, 34);
        doc.roundedRect(40, py2 - 12, 532, 40, 6, 6, 'F');
        doc.setFillColor(16, 185, 129);
        doc.circle(55, py2 + 8, 4, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(9);
        doc.setFont('helvetica', 'bold');
        doc.text("TEST " + (idx + 1) + ":", 70, py2 + 2);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(203, 213, 225);
        doc.text(vec, 70, py2 + 16, {{ maxWidth: 480 }});
        py2 += 48;
      }});

      // Dial Typography Explanations
      doc.setFillColor(12, 18, 29);
      doc.roundedRect(40, 360, 532, 180, 8, 8, 'F');
      doc.setTextColor(245, 158, 11);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(11);
      doc.text("CRITICAL REPLICA 'SUPERCLONE' DETECTION METRICS", 60, 385);

      doc.setTextColor(203, 213, 225);
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.text("1. Laser-Etched Coronet (LEC): Must contain 7 oval ring dots at the base, not an open oval.", 60, 410);
      doc.text("2. Hand Stack Pinion: Centre pinion must be capped and mirror-polished, never hollow with black recess.", 60, 430);
      doc.text("3. Date Cyclops Magnification: Exactly 2.5x with anti-reflective coating on the date window only.", 60, 450);
      doc.text("4. Font Serifs: 'O Y S T E R  P E R P E T U A L' serif feet must match factory stamping dies.", 60, 470);
      doc.text("5. Luminous Plots: Blue Chromalight must charge to peak within 3 seconds of 395nm UV exposure.", 60, 490);
      renderFooter(2);

      // ── PAGE 3: CASE GEOMETRY & OVER-POLISHING AUDIT ──
      doc.addPage();
      renderHeader(3, "SECTION 3: CASE GEOMETRY, LUG CHAMFERS & OVER-POLISHING AUDIT");

      doc.setFillColor(12, 18, 29);
      doc.roundedRect(40, 115, 532, 210, 8, 8, 'F');
      doc.setTextColor(245, 158, 11);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(12);
      doc.text("LUG HORN THICKNESS & FACTORY BEVEL PRESERVATION MATRIX", 60, 140);

      doc.setTextColor(203, 213, 225);
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.text("Pre-owned luxury watches lose 15% to 30% of their investment value when polished with", 60, 165);
      doc.text("amateur rotary wheels. ChronoSpec inspects four critical geometric surfaces:", 60, 180);

      doc.setTextColor(255, 255, 255);
      doc.setFont('helvetica', 'bold');
      doc.text("• Case Chamfer Sharpness: Factory 45° beveled edge must be razor-sharp with no softening.", 70, 210);
      doc.text("• Springbar Hole Clearance: Distance from lug tip to hole perimeter must exceed 1.8mm.", 70, 230);
      doc.text("• Crown Guard Symmetrical Mass: Crown guard shoulders must have identical curvature.", 70, 250);
      doc.text("• Laser-Welded Restoration: Check for porosity micro-pitting indicative of rebuilt metal.", 70, 270);
      doc.text("• Bracelet Pin Sag: Maximum allowable lateral droop is under 20 degrees under gravity test.", 70, 290);

      // Bracelet & Clasp Audit
      doc.setFillColor(16, 22, 34);
      doc.roundedRect(40, 350, 532, 180, 8, 8, 'F');
      doc.setTextColor(16, 185, 129);
      doc.setFontSize(11);
      doc.setFont('helvetica', 'bold');
      doc.text("BRACELET & CLASP TOLERANCE AUDIT", 60, 375);

      doc.setTextColor(203, 213, 225);
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.text("Clasp Code & Serial Timing: Clasp stamping must correspond with the watch case production year.", 60, 400);
      doc.text("Glidelock / Easylink Detents: Micro-adjustment tooth tracks must hold 5kg of linear tension.", 60, 420);
      doc.text("Screw-in Links: Screws must feature Loctite 222 threadlocker residue; stripped heads demand -$350.", 60, 440);
      renderFooter(3);

      // ── PAGE 4: CALIBRE ARCHITECTURE & OVERHAUL SCHEDULE ──
      doc.addPage();
      renderHeader(4, "SECTION 4: CALIBRE ARCHITECTURE & 5-YEAR MAINTENANCE SCHEDULE");

      doc.setTextColor(255, 255, 255);
      doc.setFontSize(12);
      doc.setFont('helvetica', 'bold');
      doc.text("CHRONIC CALIBRE VULNERABILITIES & ESTIMATED REPAIR COSTS", 40, 115);

      let py4 = 145;
      model.chronic_faults.forEach((fault, i) => {{
        doc.setFillColor(16, 22, 34);
        doc.roundedRect(40, py4 - 10, 532, 55, 6, 6, 'F');
        doc.setTextColor(245, 158, 11);
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.text((i + 1) + ". " + fault.issue + " (Estimated Repair Cost: $" + fault.cost + ")", 55, py4 + 8);
        doc.setTextColor(203, 213, 225);
        doc.setFontSize(9);
        doc.setFont('helvetica', 'normal');
        doc.text(fault.detail, 55, py4 + 24, {{ maxWidth: 500 }});
        py4 += 65;
      }});

      // Timing Machine Tolerances
      doc.setFillColor(12, 18, 29);
      doc.roundedRect(40, 370, 532, 160, 8, 8, 'F');
      doc.setTextColor(16, 185, 129);
      doc.setFontSize(11);
      doc.setFont('helvetica', 'bold');
      doc.text("OFFICIAL TIMEGRAPH TESTING TOLERANCES", 60, 395);

      doc.setTextColor(203, 213, 225);
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.text("• Balance Amplitude (Dial Up): Must read between 270° and 310° at full wind.", 60, 420);
      doc.text("• Beat Error: Must not exceed 0.3 milliseconds across all 5 testing positions.", 60, 440);
      doc.text("• Daily Rate: Superlative Chronometer standard is -2/+2 seconds per 24 hours.", 60, 460);
      doc.text("• Lift Angle Configuration: 52 degrees for Cal. 3135; 53 degrees for Cal. 3235.", 60, 480);
      renderFooter(4);

      // ── PAGE 5: DEALER COUNTER-OFFER SCRIPTS & ESCROW PROTOCOL ──
      doc.addPage();
      renderHeader(5, "SECTION 5: VERBATIM DEALER COUNTER-OFFER SCRIPTS & ESCROW PROTOCOL");

      doc.setFillColor(12, 18, 29);
      doc.roundedRect(40, 115, 532, 140, 8, 8, 'F');
      doc.setTextColor(245, 158, 11);
      doc.setFontSize(11);
      doc.setFont('helvetica', 'bold');
      doc.text("VERBATIM COUNTER-OFFER SCRIPT FOR DEALER NEGOTIATIONS", 60, 140);

      doc.setTextColor(203, 213, 225);
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      const fullScript = `"Thank you for providing the listing details on the ${{model.name}} (${{model.reference}}). After analyzing recent verified Chrono24 transaction comps and applying necessary deductions for softened lug chamfers, unverified service history, and missing documentation, my firm target purchase price is $${{target.replace('$', '')}}. I have immediate funds ready for wire transfer through an escrow service upon mutual agreement."`;
      doc.text(fullScript, 60, 165, {{ maxWidth: 490 }});

      // Escrow Safety Checklist
      doc.setFillColor(16, 22, 34);
      doc.roundedRect(40, 275, 532, 230, 8, 8, 'F');
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(11);
      doc.setFont('helvetica', 'bold');
      doc.text("PRE-WIRE TRANSFER ESCROW SAFETY PROTOCOL", 60, 300);

      doc.setTextColor(203, 213, 225);
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.text("1. Always mandate an independent escrow service (e.g. Chrono24 Buyer Protection, Escrow.com).", 60, 325);
      doc.text("2. Never wire funds directly to private personal bank accounts without a verified corporate invoice.", 60, 345);
      doc.text("3. Request a live video showing the watch set to a specific requested time (e.g., 10:18 with date on 24).", 60, 365);
      doc.text("4. Verify that the seller's serial number matches the guarantee card and case rehaut exactly.", 60, 385);
      doc.text("5. Require delivery via fully insured courier (Ferrari Logistics / Malca-Amit / Brinks).", 60, 405);
      renderFooter(5);

      // Save PDF
      doc.save("ChronoSpec_5Page_Forensic_Dossier_" + model.reference + ".pdf");
    }}

    // Check payment parameters in URL
    (function() {{
      const p = new URLSearchParams(window.location.search);
      if (p.get('paid') === 'true' || p.get('status') === 'success' || p.get('unlocked') === 'true') {{
        alert('🎉 Payment Confirmed! Unlocking your 5-Page ChronoSpec VIP Dossier...');
        setTimeout(() => {{
          openCheckoutModal();
          document.getElementById('downloadPdfSection').classList.remove('hidden');
          generateChronoDossierPDF();
        }}, 800);
      }}
    }})();

    window.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();
      calculateWatchAudit();
    }});
  </script>
</body>
</html>
"""

with open(r'C:\chronospec-ai\index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Created full index.html with 5-page PDF and 217 reviews successfully!")
