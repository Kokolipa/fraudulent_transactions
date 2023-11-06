# Importing dependencie
# ----------------------------------------------------------------

# * Analysis & Manipulation libraries
import pandas as pd 
import numpy as np

# * Dashboard creation libraries
import plotly.express as px 
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

# * Flask Dependencies
from flask import Flask, session


# Loading the dataset
path = session.get('file_path')

fraud_df = pd.read_csv(path, parse_dates=["trans_date_trans_time", "dob"],infer_datetime_format=True)

columns_to_drop = ["Unnamed: 0", "cc_num", "unix_time", "zip"]
fraud_df = fraud_df.drop(columns_to_drop, axis=1)

# Formatting category & merchant
fraud_df['merchant'] = fraud_df['merchant'].str.replace("fraud_", "")
fraud_df['category'] = fraud_df['category'].str.replace("_", " ")

# Calculating the age of the person at the time of the transaction
fraud_df['age'] = (fraud_df['trans_date_trans_time'] - fraud_df['dob']).apply(lambda x: x.days // 365)

# Dropping the dob column
fraud_df = fraud_df.drop('dob', axis=1)

# Modifying the gender column
fraud_df['gender'] = fraud_df['gender'].str.replace("M", "Male")
fraud_df['gender'] = fraud_df['gender'].str.replace("F", "Female")

# Amount of transactions in the dataset
total_transactios = fraud_df['trans_num'].count()
total_transactios_formatted = str(total_transactios)[:3] +"," +str(total_transactios)[3:]

# The percentage of fraudulent transactions relative to non-fraudulent transactions
percentage_fraudulent = round((fraud_df.query("is_fraud == 1")['is_fraud'].count()) / (fraud_df.query("is_fraud == 0")['is_fraud'].count()), 3)
percentage_fraudulent_formatted = f"%{percentage_fraudulent}"

# Importing external stylesheets
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Nameing the app and using the SLATE style theme
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

# Configuring the SLATE style theme on the figures
load_figure_template("SLATE")

# Define filter labels
FILTER_LABELS = {
    1: 'Fraudulent',
    0: 'Non-Fraudulent',
    -1: 'All'
}

# Define chart colors
color_list = ["#FC0303", "#31FC03"]

# Determining the app_layout
app.layout = html.Div(
    style={"width": "80%", "height": "80%", "margin-left": "10%", "margin-right": "10%", "margin-top": "20%"},
    children=[
    dbc.Row(html.H1(id="header"), style={"color":"white", "margin-top":"5px", "margin-left":"5px", "fontSize": "35px"}),
    dbc.Row(dbc.Card(dbc.RadioItems(
        id="dataFilter",
        options= [
            {'label': 'Fraudulent', 'value': 1},
            {'label': 'Non-Fraudulent', 'value': 0},
            {'label': 'All', 'value': -1}],
            value=0,
            inline=True
    ), style={"textAlign":"center"})),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(f"Total Transactions: {total_transactios_formatted}"), style={"textAlign":"center",
                                                                                      "fontSize": "20px"},),
        dbc.Col(dbc.Card(f"Fraudulent: {percentage_fraudulent_formatted}"), style={"textAlign":"center",
                                                                                    "fontSize": "20px"}),
        ]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card([
            dcc.Dropdown(
                id="features",
                options=fraud_df.select_dtypes(include='object').columns[:-1],
                value= "category",
                className='dbc'
            ),
            dbc.RadioItems(
                id="asc-desc",
                options= [
                    {'label': 'Ascending', 'value': True},
                    {'label': 'Descending', 'value': False}],
                value=False,
                inline=True),
            dcc.Graph(id="hBarChart"),
            ]), width=4),
        dbc.Col(dbc.Card(dcc.Graph(id="histogram")), width=4),
        dbc.Col(dbc.Card(dcc.Graph(id="pieChart")), width=4)
        ]),
    html.Br(),
    dbc.Row(dbc.Card(dcc.Graph(id="scatterMapBox", style={"width": "100%"})))
])
@app.callback(
    Output("header", "children"),
    Output("hBarChart", "figure"),
    Output("histogram", "figure"),
    Output("pieChart", "figure"),
    Output("scatterMapBox", "figure"),
    Input("dataFilter", "value"),
    Input("features", "value"),
    Input("asc-desc", "value")
)
def dashboard(filter_item, feature, sort_order):
    # * Prevent None values
    if filter_item is None:
        raise PreventUpdate()
    
    # * Match the filted label to the selected filter item
    filter_label = FILTER_LABELS.get(filter_item, 'Unknown Filter')
    
    # * Create a dynamic header
    header = f"{filter_label} Dashboard"

    # * Filter the datset based on the selected filter item
    if filter_item == 1:
        df = fraud_df.query("is_fraud == 1")
    elif filter_item == 0:
        df = fraud_df.query("is_fraud == 0")
    else:
        df = fraud_df

    # * Plot the bar chart 
    bar = (
        px.bar(
        df.groupby(feature, as_index=False)["trans_num"].count().sort_values(by="trans_num", ascending=sort_order),
        x="trans_num",
        y=feature,
        color="trans_num",
        color_continuous_scale="Tealgrn",
        text_auto='.2s',
        title=f"Total Transactions by {feature} ({filter_label})"
        )
        .update_xaxes(
        title =f"Total Transactions")
        .update_layout(
        title = {
            'x': 0.12,
            'y': .85
        },
        coloraxis_showscale=False,
        plot_bgcolor='rgba(15, 15, 15, 0)',
        paper_bgcolor='rgba(15, 15, 15, 0.5)'
        )
    )

    # * Plot the histogram
    histogram = (
    px.histogram(
        df.groupby("age", as_index=False)['trans_num'].count(),
        x="age",
        y="trans_num",
        title=f"Destribution of Transactions by Age ({filter_label})"
        )
        .update_traces(marker_color='rgba(49, 252, 3, 0.6)', marker_line_color='#2ad104',
                       marker_line_width=1.5,
                       opacity=0.6)
        .update_layout(
        title = {
            "x": 0.075,
            "y": .85
        },
        plot_bgcolor='rgba(15, 15, 15, 0)',
        paper_bgcolor='rgba(15, 15, 15, 0.5)')
    )

    # * Plot the pie chart
    pie = (
        px.pie(
        df.groupby("gender", as_index=False)["trans_num"].count(),
        values="trans_num",
        names="gender",
        hole=0.46,
        color_discrete_sequence=['rgba(252, 3, 3, 0.7)', 'rgba(49, 252, 3, 0.6)'])
        .update_layout(
        title_text=f"Transactions Breakdown ({filter_label})",
        annotations=[dict(text='Gender %',
                     x=0.5,
                     y=0.5,
                     font_size=20,
                     showarrow=False)],
        title = {
            "x": 0.48
        },
        plot_bgcolor='rgba(15, 15, 15, 0)',
        paper_bgcolor='rgba(15, 15, 15, 0.5)')
    )

    # * Plot the scatter_mapbox
    map_scatter = (
        px.scatter_mapbox(
        df.groupby(["city", "lat", "long"])["trans_num"].count().reset_index(),
        lat="lat",
        lon="long",
        size="trans_num",
        color="trans_num",
        color_continuous_scale=px.colors.sequential.Jet,
        zoom=4.5,
        center=dict(
        lat=37.9931,
        lon=-100.9893
        ),
        mapbox_style="carto-darkmatter",
        title=f"Destribution of Transactions ({filter_label})",
        hover_data=["city"],
        hover_name="city",
        )
        .update_layout(
        title={
            "x":0.038,
            "y":.85
        },
        coloraxis_colorbar = dict(
        thicknessmode="pixels",
        thickness=15,
        title="Count"
        ),
        plot_bgcolor='rgba(15, 15, 15, 0)',
        paper_bgcolor='rgba(15, 15, 15, 0.5)')
    )


    return header, bar, histogram, pie, map_scatter

if __name__ == "__main__":
    app.run_server(debug=True, port=1891)