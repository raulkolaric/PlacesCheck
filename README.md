# 🗺️ PlacesCheck

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Supabase](https://img.shields.io/badge/Supabase-API-green.svg)
![Rich](https://img.shields.io/badge/Rich_TUI-13.0+-orange.svg)

A beautiful terminal application to verify place names against a large Supabase database, featuring a colorful and responsive TUI interface with smart parsing and progress tracking.

## ✨ Features

- **One-Click Operations**: Easily fetch and compare places from terminal  
- **Smart Parsing**: Supports comma-separated, bulleted, and numbered lists  
- **Progress Bars**: Clear visual progress using `rich.progress`  
- **Colorful Output**: Displays results in neatly formatted tables  
- **Windows Friendly**: Built-in Unicode handling  

## 🛠️ Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/raulkolaric/PlacesCheck.git
   cd PlacesCheck
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Supabase credentials**:
   Create a `.env` file:
   ```env
   SUPABASE_URL=your_project_url
   SUPABASE_SERVICE_ROLE_KEY=your_service_key
   ```

## 🚀 Usage

Run the app:
```bash
python src/main.py
```

### Menu Options:

1. **Fetch Data** – Loads existing place names from Supabase table `google_places`  
2. **Compare** – Parses `insert.txt` and compares each name  
3. **Exit** – Closes the program

![{3D06C0BF-52BF-443A-A3C1-08FC989EA9EE}](https://github.com/user-attachments/assets/6c50d3b0-6ea7-453d-ae91-6a3d12741905)



## 📁 Project Structure

```
PlacesCheck/
├── src/
│   └── main.py             # Main application
│   └── compare.py
│   └── fetch.py
├── data/          # Input list of place names
│   └── fetched_data.json       # Cached data from Supabase
│   └── missing_places.txt      # Auto-saved unmatched entries
│   └── insert.txt              # Your input against the data from Supabase
├── .env                    # Your Supabase credentials
├── requirements.txt        # Python dependencies
└── README.md               # Project overview
```

## ⚙️ Configuration

Default values:
```python
TABLE_NAME = "google_places"
COLUMN_NAME = "name"
```
Change these in `main.py` to use a different table or column.

## 💡 Tips

- Supports copy-pasting from various formats (e.g., Excel, Google Docs)  
- Automatically saves unmatched entries to `missing_places.txt`  
- Press `Ctrl+C` to exit safely at any time  

## 📜 License

MIT License – Free to use, modify, and distribute!
