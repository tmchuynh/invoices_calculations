from flask import Flask, request, render_template, Blueprint
import pandas as pd

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
    currency_columns = ['Total $$ for the month', 'Did you work on any side projects?', 'Any invoices/receipts?']  # Specify columns to format
    # Print column names for debugging
    print("Columns in DataFrame:", df.columns)
    # Map columns to their actual names if necessary
    for col in currency_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
    return df

@bp.route('/see_all', methods=['POST'])
def see_all():
    global df_global
    if df_global is not None:
        # Show all data without any filters
        table_html = df_global.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
        return render_template('results.html', table_html=table_html)
    return render_template('upload.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global df_global
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            month = int(request.form.get('month', 1))  # Default to January if no month is provided
            email_filter = request.form.get('email', '')
            name_filter = request.form.get('name', '')
            if file:
                df = read_excel(file)
                df = format_currency(df)
                df = df.fillna('')
                df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
                # Store the DataFrame in the global variable
                df_global = df
                # Ensure the timestamp column is correctly named
                timestamp_column = 'Timestamp'  # Adjust this to match your actual column name
                if timestamp_column in df.columns:
                    df = filter_by_month(df, timestamp_column, month)
                # Apply additional filters
                if email_filter:
                    df = filter_by_column(df, 'Email', email_filter)
                if name_filter:
                    df = filter_by_column(df, 'Full Name', name_filter)
                # Format specified columns
                table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
                return render_template('results.html', table_html=table_html, month=month, email=email_filter, name=name_filter)
        elif 'upload' in request.form:
            month = int(request.form.get('month', 1))
            email_filter = request.form.get('email', '')
            name_filter = request.form.get('name', '')
            if df_global is not None:
                df = df_global
                # Apply filters
                if email_filter:
                    df = filter_by_column(df, 'Email', email_filter)
                if name_filter:
                    df = filter_by_column(df, 'Full Name', name_filter)
                if 'Timestamp' in df.columns:
                    df = filter_by_month(df, 'Timestamp', month)
                # Format specified columns
                df = format_currency(df)
                table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
                return render_template('results.html', table_html=table_html, month=month, email=email_filter, name=name_filter)
    return render_template('upload.html')
