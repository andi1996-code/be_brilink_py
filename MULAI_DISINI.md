# 🚀 CARA MENGGUNAKAN - Brilink Backend EXE

## Langkah Paling Mudah (Untuk Pemula)

### 1. Buka Menu Master
```
Double-click: MENU.bat
```

### 2. Pilih Menu
- **Menu 7**: Install Dependencies (pertama kali saja)
- **Menu 1**: Check Requirements (pastikan semua OK)
- **Menu 4**: Build EXE
- **Menu 5**: Run EXE

Selesai! ✅

---

## Langkah Manual (Untuk Developer)

### A. Persiapan Awal (Sekali Saja)

1. **Install Python 3.8+**
   - Download dari python.org
   - Pastikan "Add to PATH" dicentang saat install

2. **Install MySQL**
   - Download dan install MySQL Server
   - Catat username dan password

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### B. Build Executable

1. **Check Requirements**
   ```bash
   python check_requirements.py
   ```
   Pastikan semua ✅

2. **Build EXE**
   ```bash
   python build_exe.py
   ```
   Tunggu 2-5 menit

3. **Hasil Build**
   - File EXE ada di folder `dist/`
   - Nama file: `BrilinkBackend.exe`

### C. Jalankan Aplikasi

1. **Run EXE**
   ```bash
   cd dist
   BrilinkBackend.exe
   ```

2. **Konfigurasi Database**
   - Window GUI akan muncul
   - Isi form:
     - Host: `localhost`
     - Port: `3306`
     - Database: `db_api_brilink`
     - Username: `root`
     - Password: `[password MySQL Anda]`
     - Secret Key: `[string random]`

3. **Test Connection**
   - Klik tombol "Test Connection"
   - Tunggu sampai ✅ sukses

4. **Start Server**
   - Klik "Save & Start Server"
   - Server jalan di: `http://localhost:5000`

---

## Testing API

1. **Health Check**
   - Buka browser: `http://localhost:5000/health`
   - Harus return JSON status OK

2. **Import Postman Collection**
   - File: `Brilink_API.postman_collection.json`
   - Import ke Postman
   - Test semua endpoint

3. **Login**
   ```
   POST http://localhost:5000/auth/login
   Body: {
     "username": "admin",
     "password": "admin123"
   }
   ```
   - Copy token dari response
   - Gunakan untuk endpoint lain

---

## FAQ (Pertanyaan Sering Ditanya)

### Q: Build EXE gagal terus?
**A:** Coba langkah ini:
1. Hapus folder `build` dan `dist`
2. Run `pip install --upgrade pyinstaller`
3. Build ulang

### Q: Database connection failed?
**A:** Pastikan:
1. MySQL service running (cek Task Manager)
2. Username/password benar
3. Port 3306 tidak diblokir firewall

### Q: GUI tidak muncul?
**A:** Coba:
1. Test dengan `python database_config_gui.py`
2. Install ulang Python dengan tkinter
3. Run as Administrator

### Q: Port 5000 sudah digunakan?
**A:** Edit `launcher.py`:
```python
app.run(host='0.0.0.0', port=8080)  # Ganti ke port lain
```

### Q: Bagaimana cara update aplikasi?
**A:**
1. Edit code yang perlu diubah
2. Run `python build_exe.py` lagi
3. EXE baru akan dibuat di folder `dist/`

### Q: Bisa running tanpa build EXE?
**A:** Bisa! Run langsung:
```bash
python launcher.py
```

---

## Troubleshooting Cepat

| Masalah | Solusi |
|---------|--------|
| Import error saat build | `pip install -r requirements.txt` |
| PyInstaller not found | `pip install pyinstaller` |
| Tkinter error | Reinstall Python dengan tcl/tk |
| MySQL not found | Install MySQL Server |
| Port conflict | Ganti port di `launcher.py` |
| Permission denied | Run as Administrator |
| Antivirus block | Tambahkan exception |

---

## File & Folder Penting

```
📁 backend_brilink_v2/
│
├── 🎯 MENU.bat                    ← START DI SINI!
├── 📖 MULAI_DISINI.md            ← File ini
│
├── 🔧 Tools
│   ├── check_requirements.bat
│   ├── build_exe.bat
│   ├── run_launcher.bat
│   └── test_gui.bat
│
├── 📱 Python Files
│   ├── launcher.py               ← Main entry
│   ├── database_config_gui.py    ← GUI config
│   ├── build_exe.py              ← Build script
│   └── check_requirements.py     ← Check tools
│
├── 📚 Documentation
│   ├── README_EXE.md             ← Dokumentasi lengkap
│   ├── QUICKSTART.md             ← Panduan cepat
│   └── BUILD_GUIDE.md            ← Panduan build detail
│
└── 📦 Hasil Build
    └── dist/
        └── BrilinkBackend.exe    ← Executable final
```

---

## Kontak & Support

Jika masih ada masalah:
1. Baca file README_EXE.md
2. Cek console output untuk error message
3. Cek file .env sudah terbuat
4. Test koneksi MySQL manual

---

## Tips Untuk Production

1. **Secret Key**
   - Gunakan string random yang kuat
   - Generate dengan: `python -c "import secrets; print(secrets.token_hex(32))"`

2. **Database**
   - Backup database secara berkala
   - Gunakan user MySQL khusus (bukan root)
   - Set permission minimal yang diperlukan

3. **Network**
   - Gunakan reverse proxy (nginx/apache) untuk HTTPS
   - Batasi akses dengan firewall
   - Monitor logs dan performance

4. **Distribution**
   - Zip folder `dist/` untuk distribusi
   - Include README.txt di dalam
   - Provide MySQL access info

---

**Selamat Menggunakan! 🎉**

Made with ❤️ for Brilink
November 2025
