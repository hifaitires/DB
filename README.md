# Tyre Stock System

A lightweight, Linux-friendly terminal application for managing tyre inventory, logs, CSV import/export, and audit trails.  
Built with Python + SQLite. No GUI, no external dependencies.

---

## Features

### Inventory Management
- Add tyres (SKU, brand, size, type, pattern, quantity, price, description)
- Edit existing entries
- Change quantity (+/- or absolute)
- Delete individual tyres
- Bulk delete via ID list or ranges (e.g. `1,3-7,20`)
- Search by SKU, brand, or text (size or description)
- Pagination (25 items per page)
- Sorting options:
  - ID ascending / descending  
  - Newest / oldest  
  - Brand + size  
- Automatic timestamp for each added tyre

### CSV Integration
- Export stock to CSV (semicolon-separated)
- Import new stock from CSV  
- **Logs are never exported or imported**

### Audit Log (History)
- Every ADD, UPDATE, QTY_CHANGE, DELETE is logged
- Log entries include:
  - Timestamp  
  - Action  
  - SKU, brand, size, quantity, price  
  - **User who performed the action** (Coming soon)

### User Authentication  
*(Coming soon – In development)*
- Login system with hashed passwords  
- Users stored in SQLite  
- Disabled users cannot log in  
- All changes tied to the logged-in user  

---

## Project Structure

```
tyre_app/
├─ main.py
├─ db.py
├─ models.py
├─ utils.py
├─ tyres.db              # auto-created on first run
└─ menus/
   ├─ __init__.py
   ├─ menu_main.py
   ├─ menu_auth.py
   ├─ menu_list.py
   ├─ menu_detail.py
   ├─ menu_add.py
   ├─ menu_logs.py
   ├─ menu_csv.py
   ├─ menu_bulk_delete.py
   └─ sorting.py
```

---

## Installation

You can install the system manually or using the provided **`tyres.sh` script**.

---

## Option A: Installation with `tyres.sh` (recommended)

1. Make the script executable:

```bash
chmod +x tyres.sh
```

2. Run it:

```bash
./tyres.sh
```

The script will:

- Create a Python virtual environment  
- Ensure Python & SQLite are available  
- Install dependencies  
- Initialize the database  
- Start the application  

To run the app again, simply:

```bash
./tyres.sh
```

---

## Option B: Manual Installation

### 1. Install Python 3  
Most distros:

```bash
sudo apt install python3 python3-venv -y
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Run the application

```bash
python3 main.py
```

---

## Main Menu Options

```
1) List / search tyres
2) Add tyre
3) View logs
4) Export to CSV
5) Import from CSV
6) Bulk delete tyres
0) Exit
```

---

## CSV Format

### Required header:

```
sku;brand;size;tyre_type;pattern;quantity;price;description
```

### Example row:

```
20555R16;Continental;205/55R16 91H;Summer;EcoContact 6;12;79.90;High-quality tyre
```

---

## Bulk Delete Format

Examples:

```
1,5,7
2-10
1,3-5,12
```

---

## Uninstall

```bash
rm -rf tyre_app
```

If you used a virtual environment:

```bash
deactivate
rm -rf venv
```
