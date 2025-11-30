from rich import print
from rich.console import Console
import os
import json

console = Console()

ASCII_TITLE = r"""
 ███████████  ███  ████             █████████            ████          
▒█▒▒▒███▒▒▒█ ▒▒▒  ▒▒███            ███▒▒▒▒▒███          ▒▒███          
▒   ▒███  ▒  ████  ▒███   ██████  ███     ▒▒▒   ██████   ▒███   ██████ 
    ▒███    ▒▒███  ▒███  ███▒▒███▒███          ▒▒▒▒▒███  ▒███  ███▒▒███
    ▒███     ▒███  ▒███ ▒███████ ▒███           ███████  ▒███ ▒███ ▒▒▒ 
    ▒███     ▒███  ▒███ ▒███▒▒▒  ▒▒███     ███ ███▒▒███  ▒███ ▒███  ███
    █████    █████ █████▒▒██████  ▒▒█████████ ▒▒████████ █████▒▒██████ 
   ▒▒▒▒▒    ▒▒▒▒▒ ▒▒▒▒▒  ▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒ ▒▒▒▒▒  ▒▒▒▒▒▒  
                                                                       
                                                                       
                                                                       
"""

unit_system = 'metric'  # 'metric' or 'imperial'
history = []

tile_db_file = 'tiles.json'

class Tile:
    def __init__(self, name, price, width, length):
        self.name = name
        self.price = price
        self.width = width
        self.length = length
        self.sq_price_m2, self.sq_price_ft2 = self.calculate_sq_prices()

    def calculate_sq_prices(self):
        if unit_system == 'metric':
            width_m = self.width / 1000
            length_m = self.length / 1000
        else:
            width_m = self.width / 12
            length_m = self.length / 12
        area_m2 = width_m * length_m
        area_ft2 = area_m2 * 10.7639
        price_per_m2 = self.price / area_m2 if area_m2 > 0 else 0
        price_per_ft2 = self.price / area_ft2 if area_ft2 > 0 else 0
        return price_per_m2, price_per_ft2

    def to_dict(self):
        return {'name': self.name, 'price': self.price, 'width': self.width, 'length': self.length}

    @staticmethod
    def from_dict(data):
        return Tile(data['name'], data['price'], data['width'], data['length'])

def load_tiles():
    global history
    if os.path.exists(tile_db_file):
        with open(tile_db_file, 'r') as f:
            data = json.load(f)
            history = [Tile.from_dict(d) for d in data]
        console.print(f"[green]Loaded {len(history)} tiles from database.[/green]")
    else:
        console.print("[yellow]No tile database found, starting fresh.[/yellow]")

def save_tiles():
    with open(tile_db_file, 'w') as f:
        json.dump([tile.to_dict() for tile in history], f, indent=2)
    console.print(f"[green]Saved {len(history)} tiles to database.[/green]")

def calculate_new():
    if unit_system == 'metric':
        width_label = "width (mm)"
        length_label = "length (mm)"
    else:
        width_label = "width (inches)"
        length_label = "length (inches)"

    name = console.input(f"[green]Enter tile name:[/green] ")
    price = float(console.input(f"[green]Enter unit price:[/green] "))
    width = float(console.input(f"[green]Enter {width_label}:[/green] "))
    length = float(console.input(f"[green]Enter {length_label}:[/green] "))

    tile = Tile(name, price, width, length)
    history.append(tile)
    console.print(f"\n[magenta]{tile.name}: {tile.sq_price_m2:.2f} per m², {tile.sq_price_ft2:.2f} per ft²[/magenta]\n")
    console.input("Press Enter to return to the main menu...")

