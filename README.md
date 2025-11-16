# Brilink API Backend

API backend untuk aplikasi Brilink menggunakan Python Flask dengan arsitektur single-agent.

> 📖 **Panduan Cepat**: Lihat [QUICK_START.md](QUICK_START.md) untuk setup 5 menit!

## 🚀 Quick Start

### Persyaratan Sistem
- **Python**: 3.8 atau lebih baru
- **Database**: MySQL 5.7+ atau MariaDB 10.0+
- **OS**: Windows 10+, macOS, atau Linux

### 1. Extract Project Files

Extract file zip project ke folder yang diinginkan:

```bash
# Extract zip file ke folder backend_brilink_v2
unzip brilink_backend.zip -d backend_brilink_v2
cd backend_brilink_v2
```

**Windows**: Extract menggunakan Windows Explorer atau 7-Zip ke folder `backend_brilink_v2`

### 2. Setup Python Virtual Environment

**Windows (Automated Setup):**
```cmd
setup.bat
```

**Windows (Manual):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS/Linux (Automated Setup):**
```bash
chmod +x setup.sh
./setup.sh
```

**macOS/Linux (Manual):**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies utama:**
- Flask 2.3+ - Web framework
- Flask-SQLAlchemy - ORM untuk database
- PyMySQL - MySQL connector
- python-dotenv - Environment variables
- PyJWT - JSON Web Tokens
- Werkzeug - Password hashing

### 4. Setup Database

