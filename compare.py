import json
import re
import sys
from pathlib import Path
from typing import List, Set
from rich.console import Console

# Configure console for Windows compatibility
try:
    console = Console()
except UnicodeEncodeError:
    # Fallback for Windows encoding issues
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    console = Console(force_terminal=True)

def clean_name(name: str) -> str:
    """Clean names from various formats"""
    # Remove numbering, bullets, and extra spaces
    name = re.sub(r'^(\d+[.)]|\s*[-•*]\s*)', '', name.strip())
    return name.strip('"\'')

def parse_insert_file() -> List[str]:
    """Parse insert.txt with multiple format support"""
    try:
        with open('insert.txt', 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            console.print("[red]Error: insert.txt is empty")
            return []
            
        # Try different delimiters
        lines = []
        if '\n' in content:  # Multi-line format
            lines = [line.strip() for line in content.split('\n') if line.strip()]
        elif ',' in content:  # Comma-separated
            lines = [item.strip() for item in content.split(',') if item.strip()]
        else:  # Single item
            lines = [content]
            
        return [clean_name(line) for line in lines if line]
        
    except FileNotFoundError:
        console.print("[red]Error: insert.txt not found")
        return []
    except Exception as e:
        console.print(f"[red]Error reading file: {e}")
        return []

def load_fetched_data() -> Set[str]:
    """Load data from JSON with error handling"""
    try:
        with open('fetched_data.json', 'r', encoding='utf-8') as f:
            return set(json.load(f))
    except FileNotFoundError:
        console.print("[red]Error: fetched_data.json not found. Run fetch.py first")
        return set()
    except Exception as e:
        console.print(f"[red]Error loading data: {e}")
        return set()

def compare_lists(db_names: Set[str], check_names: List[str]) -> List[str]:
    """Compare two lists safely"""
    if not db_names:
        console.print("[yellow]Warning: No data loaded from database[/]")
    if not check_names:
        console.print("[yellow]Warning: No names to check[/]")
    return [name for name in check_names if name not in db_names]

def display_results(missing: List[str], total: int):
    """Display results safely"""
    if not missing:
        console.print("[green]✓ All names exist in the database!")
        return
        
    console.print(f"\n[bold]RESULTS:[/]")
    console.print(f"Checked: {total} names")
    console.print(f"Missing: {len(missing)} names")
    
    # Display first 20 missing names to avoid overflow
    console.print("\n[bold]First 20 missing names:[/]")
    for i, name in enumerate(missing[:20], 1):
        console.print(f"{i}. {name}")
    
    if len(missing) > 20:
        console.print(f"\n...and {len(missing)-20} more")

def save_missing_names(names: List[str]):
    """Save missing names with validation"""
    if not names:
        return
        
    try:
        with open('missing_names.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(names))
        console.print(f"[green]✓ Saved {len(names)} names to missing_names.txt")
    except Exception as e:
        console.print(f"[red]Error saving file: {e}")

def main():
    console.print("[bold]LIST COMPARISON TOOL[/]", style="bold magenta")
    
    # Load data
    db_names = load_fetched_data()
    check_names = parse_insert_file()
    
    if not db_names or not check_names:
        return
        
    # Compare
    missing = compare_lists(db_names, check_names)
    
    # Show results
    display_results(missing, len(check_names))
    
    # Save if needed
    if missing and console.input("\nSave missing names? (y/n): ").lower() == 'y':
        save_missing_names(missing)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"[red]Fatal error: {e}")
    finally:
        console.print("\n[dim]Operation completed[/]")