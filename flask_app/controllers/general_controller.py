from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

def read_excel(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df

# Reading from a file path
def read_excel_from_path(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

def filter_data(df, column_name, value):
    filtered_df = df[df[column_name] == value]
    return filtered_df

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = read_excel(file)
            # Convert DataFrame to HTML table
            table_html = df.to_html(classes='table table-striped')
            return render_template('results.html', table_html=table_html)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
