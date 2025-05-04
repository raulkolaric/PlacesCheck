import os
import platform 
from rich import print
from rich.console import Console
from rich.terminal_theme import MONOKAI
import subprocess

def open_terminal(): 
    command = f"start cmd.exe /K mode con: cols={30} lines={30}"
    subprocess.run(command, shell=True)

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else: 
        os.system("clear")

def main():
    open_terminal()
    os.system("mode con: cols=120 lines=10")
    clear_terminal()
    console = Console()
    console.size = (1000, 1000)
    
    # console.print("[bold red]Hello World![/bold red]")
    print("[italic red]Hello[/italic red] World!",)

if __name__ == "__main__":
    main()
