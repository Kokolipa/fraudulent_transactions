import dash
from dash import html, dcc
import subprocess
import pandas as pd
from flask import request, render_template

external_stylesheets_scripts = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
    'https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,300;1,300&family=Noto+Sans+Display:wght@300&display=swap',
]


dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets_scripts)


@dash_app.server.route('/')
def home():
    subprocess.call(["python", "-m", "http.server", "8000"])
    return dcc.Location(pathname='flask/templates/index.html')

@dash_app.server.route('/transactions')
def transactions():
    subprocess.call(["python", "-m", "http.server", "8000"])
    return dcc.Location(pathname='flask/templates/transactions.html')

# Upload route for processing the uploaded file
@dash_app.server.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file
            file.save('uploaded_file.csv')

            fraud_df = pd.read_csv('uploaded_file.csv')

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



dash_app.layout = html.Div([
    html.Header([
        html.Meta(charSet='UTF-8'),
        html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        html.Meta(httpEquiv='X-UA-Compatible', content='ie=edge'),
        html.Title('Credit Card Fraud Analysis-dashboard'),
        # Define the CSS links
        html.Link(rel='preconnect', href='https://fonts.googleapis.com'),
        html.Link(rel='preconnect', href='https://fonts.gstatic.com', crossOrigin='true'),
        html.Link(rel='stylesheet', href='/static/styles.css'),  # Replace with the correct path
    ]),
    html.Div([
        html.Nav(className='navbar navbar-dark bg-dark fixed-top', children=[
            html.Div(className='container-fluid', children=[
                html.A('Gal Beeri, Katharine Tamas, Mireille Walton', className='navbar-brand'),
                html.Button(className='navbar-toggler', type='button', **{
                    'data-bs-toggle': 'offcanvas',
                    'data-bs-target': '#offcanvasDarkNavbar',
                    'aria-controls': 'offcanvasDarkNavbar',
                    'aria-label': 'Toggle navigation'
                }),
                html.Div(className='offcanvas offcanvas-end text-bg-dark', tabIndex='-1', id='offcanvasDarkNavbar', children=[
                    html.Div(className='offcanvas-body', children=[
                        html.Ul(className='navbar-nav justify-content-end flex-grow-1 pe-3', children=[
                            html.Li(className='nav-item', children=[
                                dcc.Link('Home', className='nav-link active', href='/templates/', target = "_blank"),
                            ]),
                            html.Li(className='nav-item', children=[
                                dcc.Link('Upload and view transactions', className='nav-link', href='flask/templates/transactions.html', target = "_blank"),
                                dcc.Link('Home', className='nav-link', href='flask/templates//templates/', target="_blank"),
                            ]),
                        ]),
                    ]),
                ], **{'aria-label': 'offcanvasDarkNavbarLabel'})
            ]),
        ]),

        # HERO BANNER
        html.Div(className='hero_banner', style={'height': '20px'}, children=[
            html.Img(src='/static/images/homepg_image.jpg', width='100%', height='350px'),
            html.Div(className='container-fluid', children=[
                html.Br(),html.H1('Fraudulent Transactions Dashboard', className='jumbotron-heading'),
                html.Div(className='row', children=[
                    html.Div(className='col-md-2'),
                    html.Div(className='col-md-8', style={'height': '120px', 'margin-bottom':'30px'}, children=[
                        html.Br(),
                        html.P('This dashboard provides an analysis of all transactions within the dataset.', className='lead text-muted'),
                    ]),
                    html.Div(className='col-md-2'),
                ]),
            ]),
        ]),
        
        # DEFINE BACK TO TRANSACTIONS PAGE BUTTON LAYOUT
        html.Div(className='file_upload_layout', children=[
            html.Div(className='container-fluid', children=[
                html.Div(className='row', style={'margin-top': '70px'}, children=[
                    html.Div(className='col-3 mx-auto my-5', children=[
                        html.Div(className='card', style={'borderColor': 'white'}, children=[
                            html.Div(className='card-body', style={'backgroundColor': 'white', 'textAlign': 'center'}, children=[
                                dcc.Link('Back to view transactions', className='btn btn-secondary', style={'color': 'white'}, href='flask/templates/transactions', target = "_blank"),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),

        # DASH - DASHBOARD DATA
        html.Div(className='dashboard_layout', children=[
            html.Div(className='container-fluid', children=[
                html.Div(className='col-md-3'),
                html.Br(),
                html.Br(),
                html.Div(id='dashboard-content'),
            ]),
        ]),
    ]),
])

def get_dash_app():
    return dash_app


if __name__ == '__main__':
    dash_app.run(debug=True, host='0.0.0.0', port=8000)

