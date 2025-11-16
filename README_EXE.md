# 🏦 Brilink Backend API v2.0 - Executable Edition

Backend API untuk sistem Brilink dengan kemampuan build menjadi Windows Executable (.exe) dan konfigurasi database dinamis melalui GUI.

## 🌟 Fitur Utama

### ✨ Fitur Baru (v2.0)
- **GUI Konfigurasi Database** - Interface grafis untuk setup database
- **Test Koneksi Real-time** - Validasi koneksi sebelum start server
- **Build ke EXE** - Single executable file, mudah didistribusikan
- **Konfigurasi Dinamis** - User bisa input database credentials sendiri
- **Auto Database Creation** - Database dibuat otomatis jika belum ada

### 📋 Fitur API
- Autentikasi & Autorisasi (JWT)
- Manajemen Agent
- Manajemen EDC Machine
- Transaksi & Cash Flow
- Service & Fee Management
- Dashboard & Reports
- Export PDF Reports

## 🚀 Quick Start

### Untuk Development

```bash
# 1. Clone repository
git clone <repository-url>
cd backend_brilink_v2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run dengan launcher
python launcher.py
```

### Untuk Build EXE

```bash
# 1. Check requirements
python check_requirements.py

# 2. Build executable
python build_exe.py
# atau
build_exe.bat

# 3. Jalankan EXE
cd dist
BrilinkBackend.exe
```

## 📚 Dokumentasi Lengkap

- **[QUICKSTART.md](QUICKSTART.md)** - Panduan cepat memulai
- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - Panduan lengkap build EXE
- **[README_SEEDER.md](README_SEEDER.md)** - Panduan seeder data

## 📂 Struktur Project

```
backend_brilink_v2/
│
├── 🚀 Launcher & Build Scripts
│   ├── launcher.py                # Main entry point
│   ├── database_config_gui.py     # GUI konfigurasi database
│   ├── launcher.spec              # PyInstaller spec file
│   ├── build_exe.py               # Script build otomatis
│   ├── check_requirements.py      # Check dependencies
│   └── *.bat                      # Batch files helper
│
├── 📱 Application Core
│   ├── app.py                     # Flask application factory
│   ├── config.py                  # Configuration
│   ├── main.py                    # Alternative entry point
│   └── seeder.py                  # Database seeder
│
├── 📦 Models (Database)
│   ├── user.py
│   ├── agent_profile.py
│   ├── transaction.py
│   ├── cash_flow.py
│   ├── edc_machine.py
│   ├── service.py
│   ├── service_fee.py
│   └── bank_fee.py
│
├── 🛣️ Routes (API Endpoints)
│   ├── auth.py                    # Login, register
│   ├── agent.py                   # Agent management
│   ├── transaction.py             # Transactions
│   ├── cash_flow.py               # Cash flow tracking
│   ├── edc.py                     # EDC machines
│   ├── service.py                 # Services
│   ├── service_fee.py             # Service fees
│   ├── bank_fee.py                # Bank fees
│   ├── dashboard.py               # Dashboard data
│   ├── reports.py                 # Report generation
│   └── health.py                  # Health check
│
├── 🔧 Utils
│   ├── jwt_handler.py             # JWT authentication
│   ├── response.py                # Standard responses
│   └── validators.py              # Input validation
│
├── 📖 Documentation
│   ├── README.md                  # This file
│   ├── QUICKSTART.md              # Quick start guide
│   ├── BUILD_GUIDE.md             # Build guide
│   └── README_SEEDER.md           # Seeder guide
│
└── 📦 Config & Dependencies
    ├── requirements.txt           # Python dependencies
    ├── .env                       # Environment config (generated)
    ├── db_config.json             # Saved config (generated)
    └── Brilink_API.postman_collection.json
```

## 🎯 Cara Kerja Aplikasi

### 1. Development Mode

```
User → python launcher.py
         ↓
    Database Config GUI
         ↓
    Test Connection
         ↓
    Flask Server Start
         ↓
    API Ready di http://localhost:5000
```

### 2. Production Mode (EXE)

```
User → BrilinkBackend.exe
         ↓
    Check .env exists
         ↓
    Database Config GUI (jika perlu)
         ↓
    Test Connection
         ↓
    Flask Server Start
         ↓
    API Ready di http://localhost:5000
```

## 🔧 File Konfigurasi

### .env (Auto-generated)
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_api_brilink
DB_USER=root
DB_PASSWORD=yourpassword
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