def edit_tile():
    if not history:
        console.print("\n[red]No tiles available to edit.[/red]\n")
        console.input("Press Enter to return to the main menu...")
        return

    console.print("\n[cyan]--- EDIT TILE ---[/cyan]")
    for idx, tile in enumerate(history, 1):
        console.print(f"{idx}. {tile.name} ({tile.sq_price_m2:.2f} per m²)")

    choice = int(console.input("Enter the number of the tile to edit: "))
    if choice < 1 or choice > len(history):
        console.print("[red]Invalid choice.[/red]")
        console.input("Press Enter to return to the main menu...")
        return

    tile = history[choice - 1]

    if unit_system == 'metric':
        width_label = f"width (mm) [{tile.width}]"
        length_label = f"length (mm) [{tile.length}]"
    else:
        width_label = f"width (inches) [{tile.width}]"
        length_label = f"length (inches) [{tile.length}]"

    tile.name = console.input(f"Enter tile name [{tile.name}]: ") or tile.name
    tile.price = float(console.input(f"Enter unit price [{tile.price}]: ") or tile.price)
    tile.width = float(console.input(f"Enter {width_label}: ") or tile.width)
    tile.length = float(console.input(f"Enter {length_label}: ") or tile.length)
    tile.sq_price_m2, tile.sq_price_ft2 = tile.calculate_sq_prices()

    console.print(f"\n[green]Tile updated: {tile.name}: {tile.sq_price_m2:.2f} per m², {tile.sq_price_ft2:.2f} per ft²[/green]\n")
    console.input("Press Enter to return to the main menu...")

def view_history_alphabetical():
    if not history:
        console.print("\n[red]No history available.[/red]\n")
        console.input("Press Enter to return to the main menu...")
        return
    console.print("\n[cyan]--- PRICE HISTORY (Alphabetical) ---[/cyan]")
    for tile in sorted(history, key=lambda t: t.name.lower()):
        console.print(f"[yellow]{tile.name}[/yellow]: [blue]{tile.sq_price_m2:.2f} per m²[/blue], [blue]{tile.sq_price_ft2:.2f} per ft²[/blue]")
    console.print()
    console.input("Press Enter to return to the main menu...")

def view_history_by_price():
    if not history:
        console.print("\n[red]No history available.[/red]\n")
        console.input("Press Enter to return to the main menu...")
        return
    console.print("\n[cyan]--- PRICE HISTORY (Sorted by Price) ---[/cyan]")
    for tile in sorted(history, key=lambda t: t.sq_price_m2):
        console.print(f"[yellow]{tile.name}[/yellow]: [blue]{tile.sq_price_m2:.2f} per m²[/blue], [blue]{tile.sq_price_ft2:.2f} per ft²[/blue]")
    console.print()
    console.input("Press Enter to return to the main menu...")

def switch_units():
    global unit_system
    unit_system = 'imperial' if unit_system == 'metric' else 'metric'
    console.print(f"[cyan]Switched to {unit_system} system.[/cyan]")
    console.input("Press Enter to return to the main menu...")

def main():
    load_tiles()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(f"[bold cyan]{ASCII_TITLE}[/bold cyan]")
        console.print("[cyan]MAIN MENU[/cyan]")
        console.print("[green]1. CALCULATE NEW SQ PRICE[/green]")
        console.print("[yellow]2. VIEW HISTORY ALPHABETICALLY[/yellow]")
        console.print("[magenta]3. VIEW HISTORY BY PRICE[/magenta]")
        console.print("[blue]4. SWITCH UNIT SYSTEM[/blue]")
        console.print("[cyan]5. EDIT EXISTING TILE[/cyan]")
        console.print("[cyan]6. SAVE TILE DATABASE[/cyan]")
        console.print("[red]7. EXIT[/red]")
        choice = console.input("Choose an option: ")

        if choice == "1":
            calculate_new()
        elif choice == "2":
            view_history_alphabetical()
        elif choice == "3":
            view_history_by_price()
        elif choice == "4":
            switch_units()
        elif choice == "5":
            edit_tile()
        elif choice == "6":
            save_tiles()
            console.input("Press Enter to return to the main menu...")
        elif choice == "7":
            save_tiles()
            console.print("Exiting...")
            break
        else:
            console.print("[red]Invalid option, try again.[/red]\n")

if __name__ == "__main__":
    main()
