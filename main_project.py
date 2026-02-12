# main_project.py
# ---------------------------------------------------------
# COMMERCIAL DASHBOARD UI (With Delete Functionality)
# ---------------------------------------------------------

'''
==============================================================================
> PROJECT: A&E Finance Dashboard
> FILE: main_project.py
------------------------------------------------------------------------------
> DEVELOPER: Antonio Lujan
> DATE: February 2026

> DESCRIPTION:
The main entry point for the Finance Dashboard application. This file handles 
the Modern UI implementation using CustomTkinter, event handling, and 
user interaction logic.
==============================================================================
'''

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from tkcalendar import DateEntry
import finance_logic  # Imports your backend logic

# --- APP CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class MetricCard(ctk.CTkFrame):
    """Custom Widget: A box that shows a Label and a Value"""
    def __init__(self, parent, title, value, icon_color, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color=("gray90", "gray13"))
        
        self.lbl_title = ctk.CTkLabel(self, text=title, font=("Arial", 12, "bold"), text_color="gray60")
        self.lbl_title.pack(padx=10, pady=(10, 0), anchor="w")
        
        self.lbl_value = ctk.CTkLabel(self, text=value, font=("Arial", 20, "bold"), text_color=icon_color)
        self.lbl_value.pack(padx=10, pady=(0, 10), anchor="w")

    def update_value(self, new_value):
        self.lbl_value.configure(text=new_value)