#### Opsi A: Menggunakan XAMPP (Windows)
1. Download dan install [XAMPP](https://www.apachefriends.org/)
2. Start Apache dan MySQL di XAMPP Control Panel
3. Buka phpMyAdmin: `http://localhost/phpmyadmin`
4. Buat database baru: `db_api_brilink`

#### Opsi B: Menggunakan MySQL Server
```sql
CREATE DATABASE db_api_brilink CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Konfigurasi Environment

```bash
# Copy template environment
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

Edit file `.env`:
```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-super-secret-key-here-change-this-in-production

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=db_api_brilink

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### 6. Inisialisasi Database

```bash
# Jalankan aplikasi untuk membuat tabel
python app.py
```

Aplikasi akan otomatis membuat semua tabel database saat pertama kali dijalankan.

### 7. Seed Database (Untuk Testing)

```bash
# Jalankan seeder interaktif
python seeder.py
```

Pilih opsi:
1. **Clear existing data dan seed baru** - Hapus semua data dan buat data baru
2. **Tambah data tanpa menghapus existing** - Tambah data tanpa menghapus yang ada
3. **Seed hanya transaksi** - Hanya buat data transaksi
4. **Seed hanya cash flow** - Hanya buat data cash flow
5. **Lihat statistik database** - Lihat ringkasan data

### 8. Jalankan Aplikasi

```bash
python app.py
```

**Output yang diharapkan:**
```
* Serving Flask app 'app'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

### 9. Verifikasi Setup

```bash
python verify_setup.py
```

Script ini akan memeriksa:
- ✅ Python version
- ✅ Dependencies terinstall
- ✅ Environment configuration
- ✅ Database connection
- ✅ API health

### 10. Test API

```bash
# Health check
curl http://localhost:5000/api/health

# Expected response:
{
  "success": true,
  "message": "API is healthy",
  "data": {
    "status": "ok",
    "timestamp": "2025-10-30T...",
    "version": "1.0.0"
  }
}
```

## 🛠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solusi:** Pastikan virtual environment aktif dan dependencies terinstall
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Error: "Can't connect to MySQL server"
**Solusi:** Periksa konfigurasi database di `.env`
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=db_api_brilink
```

### Error: "Access denied for user"
**Solusi:** Pastikan MySQL user memiliki akses ke database
```sql
GRANT ALL PRIVILEGES ON db_api_brilink.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

### Error: "Port 5000 already in use"
**Solusi:** Gunakan port lain atau hentikan proses yang menggunakan port tersebut
```bash
# Windows - find process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Change port in app.py if needed
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Error: "decimal.Decimal object has no attribute 'keys'"
**Solusi:** Pastikan menggunakan Python 3.8+ dan dependencies terbaru
```bash
pip install --upgrade -r requirements.txt
```

## 📁 Struktur Project

```
backend_brilink_v2/
├── app.py                    # Main Flask application
├── config.py                 # Database & app configuration
├── seeder.py                 # Database seeder untuk dummy data
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── Brilink_API.postman_collection.json  # Postman collection
├── models/                  # Database models
│   ├── user.py             # User model
│   ├── agent_profile.py    # Agent profile model
│   ├── transaction.py      # Transaction model
│   ├── cash_flow.py        # Cash flow model
│   ├── edc_machine.py      # EDC machine model
│   ├── service.py          # Service model
│   └── ...
├── routes/                  # API endpoints
│   ├── auth.py             # Authentication (login/register/users)
│   ├── dashboard.py        # Dashboard metrics
│   ├── reports.py          # Period reports
│   ├── agent.py            # Agent management
│   ├── transaction.py      # Transaction CRUD
│   └── ...
├── utils/                   # Utility functions
│   ├── jwt_handler.py      # JWT token management
│   ├── response.py         # Standardized API responses
│   ├── validators.py       # Input validation
│   └── ...
└── __pycache__/            # Python cache (auto-generated)
```

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user (owner/kasir)
- `POST /api/auth/login` - Login dan dapat JWT token
- `GET /api/auth/users` - Get all users (dengan pagination & filter)

### Dashboard
- `GET /api/dashboard` - Complete dashboard overview
- `GET /api/dashboard/cards/total-revenue-today` - Revenue hari ini
- `GET /api/dashboard/cards/saldo-tunai` - Saldo tunai
- `GET /api/dashboard/cards/saldo-edc` - Saldo EDC
- `GET /api/dashboard/cards/total-transactions-today` - Total transaksi hari ini
- `GET /api/dashboard/cards/recent-transactions` - Transaksi terbaru

### Reports
- `GET /api/reports?period=daily` - Laporan harian
- `GET /api/reports?period=weekly` - Laporan mingguan
- `GET /api/reports?period=monthly` - Laporan bulanan
- `GET /api/reports?period=custom&start_date=2024-01-01&end_date=2024-01-31` - Laporan custom

### Management
- `GET/PUT /api/agents` - Agent profile management
- `GET/POST/PUT/DELETE /api/transactions` - Transaction CRUD
- `GET/POST/PUT/DELETE /api/cash-flows` - Cash flow management
- `GET/POST/PUT/DELETE /api/edc-machines` - EDC machine management
- `GET/POST/PUT/DELETE /api/services` - Service management

## 🧪 Testing dengan Postman

1. **Import Collection**: Import file `Brilink_API.postman_collection.json`
2. **Set Environment**: Buat environment dengan variable `token`
3. **Test Flow**:
   - Register owner → Login → Get token → Test endpoints lain

## 📊 Database Schema

### Single-Agent Architecture
- **1 Owner** = **1 Agent Profile** (auto-created saat register)
- **Multiple Kasir** dapat assign ke **1 Agent Profile** owner
- Agent creation/deletion **DISABLED** untuk menjaga single-agent mode

### Tables
- `users` - User accounts (owner, kasir)
- `agent_profiles` - Agent information (1 per owner)
- `transactions` - Transaction records
- `cash_flows` - Cash in/out records
- `edc_machines` - EDC machine configuration
- `services` - Available services
- `service_fees` - Fee configuration per service
- `bank_fees` - Bank fees per EDC-service combination

## 🔒 Security Features

- **JWT Authentication** - Token-based auth untuk semua protected endpoints
- **Password Hashing** - bcrypt untuk secure password storage
- **Input Validation** - Comprehensive validation untuk semua inputs
- **SQL Injection Protection** - ORM dengan parameterized queries
- **CORS Support** - Cross-origin resource sharing

## 📈 Development Tips

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add docstrings untuk functions penting
- Handle exceptions properly

### Database Migrations
Saat ada perubahan model, restart aplikasi untuk auto-create/update tables.

### Logging
Logs akan muncul di console saat `FLASK_DEBUG=True`.

### Performance
- Gunakan pagination untuk large datasets
- Index database columns yang sering di-query
- Cache results jika memungkinkan

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

Jika ada pertanyaan atau masalah:
1. Check [Troubleshooting](#-troubleshooting) section
2. Review API documentation
3. Check Flask/SQLAlchemy documentation
4. Create GitHub issue dengan detail error

---

**Happy Coding! 🚀**
