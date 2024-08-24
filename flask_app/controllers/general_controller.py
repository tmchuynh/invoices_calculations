from flask import Flask, request, render_template, Blueprint
import pandas as pd
import re

# Create a Blueprint
bp = Blueprint('general', __name__)

df_global = None

def read_excel(file):
    df = pd.read_excel(file, engine='openpyxl', dtype=str)
    return df

def filter_by_month(df, timestamp_column, month):
    # Convert the timestamp column to datetime
    df[timestamp_column] = pd.to_datetime(df[timestamp_column], format='%Y-%m-%d %H:%M:%S')
    # Filter the DataFrame by the specified month
    filtered_df = df[df[timestamp_column].dt.month == month]
    return filtered_df

def filter_by_column(df, column_name, value):
    if column_name in df.columns:
        return df[df[column_name].str.contains(value, case=False, na=False)]
    return df

def format_currency(df):
    currency_columns = ['Total $$ for the month', 'Did you work on any side projects?']  # Specify columns to format
    # Map columns to their actual names if necessary
    for col in currency_columns:
        if col in df.columns:
            df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
            df.loc[:, col] = df[col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
    return df

def sum_and_format_numbers(df, column_name):
    # Function to extract numbers from a string and sum them
    def extract_and_sum_numbers(text):
        numbers = re.findall(r'\d+\.?\d*', text)  # Find all numbers
        print(numbers)
        numbers = map(float, numbers)  # Convert to float
        return sum(numbers)
    
    if column_name in df.columns:
        df.loc[:, 'Any invoices/receipts?'] = df['Any invoices/receipts?'].apply(lambda x: extract_and_sum_numbers(x))
        df.loc[:, 'Any invoices/receipts?'] = df['Any invoices/receipts?'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
    return df

@bp.route('/see_all', methods=['POST'])
def see_all():
    global df_global
    if df_global is not None:
        # Apply the sum and format operations on the global DataFrame
        df_global = sum_and_format_numbers(df_global, 'Any invoices/receipts?') 
        df_global = format_currency(df_global)
        
        # Render the modified DataFrame
        table_html = df_global.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
        return render_template('results.html', table_html=table_html)
    
    return render_template('upload.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global df_global
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            month = int(request.form.get('month', 0))  # Default to 0 (no filter)
            email_filter = request.form.get('email', '')
            name_filter = request.form.get('name', '')
            if file:
                df = read_excel(file)
                df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
                df = df.fillna('')
                df_global = df
                
                # Only filter by month if a specific month is selected
                if month != 0 and 'Timestamp' in df.columns:
                    df = filter_by_month(df, 'Timestamp', month)
                    
                if email_filter:
                    df = filter_by_column(df, 'Email', email_filter)
                if name_filter:
                    df = filter_by_column(df, 'Full Name', name_filter)
                
                df = sum_and_format_numbers(df, 'YourColumnName')  # Replace with actual column name
                df = format_currency(df)
                table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
                return render_template('results.html', table_html=table_html, month=month, email=email_filter, name=name_filter)
    return render_template('upload.html')


