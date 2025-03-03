import os
import csv
from product import Product
from tkinter import messagebox
from datetime import date, datetime

class Inventory:
    """
    Attributes:
        products (list): A list that stores all products in the inventory.

    Methods:
        add_product(self, product: Product):
            Adds a new product to the inventory if its ID is not already in use.
        remove_product(self, product_id: int):
            Removes a product from the inventory by its ID, if found.
        list_inventory(self):
            Displays all current products in the inventory.
        search_product(self, product_id: int) -> Product | None:
            Searches for a product by its ID and returns it if found, otherwise returns None.
        update_quantity(self, product_id: int, new_quantity: int):
            Updates the quantity of an existing product by its ID.
        load_from_csv(self, filename: str = "inventory.csv"):
            Loads products and information from a CSV file into the inventory.
        save_to_csv(self, filename: str = "inventory.csv"):
            Saves the current inventory data to a CSV file.
    """

    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        if any(p.id == product.id for p in self.products):
            messagebox.showwarning("Warning", "The product already exists in the inventory.")
        else:
            self.products.append(product)
            messagebox.showinfo("Product Added", f"Product {product.name} successfully added to inventory.")

    def remove_product(self, id: int):
        product = self.search_product(id)
        if product:
            self.products.remove(product)
            messagebox.showinfo("Product Removed", f"Product {product.name} removed successfully from inventory.")
        else:
            messagebox.showerror("Error", f"Product with ID {id} not found.")

    def list_inventory(self):
        inventory_list = "\n=== Current Inventory ===\n"
        if not self.products:
            inventory_list += "The inventory is empty."
        for product in self.products:
            inventory_list += f"{product}\n"
        return inventory_list

    def search_product(self, id: int):
        for product in self.products:
            if product.id == id:
                return product
        return None

    def update_quantity(self, id: int, new_quantity: int):
        try:
            product = self.search_product(id)
            if product is None:
                raise ValueError(f"Product with ID {id} not found.")  # Exception if the ID doesn't exists

            if not isinstance(new_quantity, int):
                raise TypeError("Quantity must be an integer.")  # Exception is the quantity is not an integer

            if new_quantity < 0:
                raise ValueError("Quantity cannot be negative.")  # Exception if new_quantity is negative

            product.quantity = new_quantity
            messagebox.showinfo("Quantity Updated", f"Successfully updated quantity of {product.name} to {product.quantity}.\n")

        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", f"Error in update_quantity: {e}\n")

    def save_to_csv(self, filename: str = "inventory.csv"):
        # Saves the current inventory to a CSV file.
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Encabezado
            writer.writerow(["id", "name", "price", "base_price", "quantity", "category", "entry_date", "exit_date"])
            # Datos de cada producto
            for product in self.products:
                entry_date_str = product.entry_date.isoformat()
                exit_date_str = product.exit_date.isoformat() if product.exit_date else ""
                writer.writerow([
                    product.id,
                    product.name,
                    product.get_price(),
                    product.get_base_price(),  # Save the base price on the csv
                    product.quantity,
                    product.category,
                    entry_date_str,
                    exit_date_str
                ])
        messagebox.showinfo("Success", f"Inventory saved to {filename} successfully.")

    def load_from_csv(self, filename: str = "inventory.csv"):
        ''' Loads products and information from a CSV file into the current inventory.'''
        # Clear the list for "reconstructing" the inventory
        self.products.clear()

        # Verificamos si el archivo existe
        if not os.path.exists(filename):
            messagebox.showwarning("Warning", f"File '{filename}' does not exist. Starting with an empty inventory.")
            return

        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product_id = int(row["id"])
                    name = row["name"]
                    price = float(row["price"])
                    base_price = float(row["base_price"])  # Load base price
                    quantity = int(row["quantity"])
                    category = row["category"]

                    # Convertir string a date usando isoformat
                    entry_date = datetime.fromisoformat(row["entry_date"]) if row["entry_date"] else None
                    exit_date = datetime.fromisoformat(row["exit_date"]) if row["exit_date"] else None

                    new_product = Product(
                        id=product_id,
                        name=name,
                        base_price=price,
                        quantity=quantity,
                        category=category,
                        entry_date=entry_date,
                        exit_date=exit_date
                    )
                    new_product.set_price(price)  # Setter for price
                    new_product.set_base_price(base_price) # Restore base price
                    self.products.append(new_product)


            messagebox.showinfo("Success", f"Inventory loaded from {filename} successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load inventory: {e}")