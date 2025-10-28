import json
import logging
from datetime import datetime
from typing import Dict, List, Union, Optional

class InventorySystem:
    def __init__(self):
        self.stock_data: Dict[str, int] = {}
        self.logger = logging.getLogger(__name__)
        
    def addItem(self, item: str, qty: int, logs: Optional[List[str]] = None) -> bool:
        """Add items to inventory with validation."""
        if logs is None:
            logs = []
            
        if not isinstance(item, str):
            self.logger.error(f"Invalid item type: {type(item)}")
            return False
            
        if not isinstance(qty, int):
            self.logger.error(f"Invalid quantity type: {type(qty)}")
            return False
            
        if qty <= 0:
            self.logger.error(f"Invalid quantity value: {qty}")
            return False
            
        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        log_entry = f"{datetime.now()}: Added {qty} of {item}"
        logs.append(log_entry)
        self.logger.info(log_entry)
        return True

    def removeItem(self, item: str, qty: int) -> bool:
        """Remove items from inventory with validation."""
        if not isinstance(item, str) or not isinstance(qty, int):
            self.logger.error("Invalid input types")
            return False
            
        if item not in self.stock_data:
            self.logger.error(f"Item {item} not found in inventory")
            return False
            
        if qty <= 0:
            self.logger.error(f"Invalid quantity for removal: {qty}")
            return False
            
        if self.stock_data[item] < qty:
            self.logger.error(f"Insufficient stock for {item}")
            return False
            
        self.stock_data[item] -= qty
        if self.stock_data[item] <= 0:
            del self.stock_data[item]
        return True

    def getQty(self, item: str) -> Optional[int]:
        """Get quantity of an item in inventory."""
        if not isinstance(item, str):
            self.logger.error(f"Invalid item type: {type(item)}")
            return None
        return self.stock_data.get(item, 0)

    def loadData(self, file: str = "inventory.json") -> bool:
        """Load inventory data from JSON file."""
        try:
            with open(file, "r") as f:
                self.stock_data = json.loads(f.read())
            return True
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading data: {str(e)}")
            return False

    def saveData(self, file: str = "inventory.json") -> bool:
        """Save inventory data to JSON file."""
        try:
            with open(file, "w") as f:
                json.dump(self.stock_data, f, indent=2)
            return True
        except IOError as e:
            self.logger.error(f"Error saving data: {str(e)}")
            return False

    def printData(self) -> None:
        """Print current inventory report."""
        print("Items Report")
        for item, qty in self.stock_data.items():
            print(f"{item} -> {qty}")

    def checkLowItems(self, threshold: int = 5) -> List[str]:
        """Check items below threshold quantity."""
        if not isinstance(threshold, int) or threshold < 0:
            self.logger.error(f"Invalid threshold: {threshold}")
            return []
        return [item for item, qty in self.stock_data.items() if qty < threshold]

def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, no check
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    eval("print('eval used')")  # dangerous

main()
