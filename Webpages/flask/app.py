from flask import Flask, request, render_template
from dash import dash, html
import plotly.express as px
import pandas as pd
import joblib

df = pd.read_csv("insert file name")

app = Flask(__name__)

# DEFINE ROUTE FOR HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')

# DEFINE ROUTE FOR TRANSACTION & ML MODEL RESULTS

# Load the ML model
model = joblib.load("INSERT NAME OF MODEL .PKL FILE - CONSIDER FILE PATH")

# Upload file
@app.route('/transactions')
def upload_file():
    return render_template('upload.html')

# Run the model
@app.route('/transactions', methods=['POST'])
def transaction_predictions():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        
        data_prediction = pd.read_csv(file)
        
        # Perform prediction using the loaded model
        prediction = model.predict(data_prediction)
        
        # Handle the prediction as needed
        return f"Potentially Fraudlent Transactions: {prediction}"

if __name__ == '__main__':
    app.run(debug=True)


# DEFINE ROUTE FOR DASHBOARD
@app.route('/dashboard')
def dashboard():

    # Create a Dash dashboard app 
    dash_app = dash.Dash(__name__, server = app, url_base_pathname = "/dashboard/")

    # Define the layout in html
    dash_app.layout = html.Div("INSERT DASH CODE HERE")

    # render the dashboard to the html page
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)


