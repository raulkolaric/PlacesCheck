import os
import platform 
from rich import print
from rich.console import Console
from rich.terminal_theme import MONOKAI

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else: 
        os.system("clear")

def main():
    clear_terminal()
    console = Console()

    console.print([1, 2, 3])
    console.print("[blue underline]Looks like a link")
    console.print(locals())
    console.print("FOO", style="white on blue")

if __name__ == "__main__":
    main()
