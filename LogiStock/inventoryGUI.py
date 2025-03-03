from inventory import Inventory
from product import Product
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date



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
        self.create_add_product_tab()
        self.create_remove_product_tab()
        self.create_list_products_tab()
        self.create_search_product_tab()
        self.create_update_quantity_tab()
        self.create_register_entry_exit_tab()
        self.create_discount_tab()
        self.create_csv_tab()

    def create_add_product_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Add Product")

        Label(frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
        self.add_product_id = Entry(frame)
        self.add_product_id.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Product Name:").grid(row=1, column=0, padx=10, pady=5)
        self.add_product_name = Entry(frame)
        self.add_product_name.grid(row=1, column=1, padx=10, pady=5)

        Label(frame, text="Product Price:").grid(row=2, column=0, padx=10, pady=5)
        self.add_product_price = Entry(frame)
        self.add_product_price.grid(row=2, column=1, padx=10, pady=5)

        Label(frame, text="Product Quantity:").grid(row=3, column=0, padx=10, pady=5)
        self.add_product_quantity = Entry(frame)
        self.add_product_quantity.grid(row=3, column=1, padx=10, pady=5)

        Label(frame, text="Product Category:").grid(row=4, column=0, padx=10, pady=5)
        self.add_product_category = Entry(frame)
        self.add_product_category.grid(row=4, column=1, padx=10, pady=5)

        Label(frame, text="Entry Date (YYYY-MM-DD):").grid(row=5, column=0, padx=10, pady=5)
        self.add_product_entry_date = Entry(frame)
        self.add_product_entry_date.grid(row=5, column=1, padx=10, pady=5)

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


    def add_product(self):
        try:
            id = int(self.add_product_id.get())
            name = self.add_product_name.get()
            price = float(self.add_product_price.get())
            quantity = int(self.add_product_quantity.get())
            category = self.add_product_category.get()
            entry_date_str = self.add_product_entry_date.get()
            entry_date = date.fromisoformat(entry_date_str) if entry_date_str else date.today()
            
            product = Product(id, name, price, quantity, category, entry_date)
            product.set_base_price(price)  # Establish _base_price

            self.inventory.add_product(product)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def remove_product(self):
        try:
            id = int(self.remove_product_id.get())
            self.inventory.remove_product(id)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def list_products(self):
        self.list_products_text.delete(1.0, END)
        inventory_list = self.inventory.list_inventory()
        self.list_products_text.insert(END, inventory_list)

    def search_product(self):
        try:
            id = int(self.search_product_id.get())
            product = self.inventory.search_product(id)
            if product:
                self.search_product_text.delete(1.0, END)
                self.search_product_text.insert(END, str(product))
            else:
                messagebox.showinfo("Not Found", f"Product with ID {id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_quantity(self):
        try:
            id = int(self.update_quantity_id.get())
            new_quantity = int(self.update_quantity_value.get())
            self.inventory.update_quantity(id, new_quantity)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def register_entry(self):
        try:
            id = int(self.entry_exit_product_id.get())
            quantity = int(self.entry_exit_quantity.get())
            product = self.inventory.search_product(id)
            if product:
                product.register_entry(quantity)
            else:
                messagebox.showinfo("Not Found", f"Product with ID {id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def register_exit(self):
        try:
            id = int(self.entry_exit_product_id.get())
            quantity = int(self.entry_exit_quantity.get())
            product = self.inventory.search_product(id)
            if product:
                product.register_exit(quantity)
            else:
                messagebox.showinfo("Not Found", f"Product with ID {id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def apply_discount(self):
        try:
            id = int(self.discount_product_id.get())
            discount_pct = float(self.discount_percentage.get())

            product = self.inventory.search_product(id)
            if product:
                product.apply_discount(discount_pct)
                messagebox.showinfo("Success", f"Discount applied successfully! New price: ${product.get_price():.2f}")
            else:
                messagebox.showinfo("Not Found", f"Product with ID {id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def save_to_csv(self):
        filename = self.csv_filename.get()
        self.inventory.save_to_csv(filename)

    def load_from_csv(self):
        filename = self.csv_filename.get()
        self.inventory.load_from_csv(filename)