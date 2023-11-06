import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import subprocess
import pandas as pd
from flask import request, render_template

external_stylesheets_scripts = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
    'https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,300;1,300&family=Noto+Sans+Display:wght@300&display=swap',
]


dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets_scripts)

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