class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("A&E Finance Dashboard") 
        self.geometry("1400x750")
        self.manager = finance_logic.FinanceManager()

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= SIDEBAR =================
        self.sidebar = ctk.CTkFrame(self, width=380, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="A&E FINANCE", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input Section
        self.lbl_new = ctk.CTkLabel(self.sidebar, text="NEW TRANSACTION", text_color="gray60", font=("Arial", 10, "bold"))
        self.lbl_new.grid(row=1, column=0, padx=20, pady=(20, 5), sticky="w")

        self.type_var = ctk.StringVar(value="Expense")
        self.type_menu = ctk.CTkSegmentedButton(self.sidebar, values=["Income", "Expense"], variable=self.type_var)
        self.type_menu.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.date_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.date_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.date_frame, text="Date:").pack(side="left", padx=(0, 10))
        self.date_entry = DateEntry(self.date_frame, width=12, background='#1f538d', 
                                    foreground='white', borderwidth=0, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(side="right")

        # Inputs
        self.desc_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Description (e.g. Salary)", 
                                     width=320, justify="center")
        self.desc_entry.grid(row=4, column=0, padx=20, pady=10)

        self.amount_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Amount (0.00)", 
                                       width=320, justify="center")
        self.amount_entry.grid(row=5, column=0, padx=20, pady=10)

        self.cat_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Category (Optional)", 
                                    width=320, justify="center")
        self.cat_entry.grid(row=6, column=0, padx=20, pady=10)

        # Add Button
        self.add_btn = ctk.CTkButton(self.sidebar, text="Add Transaction", command=self.add_entry, width=320)
        self.add_btn.grid(row=7, column=0, padx=20, pady=20)

        # Theme Switch
        self.theme_switch = ctk.CTkSwitch(self.sidebar, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.select()
        self.theme_switch.grid(row=11, column=0, padx=20, pady=20, sticky="s")

        # ================= MAIN DASHBOARD =================
        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_view.grid_rowconfigure(2, weight=1)

        # KPI Cards
        self.kpi_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.kpi_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.kpi_frame.grid_columnconfigure((0,1,2), weight=1)

        self.card_inc = MetricCard(self.kpi_frame, "TOTAL INCOME", "$0.00", "#2cc985")
        self.card_inc.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.card_exp = MetricCard(self.kpi_frame, "TOTAL EXPENSES", "$0.00", "#ff4d4d")
        self.card_exp.grid(row=0, column=1, sticky="ew", padx=10)

        self.card_bal = MetricCard(self.kpi_frame, "NET BALANCE", "$0.00", "#3B8ED0")
        self.card_bal.grid(row=0, column=2, sticky="ew", padx=(10, 0))

        # List
        self.list_frame = ctk.CTkFrame(self.main_view)
        self.list_frame.grid(row=2, column=0, sticky="nsew")
        
        self.tree = ttk.Treeview(self.list_frame, columns=("Date", "Type", "Amount", "Description"), show="headings")
        
        self.tree.heading("Date", text="Date", anchor="center")
        self.tree.heading("Type", text="Type", anchor="center")
        self.tree.heading("Amount", text="Amount", anchor="center")
        self.tree.heading("Description", text="Description", anchor="center")
        
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Type", width=150, anchor="center")
        self.tree.column("Amount", width=150, anchor="center")
        self.tree.column("Description", width=500, anchor="center")

        self.style_treeview() # Apply styles

        scrollbar = ctk.CTkScrollbar(self.list_frame, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y", padx=2, pady=2)
        
        # --- ACTION BUTTONS ROW (Export & Delete) ---
        self.btn_row = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.btn_row.grid(row=3, column=0, pady=10, sticky="e")

        # Delete Button (Red)
        self.delete_btn = ctk.CTkButton(self.btn_row, text="Delete Selected", command=self.delete_entry,
                                        fg_color="#cf3a3a", hover_color="#a12b2b", width=120)
        self.delete_btn.pack(side="left", padx=(0, 10))

        # Export Button (Transparent/Bordered)
        self.save_btn = ctk.CTkButton(self.btn_row, text="Export Report", command=self.save_data, 
                                      fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.save_btn.pack(side="left")

    def style_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            bg, fg = "#2b2b2b", "white"
            h_bg, h_fg = "#1f538d", "white"
        else:
            bg, fg = "white", "black"
            h_bg, h_fg = "#e1e1e1", "black"
        
        style.configure("Treeview", background=bg, foreground=fg, fieldbackground=bg, borderwidth=0, rowheight=30)
        style.configure("Treeview.Heading", background=h_bg, foreground=h_fg, relief="flat")
        style.map("Treeview", background=[('selected', '#3B8ED0')])

    def add_entry(self):
        date = self.date_entry.get()
        desc = self.desc_entry.get()
        t_type = self.type_var.get()
        category = self.cat_entry.get()

        try:
            val = self.amount_entry.get()
            if not val: raise ValueError
            amount = float(val)
            if amount < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        if not desc:
            messagebox.showwarning("Error", "Description is required.")
            return

        if t_type == "Expense":
            if not category: category = "General"
            new_record = finance_logic.Expense(date, amount, desc, category)
        else:
            new_record = finance_logic.Transaction(date, amount, desc)

        self.manager.add_transaction(new_record)
        self.update_dashboard()
        
        self.amount_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.cat_entry.delete(0, "end")

    # --- NEW FUNCTION TO DELETE ENTRIES ---
    def delete_entry(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please click on a transaction to select it first.")
            return

        # Confirmation Dialog
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?")
        if confirm:
            # The treeview index matches the list index because we insert them in order
            index = self.tree.index(selected_item[0])
            
            # Remove from backend list
            self.manager.transactions.pop(index)
            
            # Refresh UI
            self.update_dashboard()

    def update_dashboard(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for t in self.manager.transactions:
            t_type = "Expense" if isinstance(t, finance_logic.Expense) else "Income"
            self.tree.insert("", "end", values=(t.date, t_type, f"${t.amount:.2f}", t.description))

        inc = self.manager.get_total_income()
        exp = self.manager.get_total_expense()
        bal = self.manager.calculate_balance()

        self.card_inc.update_value(f"${inc:,.2f}")
        self.card_exp.update_value(f"${exp:,.2f}")
        self.card_bal.update_value(f"${bal:,.2f}")

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        self.style_treeview()

    def save_data(self):
        if self.manager.save_to_file():
            messagebox.showinfo("Success", "Report exported successfully!")
        else:
            messagebox.showerror("Error", "Could not save file.")

if __name__ == "__main__":
    try:
        app = FinanceApp()
        app.mainloop()
    except Exception as e:
        import traceback
        print("\n!!! PROGRAM CRASHED !!!")
        print("Here is the exact error:")
        print("-" * 30)
        traceback.print_exc()
        print("-" * 30)
        input("Press Enter to close this window...")