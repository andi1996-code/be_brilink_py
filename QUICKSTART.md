# 🚀 Quick Start - Brilink Backend EXE

## Langkah Cepat: Development ke EXE

### 1️⃣ Persiapan (Satu Kali Saja)

```bash
# Install semua dependencies
pip install -r requirements.txt
```

### 2️⃣ Test GUI Konfigurasi (Optional)

```bash
# Test GUI sebelum build
test_gui.bat
```

atau

```bash
python database_config_gui.py
```

### 3️⃣ Build EXE

```bash
# Cara termudah - jalankan batch file
build_exe.bat
```

Tunggu proses build selesai (± 2-5 menit)

### 4️⃣ Jalankan EXE

```bash
cd dist
BrilinkBackend.exe
```

## 🎯 Alur Penggunaan EXE

```
1. Double-click BrilinkBackend.exe
   ↓
2. Window GUI muncul
   ↓
3. Input konfigurasi database:
   • Host: localhost
   • Port: 3306
   • DB Name: db_api_brilink
   • Username: root
   • Password: [your password]
   • Secret Key: [random string]
   ↓
4. Klik "Test Connection"
   ↓
5. Jika sukses, klik "Save & Start Server"
   ↓
6. Server running di http://localhost:5000
```

## ✅ Checklist Sebelum Build

- [ ] MySQL Server terinstall dan running
- [ ] Python 3.8+ terinstall
- [ ] Semua dependencies terinstall (`pip install -r requirements.txt`)
- [ ] Tidak ada error saat run `python launcher.py`
- [ ] Port 5000 tidak digunakan aplikasi lain

## 📂 Struktur File Penting

```
backend_brilink_v2/
│
├── launcher.py                 # Main entry point
├── database_config_gui.py      # GUI untuk konfigurasi
├── launcher.spec              # Spec file PyInstaller
├── build_exe.py               # Script build otomatis
├── build_exe.bat              # Batch file untuk build
│
├── app.py                     # Flask application
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
│
└── dist/                      # Hasil build (setelah build)
    └── BrilinkBackend.exe     # File executable
```

## 🔧 Konfigurasi yang Disimpan

Setelah konfigurasi pertama, file berikut dibuat:

1. **`.env`** - Konfigurasi runtime
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=db_api_brilink
   DB_USER=root
   DB_PASSWORD=yourpassword
   SECRET_KEY=your-secret-key
   FLASK_ENV=production
   ```

2. **`db_config.json`** - Cache konfigurasi (tanpa password)
   ```json
   {
       "DB_HOST": "localhost",
       "DB_PORT": "3306",
       "DB_NAME": "db_api_brilink",
       "DB_USER": "root",
       "SECRET_KEY": "your-secret-key"
   }
   ```

## 🎨 Fitur GUI

### Window Konfigurasi
- ✅ Input Host, Port, Database Name
- ✅ Input Username & Password (dengan show/hide)
- ✅ Input Secret Key untuk JWT
- ✅ Tombol Test Connection
- ✅ Log area untuk status
- ✅ Auto-save konfigurasi sebelumnya

### Test Connection
- Validasi koneksi ke MySQL
- Cek apakah database exists
- Buat database jika belum ada
- Tampilkan status di log area

### Save & Start
- Simpan konfigurasi ke `.env`
- Auto-start Flask server
- Tampilkan URL endpoint

## 🐛 Troubleshooting Cepat

### Build Gagal
```bash
# Clear cache dan build ulang
rmdir /s /q build dist
python build_exe.py
```

### GUI Tidak Muncul
```bash
# Pastikan tkinter terinstall
python -m tkinter
```

### Connection Failed
- Cek MySQL running: `services.msc` → MySQL
- Cek username/password benar
- Cek firewall tidak block port 3306

### EXE Tidak Jalan
- Run as Administrator
- Cek antivirus tidak block
- Cek di folder `dist/` bukan `build/`

## 📱 Cara Distribusi

### Untuk End User:
1. Copy folder `dist/` ke komputer target
2. Pastikan MySQL accessible (local atau remote)
3. Double-click `BrilinkBackend.exe`
4. Configure dan start!

### File yang Perlu Didistribusikan:
```
📦 BrilinkBackend-Package/
├── BrilinkBackend.exe
├── README.txt
└── Brilink_API.postman_collection.json (optional)
```

## 🔄 Update Aplikasi

Jika ada perubahan code:

```bash
# 1. Update code
git pull
# atau edit manual

# 2. Build ulang
python build_exe.py

# 3. Distribusikan dist/BrilinkBackend.exe yang baru
```

## 💡 Tips & Tricks

### Development
```bash
# Run langsung tanpa build (untuk testing)
python launcher.py
```

### Production
```bash
# Build sekali, jalankan berkali-kali
python build_exe.py
dist\BrilinkBackend.exe
```

### Custom Port
Edit `launcher.py` line dengan `app.run()`:
```python
app.run(host='0.0.0.0', port=8080)  # Ganti 5000 ke 8080
```

### Custom Secret Key Generator
```python
import secrets
print(secrets.token_hex(32))
```

## 📞 Bantuan

Jika ada masalah:
1. Cek `BUILD_GUIDE.md` untuk detail lengkap
2. Cek console output untuk error message
3. Cek file `.env` sudah terbuat dengan benar
4. Test koneksi database manual dengan MySQL Workbench

---

**Happy Building! 🎉**
