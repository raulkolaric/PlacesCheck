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

# Supabase configuration
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
    """Integrated fetch functionality"""
    console.print(f"\n[{COLOR_PRIMARY}]» Fetching data...[/]")
    supabase = get_supabase_client()
    if not supabase:
        return

    table_name = console.input("[bold]Enter table name: [/]")
    column_name = console.input("[bold]Enter column name: [/]")

    try:
        data = []
        with Progress() as progress:
            # Get count first
            count = supabase.table(table_name).select(column_name, count='exact').execute().count
            task = progress.add_task("[cyan]Fetching...", total=count)

            # Fetch in batches
            for offset in range(0, count, 1000):
                batch = supabase.table(table_name)\
                         .select(column_name)\
                         .range(offset, offset+999)\
                         .execute()
                data.extend([item[column_name] for item in batch.data])
                progress.update(task, advance=len(batch.data))

        with open("fetched_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        console.print(f"[{COLOR_SUCCESS}]✓ Saved {len(data)} rows to fetched_data.json[/]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
    console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")

def compare_data():
    """Integrated compare functionality"""
    console.print(f"\n[{COLOR_PRIMARY}]» Comparing data...[/]")
    
    # Load fetched data
    try:
        with open("fetched_data.json", "r", encoding="utf-8") as f:
            db_names = set(json.load(f))
    except FileNotFoundError:
        console.print("[red]Error: Run fetch first![/]")
        console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")
        return

    # Load insert.txt
    try:
        with open("insert.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            if len(lines) == 1:  # Handle comma-separated
                lines = [item.strip() for item in content.split(',') if item.strip()]
            check_names = [re.sub(r'^(\d+[.)]|\s*[-•*]\s*)', '', line).strip('"\'') for line in lines]
    except FileNotFoundError:
        console.print("[red]Error: Create insert.txt first![/]")
        console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")
        return

    # Compare
    missing = [name for name in check_names if name not in db_names]
    
    # Display results
    if missing:
        table = Table(title="Missing Names", show_header=True, header_style="bold red")
        table.add_column("No.", style="cyan")
        table.add_column("Name")
        for i, name in enumerate(missing[:20], 1):  # Show first 20
            table.add_row(str(i), name)
        console.print(table)
        console.print(f"[{COLOR_WARNING}]Found {len(missing)} missing names[/]")
        
        if console.input("Save to missing_names.txt? (y/n): ").lower() == 'y':
            with open("missing_names.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(missing))
            console.print(f"[{COLOR_SUCCESS}]✓ Saved results[/]")
    else:
        console.print(f"[{COLOR_SUCCESS}]✓ All names exist in database![/]")
    
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