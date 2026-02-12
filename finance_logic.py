'''
==============================================================================
> PROJECT: A&E Finance Dashboard
> FILE: finance_logic.py
------------------------------------------------------------------------------
> DEVELOPER: Antonio Lujan
> DATE: February 2026

> DESCRIPTION:
The backend logic module. This file defines the core data structures 
(Transaction, Expense) and the FinanceManager class responsible for data 
manipulation, calculations, and file I/O operations.
==============================================================================
'''
# ---------------------------------------------------------
# BACKEND LOGIC MODULE
# Requirements Met:
# 1. Custom Module
# 2. Classes (Parent & Sub-class)
# 3. File Operations
# ---------------------------------------------------------

class Transaction:
    """Parent Class for Income"""
    def __init__(self, date, amount, description):
        self.date = date
        self.amount = float(amount)
        self.description = description

    def get_summary(self):
        return f"{self.date} | Income | ${self.amount:.2f} | {self.description}"

class Expense(Transaction):
    """Sub-class for Expenses"""
    def __init__(self, date, amount, description, category):
        super().__init__(date, amount, description)
        self.category = category

    def get_summary(self):
        return f"{self.date} | Expense | ${self.amount:.2f} | {self.description} ({self.category})"

class FinanceManager:
    """Manager Class to handle the list of data"""
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction_obj):
        self.transactions.append(transaction_obj)

    def calculate_balance(self):
        return self.get_total_income() - self.get_total_expense()

    def get_total_income(self):
        """Calculates total income for Dashboard Cards"""
        total = 0.0
        for t in self.transactions:
            # If it is NOT an Expense, it is Income
            if not isinstance(t, Expense):
                total += t.amount
        return total

    def get_total_expense(self):
        """Calculates total expenses for Dashboard Cards"""
        total = 0.0
        for t in self.transactions:
            if isinstance(t, Expense):
                total += t.amount
        return total

    def save_to_file(self, filename="finance_summary.txt"):
        """Saves report to text file"""
        try:
            with open(filename, "w") as file:
                file.write("--- FINANCIAL REPORT ---\n")
                file.write(f"Net Balance: ${self.calculate_balance():.2f}\n")
                file.write(f"Total Income: ${self.get_total_income():.2f}\n")
                file.write(f"Total Expenses: ${self.get_total_expense():.2f}\n")
                file.write("-" * 30 + "\n")
                for t in self.transactions:
                    file.write(t.get_summary() + "\n")
            return True
        except IOError:

            return False
