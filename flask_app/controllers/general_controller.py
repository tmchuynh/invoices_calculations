from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

def read_excel(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df

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
