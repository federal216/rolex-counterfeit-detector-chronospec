# ChronoSpec AI - Payment Gateways & Merchant Account Registry

**Son Güncelleme:** 25 Kasım 2026  
**Yönetici:** İbrahim Karakoç (`karakoc.i@gmail.com`)  
**GitHub:** [federal216/rolex-counterfeit-detector-chronospec](https://github.com/federal216/rolex-counterfeit-detector-chronospec.git)

---

## 1. Dodo Payments (Merchant of Record - Aktif Entegrasyon)
- **Portal:** [https://dodopayments.com/](https://dodopayments.com/)
- **Kullanıcı Hesabı:** `karakoc.i@gmail.com`
- **Business ID:** `bus_0NsdOsgyw5JvaPeKIIn2R`
- **Live Product ID:** `pdt_0NsdaQ7P6h6NjAauG3k4P` ($89.00 USD)
- **Desteklenen Ödeme Tipleri:** Apple Pay, Google Pay, Global Kredi/Banka Kartları (Visa, Mastercard, Amex)
- **Entegrasyon Dosyaları:**
  - `api/dodo/initialize.js` (Checkout oturumu başlatıcı)
  - `server.js` (`/api/dodo/initialize` endpoint'i)
  - `index.html` (Modal içi 1-tık checkout)
- **Durum:** ✅ Sitede ve Kodda Aktif

---

## 2. Whop (Merchant of Record - Aktif Ödeme Altyapısı)
- **Portal:** [https://whop.com/](https://whop.com/)
- **Checkout URL:** [https://whop.com/cabinetscan-ai/chronospec-ai-vip-watch-appraisal-dossier](https://whop.com/cabinetscan-ai/chronospec-ai-vip-watch-appraisal-dossier)
- **Desteklenen Ödeme Tipleri:** Apple Pay, Google Pay, Global Kredi Kartları
- **Durum:** ✅ Sitede ve Kodda Aktif

---

## 3. Web3 Kripto Ödemeleri
- **Ağlar:** USDT (TRC-20) / USDC (ERC-20)
- **Tutar:** $89.00
- **Durum:** ✅ Kodda aktif ve hazır

---

## 4. Payout Banka Bilgileri (Payoneer Citibank US)
Dodo Payments ve Whop payout alanlarına girilecek global hesap bilgileri:
- **Banka Adı:** Citibank, N.A.
- **Banka Adresi:** 111 Wall Street, New York, NY 10043, USA
- **Routing / ABA (EFT):** `031100209`
- **Hesap Numarası:** `70580640002590994`
- **Hesap Türü:** Checking (Vadesiz)
- **Lehdar:** İbrahim Karakoç
