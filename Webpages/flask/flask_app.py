#  SET UP DEPENDENCIES

from flask import Flask, request, render_template
import pandas as pd
from pathlib import Path # To specify the the file path for reading the csv file
from sklearn.preprocessing import StandardScaler
import numpy as np # For numerical operations and calculations
import pickle # import pick to enable machine learning module to run
import os # import os to enable read / write functionality
import sys #import sys to enable python interpreter interactions



# SET DIRECTORY PATH TO DASH APP AND IMPORT THE DASH APP
sys.path.append('Webpages/flask/dash_app.py') 

from dash_app import get_dash_app


# CREATE FLASK SERVER APP
server = Flask(__name__)


# DEFINE ROUTE FOR HOME PAGE
@server.route('/')
def index():
    return render_template('index.html')

# DEFINE ROUTE FOR TRANSACTIONS PAGE
@server.route('/transactions')
def transactions():
    return render_template('transactions.html')

# Upload route for processing the uploaded file
@server.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file
            file.save('uploaded_file.csv')

        # #  DEFINE THE PATH TO THE PICKLED MODEL
        #     current_directory = os.path.dirname(__file__)
        #     model_path = os.path.join(current_directory, '../../ML_and_dashboard/ML/model.pkl')

        # #  LOAD THE PICKLED MODEL

        #     with open(model_path, 'rb')as file:
        #         model = pickle.load(file)

        # #  ENCODING IMPORTED CSV 

            fraud_df = pd.read_csv('uploaded_file.csv')

        #     # Drop the second column that was the original index column
        #     fraud_df.drop(['cc_num','trans_num'], axis=1, inplace=True)

        #     # Calculate the number of rows in fraud_df
        #     total_rows = len(fraud_df)

        #     # Create an array with two ones and fill the remaining space with zeros to match the total number of rows
        #     array = np.array([1] * 2 + [0] * (total_rows - 2))

        #     # Randomly shuffle the elements in the array
        #     np.random.shuffle(array)

        #     # Create a new DataFrame with a single column named "is_fraud" containing the shuffled array data.
        #     new_column = pd.DataFrame({'is_fraud': array})

        #     # Concatenate the new DataFrame with fraud_df
        #     fraud_df = pd.concat([fraud_df, new_column], axis=1)

        #     # Convert the 'trans_date_trans_time' column to datetime objects
        #     fraud_df['trans_date_trans_time'] = pd.to_datetime(fraud_df['trans_date_trans_time'], format='%Y-%m-%d %H:%M:%S')

        #     # Convert the 'trans_date_trans_time' column to Unix timestamps
        #     fraud_df['trans_date_trans_time'] = (fraud_df['trans_date_trans_time'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

        #     # Convert the 'dob' column to datetime objects
        #     fraud_df['dob'] = pd.to_datetime(fraud_df['dob'], format='%Y-%m-%d')

        #     # Convert the 'dob' column to Unix timestamps
        #     fraud_df['dob'] = (fraud_df['dob'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

        #     # Define the columns you want to scale (assuming they are all numeric)
        #     columns_to_scale = ['trans_date_trans_time', 'amt','zip','lat','long','city_pop','dob','unix_time','merch_lat','merch_long']

        #     # Initialize the StandardScaler
        #     scaler = StandardScaler()

        #     # Fit the scaler on your data and transform the specified columns
        #     fraud_df[columns_to_scale] = scaler.fit_transform(fraud_df[columns_to_scale])
            
        #     # Implement target encoding for the 'merchant' feature and the 'is_fraud' target variable
        #     # Calculate the mean 'is_fraud' for each 'merchant'
        #     # Replace merchant column with the target encoding
        #     target_mean = fraud_df.groupby('merchant')['is_fraud'].mean()
        #     fraud_df['merchant'] = fraud_df['merchant'].map(target_mean)

        #     # Implement target encoding for the 'category' feature and the 'is_fraud' target variable
        #     # # Calculate the mean 'is_fraud' for each 'job'
        #     # Replace category column with the target encoding
        #     target_mean = fraud_df.groupby('category')['is_fraud'].mean()
        #     fraud_df['category'] = fraud_df['category'].map(target_mean)

        #     # Implement target encoding for the 'first' feature and the 'is_fraud' target variable
        #     # # Calculate the mean 'is_fraud' for each 'first'
        #     # Replace first column with the target encoding
        #     target_mean = fraud_df.groupby('first')['is_fraud'].mean()
        #     fraud_df['first'] = fraud_df['first'].map(target_mean)

        #     # Implement target encoding for the 'last' feature and the 'is_fraud' target variable
        #     # Calculate the mean 'is_fraud' for each 'last'
        #     # Replace last column with the target encoding
        #     target_mean = fraud_df.groupby('last')['is_fraud'].mean()
        #     fraud_df['last'] = fraud_df['last'].map(target_mean)

        #     # Implement target encoding for the 'street' feature and the 'is_fraud' target variable
        #     # Calculate the mean 'is_fraud' for each 'street'
        #     # Replace street column with the target encoding
        #     target_mean = fraud_df.groupby('street')['is_fraud'].mean()
        #     fraud_df['street'] = fraud_df['street'].map(target_mean)

        #     # Implement target encoding for the 'city' feature and the 'is_fraud' target variable
        #     # Calculate the mean 'is_fraud' for each 'city'
        #     # Replace city column with the target encoding
        #     target_mean = fraud_df.groupby('city')['is_fraud'].mean()
        #     fraud_df['city'] = fraud_df['city'].map(target_mean)

        #     # Implement target encoding for the 'state' feature and the 'is_fraud' target variable
        #     # Calculate the mean 'is_fraud' for each 'state'
        #     # Replace state column with the target encoding
        #     target_mean = fraud_df.groupby('state')['is_fraud'].mean()
        #     fraud_df['state'] = fraud_df['state'].map(target_mean)

        #     # Implement target encoding for the 'job' feature and the 'is_fraud' target variable
        #     # Calculate the mean 'is_fraud' for each 'job'
        #     # Replace job column with the target encoding
        #     target_mean = fraud_df.groupby('job')['is_fraud'].mean()
        #     fraud_df['job'] = fraud_df['job'].map(target_mean)

        #     # Replace "M" with 1 and "F" with 0 in the "gender" column
        #     fraud_df['gender'] = fraud_df['gender'].replace({'M': 1, 'F': 0})

        #     # Drop is_fraud column
        #     fraud_df.drop(['is_fraud'], axis=1, inplace=True)

        #     # Save the fraud_df to CSV file
        #     file_path = "fraud_df.csv"

        #     # Use the to_csv method to export teh DataFrame to CSV file
        #     fraud_df.to_csv(file_path, index = False)
            
        # #  USE LOADED PICKELED MODEDL TO PERFORM PREDICTIONS
        #     predictions_df = model.predictions(fraud_df)

        #  CREATE TABLE OF TRANSACTIONS 
        
            # Read the CSV file using pandas
            # df = pd.read_csv('uploaded_file.csv')
            # Extract the columns to return in table
            selected_column = fraud_df[['trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'trans_num', 'is_fraud']]

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
            return render_template('/transactions.html', table_html)

# UPLOAD DASH DASHBOARD 
@server.route('/dashboard')
def dashboard():
    dash_app = get_dash_app()  # Get the Dash app
    return dash_app.index()

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8050)