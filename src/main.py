import json
import re
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress
from supabase import create_client
from dotenv import dotenv_values
import os

# Windows Unicode fixes
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    os.system('')  # Enable ANSI colors in Windows cmd

console = Console()

# Configuration
COLOR_PRIMARY = "#4E32FA"
COLOR_SUCCESS = "#B7F800"
COLOR_WARNING = "#F8BD00"
TABLE_NAME = "google_places"
COLUMN_NAME = "name"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def display_header():
    console.clear()
    header = Panel.fit(
        Text("MAPARI PLACE CHECKER", style=f"bold {COLOR_PRIMARY}"),
        border_style=COLOR_PRIMARY,
        padding=(1, 2)
    )
    console.print(header)

def get_supabase_client():
    try:
        config = dotenv_values(".env")
        return create_client(config["SUPABASE_URL"], config["SUPABASE_SERVICE_ROLE_KEY"])
    except Exception as e:
        console.print(f"[red]Supabase error: {e}[/]")
        return None

def fetch_data():
    console.print(f"\n[{COLOR_PRIMARY}]» Fetching place names...[/]")
    supabase = get_supabase_client()
    if not supabase:
        return

    try:
        data = []
        with Progress() as progress:
            count_res = supabase.table(TABLE_NAME).select(COLUMN_NAME, count='exact').execute()
            task = progress.add_task("[cyan]Fetching...", total=count_res.count)
            
            for offset in range(0, count_res.count, 1000):
                batch = supabase.table(TABLE_NAME) \
                         .select(COLUMN_NAME) \
                         .range(offset, offset + 999) \
                         .execute()
                data.extend([item[COLUMN_NAME] for item in batch.data])
                progress.update(task, advance=len(batch.data))

        output_file = DATA_DIR / "fetched_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        console.print(f"[{COLOR_SUCCESS}]Saved {len(data)} place names[/]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/]")
    console.input("\nPress Enter to continue...")

def compare_data():
    console.print(f"\n[{COLOR_PRIMARY}]» Comparing place names...[/]")
    
    try:
        # Load fetched data
        with open(DATA_DIR / "fetched_data.json", "r", encoding="utf-8") as f:
            db_names = set(json.load(f))
    except FileNotFoundError:
        console.print("[red]Error: No fetched data found. Run fetch first![/]")
        console.input("\nPress Enter to continue...")
        return

    try:
        # Load and clean names from insert.txt
        with open(DATA_DIR / "insert.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            if len(lines) == 1:  # Handle comma-separated
                lines = [item.strip() for item in content.split(',') if item.strip()]
            check_names = [re.sub(r'^(\d+[.)]|\s*[-•*]\s*)', '', line).strip('"\'') for line in lines]
    except FileNotFoundError:
        console.print("[red]Error: Missing insert.txt in data folder[/]")
        console.input("\nPress Enter to continue...")
        return

    # Compare
    missing = [name for name in check_names if name not in db_names]
    
    if missing:
        console.print(f"\n[{COLOR_WARNING}]Missing {len(missing)} places:[/]")
        for i, name in enumerate(missing[:20], 1):
            console.print(f"  {i}. {name}")
        if len(missing) > 20:
            console.print(f"  ...and {len(missing)-20} more")
        
        if console.input("\nSave to missing_places.txt? (y/n): ").lower() == 'y':
            with open(DATA_DIR / "missing_places.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(missing))
            console.print(f"[{COLOR_SUCCESS}]Saved results[/]")
    else:
        console.print(f"[{COLOR_SUCCESS}]All places exist in database![/]")
    
    console.input("\nPress Enter to continue...")

def main():
    while True:
        try:
            display_header()
            
            menu = Table.grid(padding=(1, 3))
            menu.add_column(style="bold white")
            menu.add_row("1. Fetch data from Supabase")
            menu.add_row("2. Compare with insert.txt")
            menu.add_row("3. Exit")
            console.print(menu)
            
            choice = console.input(f"\n[{COLOR_WARNING}]Select option (1-3): [/]")
            
            if choice == "1":
                fetch_data()
            elif choice == "2":
                compare_data()
            elif choice == "3":
                console.print(f"\n[{COLOR_SUCCESS}]Goodbye![/]")
                break
            else:
                console.print("[red]Invalid choice![/]")
                sleep(1)
                
        except KeyboardInterrupt:
            console.print(f"\n[{COLOR_WARNING}]Operation cancelled[/]")
            break
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/]")
            sleep(2)

if __name__ == "__main__":
    main()