### db_config.json (Auto-generated)
```json
{
    "DB_HOST": "localhost",
    "DB_PORT": "3306",
    "DB_NAME": "db_api_brilink",
    "DB_USER": "root",
    "SECRET_KEY": "your-secret-key-here"
}
```

## 🛠️ Batch Files Helper

| File | Deskripsi |
|------|-----------|
| `check_requirements.bat` | Cek dependencies sebelum build |
| `build_exe.bat` | Build executable |
| `run_launcher.bat` | Run launcher untuk testing |
| `test_gui.bat` | Test GUI konfigurasi |
| `run.bat` | Run Flask app langsung |
| `run_seeder.bat` | Run database seeder |

## 📡 API Endpoints

Base URL: `http://localhost:5000`

### Health Check
- `GET /health` - Check API status

### Authentication
- `POST /auth/register` - Register user baru
- `POST /auth/login` - Login dan dapatkan token

### Agents
- `GET /agents` - List semua agent
- `GET /agents/:id` - Detail agent
- `POST /agents` - Tambah agent
- `PUT /agents/:id` - Update agent
- `DELETE /agents/:id` - Hapus agent

### Transactions
- `GET /transactions` - List transaksi
- `POST /transactions` - Tambah transaksi
- `GET /transactions/:id` - Detail transaksi

### Dashboard
- `GET /dashboard/summary` - Summary data
- `GET /dashboard/stats` - Statistics

### Reports
- `GET /reports/daily` - Daily report
- `GET /reports/monthly` - Monthly report
- `GET /reports/export` - Export to PDF

*Lihat `Brilink_API.postman_collection.json` untuk detail lengkap*

## 💻 System Requirements

### Development
- Python 3.8+
- MySQL Server 5.7+
- 200MB disk space

### Running EXE
- Windows 7/8/10/11 (64-bit)
- MySQL Server 5.7+ (local/remote)
- 100MB disk space
- Network access ke MySQL

## 🐛 Troubleshooting

### Build Issues

**PyInstaller Error**
```bash
pip install --upgrade pyinstaller
```

**Missing Module**
```bash
pip install -r requirements.txt
```

### Runtime Issues

**Database Connection Failed**
- ✅ Cek MySQL running
- ✅ Cek credentials benar
- ✅ Cek firewall settings

**Port 5000 Sudah Digunakan**
- Edit `launcher.py`, ganti port di `app.run()`

**Tkinter Error**
- Reinstall Python dengan tcl/tk support

## 🔐 Security Considerations

1. **Production Deployment**
   - Gunakan strong secret key
   - Aktifkan HTTPS via reverse proxy
   - Batasi akses database
   - Gunakan firewall

2. **Credentials**
   - Jangan commit `.env` ke Git
   - Gunakan environment-specific configs
   - Rotate secret keys secara berkala

3. **API Security**
   - Semua endpoint (kecuali health & auth) perlu JWT
   - Validasi input di semua endpoint
   - Rate limiting untuk production

## 📦 Distribusi

### Untuk Internal Team
```
1. Share folder dist/
2. Include README.txt
3. Provide MySQL access
```

### Untuk Client
```
1. Build EXE
2. Package dengan installer (optional)
3. Provide setup guide
4. Provide support
```

## 🔄 Update & Maintenance

### Update Code
```bash
git pull
python check_requirements.py
python build_exe.py
```

### Database Migration
```bash
# Backup database
mysqldump db_api_brilink > backup.sql

# Update models
# Edit models/*.py

# Rebuild dan restart
python build_exe.py
```

## 📞 Support

- **Documentation**: Lihat folder docs
- **Issues**: Report via GitHub issues
- **Email**: support@brilink.com (jika ada)

## 📄 License

Proprietary - Brilink Backend API v2.0

---

## 🎓 Development Tips

### Testing Local
```bash
# Test GUI
python database_config_gui.py

# Test Launcher
python launcher.py

# Test API langsung
python app.py
```

### Building
```bash
# Clean build
rmdir /s /q build dist
python build_exe.py

# Quick rebuild
python build_exe.py
```

### Debugging
```bash
# Run with console
BrilinkBackend.exe

# Check logs di console output
# Check .env file dibuat
# Check db_config.json
```

## 🌟 Changelog

### v2.0 (Current)
- ✅ GUI untuk konfigurasi database
- ✅ Build ke executable
- ✅ Test koneksi database
- ✅ Auto database creation
- ✅ Improved error handling

### v1.0
- Basic API endpoints
- JWT authentication
- CRUD operations
- PDF reports

---

**Made with ❤️ for Brilink**

Last Updated: November 2025
