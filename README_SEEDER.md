# 🌱 Brilink Database Seeder

Seeder untuk mengisi database dengan data dummy transaksi dan cash flow untuk testing dan development.

## 📋 Prerequisites

Pastikan database sudah memiliki data master berikut:
- Services (minimal 1 service)
- EDC Machines (minimal 1 EDC)
- Agent Profiles (minimal 1 agent)
- Users dengan role 'kasir' (minimal 1 kasir)
- Service Fees (untuk perhitungan biaya service)
- Bank Fees (untuk perhitungan biaya bank)

## 🚀 Cara Penggunaan

### 1. Jalankan Seeder

#### **Command Line Mode (Direct - Recommended):**
```bash
cd f:\develop\FLUTTER\backend_brilink_v2

# Clear existing data and seed new data
python seeder.py --clear-and-seed

# Add additional data (keep existing)
python seeder.py --add-data

# Seed only transactions (default: 50)
python seeder.py --transactions
python seeder.py --transactions 100

# Seed only cash flows (default: 30)
python seeder.py --cashflows
python seeder.py --cashflows 50

# Show statistics only
python seeder.py --stats
```

#### **Interactive Mode (Menu):**
```bash
python seeder.py
```

#### **Windows Batch File:**
```bash
run_seeder.bat
```

### 2. Pilih Opsi (Interactive Mode)

Seeder akan menampilkan menu berikut:

```
🌱 Brilink Database Seeder
==================================================
📊 Current Database Statistics:
----------------------------------------
Transactions: 0
Cash Flows: 0
Services: 5
EDC Machines: 2
Agents: 1
Users: 3

Options:
1. Clear existing data and seed new data
2. Seed additional data (keep existing)
3. Seed only transactions
4. Seed only cash flows
5. Show statistics only

Choose option (1-5):
```

### 3. Opsi yang Tersedia

#### **Opsi 1: Clear existing data and seed new data**
- Menghapus semua data transaksi dan cash flow yang ada
- Membuat 50 transaksi baru
- Membuat 30 cash flow baru

#### **Opsi 2: Seed additional data (keep existing)**
- Menambah data tanpa menghapus yang sudah ada
- Membuat 25 transaksi tambahan
- Membuat 15 cash flow tambahan

#### **Opsi 3: Seed only transactions**
- Hanya membuat data transaksi
- User bisa tentukan jumlah (default: 50)

#### **Opsi 4: Seed only cash flows**
- Hanya membuat data cash flow
- User bisa tentukan jumlah (default: 30)

#### **Opsi 5: Show statistics only**
- Hanya menampilkan statistik database saat ini

## 📊 Data yang Dihasilkan

### Transaksi
- **Transaction Number**: TXN + timestamp + random suffix
- **Amount**: Bervariasi berdasarkan kategori service
  - Transfer: 50rb - 2jt
  - Pulsa: 25rb, 50rb, 100rb, 150rb, 200rb
  - PLN: 20rb - 2jt
  - Lainnya: 10rb - 500rb
- **Fees**: Diambil dari tabel service_fees dan bank_fees
- **Customer Names**: 16 nama Indonesia realistik
- **Dates**: Random dalam 30 hari terakhir
- **Target Numbers**: Generated untuk service yang requires_target

### Cash Flow
- **Type**: 60% cash_in, 40% cash_out
- **Sources**: 12 sumber pemasukan, 12 sumber pengeluaran
- **Amount**:
  - Cash In: 50rb - 2jt
  - Cash Out: 25rb - 500rb
- **Descriptions**: Auto-generated dengan konteks bulan dan tahun

## 📈 Statistik Database

Seeder akan menampilkan statistik sebelum dan sesudah seeding:

```
📊 Current Database Statistics:
----------------------------------------
Transactions: 50
Cash Flows: 30
Services: 5
EDC Machines: 2
Agents: 1
Users: 3
Total Revenue: Rp 25,000,000
Total Cash In: Rp 15,000,000
Total Cash Out: Rp 8,000,000
Net Cash Flow: Rp 7,000,000
```

## 🔧 Troubleshooting

### Error: Missing required data
**Solusi**: Pastikan data master sudah ada. Jalankan seeder untuk services, EDC, agents, dan users terlebih dahulu.

### Error: Foreign key constraint
**Solusi**: Pastikan ID yang direferensikan valid. Cek database untuk memastikan data master lengkap.

### Error: Duplicate transaction number
**Solusi**: Transaction number menggunakan timestamp, seharusnya unik. Jika masih duplicate, cek sistem clock.

## 💡 Tips Penggunaan

1. **Development**: Gunakan opsi 1 untuk fresh data setiap kali develop
2. **Testing**: Gunakan opsi 2 untuk menambah data tanpa kehilangan existing
3. **Performance Testing**: Jalankan multiple kali untuk data besar
4. **Demo**: Gunakan opsi 1 dengan data yang sudah di-prepare

## 🎯 Testing API

Setelah seeding, test API berikut:

### Dashboard
```bash
GET /api/dashboard
GET /api/dashboard/cards/total-revenue-today
GET /api/dashboard/cards/saldo-tunai
GET /api/dashboard/cards/saldo-edc
GET /api/dashboard/cards/total-transactions-today
GET /api/dashboard/cards/recent-transactions
```

### Reports
```bash
GET /api/reports?period=daily
GET /api/reports?period=weekly
GET /api/reports?period=monthly
GET /api/reports?period=custom&start_date=2025-01-01&end_date=2025-01-31
```

### Transactions & Cash Flow
```bash
GET /api/transactions
GET /api/cash-flows
```

## 🔄 Re-run Seeder

Seeder bisa dijalankan berulang kali tanpa masalah. Gunakan opsi yang sesuai:

- **Fresh start**: Opsi 1
- **Add more data**: Opsi 2
- **Specific data**: Opsi 3 atau 4

---

**Happy Seeding! 🌱**