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
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        self.inventory = Inventory()

        # Create the notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill='both')

        # Add tabs and reports Button
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
        if not filename:
            filename = "inventory.csv"
        self.inventory.save_to_csv(filename)
        self.list_products()
        

    def load_from_csv(self):
        filename = self.csv_filename.get().strip()
        if not filename:
            filename = "inventory.csv"
        self.inventory.load_from_csv(filename)
        self.list_products()

    def generate_report(self):
        try:
            report = Report(self.inventory)  # Instancia de la clase Report
            report.generate_current_report()  # Método para generar el reporte
            messagebox.showinfo("Reporte generated succesfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {e}")