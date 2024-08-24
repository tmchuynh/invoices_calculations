from flask import Flask, request, render_template, Blueprint
import pandas as pd

# Create a Blueprint
bp = Blueprint('general', __name__)

def read_excel(file):
    df = pd.read_excel(file, engine='openpyxl', dtype=str)
    return df

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = read_excel(file)
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            # Convert DataFrame to HTML table
            table_html = df.to_html(classes='table table-striped', index=False)
            return render_template('results.html', table_html=table_html)
    return render_template('upload.html')