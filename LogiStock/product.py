from tkinter import messagebox
from datetime import date, datetime

class Product:
    """
    This class represents a product with attributes such as ID, name,
    price, and quantity

    Attributes:
        id (int): Product ID, name (str): Product name, price (float): Product price,
        base_price (float): Original base price of the product, quantity (int): Product quantity,
        category (str): Product category, entry_date (date): Date the product entered inventory,
        exit_date (date): Date the product left inventory.

    Methods:
        __str__() -> str:
            Returns product attributes.
        register_entry(self, quantity):
            Increases product quantity.
        register_exit(self, quantity):
            Reduces product quantity.
        @property price(self) -> float:
            Getter that returns the product price.
        @price.setter (self, value: float):
            Setter for product price.
        @property base_price(self) -> float:
            Getter that returns the base price of the product.
        @base_price.setter(self, value: float):
            Setter for the base price of the product.
    """

    def __init__(self, id: int, name: str, price: float, quantity: int, category: str, entry_date: date, exit_date: date = None, base_price = None):
        self.id = id
        self.name = name
        self._price = price
        self._base_price = base_price if base_price is not None else price  # Original price that doesn't changes, _base_price preserves the initial value that the product had when was created.
        self.quantity = quantity
        self.quantity_history = [(datetime.now(), quantity)]
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
