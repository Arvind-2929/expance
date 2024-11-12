import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Database setup
conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()

# Create table
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS ExpenseTracker
                 (Date TEXT, Payee TEXT, Description TEXT, Amount REAL, ModeOfPayment TEXT)''')
create_table()

# Add a new expense
def add_expense(date, payee, desc, amount, mode):
    c.execute("INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)",
              (date, payee, desc, amount, mode))
    conn.commit()

# View all expenses
def view_all_expenses():
    c.execute("SELECT * FROM ExpenseTracker")
    data = c.fetchall()
    return data

# Streamlit App
st.title("Expense Tracker")

# Sidebar for adding a new expense
st.sidebar.header("Add New Expense")
date = st.sidebar.date_input("Date", datetime.now())
payee = st.sidebar.text_input("Payee")
desc = st.sidebar.text_area("Description")
amount = st.sidebar.number_input("Amount", min_value=0.0, format="%.2f")
mode = st.sidebar.selectbox("Mode of Payment", ["Cash", "Credit Card", "Debit Card", "Online"])

if st.sidebar.button("Add Expense"):
    add_expense(date.strftime("%Y-%m-%d"), payee, desc, amount, mode)
    st.sidebar.success("Expense added successfully")

# Main section to view expenses
st.header("All Expenses")

# Display all expenses in a table
expenses = view_all_expenses()
if expenses:
    expense_df = pd.DataFrame(expenses, columns=["Date", "Payee", "Description", "Amount", "ModeOfPayment"])
    st.write(expense_df)
else:
    st.write("No expenses to show.")

# Closing database connection
conn.close()