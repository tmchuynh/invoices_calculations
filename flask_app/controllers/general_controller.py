from flask import Flask, request, render_template, Blueprint, redirect
import re
import pandas as pd
import numpy as np
import matplotlib as mpl
from pandas.io.formats.style import Styler

# Create a Blueprint
bp = Blueprint('general', __name__)

df_global = None

def read_excel(file):
    df = pd.read_excel(file, engine='openpyxl', dtype=str)
    return df


def filter_by_month(df, column_name, month):
    df[column_name] = pd.to_datetime(df[column_name], format='%b %d %y %I:%M:%S %p')
    return df[df[column_name].dt.month == month]


def filter_by_column(df, column_name, value):
    if column_name in df.columns:
        return df[df[column_name].str.contains(value, case=False, na=False)]
    return df


def addition(df, row_index):
    # Ensure 'Total # of Classes' column exists
    if 'Total # of Classes' not in df.columns:
        df['Total # of Classes'] = 0
    
    # Get column indices to sum based on the position
    start_col = 11  # Index of the first column to include in the sum

    # Iterate over each row to calculate the total
    total = 0
    for col_index in range(start_col, len(df.columns)):
        col_name = df.columns[col_index]
        value = pd.to_numeric(df.iloc[row_index, col_index], errors='coerce')
        df.at[row_index, 'Total # of Classes'] = total
        
        if pd.isna(value):
            value = 0
        total += value

    return df


def convert_to_number(df):
    column_indices = [
        'Calculated Total Amount',
        'Instructor Provided Total',
        'Work Meetings',
        'Admin Meetings',
        'Side Projects',
        'Invoices/Receipts',
        'Total # of Classes',
        'Arroyo',
        'Myford',
        'Tustin Ranch',
        'Ladera',
        'Anaheim Hills',
        'Historic Anaheim',
        'North Tustin',
        'San Juan Capistrano',
        'Hicks Canyon',
        'Orchard Hills',
        'Peters Canyon',
        'TMA'
    ]
    
    # Convert the specified columns to numeric
    for col in column_indices:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
            
    return df


def rename_columns(df):
    df = df.rename(columns={
        "Timestamp": "Date",
        "How many work meetings did you attend?": "Work Meetings",
        "How many administrative meetings did you attend?": "Admin Meetings",
        "Total $$ for the month": "Instructor Provided Total",
        "Did you work on any side projects?": "Side Projects",
        "Any invoices/receipts?": "Invoices/Receipts",
        "How many classes did you teach this month? [Arroyo]": "Arroyo",
        "How many classes did you teach this month? [Myford]": "Myford",
        "How many classes did you teach this month? [Tustin Ranch]": "Tustin Ranch",
        "How many classes did you teach this month? [Ladera]": "Ladera",
        "How many classes did you teach this month? [Anaheim Hills]": "Anaheim Hills",
        "How many classes did you teach this month? [Historic Anaheim]": "Historic Anaheim",
        "How many classes did you teach this month? [North Tustin]": "North Tustin",
        "How many classes did you teach this month? [San Juan Capistrano]": "San Juan Capistrano",
        "How many classes did you teach this month? [Hicks Canyon]": "Hicks Canyon",
        "How many classes did you teach this month? [Orchard Hills]": "Orchard Hills",
        "How many classes did you teach this month? [Peters Canyon]": "Peters Canyon",
        "How many classes did you teach this month? [TMA]": "TMA"
        })
    return df


def format_currency(df):
    currency_columns = ['Instructor Provided Total', 'Side Projects', 'Invoices/Receipts', 'Rate']
    for col in currency_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].replace('', '0.00').fillna('0.00').astype('float')
            df[col] = df[col].apply(lambda x: f"${x:,.2f}")
    
    df['Calculated Total Amount'] = df['Calculated Total Amount'].apply(lambda x: f"${x:,.2f}")
            
    return df


def sum_and_format_numbers(df, column_name):
    # Function to extract numbers and clean text
    def extract_and_sum_numbers(text):
        # Extract numbers and remove them from text
        numbers = re.findall(r'\d+\.?\d*', text)
        # Convert extracted numbers to floats and sum them
        numbers = map(float, numbers)
        return sum(numbers)
    
    # Ensure the specified column exists in the DataFrame
    if column_name in df.columns:
        # Apply extraction and summing function to each row
        df[column_name] = df[column_name].apply(lambda x: extract_and_sum_numbers(x) if pd.notna(x) else 0)
        
        # Convert the column to numeric
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0)
    
    return df


def calculate_total(df):
    # Ensure 'Calculated Total Amount' column exists
    if 'Calculated Total Amount' not in df.columns:
        df['Calculated Total Amount'] = 0.0
    
    # Calculate total from meetings and classes
    df = calculate_meetings(df)
    df = calculate_classes(df)
    
    # List of columns for extra income
    extra_income_cols = ['Side Projects', 'Invoices/Receipts']
    
    # Calculate total from extra income columns
    for col in extra_income_cols:
        if col in df.columns:
            # Use row-wise sum for extra income
            df['Calculated Total Amount'] += df[col].fillna(0).astype(float)
    
    return df


