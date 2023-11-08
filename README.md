# Project 4 [![Presentation-Fraudulent](https://img.shields.io/badge/Presentation-Fraudulent-black?style=flat&logo=codereview)](https://docs.google.com/presentation/d/1BzXgtBJl6xi0m6Rl9t7ku_83Ji0DmChB/edit?usp=sharing&ouid=109196441157952287856&rtpof=true&sd=true)
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
│   |   |   ├── flask_app.py    
│──README.md    
|──.gitignore          
``` 

## Table of Contents

- [About](#about)
    - [Part 1: Exploratory Data Analysis and Data Preprocessing](#part-1-exploratory-data-analysis-and-data-preprocessing)
    - [Part 2: Supervised Machine Learning Models](#part-2-supervised-machine-learning-models)
    - [Part 3: Create and Deploy Web Application](#part-3-create-and-deploy-web-application)
- [Getting Started](#getting-started)
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

**Assumption and Overview**
Since we aim to predict fraudulent transactions based on the ‘fraud_encoded’ dataset, we will evaluate two Machine Learning models that could produce accurate results. The main metric we will consider when running **confusion metrics is recall**, as the main aim is to identify fraudulent transactions with high accuracy.
<br>
The models evaluated were:
1. Logistic regression -> As it predicts a binary result.
2. Decision Tree -> As it can take into account multiple features when evaluating whether a certain transaction is/isn’t fraudulent.

**Assumption**
*Decision tree* is likely to perform better as our data cleansing, manipulation, and engineering indicated that there is no correlation coefficient between a feature in the dataset and the target column ‘is_fraud’ feature. Therefore, multiple features will need to be evaluated together to result in a fraudulent/non-fraudulent transaction.

### Creating a logistic regression model
We ran a logistic regression model with the `lbfgs` solver, with no other specifications. The results of the model from the confusion matrix and the classification report (0 accuracy score for precision, recall, and f1 scores) indicated that logistic regression performs poorly in identifying fraudulent transactions.

### Decision Tree Model
To evaluate the decision tree model, we took the following approaches:

1. **Model 1:** Running a “default” decision tree model and comparing it to the logistic regression model, assuming we receive better results, we move on with the evaluation methods below.

![image](https://github.com/Kokolipa/fraudulent_transactions/assets/132874272/4dccab4a-d5e9-4628-90c2-07951aa2b40a)


2. **Model 2:** Running a decision tree model with the following specifications:
   
    a. criterion = ‘log_loss’ -> To evaluate how well the model predicts probabilities for each class.
    
    b. splitter = ‘best’ -> A default spec to split the leaves of the tree.
    
    c. max_depth = 12 -> The depth of the tree model.
    
    d. random_state = 72
    
    e. max_features = 10 -> The maximum number of features that the algorithm considers when splitting a node.

![image](https://github.com/Kokolipa/fraudulent_transactions/assets/132874272/65da6761-47e4-4caa-a607-6f7050b5f565)


3. **Model 3:** Running a GridSearchCV tool to find the optimal parameters for the decision tree model with the following specifications enabled:
   
        a. criterion’:[‘gini’,‘entropy’, ‘log_loss’] -> Enabling the model to evaluate all the different evaluation parameters for the tree “impurity”/“probabilities of binary classification problems”/ “information gain” (entropy).
        
        b. max_depth: [7,8,9,10,11,12] -> Since our dataset contains above 1M records. Reducing the depth of the tree below seven will reduce all accuracy scores within the scope of the classification report. However, above 12 can be classified as an overfitted tree, hence the depth range between seven and a max of twelve.
        
        c. ‘max_features’: [‘auto’, ‘sqrt’, ‘log2’] ->
        
        auto = considering the best split at each node.
        
        sqrt = limiting the number of features to the square root of the total number of features in the dataset.
        
        ’log2 = Limiting the number of features to the base-2 logarithm of the total number of features in the dataset.
        
        d. ’min_samples_split: [8000,10000,15000,25000, 30000] -> How many samples are required to split an internal node during the training process?
        
        e. class_weight -> Because our dataset is imbalanced, with a large proportion of non-fraudulent transactions and a low proportion of fraudulent ones, specifying the weight, the ratio between these two, enables the model to give more importance to the minority class (fraudulent transactions) during the training process.
        
        f. Scorer (recall) -> To focus our model on the most critical metric, recall.
        
        g. n_jobs -> specifies the number of CPU cores to use when performing the cross-validated grid search.
        
        h. cv=10 (cross-validation)-> We used k-fold 10 to separate our dataset into 10 equal subsets. So, we evaluate nine subsets of the data and leave one subset for validation.

![image](https://github.com/Kokolipa/fraudulent_transactions/assets/132874272/532ab7f8-e4f0-497b-931d-9360a0863132)

5. **Model 4:** Here, we created a balanced dataset. We used the X_train to find all the instances of fraudulent transactions (7000 +) and merged them with 10k records of non-fraudulent ones. We shuffled the data and ran the model with the grid search results.

6. **Model 5:** Here, we assumed that categorical features didn’t provide meaningful information to the decision tree model and could potentially lead to confusion and clutter as opposed to focusing attention on details and accuracy. We went by the assumption due to the predict_proba results (we evaluated the x_test with predict proba and attached a y_test (is_fraud column) to compare the results with a histogram chart indicating inaccuracies). We ran all the previous models, including the logistic regression, and compared all the models to the best model found in the above three models.
   
From the above models, we found that model 3 performed the best, with 0.9 recall score for Fraudulent transactions, 0.93 for non-fraudulent ones and an overall score of 0.93.
- Regarding precision, it’s important to note that the precision score for fraudulent transactions was low at 0.06, while it was 1 for non-fraudulent transactions. This discrepancy arises due to the dataset’s imbalance, predominantly comprising non-fraudulent transactions. Consequently, achieving a high precision score for fraudulent transactions is inherently challenging in such imbalanced datasets.

**Our Scripts:**
- ml_model.ipynb
- ml_model_remove_categorical.ipynb

**Pickled Model:**
- model.pkl

**Tools/Libraries We Imported:**

#NOTE: Analysis libraries
- import pandas as pd
- import numpy as np 
- import seaborn as sns
- import matplotlib.pyplot as plt

#NOTE: Importing model libraries
- from sklearn.tree import DecisionTreeClassifier
- from sklearn.linear_model import LogisticRegression
- from sklearn.model_selection import train_test_split
- from sklearn.metrics import confusion_matrix,classification_report # * Testing methods 
- from sklearn.tree import plot_tree # * Tree plotting function
- from sklearn.metrics import make_scorer, recall_score

**This library will be used to optimise the parameters of the decision tree**
- from sklearn.model_selection import GridSearchCV

**Pickling library**
- import pickle

### Part 3: Create and Deploy Web Application

![image](https://github.com/Kokolipa/fraudulent_transactions/assets/132874272/c079b5e1-5514-45fd-a1aa-ef8635b8f31d)


**Flask / Dash Script:**

- flask_app.py

**HTML Script:**

- index.html
- transactions.html
- dashboard.html
  
**CCS Script:**

- style.css

**Tools/Libraries We Imported:**

***Directory libraries***

- from pathlib import Path 

***Analysis and manipulation libraries***

- import pandas as pd
- import numpy as np 
- import random
- from datetime import datetime, timedelta

***ML libraries***

- from sklearn.preprocessing import StandardScaler 
- import pickle

***Application libraries***

- from flask import Flask, render_template, request, redirect, session, url_for
- from werkzeug.middleware.dispatcher import DispatcherMiddleware

***Dashboard libraries***
- import plotly.express as px 
- from dash import Dash, html, dcc
- from dash.dependencies import Output, Input
- from dash.exceptions import PreventUpdate
- from dash_bootstrap_templates import load_figure_template
- import dash_bootstrap_components as dbc


## Getting Started

**Programs/software we used:**
 - Visual Studio Code: used for python coding.
 - Microsoft Excel: to view csv files. Should be available by default on all PCs.
 - Chrome: to view web application.

**To get webpage running:**
 - Open flash_app.py in Visual Studio Code
 - Navigate to folder location of flask_app.py in terminal
 - Type: python flask_app.py
 - Click url link returned in the terminal to view the web app

**To activate dev environment:**
- Open Anaconda Prompt
- Activate dev environment, type 'conda activate dev'


## Contributing

- Dash plotly website: (https://dash.plotly.com/)

## Sources

**References:**

•	Python Tutorial, “Session data in Python Flask”, https://pythonbasics.org/flask-sessions/, accessed 6 November 2023

•	Nihal, 8 Jan 2019, “How to import function into main file in flask?”, https://stackoverflow.com/questions/54090720/how-to-import-function-into-main-file-in-flask, accessed 6 November 2023

•	Plotly, date unknown, “Embedding Dash Apps in Other Web Platforms”, https://dash.plotly.com/integrating-dash, accessed 6 November 2023

•	Amrit Kumar Toward, 21 May 2021, Stackoverflow, “How to embed a python dish app to a HTML webpage”, https://stackoverflow.com/questions/67623637/how-to-embed-a-python-dash-app-to-a-html-webpage, accessed 6 November 2023

•	Udemy, Jose Portillo, Pierian Traning, “Interactive Python Dashboards with Plotly and Dash”, https://www.udemy.com/course/python-and-flask-bootcamp-create-websites-using-flask/learn/, accessed 6 November 2023

•	Todd Birchard, 10 December 2018, Hackers and Slackers, “Integrate Plotly Dash into your Flask App”, https://hackersandslackers.com/plotly-dash-with-flask/, accessed 4 November 2023

•	Lauren Kirsch 21 Feb, 2021, edited by Michel 18 June 2021, Stackoverflow, “Need help linking to local HTML file in Dash app”, https://stackoverflow.com/questions/66298784/need-help-linking-to-local-html-file-in-dash-app, accessed 5 November 2023

•	Alex, 20 April 2022, Stackoverflow, “plotly dash link to local html file”, https://stackoverflow.com/questions/71942222/plotly-dash-link-to-local-html-file, accessed 5 November 2023

•	Udemy, Jose Portillo, Pierian Traning, “Python and Flask Bootcamp: Create Websites using Flask”, https://www.udemy.com/course/interactive-python-dashboards-with-plotly-and-dash/learn/lecture/, accessed 4 November 2023

•	Webpage & powerpoint images sourced from Shutterstock under subscription, https://www.shutterstock.com/search/app-development?image_type=photo, accessed 1 and 4 November 2023.

•	MDB, date unknown, “Bootstrap 5 Colors Code”, https://mdbootstrap.com/docs/standard/extended/colors-code/, accessed 4 November 2023

•	Eli the Computer Guy, 20 March 2020, YouTube, “CSS and HTML5 - Table Formatting”, https://www.youtube.com/watch?v=-WfsM9WfvMw, accessed 3 November 2023

•	Datacamp, “Building Dashboards with Dash and Plotly”, https://campus.datacamp.com/courses/building-dashboards-with-dash-and-plotly/advanced-dash-apps?ex=8, accessed 3 November 2023

•	Tutorialspoint, “Flask-FileUploading”, https://www.tutorialspoint.com/flask/flask_file_uploading.htm#:~:text=Handling%20file%20upload%20in%20Flask,it%20to%20the%20desired%20location, accessed 3 November 2023 mdn web docs, date unknown, “HTML table basics:=“, https://developer.mozilla.org/en-US/docs/Learn/HTML/Tables/Basics, 3 November 2023

•	Tech with Tim, 19 November 2019, YouTube,“Flask Tutorial #9 - Static Files (Custom CSS, Images & Javascript)”, https://www.youtube.com/watch?v=tXpFERibRaU, accessed 3 November 2023

•	Udemy, The App Brewery, “The Complete 2023 Web Development Bootcamp”, https://www.udemy.com/course/the-complete-web-development-bootcamp/learn/lecture/37349924#overview, accessed 28, October 2023

•	Author Unknown, date unknown, Bootstrap, “Buttons”, https://getbootstrap.com/docs/4.0/components/buttons/, accessed 30 October 2023

•	Oleg Komarov, 3 Jan 2019, “How to embed a Dash app into an existing Flask app”, https://medium.com/@olegkomarov_77860/how-to-embed-a-dash-app-into-an-existing-flask-app-ea05d7a2210b, accessed 31 October 2023

•	Bootstrap, “Album Example”, https://getbootstrap.com/docs/4.0/examples/album/, accessed 29 October 2023

•	Plotly, date unknown, “html.Code”, https://dash.plotly.com/advanced-callbacks, 31 October 2023

•	Plotly, date unknown, “html.Code”, https://dash.plotly.com/dash-html-components/code, 31 October 2023
