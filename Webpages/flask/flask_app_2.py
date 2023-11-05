from flask import Flask, render_template, request, session
import pandas as pd
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'  # Define the folder to save files on the server

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/transactions', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file:
            file_content = file.read()  # Get the file content

            # Set the file path on the server
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            # Save the file content to the server
            with open(file_path, 'wb') as f:
                f.write(file_content)

            # Assign the file path to the session
            session['file_path'] = file_path

            # Use pandas to read the file content
            df = pd.read_csv(file_path)

            # Process the DataFrame as needed...
            # (Add your DataFrame manipulation and HTML generation code here)

            # Example: Extract the columns
            selected_column = df[['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'trans_num', 'is-fraud']]

            # Convert the selected data to an HTML table
            table_html = selected_column.to_html()

            # Return the HTML content using JavaScript to update the div
            return f'<script>displayTable(`{table_html}`);</script>'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
