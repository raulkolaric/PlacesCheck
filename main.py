from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
import subprocess
import sys

console = Console()

def show_menu():
    console.clear()
    console.print(Panel.fit("[bold magenta]SUPABASE DATA MANAGER[/]", style="magenta"))
    
    table = Table.grid(padding=(1, 3))
    table.add_column(style="bold cyan")
    
    table.add_row("1. Fetch data from Supabase")
    table.add_row("2. Compare with local list")
    table.add_row("3. Exit")
    
    console.print(table)
    
    choice = console.input("\n[bold]Select an option (1-3): [/]")
    return choice

def run_fetch():
    console.print("\n[bold cyan]Running Data Fetch...[/]")
    try:
        subprocess.run([sys.executable, "fetch.py"], check=True)
    except subprocess.CalledProcessError:
        console.print("[bold red]Error during fetch operation[/]")
    console.input("\nPress Enter to return to menu...")

def run_compare():
    console.print("\n[bold cyan]Running Comparison...[/]")
    try:
        subprocess.run([sys.executable, "compare.py"], check=True)
    except subprocess.CalledProcessError:
        console.print("[bold red]Error during compare operation[/]")
    console.input("\nPress Enter to return to menu...")

def main():
    while True:
        choice = show_menu()
        
        if choice == "1":
            run_fetch()
        elif choice == "2":
            run_compare()
        elif choice == "3":
            console.print("[bold green]Goodbye![/]")
            break
        else:
            console.print("[bold red]Invalid choice![/]")
            console.input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold green]Program terminated by user[/]")