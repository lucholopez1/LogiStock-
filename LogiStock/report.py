from inventory import Inventory
from tkinter import messagebox
import threading

class Report:
    # Class that manages reports of inventory
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def _generate_report_logic(self):
        # Internal method to generate the report without blocking the main thread.
        report = self.inventory.list_inventory()
        messagebox.showinfo("Current Inventory Report", report)

    def generate_current_report(self):
        # Generates a report of the current inventory on a separated thread
        thread = threading.Thread(target=self._generate_report_logic)
        thread.start()

    def generate_historical_report(self):
        # Generates an historical report of inventory
        historical_report = "Historical Inventory Report:\n"
        for product in self.inventory.products:
            historical_report += (f"Product: {product.name}, Entry Date: {product.entry_date}, "
                                  f"Exit Date: {product.exit_date or 'N/A'}\n")
        messagebox.showinfo("Historical Inventory Report", historical_report)