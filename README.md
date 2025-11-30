# tileCalc
TileCalc - tile price calculator utility
A Python console application for calculating the square meter and square foot price of tiles. Users can save, view, and edit tile information with support for both metric and imperial units. The application features colored output using Rich and saves tile data to a JSON database.

Features

Calculate square meter and square foot price of tiles.
Store tile information in a JSON database (tiles.json).
View tile history sorted alphabetically or by price.
Edit existing tile information.
Switch between metric and imperial units.
Colored console output and clear interface using Rich.

Installation
Ensure you have Python 3.7+ installed.

Install the required library:
pip install rich
Download the tileCalculator.py script.

Usage
Run the program:
python tileCalculator.py

The main menu provides the following options:
Calculate New Square Price
View History Alphabetically
View History By Price
Switch Unit System (Metric/Imperial)
Edit Existing Tile
Save Tile Database
Exit

Follow the on-screen prompts to input tile details or interact with the database.

Data Storage
Tile data is automatically loaded from and saved to tiles.json. You can manually save at any time via the menu.
