from inventory import Inventory
import threading
from tkinter import filedialog, messagebox

class Report:
    def __init__(self, inventory : Inventory):
        self.inventory = inventory

    def _generate_report_logic(self, file_path):
        """ Genera un reporte de inventario y lo guarda en un archivo .txt """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("📦 INVENTORY REPORT 📦\n\n")
                file.write("Product Name | Entry Date | Exit Date | Current Quantity | Quantity Changes\n")
                file.write("-" * 80 + "\n")

                for product in self.inventory.products:
                    entry_date = product.entry_date
                    exit_date = product.exit_date if product.exit_date else "Still in stock"
                    quantity_changes = ", ".join([f"{change} on {date}" for date, change in product.quantity_history])
                    
                    file.write(f"{product.name} | {entry_date} | {exit_date} | {product.quantity} | {quantity_changes}\n")
            
            messagebox.showinfo("Report Generated", f"Report saved successfully:\n{file_path}")
            self._open_report(file_path)  # Abre el archivo después de crearlo

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def _open_report(self, file_path):
        """ Intenta abrir el archivo del reporte en el bloc de notas """
        import os
        try:
            os.startfile(file_path)  # Windows
        except AttributeError:
            os.system(f"open {file_path}")  # macOS
        except Exception:
            os.system(f"xdg-open {file_path}")  # Linux

    def generate_current_report(self):
        """ Permite al usuario elegir dónde guardar el archivo y genera el reporte en un hilo separado """
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                 title="Save Report As")
        if file_path:
            thread = threading.Thread(target=self._generate_report_logic, args=(file_path,))
            thread.start()