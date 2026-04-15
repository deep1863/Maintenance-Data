# Machine Maintenance Management System

A local LAN-based web application for digitizing and managing machine maintenance records.

---

## Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
python app.py
```

### 3. Open in browser

- **This machine:** http://localhost:5000
- **Other devices on LAN:** http://192.168.x.x:5000  
  *(replace with your machine's local IP — find it using `ipconfig` on Windows or `hostname -I` on Linux)*

---

## Load Sample Data (Optional)

To pre-populate the system with sample entries matching the reference Excel format:

```bash
python seed_data.py
```

---

## Project Structure

```
machine_mgmt/
├── app.py              # Flask backend + all API routes
├── seed_data.py        # Sample data loader
├── requirements.txt    # Python dependencies
├── instance/
│   └── machine_data.db # SQLite database (auto-created)
└── templates/
    └── index.html      # Full frontend (HTML + CSS + JS)
```

---

## Database Schema

```sql
machines (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    department TEXT,
    created_at TEXT
)

maintenance_log (
    id INTEGER PRIMARY KEY,
    machine_id INTEGER,        -- FK → machines.id
    sno INTEGER,               -- Auto-incremented per machine
    entry_date TEXT,           -- YYYY-MM-DD
    breakdown_details TEXT,
    action_taken TEXT,
    spares_used TEXT,
    nature_of_work TEXT,       -- BD | PM
    nature_of_bd TEXT,         -- New | Repeat | N/A
    total_down_time TEXT,
    bd_cleared TEXT,           -- Int | Ext
    created_at TEXT,
    updated_at TEXT
)
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/machines` | List all machines |
| POST | `/api/machines` | Add a machine |
| DELETE | `/api/machines/<id>` | Delete machine + records |
| GET | `/api/entries` | All entries (optional: ?machine_id=N, ?search=X) |
| POST | `/api/entries` | Create new entry |
| PUT | `/api/entries/<id>` | Update entry |
| DELETE | `/api/entries/<id>` | Delete entry |
| GET | `/api/dashboard` | Dashboard stats |
| GET | `/api/export/all` | Download master Excel (all machines) |
| GET | `/api/export/machine/<id>` | Download machine-specific Excel |

---

## Excel Export

- **Master Export** (top-right button): Downloads `master_maintenance_log.xlsx` with:
  - Sheet 1: All records across all machines
  - Additional sheets: One per machine
- **Machine Export**: Per-machine Excel matching original format
- Files download via browser. To save to Desktop automatically, move the downloaded file, or configure your browser's default download folder to your Desktop.

### Desktop Path by OS

| OS | Desktop Path |
|----|-------------|
| Windows | `C:\Users\<Username>\Desktop` |
| Linux | `/home/<username>/Desktop` |
| macOS | `/Users/<username>/Desktop` |

---

## Features vs. Excel

| Feature | Old Excel | This System |
|---------|-----------|-------------|
| Multi-user access | ❌ (file conflicts) | ✅ LAN web app |
| Search & filter | ❌ Manual | ✅ Global search |
| Duplicate detection | ❌ None | ✅ Auto-detected |
| Auto S.No per machine | ❌ Manual | ✅ Auto-assigned |
| Timestamps | ❌ Manual | ✅ Auto (created/updated) |
| Validation | ❌ None | ✅ Required fields |
| Dashboard stats | ❌ None | ✅ Charts & counts |
| Excel export | ✅ Native | ✅ Formatted export |
| Separate machine views | ❌ Multiple files | ✅ Sidebar navigation |
| Data consistency | ❌ Error-prone | ✅ Enforced by DB |

---

## LAN Access (Finding Your IP)

**Windows:**
```cmd
ipconfig
# Look for: IPv4 Address . . . . . . . . . : 192.168.x.x
```

**Linux / macOS:**
```bash
hostname -I
# or
ip addr show
```

Then share `http://192.168.x.x:5000` with colleagues on the same network.
