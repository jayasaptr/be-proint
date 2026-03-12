# E-Recruitment Backend (SQL Server)

Backend API untuk E-Recruitment menggunakan Flask dan SQL Server.

## Setup

1. Buat virtual environment (opsional tapi direkomendasikan):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables di `.env`:

```env
DB_SQLSERVER_CONNECTION=sqlsrv
DB_SQLSERVER_HOST=10.105.4.203
DB_SQLSERVER_PORT=1433
DB_SQLSERVER_DATABASE="Crystal_DH"
DB_SQLSERVER_USERNAME=ITNonPayroll
DB_SQLSERVER_PASSWORD=123abc
SECRET_KEY=your-secret-key-here
```

4. Jalankan aplikasi:

```bash
python main.py
```

Server akan berjalan di `http://localhost:5002`

## API Endpoints

### Education Level (Jenjang Pendidikan)

- `GET /api/edulevels` - Get all education levels (dengan pagination)
  - Query Parameters:
    - `page`: Nomor halaman (default: 1)
    - `per_page`: Jumlah item per halaman (default: 100, max: 500)
    - `sort_by`: Field untuk sorting (default: "EduLevel")
    - `sort_order`: Urutan sorting "asc" atau "desc" (default: "asc")
    - `active_only`: Filter hanya data aktif (default: true)

- `GET /api/edulevels/<id>` - Get education level by ID

- `GET /api/edulevels/active/all` - Get all active education levels (tanpa pagination)

### Contoh Request:

```bash
# Get all education levels (page 1, 10 items per page)
curl http://localhost:5002/api/edulevels?page=1&per_page=10

# Get education level by ID
curl http://localhost:5002/api/edulevels/EDU001

# Get all active education levels
curl http://localhost:5002/api/edulevels/active/all
```

## Database Connection

Aplikasi ini menggunakan `pymssql` untuk koneksi ke SQL Server. Jika Anda ingin menggunakan `pyodbc` sebagai gantinya, edit file `app/config.py` dan uncomment bagian pyodbc connection.

## Struktur Folder

```
be-proint/
├── main.py                 # Entry point aplikasi
├── requirements.txt        # Dependencies
├── .env                   # Environment variables
├── README.md
└── app/
    ├── __init__.py        # App factory
    ├── config.py          # Configuration
    ├── models/            # Database models
    │   ├── __init__.py
    │   └── edulevel.py    # PMEduLevel model
    ├── routes/            # API routes/endpoints
    │   ├── __init__.py
    │   └── edulevel_route.py
    └── services/          # Business logic
        ├── __init__.py
        └── edulevel_service.py
```