def calculate_meetings(df):
    # Define rates
    work_meeting_rate = 20
    admin_meeting_rate = 35
    
    # Ensure 'Calculated Total Amount' column exists
    if 'Calculated Total Amount' not in df.columns:
        df['Calculated Total Amount'] = 0.0
    
    # Calculate work meetings and admin meetings income
    work_meetings_income = pd.Series(0, index=df.index)
    admin_meetings_income = pd.Series(0, index=df.index)
    
    if 'Work Meetings' in df.columns:
        work_meetings_income = pd.to_numeric(df['Work Meetings'], errors='coerce').fillna(0) * work_meeting_rate
    
    if 'Admin Meetings' in df.columns:
        admin_meetings_income = pd.to_numeric(df['Admin Meetings'], errors='coerce').fillna(0) * admin_meeting_rate
    
    # Sum income from work meetings and admin meetings
    df['Calculated Total Amount'] += work_meetings_income + admin_meetings_income
    
    return df


def input_rates(df):
    rates = {
        'Jessalyn nguyen': 50,
        'Jaqueline Rodriguez': 75,
        'Krystal Alexander': 55
    }

    for index in range(len(df)):
        if index in df.index and 'Full Name' in df.columns:
            full_name = df.loc[index, 'Full Name']
        else:
            continue
            # print(f"Index {index} or column 'Full Name' not found in DataFrame")
        # full_name = df.loc[index, 'Full Name']
        if full_name in rates:
            df.at[index, 'Rate'] = rates[full_name]
    
    return df


def calculate_classes(df):
    df = input_rates(df)
    
    num_of_classes = df['Total # of Classes']
    rate = df['Rate']
    
    class_income = pd.Series(0, index=df.index)
    class_income += rate * num_of_classes
    
    df['Calculated Total Amount'] += class_income
    
    return df


def refresh(df):
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
        df['Timestamp'] = df['Timestamp'].dt.strftime('%b %d %y %I:%M:%S %p')
    else:
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
        df['Date'] = df['Date'].dt.strftime('%b %d %y %I:%M:%S %p')

    return df


@bp.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                try:
                    df = read_excel(file)
                    df = refresh(df)
                except Exception as e:
                    return render_template('upload.html', error=f"Error processing file: {str(e)}")

                df.insert(8, 'Total # of Classes', 0)
                df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
                df = df.fillna('0')
                df.insert(3, 'Rate', 0)
                df.insert(4, 'Calculated Total Amount', 0)

                global df_global
                df_global = df
                
                return redirect('/results')
    return render_template('upload.html')


@bp.route('/results', methods=['GET', 'POST'])
def results():
    global df_global
    if df_global is not None:
        df = df_global.copy()
        
        # Check if filters are applied
        month = int(request.form.get('month', 0))
        email = request.form.get('email', '').strip()
        name = request.form.get('name', '').strip()
        
        # Check if no filters are applied
        if not any([month != '0', email, name]):
            return redirect('/results')  # Refresh the page
        
        df = rename_columns(df)

        if request.method == 'POST':
            # Apply filters if provided
            if month != 0 and 'Date' in df.columns:
                df = filter_by_month(df, 'Date', month)
                df = refresh(df)                
            if email:
                df = filter_by_column(df, 'Email', email)
            if name:
                df = filter_by_column(df, 'Full Name', name)
                
            # Drop rows where all values are NaN
            df = df.dropna(how='all')

            # Reset index after dropping rows
            df = df.reset_index(drop=True)
            
            # Iterate over each row and apply the addition function
            for index in range(df.shape[0]):
                df = df.dropna(how='all')
                df = addition(df, index)
                
            df = sum_and_format_numbers(df, 'Any invoices/receipts?')
            df = convert_to_number(df)
            df = calculate_total(df)
            numbers_df = df.copy()
            df = format_currency(df)
            
            
            # Convert to HTML table
            table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
            return render_template('results.html', table_html=table_html, df_global=df, numbers_df=numbers_df, zip=zip)

        elif request.method == 'GET':
            # If GET request, show all data without filters
            # Iterate over each row and apply the addition function
            for index in range(len(df)):
                df = addition(df, index)
            df = sum_and_format_numbers(df, 'Any invoices/receipts?')
            df = convert_to_number(df)
            df = calculate_total(df)
            numbers_df = df.copy()
            df = format_currency(df)
            
            table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
            return render_template('results.html', table_html=table_html, df_global=df, numbers_df=numbers_df, zip=zip)
    return redirect('/')


@bp.route('/see_all', methods=['GET'])
def see_all():
    global df_global
    if df_global is not None:
        df = df_global.copy()
        # Iterate over each row and apply the addition function
        for index in range(len(df)):
            df = addition(df, index)
        df = sum_and_format_numbers(df, 'Any invoices/receipts?')
        df = rename_columns(df)
        df = convert_to_number(df)
        df = calculate_total(df)
        numbers_df = df.copy()
        df = format_currency(df)

        # Render the modified DataFrame as HTML
        table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
        return render_template('results.html', table_html=table_html, df_global=df, numbers_df=numbers_df, zip=zip)

    return redirect('/')

