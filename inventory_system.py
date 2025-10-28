"""
Inventory System Module
-----------------------
This module provides basic functions to manage an inventory system including
adding, removing, and listing items, as well as loading and saving data.
"""

import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Global variable for storing inventory data
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add a specific quantity of an item to the stock."""
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning("Invalid input types for item or qty.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Remove a specific quantity of an item from the stock."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.warning("Tried to remove a non-existent item: %s", item)
    except TypeError as e:
        logging.error("Invalid type during removal: %s", e)


def get_qty(item):
    """Get the quantity of a specific item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from a JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Data loaded successfully from %s", file)
    except FileNotFoundError:
        logging.warning("File %s not found. Starting with empty stock.", file)
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON file %s: %s", file, e)


def save_data(file="inventory.json"):
    """Save inventory data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Data saved successfully to %s", file)
    except OSError as e:
        logging.error("Error saving data to %s: %s", file, e)


def print_data():
    """Display all items and their quantities."""
    print("Items Report")
    for item, quantity in stock_data.items():
        print(f"{item} -> {quantity}")


def check_low_items(threshold=5):
    """Return a list of items below a certain quantity threshold."""
    result = [item for item, qty in stock_data.items() if qty < threshold]
    return result


def main():
    """Main execution block for demonstration."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item("orange", 5)

    remove_item("apple", 3)
    remove_item("orange", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    save_data()
    load_data()
    print_data()

    # Removed eval() for security reasons
    logging.info("Static analysis: insecure eval() removed.")


if __name__ == "__main__":
    main()
