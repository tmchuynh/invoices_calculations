from flask import Flask, request, render_template, Blueprint
import pandas as pd

# Create a Blueprint
bp = Blueprint('general', __name__)

def read_excel(file):
    df = pd.read_excel(file, engine='openpyxl', dtype=str)
    return df

def filter_by_month(df, timestamp_column, month):
    # Convert the timestamp column to datetime
    df[timestamp_column] = pd.to_datetime(df[timestamp_column], format='%Y-%m-%d %H:%M:%S')
    # Filter the DataFrame by the specified month
    filtered_df = df[df[timestamp_column].dt.month == month]
    return filtered_df

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        month = int(request.form.get('month', 1))  # Default to January if no month is provided
        if file:
            df = read_excel(file)
            # Replace NaN values with empty strings
            df = df.fillna('')
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            # Ensure the timestamp column is correctly named
            timestamp_column = 'Timestamp'  # Adjust this to match your actual column name
            if timestamp_column in df.columns:
                df = filter_by_month(df, timestamp_column, month)
            # Convert DataFrame to HTML, ensuring no truncation
            table_html = df.to_html(classes='table table-striped', index=False, na_rep='', max_rows=None, max_cols=None)
            return render_template('results.html', table_html=table_html)
    return render_template('upload.html')