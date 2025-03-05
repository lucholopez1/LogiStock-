from tkinter import messagebox

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