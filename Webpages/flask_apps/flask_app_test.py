from flask import Flask, render_template, request
import pandas as pd
import get_transactions
import dash_app

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

            def upload_transactions():
                    return get_transactions

    # Return the HTML content as the response
    return render_template('/transactions.html', upload)


@app.route('/dashboard')
def dashboard():
    return dash_app

if __name__ == '__main__':
    app.run(debug=True)