# 🗺️ Mapari Place Checker

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Supabase](https://img.shields.io/badge/Supabase-3.0+-green.svg)
![Rich](https://img.shields.io/badge/Rich_TUI-13.0+-orange.svg)

A beautiful terminal application to verify place names against a Supabase database, featuring a colorful TUI interface with progress tracking.

## ✨ Features

- **One-Click Operations**: Fetch and compare with simple menu options
- **Smart List Parsing**: Handles numbered, bulleted, or comma-separated lists
- **Progress Tracking**: Visual progress bars for data fetching
- **Windows Compatible**: Full Unicode support with proper encoding
- **Beautiful Output**: Color-coded results with clean tables

## 🛠️ Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mapari-place-checker.git
   cd mapari-place-checker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   Create a `.env` file with your Supabase credentials:
   ```env
   SUPABASE_URL=your_project_url
   SUPABASE_SERVICE_ROLE_KEY=your_secret_key
   ```

## 🚀 Usage

```bash
python main.py
```

### Menu Options:
1. **Fetch Data**: Retrieves all place names from `google_places` table
2. **Compare**: Checks `insert.txt` against fetched data
3. **Exit**: Quits the application

![TUI Screenshot](https://i.imgur.com/placeholder.png) *(Example screenshot placeholder)*

## 📁 File Structure

```
.
├── main.py            # Main application
├── insert.txt         # Your list of places to check
├── fetched_data.json  # Auto-generated place data
├── missing_places.txt # Auto-generated missing places
├── .env               # Supabase credentials
└── README.md          # This file
```

## 🔧 Configuration

The application automatically uses:
- Table: `google_places`
- Column: `name`

To modify these, edit the constants at the top of `main.py`:
```python
TABLE_NAME = "google_places"
COLUMN_NAME = "name"
```

## 💡 Tips

- Place your list in `insert.txt` (supports multiple formats)
- Missing places save to `missing_places.txt`
- Press Ctrl+C to cancel any operation

## 📜 License

MIT License - Feel free to use and modify for your projects!

---

> "A good traveler has no fixed plans and is not intent on arriving." - Lao Tzu
