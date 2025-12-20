import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from model_predict import predict_house_value

def launch_gui():
    def predict():
        try:
            # Get input values from GUI
            longitude = float(entry_longitude.get())
            latitude = float(entry_latitude.get())
            housing_median_age = float(entry_age.get())
            total_rooms = float(entry_rooms.get())
            total_bedrooms = float(entry_bedrooms.get())
            population = float(entry_population.get())
            households = float(entry_households.get())
            median_income = float(entry_income.get())
            ocean = ocean_var.get()

            # Prepare input dataframe
            input_df = pd.DataFrame([{
                'longitude': longitude,
                'latitude': latitude,
                'housing_median_age': housing_median_age,
                'total_rooms': total_rooms,
                'total_bedrooms': total_bedrooms,
                'population': population,
                'households': households,
                'median_income': median_income,
                'ocean_proximity': ocean
            }])

            # Predict
            pred = predict_house_value(input_df)

            # Custom styled messagebox
            result_window = tk.Toplevel(root)
            result_window.title("Prediction Result")
            result_window.geometry("400x200")
            result_window.configure(bg="#2c3e50")
            result_window.resizable(False, False)

            # Center the window
            result_window.transient(root)
            result_window.grab_set()

            tk.Label(
                result_window,
                text="🏡 Predicted House Value",
                font=("Helvetica", 14, "bold"),
                bg="#2c3e50",
                fg="#ecf0f1",
                pady=20
            ).pack()

            tk.Label(
                result_window,
                text=f"${pred:,.2f}",
                font=("Helvetica", 28, "bold"),
                bg="#2c3e50",
                fg="#27ae60"
            ).pack(pady=10)

            tk.Button(
                result_window,
                text="OK",
                command=result_window.destroy,
                font=("Helvetica", 11),
                bg="#3498db",
                fg="white",
                activebackground="#2980b9",
                activeforeground="white",
                relief=tk.FLAT,
                padx=30,
                pady=8,
                cursor="hand2"
            ).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def on_enter(e):
        e.widget['background'] = '#2980b9'

    def on_leave(e):
        e.widget['background'] = '#3498db'

    # GUI layout
    root = tk.Tk()
    root.title("California Housing Price Predictor")
    root.geometry("550x650")
    root.configure(bg="#ecf0f1")
    root.resizable(False, False)

    # Header
    header_frame = tk.Frame(root, bg="#3498db", height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="🏠 California Housing Price Predictor",
        font=("Helvetica", 18, "bold"),
        bg="#3498db",
        fg="white"
    ).pack(expand=True)

    # Main content frame
    main_frame = tk.Frame(root, bg="#ecf0f1")
    main_frame.pack(pady=30, padx=40, fill=tk.BOTH, expand=True)

    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')

    # Configure entry style
    style.configure(
        "Custom.TEntry",
        fieldbackground="white",
        borderwidth=0,
        relief=tk.FLAT
    )

    labels = [
        "Longitude", "Latitude", "Housing Median Age", "Total Rooms",
        "Total Bedrooms", "Population", "Households", "Median Income"
    ]
    entries = []

    for i, text in enumerate(labels):
        # Label
        tk.Label(
            main_frame,
            text=text,
            font=("Helvetica", 11),
            bg="#ecf0f1",
            fg="#2c3e50",
            anchor="w"
        ).grid(row=i, column=0, sticky="w", pady=8)

        # Entry with styled frame
        entry_frame = tk.Frame(main_frame, bg="white", highlightbackground="#bdc3c7", highlightthickness=1)
        entry_frame.grid(row=i, column=1, sticky="ew", pady=8, padx=(10, 0))

        entry = tk.Entry(
            entry_frame,
            font=("Helvetica", 11),
            bg="white",
            fg="#2c3e50",
            relief=tk.FLAT,
            borderwidth=5
        )
        entry.pack(fill=tk.BOTH, expand=True)
        entries.append(entry)

    (entry_longitude, entry_latitude, entry_age, entry_rooms,
     entry_bedrooms, entry_population, entry_households, entry_income) = entries

    # Configure grid weights
    main_frame.columnconfigure(1, weight=1)

    # Ocean Proximity dropdown
    tk.Label(
        main_frame,
        text="Ocean Proximity",
        font=("Helvetica", 11),
        bg="#ecf0f1",
        fg="#2c3e50",
        anchor="w"
    ).grid(row=8, column=0, sticky="w", pady=8)

    ocean_var = tk.StringVar(root)
    ocean_var.set("INLAND")

    # Styled dropdown
    ocean_frame = tk.Frame(main_frame, bg="white", highlightbackground="#bdc3c7", highlightthickness=1)
    ocean_frame.grid(row=8, column=1, sticky="ew", pady=8, padx=(10, 0))

    ocean_menu = tk.OptionMenu(
        ocean_frame,
        ocean_var,
        "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN", "<1H OCEAN"
    )
    ocean_menu.config(
        font=("Helvetica", 11),
        bg="white",
        fg="#2c3e50",
        relief=tk.FLAT,
        activebackground="#ecf0f1",
        activeforeground="#2c3e50",
        highlightthickness=0,
        borderwidth=0
    )
    ocean_menu["menu"].config(
        font=("Helvetica", 10),
        bg="white",
        fg="#2c3e50",
        activebackground="#3498db",
        activeforeground="white"
    )
    ocean_menu.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

    # Predict button
    predict_btn = tk.Button(
        main_frame,
        text="Predict Price",
        command=predict,
        font=("Helvetica", 13, "bold"),
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        relief=tk.FLAT,
        padx=40,
        pady=12,
        cursor="hand2"
    )
    predict_btn.grid(row=9, column=0, columnspan=2, pady=30)

    # Hover effects for button
    predict_btn.bind("<Enter>", on_enter)
    predict_btn.bind("<Leave>", on_leave)

    # Footer
    tk.Label(
        root,
        text="Enter property details to estimate market value",
        font=("Helvetica", 9),
        bg="#ecf0f1",
        fg="#7f8c8d"
    ).pack(side=tk.BOTTOM, pady=10)

    root.mainloop()

# Launch GUI when this file is run
if __name__ == "__main__":
    launch_gui()