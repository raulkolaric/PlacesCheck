import json
import sys
from supabase import create_client
from dotenv import dotenv_values
from rich.console import Console
from rich.progress import Progress

# Windows-specific console configuration
if sys.platform == "win32":
    # Configure console for Windows Unicode support
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

console = Console()

def get_supabase_client():
    """Initialize Supabase client with error handling"""
    try:
        config = dotenv_values(".env")
        if not config.get("SUPABASE_URL") or not config.get("SUPABASE_SERVICE_ROLE_KEY"):
            console.print("[red]Error: Missing Supabase credentials in .env file[/]")
            sys.exit(1)
        return create_client(config["SUPABASE_URL"], config["SUPABASE_SERVICE_ROLE_KEY"])
    except Exception as e:
        console.print(f"[red]Error initializing Supabase client: {e}[/]")
        sys.exit(1)

def fetch_data(table: str, column: str, max_rows=10000):
    """Fetch data with pagination and error handling"""
    try:
        supabase = get_supabase_client()
        data = []
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Fetching data...", total=max_rows)
            
            for offset in range(0, max_rows, 1000):
                batch = supabase.table(table)\
                         .select(column)\
                         .range(offset, offset + 999)\
                         .execute()
                
                if not batch.data:
                    break
                    
                data.extend([item[column] for item in batch.data])
                progress.update(task, advance=len(batch.data))
        
        return data[:max_rows]
    
    except Exception as e:
        console.print(f"[red]Error fetching data: {e}[/]")
        return None

def save_data(data, filename="fetched_data.json"):
    """Save data with error handling"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # ASCII-friendly success message
        console.print(f"[green]SUCCESS: Saved {len(data)} rows to {filename}[/]")
        return True
    except Exception as e:
        console.print(f"[red]Error saving data: {e}[/]")
        return False

def main():
    console.print("[bold]SUPABASE DATA FETCHER[/]", style="bold magenta", justify="center")
    
    # Configuration - change these to match your table
    TABLE_NAME = "google_places"  # Replace with your table name
    COLUMN_NAME = "name"            # Replace with your column name
    
    try:
        # Fetch data
        console.print(f"[bold]Fetching '{COLUMN_NAME}' from '{TABLE_NAME}'...[/]")
        data = fetch_data(TABLE_NAME, COLUMN_NAME)
        if not data:
            console.print("[red]No data was fetched[/]")
            return
        
        # Save data
        if save_data(data):
            console.print("\n[bold]SUMMARY:[/]")
            console.print(f"- Table: {TABLE_NAME}")
            console.print(f"- Column: {COLUMN_NAME}")
            console.print(f"- Rows fetched: {len(data)}")
            console.print(f"- Saved to: fetched_data.json")
        
    except Exception as e:
        console.print(f"[red]UNEXPECTED ERROR: {e}[/]")
    finally:
        console.print("\n[dim]Operation completed[/]")

if __name__ == "__main__":
    main()