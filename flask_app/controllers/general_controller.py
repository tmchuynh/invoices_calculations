from flask import Flask, request, render_template, Blueprint, redirect
import pandas as pd
import re
import xlwt
import numpy as np

# Create a Blueprint
bp = Blueprint('general', __name__)

df_global = None

@bp.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                df = read_excel(file)
                df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
                df = df.fillna('')
                df.insert(3, 'Calculated Total Amount', '300')

                # Store the DataFrame in the global variable
                global df_global
                df_global = df
                
                return redirect('/results')
    return render_template('upload.html')

def read_excel(file):
    df = pd.read_excel(file, engine='openpyxl', dtype=str)
    # df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%b %d %y %H:%M:%S')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')

    # Reformat the 'Timestamp' column to the desired format
    df['Timestamp'] = df['Timestamp'].dt.strftime('%b %d %y %I:%M:%S %p')
    return df

def filter_by_month(df, timestamp_column, month):
    df[timestamp_column] = pd.to_datetime(df[timestamp_column], format='%b %d %y %I:%M:%S %p')
    return df[df[timestamp_column].dt.month == month]

def filter_by_column(df, column_name, value):
    if column_name in df.columns:
        return df[df[column_name].str.contains(value, case=False, na=False)]
    return df

def format_currency(df):
    currency_columns = ['Total $$ for the month', 'Did you work on any side projects?']
    for col in currency_columns:
        if col in df.columns:
            df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
            df.loc[:, col] = df[col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
    return df

def sum_and_format_numbers(df, column_name):
    def extract_and_sum_numbers(text):
        numbers = re.findall(r'\d+\.?\d*', text)
        numbers = map(float, numbers)
        return sum(numbers)
    
    if column_name in df.columns:
        df.loc[:, column_name] = df[column_name].apply(lambda x: extract_and_sum_numbers(x))
        df.loc[:, column_name] = df[column_name].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
    return df

@bp.route('/results', methods=['GET', 'POST'])
def results():
    global df_global
    if df_global is not None:
        df = df_global.copy()

        # Check if filters are applied
        month = int(request.form.get('month', 0))
        email_filter = request.form.get('email', '').strip()
        name_filter = request.form.get('name', '').strip()

        if request.method == 'POST':
            # Apply filters if provided
            if month != 0 and 'Timestamp' in df.columns:
                df = filter_by_month(df, 'Timestamp', month)
            if email_filter:
                df = filter_by_column(df, 'Email', email_filter)
            if name_filter:
                df = filter_by_column(df, 'Full Name', name_filter)
            
            df = sum_and_format_numbers(df, 'Any invoices/receipts?')
            df = format_currency(df)

            # Convert to HTML table
            table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
            return render_template('results.html', table_html=table_html, df_global=df_global)

        elif request.method == 'GET':
            # If GET request, show all data without filters
            df = sum_and_format_numbers(df, 'Any invoices/receipts?')
            df = format_currency(df)
            table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
            return render_template('results.html', table_html=table_html, df_global=df_global)
    return redirect('/')

@bp.route('/see_all', methods=['GET'])
def see_all():
    global df_global
    if df_global is not None:
        df = df_global.copy()
        df = sum_and_format_numbers(df, 'Any invoices/receipts?')
        df = format_currency(df)

        # Render the modified DataFrame as HTML
        table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
        return render_template('results.html', table_html=table_html, df_global=df_global)
    return redirect('/')

