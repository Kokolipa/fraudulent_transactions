from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/transactions', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file
            file.save('uploaded_file.csv')

            # Read the CSV file using pandas
            df = pd.read_csv('uploaded_file.csv')

            # Extract the columns you need (change 'desired_column' to your desired column name)
            selected_column = df[['trans_date_trans_time', 'cc_num', 'merchant','category', 'amt', 'trans_num', 'is-fraud']]

            def format_fraud_column(val):
                if val == 0:
                    return '&#x2713'  # Green tick
                elif val == 1:
                    return '&xcl'  # Orange exclamation point
                else:
                    return val

            # Apply the formatting function to the 'is_fraud' column
            df['is_fraud'] = df['is_fraud'].apply(format_fraud_column)
            
            # Convert the selected data to an HTML table
            table_html = selected_column.to_html()

            # Return the HTML content using JavaScript to update the div
            return f'<script>displayTable(`{table_html}`);</script>'

if __name__ == '__main__':
    app.run(debug=True)
