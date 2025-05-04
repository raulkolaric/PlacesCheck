import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from time import sleep
from pathlib import Path

# Configure console
console = Console()

# Color theme
COLOR_PRIMARY = "#4E32FA"
COLOR_SUCCESS = "#B7F800"
COLOR_WARNING = "#F8BD00"

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

def run_fetch():
    console.print(f"\n[{COLOR_PRIMARY}]» Fetching data...[/]")
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "fetch.py")],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            console.print(f"[{COLOR_SUCCESS}]✓ Data fetched successfully![/]")
            console.print(result.stdout)
        else:
            console.print(f"[red]✗ Error during fetch:[/]")
            console.print(result.stderr)
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
    console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")

def run_compare():
    console.print(f"\n[{COLOR_PRIMARY}]» Comparing data...[/]")
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "compare.py")],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            console.print(f"[{COLOR_SUCCESS}]✓ Comparison complete![/]")
            console.print(result.stdout)
        else:
            console.print(f"[red]✗ Error during comparison:[/]")
            console.print(result.stderr)
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
    console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")

def main():
    while True:
        display_header()
        choice = show_menu()
        
        if choice == "1":
            run_fetch()
        elif choice == "2":
            run_compare()
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