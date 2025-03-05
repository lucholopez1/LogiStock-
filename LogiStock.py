import csv
import os
import threading
from datetime import date, datetime
from tkinter import *
from tkinter import ttk, messagebox

class Product:
    
    """
    This class represents a product with attributes such as ID, name,
    price, and quantity

    Attributes:
        id (int): Product ID.
        name (str): Product name.
        price (float): Product price.
        base_price (float): Original base price of the product.
        quantity (int): Product quantity.
        category (str): Product category.
        entry_date (date): Date the product entered inventory.
        exit_date (date): Date the product left inventory.

    Methods:
        __str__() -> str:
            Returns product attributes.
        register_entry(self, quantity):
            Increases product quantity.
        register_exit(self, quantity):
            Reduces product quantity.
        get_price(self) -> float:
            Getter that returns the product price.
        set_price(self, value: float):
            Setter for product price.
        get_base_price(self) -> float:
            Getter that returns the base price of the product.
        set_base_price(self, value: float):
            Setter for the base price of the product.
    """

    def __init__(self, id: int, name: str, price: float, quantity: int, category: str, entry_date: date, exit_date: date = None, base_price = None):
        self.id = id
        self.name = name
        self._price = price
        self._base_price = base_price if base_price is not None else price  # Original price that doesn't changes, _base_price preserves the initial value that the product had when was created.
        self.quantity = quantity
        self.category = category
        self.entry_date = entry_date
        self.exit_date = exit_date


    def register_entry(self, quantity: int):
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
            self.quantity += quantity
            messagebox.showinfo("Entry Registered", f"{quantity} units of {self.name} have been added. Total in inventory: {self.quantity}.")
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", f"Error: {e}")

    def register_exit(self, quantity: int):
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
            if quantity > self.quantity:
                raise ValueError("Not enough units in stock.")
            self.quantity -= quantity
            messagebox.showinfo("Exit Registered", f"{quantity} units of {self.name} have been removed. Total in inventory: {self.quantity}.")
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", f"Error: {e}")

    # Getters and setters for price and base_price
    @property
    def price(self):
        """Returns the current price of the product (_price)."""
        return self._price
    
    @price.setter
    def price(self, value: float):
        """Sets a new current price (_price) while ensuring it remains valid."""
        if value <= 0:
            raise ValueError("Price must be greater than 0.")
        self._price = value

    @property
    def base_price(self):
        """Returns the original base price (_base_price) of the product."""
        return self._base_price

    @base_price.setter
    def base_price(self, value: float):
        """Allows modifying the base price (_base_price) while ensuring it remains valid."""
        if value <= 0:
            raise ValueError("Base price must be greater than 0.")
        self._base_price = value
        self._price = value  # Also updates the actual price if the base price changes

    def apply_discount(self, discount_pct: float):
        """
        Applies a discount based on the base price (_base_price).
        discount_pct is a float representing the percentage (0 <= discount_pct <= 100).
        """
        if not (0 <= discount_pct <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")

        # Calculation of discount factor(percentage)
        discount_factor = (100 - discount_pct) / 100.0
        self.price = self.base_price * discount_factor

        print(f"\nApplied a {discount_pct:.1f}% discount to {self.name}. "
              f"New price: ${self._price:.2f} (Base Price: ${self._base_price:.2f})")

    def reset_price(self):
        """
        Resets the product's current price (_price) to the original base price (_base_price).
        """
        self.price = self.base_price
        print(f"{self.name}'s price has been reset to base price: ${self.price:.2f}")

    def apply_incremental_discount(self, discount_pct: float):
        """
        Applies a discount on the current price (_price).
        If you apply multiple times, each discount is on the already discounted price.
        """
        if discount_pct < 0 or discount_pct > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")

        discount_factor = (100 - discount_pct) / 100.0
        self.price = self.price * discount_factor

        print(f"\nApplied an incremental {discount_pct:.1f}% discount to {self.name}. "
            f"New price: ${self.price:.2f}")
        
    def __str__(self):
        exit_date_str = self.exit_date if self.exit_date else "N/A"
        return (
                f"ID: {self.id}, Name: {self.name}, Price: ${self.price:.2f}, "
                f"Quantity: {self.quantity}, Category: {self.category}, "
                f"Entry Date: {self.entry_date}, Exit Date: {exit_date_str}"
                )


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
                    product.price,
                    product.base_price,  # Save the base price on the csv
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
                    try:
                        entry_date = datetime.fromisoformat(row["entry_date"]).date() if row["entry_date"] else None
                    except ValueError:
                        entry_date = date.today

                    try:
                        exit_date = datetime.fromisoformat(row["exit_date"]).date() if row["exit_date"] else None
                    except ValueError:
                        exit_date = None 

                    new_product = Product(
                        id=product_id,
                        name=name,
                        base_price=price,
                        quantity=quantity,
                        category=category,
                        entry_date=entry_date,
                        exit_date=exit_date
                    )
                    new_product.price = price  # Setter for price
                    new_product.base_price = base_price # Restore base price
                    self.products.append(new_product)

            messagebox.showinfo("Success", f"Inventory loaded from {filename} successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load inventory: {e}")

        
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

def validate_inputs(expected_inputs):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            validated_data = {}
            for key, value in expected_inputs.items():
                entry_value = getattr(self, key).get().strip()
                if not entry_value:
                    messagebox.showerror("Error", f"Input for {key} cannot be empty.")
                    return
                try:
                    validated_data[key] = value(entry_value)
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid input for {key}: {e}")
                    return
            return func(self, **validated_data)
        return wrapper
    return decorator

from inventory import Inventory
from product import Product
from report import Report
from tkinter import *
from tkinter import ttk, messagebox, Button
from datetime import date
from validation import validate_inputs




class InventoryGUI:
    """
    This class represents the graphical user interface (GUI) for managing an inventory.

    Attributes:
        root (Tk): The main application window.
        inventory (Inventory): An instance of the Inventory class that manages products.
        notebook (ttk.Notebook): A tabbed interface for different inventory operations.

    Methods:
        create_***_tab(self):
            Each method creates the tab for adding a new product, for removing a product, for listing all products, 
            for searching a product by ID, for updating a product's quantity, for registering product entries and exits, 
            for applying discounts to products, and for saving and loading inventory data from a CSV file respectively.

        add_product(self):
            Adds a new product to the inventory from user input.
        remove_product(self):
            Removes a product from the inventory based on user input.
        list_products(self):
            Displays the list of products in the inventory.
        search_product(self):
            Searches for a product by ID and displays its details.
        update_quantity(self):
            Updates the quantity of a product in the inventory.
        register_entry(self):
            Registers an entry (increase in quantity) for a product.
        register_exit(self):
            Registers an exit (decrease in quantity) for a product.
        apply_discount(self):
            Applies a discount to a product and updates its price.
        save_to_csv(self):
            Saves the inventory data to a CSV file.
        load_from_csv(self):
            Loads inventory data from a CSV file.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        self.inventory = Inventory()

        # Create the notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill='both')

        # Add tabs
        self.report_button = Button(root, text="Generar Reporte", command=self.generate_report)
        self.report_button.pack(pady=10)
        self.create_add_product_tab()
        self.create_remove_product_tab()
        self.create_list_products_tab()
        self.create_search_product_tab()
        self.create_update_quantity_tab()
        self.create_register_entry_exit_tab()
        self.create_discount_tab()
        self.create_csv_tab()

    def generate_report(self):
        try:
            report = Report()  # Instancia de la clase Report
            report.generate()  # Método para generar el reporte
            messagebox.showinfo("Éxito", "Reporte generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {e}")

    def create_add_product_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Add Product")

        Label(frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
        self.add_id = Entry(frame)
        self.add_id.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Product Name:").grid(row=1, column=0, padx=10, pady=5)
        self.add_name = Entry(frame)
        self.add_name.grid(row=1, column=1, padx=10, pady=5)

        Label(frame, text="Product Price:").grid(row=2, column=0, padx=10, pady=5)
        self.add_price = Entry(frame)
        self.add_price.grid(row=2, column=1, padx=10, pady=5)

        Label(frame, text="Product Quantity:").grid(row=3, column=0, padx=10, pady=5)
        self.add_quantity = Entry(frame)
        self.add_quantity.grid(row=3, column=1, padx=10, pady=5)

        Label(frame, text="Product Category:").grid(row=4, column=0, padx=10, pady=5)
        self.add_category = Entry(frame)
        self.add_category.grid(row=4, column=1, padx=10, pady=5)

        Label(frame, text="Entry Date (YYYY-MM-DD):").grid(row=5, column=0, padx=10, pady=5)
        self.add_entry_date = Entry(frame)
        self.add_entry_date.grid(row=5, column=1, padx=10, pady=5)

        Button(frame, text="Add Product", command=self.add_product).grid(row=6, column=0, columnspan=2, pady=10)

    def create_remove_product_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Remove Product")

        Label(frame, text="Product ID to Remove:").grid(row=0, column=0, padx=10, pady=5)
        self.remove_product_id = Entry(frame)
        self.remove_product_id.grid(row=0, column=1, padx=10, pady=5)

        Button(frame, text="Remove Product", command=self.remove_product).grid(row=1, column=0, columnspan=2, pady=10)

    def create_list_products_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="List Products")

        Button(frame, text="List Products", command=self.list_products).pack(pady=10)

        self.list_products_text = Text(frame, wrap=WORD, width=60, height=20)
        self.list_products_text.pack(pady=10)

    def create_search_product_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Search Product")

        Label(frame, text="Product ID to Search:").grid(row=0, column=0, padx=10, pady=5)
        self.search_product_id = Entry(frame)
        self.search_product_id.grid(row=0, column=1, padx=10, pady=5)

        Button(frame, text="Search Product", command=self.search_product).grid(row=1, column=0, columnspan=2, pady=10)

        self.search_product_text = Text(frame, wrap=WORD, width=60, height=20)
        self.search_product_text.grid(row=2, column=0, columnspan=2, pady=10)

    def create_update_quantity_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Update Quantity")

        Label(frame, text="Product ID to Update:").grid(row=0, column=0, padx=10, pady=5)
        self.update_quantity_id = Entry(frame)
        self.update_quantity_id.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="New Quantity:").grid(row=1, column=0, padx=10, pady=5)
        self.update_quantity_value = Entry(frame)
        self.update_quantity_value.grid(row=1, column=1, padx=10, pady=5)

        Button(frame, text="Update Quantity", command=self.update_quantity).grid(row=2, column=0, columnspan=2, pady=10)

    def create_register_entry_exit_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Register Entry/Exit")

        Label(frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_exit_product_id = Entry(frame)
        self.entry_exit_product_id.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_exit_quantity = Entry(frame)
        self.entry_exit_quantity.grid(row=1, column=1, padx=10, pady=5)

        Button(frame, text="Register Entry", command=self.register_entry).grid(row=2, column=0, columnspan=2, pady=10)
        Button(frame, text="Register Exit", command=self.register_exit).grid(row=3, column=0, columnspan=2, pady=10)

    def create_discount_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Apply Discount")

        Label(frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
        self.discount_product_id = Entry(frame)
        self.discount_product_id.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Discount Percentage:").grid(row=1, column=0, padx=10, pady=5)
        self.discount_percentage = Entry(frame)
        self.discount_percentage.grid(row=1, column=1, padx=10, pady=5)

        Button(frame, text="Apply Discount", command=self.apply_discount).grid(row=2, column=0, columnspan=2, pady=10)

    def create_csv_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="CSV Operations")

        Label(frame, text="CSV Filename (default: 'inventory.csv'):").grid(row=0, column=0, padx=10, pady=5)
        self.csv_filename = Entry(frame)
        self.csv_filename.grid(row=0, column=1, padx=10, pady=5)
        self.csv_filename.insert(0, "inventory.csv")

        Button(frame, text="Save to CSV", command=self.save_to_csv).grid(row=1, column=0, columnspan=2, pady=10)
        Button(frame, text="Load from CSV", command=self.load_from_csv).grid(row=2, column=0, columnspan=2, pady=10)



    

    @validate_inputs({
        'add_id': int,
        'add_name': str,
        'add_price': float,
        'add_quantity': int,
        'add_category': str,
        'add_entry_date': str
    })
    def add_product(self, add_id, add_name, add_price, add_quantity, add_category, add_entry_date):
        entry_date = date.fromisoformat(add_entry_date) if add_entry_date else date.today()
        product = Product(add_id, add_name, add_price, add_quantity, add_category, entry_date)
        product.base_price = add_price # Establish _base_price
        self.inventory.add_product(product)
        self.list_products()

    @validate_inputs({'remove_product_id': int})
    def remove_product(self, remove_product_id):
        self.inventory.remove_product(remove_product_id)
        self.list_products()

    def list_products(self):
        self.list_products_text.delete(1.0, END)
        inventory_list = self.inventory.list_inventory()
        self.list_products_text.insert(END, inventory_list)

    @validate_inputs({'search_product_id': int})
    def search_product(self, search_product_id):
        product = self.inventory.search_product(search_product_id)
        self.search_product_text.delete(1.0, END)
        if product:
            self.search_product_text.insert(END, str(product))
        else:
            messagebox.showinfo("Not Found", f"Product with ID {search_product_id} not found.")

    @validate_inputs({'update_quantity_id': int, 'update_quantity_value': int})
    def update_quantity(self, update_quantity_id, update_quantity_value):
        self.inventory.update_quantity(update_quantity_id, update_quantity_value)
        self.list_products()

    @validate_inputs({'entry_exit_product_id': int, 'entry_exit_quantity': int})
    def register_entry(self, entry_exit_product_id, entry_exit_quantity):
        product = self.inventory.search_product(entry_exit_product_id)
        if product:
            product.register_entry(entry_exit_quantity)
        else:
            messagebox.showinfo("Not Found", f"Product with ID {entry_exit_product_id} not found.")

    @validate_inputs({'entry_exit_product_id': int, 'entry_exit_quantity': int})
    def register_exit(self, entry_exit_product_id, entry_exit_quantity):
        product = self.inventory.search_product(entry_exit_product_id)
        if product:
            product.register_exit(entry_exit_quantity)
        else:
            messagebox.showinfo("Not Found", f"Product with ID {entry_exit_product_id} not found.")

    @validate_inputs({'discount_product_id': int, 'discount_percentage': float})
    def apply_discount(self, discount_product_id, discount_percentage):
        product = self.inventory.search_product(discount_product_id)
        if product:
            try:
                product.apply_discount(discount_percentage)
                messagebox.showinfo("Success", f"Discount applied! New price: ${product.price:.2f}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Not Found", f"Product with ID {discount_product_id} not found.")

    def save_to_csv(self):
        filename = self.csv_filename.get()
        self.inventory.save_to_csv(filename)

    def load_from_csv(self):
        filename = self.csv_filename.get()
        self.inventory.load_from_csv(filename)
