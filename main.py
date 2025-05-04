import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import track
from time import sleep

console = Console()

# Custom color theme
COLOR_PRIMARY = "#4E32FA"
COLOR_SUCCESS = "#B7F800"
COLOR_WARNING = "#F8BD00"

def display_header():
    console.clear()
    header_text = Text("MAPARI PLACE CHECKER", style=f"bold {COLOR_PRIMARY}")
    header = Panel.fit(
        header_text,
        border_style=COLOR_PRIMARY,
        padding=(1, 2))
    console.print(header)


def show_menu():
    menu_table = Table.grid(padding=(1, 3))
    menu_table.add_column(style=f"bold white")
    
    menu_table.add_row("1. Fetch data from Supabase")
    menu_table.add_row("2. Compare with insert.txt")
    menu_table.add_row("3. Exit")
    
    console.print(menu_table)
    return console.input(f"\n[{COLOR_WARNING}]Select an option (1-3): [/]")

def run_fetch():
    console.print(f"\n[{COLOR_PRIMARY}]» Fetching data...[/]")
    try:
        with console.status(f"[{COLOR_PRIMARY}]Connecting to Supabase...[/]", spinner="dots"):
            result = subprocess.run([sys.executable, "fetch.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print(f"[{COLOR_SUCCESS}]✓ Data fetched successfully![/]")
            for line in result.stdout.split('\n'):
                if line.strip():
                    console.print(f"  {line}")
        else:
            console.print(f"[red]✗ Error during fetch:[/]")
            console.print(result.stderr)
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
    console.input(f"\n[{COLOR_WARNING}]Press Enter to continue...")

def run_compare():
    console.print(f"\n[{COLOR_PRIMARY}]» Comparing data...[/]")
    try:
        with console.status(f"[{COLOR_PRIMARY}]Processing insert.txt...[/]", spinner="dots"):
            result = subprocess.run([sys.executable, "compare.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print(f"[{COLOR_SUCCESS}]✓ Comparison complete![/]")
            # Animate results display
            for line in track(result.stdout.split('\n'), description="Loading results..."):
                if line.strip():
                    console.print(line)
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
            console.print(f"[red]Invalid choice![/]")
            sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n[{COLOR_WARNING}]Operation cancelled by user[/]")
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/]")