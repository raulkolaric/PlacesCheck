import json
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Configure paths
DATA_DIR = Path(__file__).parent.parent / "data"
console = Console()

try:
    import win_unicode_console
    win_unicode_console.enable()
except ImportError:
    pass

def clean_name(name: str) -> str:
    """Clean and standardize names"""
    return re.sub(r'^(\d+[.)]|\s*[-•*]\s*)', '', name.strip()).strip('"\'')

def parse_insert_file() -> list:
    """Parse the insert.txt file"""
    try:
        with open(DATA_DIR / "insert.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                console.print("[red]Error: insert.txt is empty[/]")
                return []
            
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            if len(lines) == 1:  # Handle comma-separated
                lines = [item.strip() for item in content.split(',') if item.strip()]
                
            return [clean_name(line) for line in lines]
    except FileNotFoundError:
        console.print("[red]Error: insert.txt not found in data directory[/]")
        return []

def load_fetched_data() -> set:
    """Load previously fetched data"""
    try:
        with open(DATA_DIR / "fetched_data.json", "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        console.print("[red]Error: Run fetch.py first to get data[/]")
        return set()

def compare_and_save():
    """Main comparison workflow"""
    db_names = load_fetched_data()
    check_names = parse_insert_file()
    
    if not db_names or not check_names:
        return

    missing = [name for name in check_names if name not in db_names]
    
    if not missing:
        console.print("[green]✓ All places exist in database![/]")
        return
    
    # Display results
    table = Table(title="Missing Places", show_header=True, header_style="bold red")
    table.add_column("No.", style="cyan")
    table.add_column("Name")
    
    for i, name in enumerate(missing[:20], 1):
        table.add_row(str(i), name)
    
    console.print(table)
    console.print(f"\n[bold]Total Checked:[/] {len(check_names)}")
    console.print(f"[bold red]Missing:[/] {len(missing)}")
    
    # Save results
    if missing and console.input("\nSave missing places? (y/n): ").lower() == 'y':
        output_file = DATA_DIR / "missing_places.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write('\n'.join(missing))
        console.print(f"[green]✓ Saved to {output_file}[/]")

if __name__ == "__main__":
    compare_and_save()