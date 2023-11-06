from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file
            file.save('uploaded_file.csv')

            # Read the CSV file using pandas
            df = pd.read_csv('uploaded_file.csv')

            # Extract the columns you need (change 'desired_column' to your desired column name)
            selected_column = df[['trans_date_trans_time', 'cc_num', 'merchant','category', 'amt', 'trans_num', 'is_fraud']]

            def format_fraud_column(val):
                if val == 0:
                    return '<span style="font-size: 25px; text-align: right; color: green;">&#x2713</span>'  #insert green tick if not fraud
                elif val == 1:
                    return '<span style="font-size: 25px; text-align: right; color: orange;">&#10071</span>'  #insert orange exclamation if potentially fraudulent
                else:
                    return val

            # Sort the 'is_fraud' column in descending order
            selected_column = selected_column.sort_values(by='is_fraud', ascending=False)

            # Apply the formatting function to the 'is_fraud' column
            selected_column['is_fraud'] = selected_column['is_fraud'].apply(format_fraud_column)

            # Convert the selected data to an HTML table
            table_html = selected_column.to_html(index=False, escape=False)

            # Return the HTML content as the response
            return render_template('/transactions.html', table_data=table_html)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)