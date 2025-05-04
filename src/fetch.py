import json
import sys
import io
from pathlib import Path
from supabase import create_client
from dotenv import dotenv_values
from rich.console import Console
from rich.progress import Progress

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
console = Console()

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import win_unicode_console
    win_unicode_console.enable()
except ImportError:
    pass

def get_supabase_client():
    try:
        config = dotenv_values(Path(__file__).parent.parent / ".env")
        return create_client(config["SUPABASE_URL"], config["SUPABASE_SERVICE_ROLE_KEY"])
    except Exception as e:
        console.print(f"[red]Supabase error: {e}[/]")
        return None

def fetch_data():
    """Fetch data from Supabase"""
    console.print("[bold cyan]Fetching place names...[/]")
    supabase = get_supabase_client()
    if not supabase:
        return

    try:
        data = []
        with Progress() as progress:
            # Get total count
            count_res = supabase.table("google_places") \
                          .select("name", count="exact") \
                          .execute()
            total = count_res.count
            
            task = progress.add_task("[cyan]Fetching...", total=total)
            
            # Fetch in batches
            for offset in range(0, total, 1000):
                batch = supabase.table("google_places") \
                         .select("name") \
                         .range(offset, offset + 999) \
                         .execute()
                data.extend([item["name"] for item in batch.data])
                progress.update(task, advance=len(batch.data))

        # Save data
        output_file = DATA_DIR / "fetched_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            console.print(f"[green]✓[/] Saved {len(data)} place names to {output_file}")  # or use "[green]SUCCESS[/]"
    except Exception as e:
        console.print(f"[red]ERROR:[/] {str(e)}")
if __name__ == "__main__":
    fetch_data()