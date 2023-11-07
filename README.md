# group-project-4
## Building a Web Application To Predict Fraudulent Credit Card Transactions
### Project Team: Gal Beeri, Mireille Walton and Katharine Tamas

In this scenario, our team has built an interactive web application where end users can upload a csv file containing credit card transactions, and through a machine learning model we can predict if a transaction is likely to be fraudulent or not. 

Our dataset consisted of two csv files containing over 1.8 million credit card transactions, with transaction dates from January 2019 to December 2020 inclusive. The credit card holders all resided within the United States. This dataset was simulated using the Markov Chain method (https://github.com/namebrandon/Sparkov_Data_Generation/tree/master), which is a mathematical model used to describe a sequence of events where the outcome of each event depends only on the outcome of the previous event. 

The data was sourced from Kaggle:

https://www.kaggle.com/datasets/kartik2112/fraud-detection


**Repository Folders and Contents:**
``` yml
.
│   ├── EDA_and_Analysis 
│   |   ├── EDA_and_preprocessing_data.ipynb
│   ├── ML_and_dashboard
│   |   ├── ML
│   |   |   ├── ml_model.ipynb
│   |   |   ├── ml_model_remove_categorical.ipynb
│   |   |   ├── model.pkl
│   |   ├── dashboard_scripts
│   |   |   ├── dash_plot.ipynb
│   |   |   ├── dash_plotly.py
│   |   ├── datagen
│   |   |   ├── datagen.ipynb
│   |   |   ├── preprocessing_datagen.ipynb
│   ├── Webpages
│   |   ├── flask
│   |   |   ├── static
│   |   |   |   ├── images
│   |   |   |   |   ├── home_tile1.jpg
│   |   |   |   |   ├── home_tile2.jpg
│   |   |   |   |   ├── home_tile3.jpg
│   |   |   |   |   ├── homepg_image.jpg
│   |   |   ├── style.css
│   |   |   ├── templates
│   |   |   |   ├── dashboard.html
│   |   |   |   ├── index.html
│   |   |   |   ├── transactions.html
│   |   |   ├── dash_app.py
│   |   |   ├── flask_app.py
│   |   ├── flask_apps
│   |   |   ├── static
│   |   |   |   ├── images
│   |   |   |   |   ├── home_tile1.jpg
│   |   |   |   |   ├── home_tile2.jpg
│   |   |   |   |   ├── home_tile3.jpg
│   |   |   |   |   ├── homepg_image.jpg
│   |   |   ├── style.css
│   |   |   ├── templates
│   |   |   |   ├── dashboard.html
│   |   |   |   ├── index.html
│   |   |   |   ├── transactions.html
│   |   |   ├── dash_app.py
│   |   |   ├── flask_app.py
│   |   |   ├── flask_app_test.py
│   |   |   ├── get_transactions.py      
│──README.md    
|──.gitignore          
``` 

## Table of Contents

- [About](#about)
    - [Part 1: Exploratory Data Analysis and Data Preprocessing](#part-1-exploratory-data-analysis-and-data-preprocessing)
    - [Part 2: Supervised Machine Learning Models](#part-2-supervised-machine-learning-models)
    - [Part 3: Create and Deploy Web Application](#part-3-create-and-deploy-web-application)
- [Getting Started](#getting-started)
- [Installing](#installing)
- [Contributing](#contributing)
- [Sources](#sources)


## About
### Part 1: Exploratory Data Analysis and Data Preprocessing

**Key Data Insights:**

In this step, we consolidated two Kaggle CSV files and conducted data exploration using Tableau Public, yielding the following key insights:

1. Only 0.52% of the dataset contained fraudulent transactions, in line with the Markov model's assumption of a fraudulent transaction every 7 days.
2. Gender distribution was evenly split between both fraudulent and non-fraudulent transactions.
3. The "Gas_Transport" category had the highest transaction volume, but "Grocery_POS" topped the list for fraudulent transactions.
4. Regular transactions exhibited a cyclic pattern, peaking in December due to holiday spending. They were most common on Mondays, occurring from midday to midnight.
5. Fraudulent transactions were sporadic, more likely on weekends, with a higher occurrence on Sundays. They primarily took place from 10 pm to 4 am, a time when vigilance is lower.
6. The average age in the dataset was 46 years, with the most frequent age group being 45 to 49 years old. For fraudulent transactions, the average age was 49, aligning with scammers' tendency to target older, less tech-savvy individuals.
7. Over 83% of transactions involved amounts under $100, with an average transaction of $70. In contrast, fraudulent transactions had a significantly higher average amount of $531, despite the majority being under $100.

**Tableau Data Exploration:**

https://public.tableau.com/views/Project4-CreditCardFraud_EDA/Presentation?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link

**EDA and Data Preprocessing:**

In our analysis, we conducted extensive Exploratory Data Analysis (EDA) and data preprocessing within a Jupyter Notebook environment. We combined two datasets to create a comprehensive dataset, which, fortunately, required minimal cleaning. Notably, there were no missing values in our dataset. 

We made some key decisions to prepare the data for machine modelling:
1. **Feature Removal**: We decided to exclude the 'Credit card number' and 'Transaction number' columns since these are randomly generated and hold no predictive value for fraud detection.
2. **Data Scaling**: To ensure a level playing field for all numeric features, we scaled them. This step is crucial because it enables features with varying units and magnitudes to contribute equally to machine learning algorithms, ultimately aiding in the model's convergence.
3. **Target Encoding**: Our dataset contained categorical columns with a high number of categories. To manage these effectively without increasing dimensionality, we employed target encoding. This technique replaces a categorical feature with the average target value of all data points belonging to that category.
4. **Gender Encoding**: We transformed the 'gender' column, originally represented as 'F' and 'M,' into numeric values '0' and '1' for modelling purposes.
Our main goal was to limit our feature set to a maximum of 19 variables to prevent overfitting.

Lastly, we checked for linear relationships between the features and target variable “is_fraud”, using the Pearson correlation coefficient.
In our investigation, we found that, as is often the case in fraud detection, there were very few significant correlations between our features and the 'is_fraud' target variable. This is because fraudulent activities are intentionally made to look like regular transactions and avoid obvious patterns.
Our approach acknowledges this absence of correlation and relies on machine learning models to spot subtle deviations from the norm, which helps us effectively identify fraudulent transactions. 


**Resource Files We Used:**

    - fraudTest.csv
    - fraudTrain.csv

**Our Jupyter Notebook Python Script:**

    - EDA_and_preprocessing_data.ipynb

**Tools/Libraries We Imported:**

    - import numpy as np # For numerical operations and calculations
    - import pandas as pd # To read and manipulate the lending data as a dataframe
    - from pathlib import Path # To specify the the file path for reading the csv file
    - from sklearn.preprocessing import StandardScaler # To scale the data
    - import seaborn as sns # To create pairplots and heatmaps to visualize data relationships and correlations
    - import matplotlib.pyplot as plt # To create and display visualizations, including heatmaps and confusion matrices
    - from scipy import stats # To calculate the Pearson correlation coefficient


### Part 2: Supervised Machine Learning Models


**Resource Files We Used:**

**Our Python Script:**

**Tools/Libraries We Imported:**


### Part 3: Create and Deploy Web Application

![image](https://github.com/KTamas03/project4_readme/assets/132874272/1fb2b9f1-ca1a-4f45-8cd4-5e4a9dbbe76a)


**Our Python Script:**

**Tools/Libraries We Imported:**




## Getting Started

**Programs/software we used:**
 - Visual Studio Code: used for python coding.
 - Microsoft Excel: to view csv files. Should be available by default on all PCs.
 - Chrome: to view web application.

**To get webpage running:**
 - Open api.py in Visual Studio Code
 - Navigate to folder location of flask_app_test.py in terminal
 - Type: python flask_app_test.py
 - Open index.html in Chrome to view website

**To activate dev environment:**
- Open Anaconda Prompt
- Activate dev environment, type 'conda activate dev'

## Installing


## Contributing

- Dash plotly website: (https://dash.plotly.com/)

## Sources

- image files for web ????????
