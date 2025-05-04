import json
import re
import sys
from typing import List, Set
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, track
from time import sleep
from supabase import create_client
from dotenv import dotenv_values

# Configure console for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

console = Console()

# Color theme
COLOR_PRIMARY = "#4E32FA"
COLOR_SUCCESS = "#B7F800"
COLOR_WARNING = "#F8BD00"

# Fixed configuration
TABLE_NAME = "google_places"
COLUMN_NAME = "name"

def get_supabase_client():
    try:
        config = dotenv_values(".env")
        return create_client(config["SUPABASE_URL"], config["SUPABASE_SERVICE_ROLE_KEY"])
    except Exception as e:
        console.print(f"[red]Supabase error: {e}[/]")
        return None

def display_header():
    console.clear()
    header = Panel.fit(
        Text("MAPARI PLACE CHECKER", style=f"bold {COLOR_PRIMARY}"),
        border_style=COLOR_PRIMARY,
        padding=(1, 2)
    )
    console.print(header)

def show_menu():
    menu = Table.grid(padding=(1, 3))
    menu.add_column(style="bold white")
    menu.add_row("1. Fetch data from Supabase")
    menu.add_row("2. Compare with insert.txt")
    menu.add_row("3. Exit")
    console.print(menu)
    return console.input(f"\n[{COLOR_WARNING}]Select option (1-3): [/]")

def fetch_data():
    """Fetch data using predefined table and column"""
    console.print(f"\n[{COLOR_PRIMARY}]» Fetching place names...[/]")
    supabase = get_supabase_client()
    if not supabase:
        console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")
        return

    try:
        data = []
        with Progress() as progress:
            # Get total count
            count_res = supabase.table(TABLE_NAME)\
                          .select(COLUMN_NAME, count='exact')\
                          .execute()
            total = count_res.count
            
            task = progress.add_task("[cyan]Fetching...", total=total)
            
            # Fetch in batches
            for offset in range(0, total, 1000):
                batch = supabase.table(TABLE_NAME)\
                         .select(COLUMN_NAME)\
                         .range(offset, offset + 999)\
                         .execute()
                data.extend([item[COLUMN_NAME] for item in batch.data])
                progress.update(task, advance=len(batch.data))

        with open("fetched_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        console.print(f"[{COLOR_SUCCESS}]✓ Saved {len(data)} place names[/]")

    except Exception as e:
        console.print(f"[red]Fetch error: {e}[/]")
    finally:
        console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")

def compare_data():
    """Compare data with insert.txt"""
    console.print(f"\n[{COLOR_PRIMARY}]» Comparing place names...[/]")
    
    # Load fetched data
    try:
        with open("fetched_data.json", "r", encoding="utf-8") as f:
            db_names = set(json.load(f))
    except FileNotFoundError:
        console.print("[red]Error: No fetched data found. Run fetch first![/]")
        console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")
        return

    # Load and parse insert.txt
    try:
        with open("insert.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            
        # Parse any list format
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if len(lines) == 1:  # Handle comma-separated
            lines = [item.strip() for item in content.split(',') if item.strip()]
            
        # Clean names
        check_names = [re.sub(r'^(\d+[.)]|\s*[-•*]\s*)', '', line).strip('"\'').strip() 
                      for line in lines if line.strip()]
    except FileNotFoundError:
        console.print("[red]Error: Missing insert.txt file[/]")
        console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")
        return

    # Compare and show results
    missing = [name for name in check_names if name not in db_names]
    
    if missing:
        console.print(f"[{COLOR_WARNING}]Missing {len(missing)} places:[/]")
        for i, name in enumerate(missing[:20], 1):  # Show first 20
            console.print(f"  {i}. {name}")
        if len(missing) > 20:
            console.print(f"  ...and {len(missing)-20} more")
        
        if console.input("\nSave to missing_places.txt? (y/n): ").lower() == 'y':
            with open("missing_places.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(missing))
            console.print(f"[{COLOR_SUCCESS}]✓ Saved results[/]")
    else:
        console.print(f"[{COLOR_SUCCESS}]✓ All places exist in database![/]")
    
    console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")

def main():
    while True:
        display_header()
        choice = show_menu()
        
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n[{COLOR_WARNING}]Operation cancelled[/]")
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/]")