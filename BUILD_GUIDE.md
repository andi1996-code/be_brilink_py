# Brilink Backend API - EXE Build Guide

## 📋 Deskripsi

Project ini adalah backend API untuk sistem Brilink yang dapat di-build menjadi executable Windows (.exe) dengan konfigurasi database yang dinamis melalui GUI.

## ✨ Fitur Baru

1. **GUI Konfigurasi Database** - Interface grafis untuk mengatur koneksi database
2. **Test Koneksi** - Validasi koneksi database sebelum start server
3. **Konfigurasi Dinamis** - Tidak perlu edit file .env secara manual
4. **Single EXE File** - Mudah didistribusikan tanpa perlu install Python
5. **Save Configuration** - Menyimpan konfigurasi untuk penggunaan selanjutnya

## 🚀 Cara Build EXE

### Persiapan

1. **Pastikan Python terinstall** (Python 3.8+)
   ```bash
   python --version
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Atau jika menggunakan virtual environment:
   ```bash
   # Buat virtual environment
   python -m venv venv
   
   # Aktifkan virtual environment
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### Build Process

**Metode 1: Menggunakan Batch File (Mudah)**
```bash
build_exe.bat
```

**Metode 2: Menggunakan Python Script**
```bash
python build_exe.py
```

**Metode 3: Manual dengan PyInstaller**
```bash
pyinstaller --clean --noconfirm launcher.spec
```

### Hasil Build

Setelah build berhasil, Anda akan menemukan:
- **Folder `dist/`** - Berisi file executable
- **File `BrilinkBackend.exe`** - Aplikasi yang siap dijalankan
- **File `README.txt`** - Panduan penggunaan

## 💻 Cara Menggunakan EXE

### 1. Run Aplikasi

Double-click file `BrilinkBackend.exe` atau jalankan dari command prompt:
```bash
BrilinkBackend.exe
```

### 2. Konfigurasi Database (Pertama Kali)

Saat pertama kali dijalankan, akan muncul window konfigurasi:

**Isi Data Database:**
- **Host**: `localhost` atau IP server MySQL
- **Port**: `3306` (default MySQL)
- **Database Name**: `db_api_brilink`
- **Username**: Username MySQL Anda
- **Password**: Password MySQL Anda
- **Secret Key**: Kunci rahasia untuk JWT (bisa random string)

### 3. Test Koneksi

1. Klik tombol **"🔌 Test Connection"**
2. Tunggu proses validasi
3. Jika berhasil, tombol **"Save & Start Server"** akan aktif

### 4. Start Server

1. Klik tombol **"✅ Save & Start Server"**
2. Server akan mulai berjalan di `http://localhost:5000`
3. Akses API endpoint sesuai kebutuhan

### 5. Penggunaan Selanjutnya

Jika Anda sudah pernah mengkonfigurasi:
- Aplikasi akan menggunakan konfigurasi yang tersimpan
- Anda bisa memilih menggunakan konfigurasi lama atau konfigurasi ulang
- File konfigurasi tersimpan di `db_config.json` dan `.env`

## 📁 File Konfigurasi

### .env File
File ini dibuat otomatis saat Anda save konfigurasi:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_api_brilink
DB_USER=root
DB_PASSWORD=yourpassword
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

### db_config.json
File ini menyimpan konfigurasi (tanpa password) untuk kemudahan:
```json
{
    "DB_HOST": "localhost",
    "DB_PORT": "3306",
    "DB_NAME": "db_api_brilink",
    "DB_USER": "root",
    "DB_PASSWORD": "",
    "SECRET_KEY": "your-secret-key-here"
}
```

## 🔧 Troubleshooting

### Build Error

**Problem**: PyInstaller tidak terinstall
```bash
# Solution
pip install pyinstaller
```

**Problem**: Import errors saat build
```bash
# Solution: Pastikan semua dependencies terinstall
pip install -r requirements.txt
```

**Problem**: Missing modules
```bash
# Edit launcher.spec dan tambahkan module yang hilang di hiddenimports
```

### Runtime Error

**Problem**: Database connection failed
- ✅ Cek MySQL server sudah running
- ✅ Cek username dan password benar
- ✅ Cek firewall tidak memblokir koneksi
- ✅ Cek user memiliki permission yang cukup

**Problem**: Port 5000 sudah digunakan
- ✅ Tutup aplikasi lain yang menggunakan port 5000
- ✅ Atau edit `launcher.py` untuk menggunakan port lain

**Problem**: Executable tidak bisa dibuka
- ✅ Run as Administrator
- ✅ Cek antivirus tidak memblokir
- ✅ Cek di folder dist/ bukan di folder build/

## 📚 API Endpoints

Setelah server running, Anda bisa akses:

- **Health Check**: `http://localhost:5000/health`
- **Authentication**: `http://localhost:5000/auth/*`
- **Agents**: `http://localhost:5000/agents/*`
- **Transactions**: `http://localhost:5000/transactions/*`
- **Reports**: `http://localhost:5000/reports/*`
- Dan lainnya...

Lihat `Brilink_API.postman_collection.json` untuk detail semua endpoint.

## 📦 Distribusi EXE

### Cara Distribusi:

1. **Copy folder `dist/`** ke komputer target
2. **Pastikan MySQL Server tersedia** di komputer target atau network
3. **Run `BrilinkBackend.exe`**
4. **Konfigurasi database** sesuai environment target

### Yang Perlu Disertakan:

```
dist/
├── BrilinkBackend.exe    # File executable utama
├── README.txt            # Panduan penggunaan
└── (optional) Postman collection untuk testing
```

### Sistem Requirements:

- Windows 7/8/10/11 (64-bit)
- MySQL Server 5.7+ (bisa remote)
- Minimal 100MB free space
- Network access ke MySQL server

## 🔐 Security Notes

1. **Secret Key**: Gunakan string yang kuat dan unik untuk production
2. **Database Password**: Tidak disimpan dalam `db_config.json`
3. **HTTPS**: Untuk production, gunakan reverse proxy dengan HTTPS
4. **Firewall**: Pastikan hanya port yang diperlukan yang terbuka

## 🛠️ Development vs Production

### Development
```bash
# Run dengan Python biasa
python launcher.py

# Atau run app.py langsung
python app.py
```

### Production (EXE)
```bash
# Build dulu
python build_exe.py

# Lalu jalankan EXE
dist\BrilinkBackend.exe
```

## 📝 Catatan Penting

1. **Database**: Pastikan MySQL server sudah running sebelum start aplikasi
2. **First Run**: Database dan tables akan dibuat otomatis jika belum ada
3. **Seeder**: Jika perlu data awal, jalankan seeder terpisah sebelum convert ke EXE
4. **Updates**: Setiap update code, perlu build ulang EXE

## 🤝 Support

Jika mengalami masalah:
1. Cek log di console window
2. Cek file `.env` sudah benar
3. Test koneksi database manual
4. Cek versi Python dan dependencies

## 📄 License

Sesuai dengan lisensi project Brilink Backend API.

---

**Last Updated**: November 2025
**Version**: 2.0
