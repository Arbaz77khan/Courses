#!/usr/bin/env python
# coding: utf-8

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Dropdown options and year list
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'yearly'},
    {'label': 'Recession Period Statistics', 'value': 'recession'}
]
year_list = [i for i in range(1980, 2024, 1)]

# Layout
app.layout = html.Div([
    html.H1("Automobile Sales Dashboard"),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='report-type',
            options=dropdown_options,
            value='yearly',
            placeholder='Select report type'
        )
    ]),

    html.Div(
        id='year-container',
        children=[
            dcc.Dropdown(
                id='select-year',
                options=[{'label': i, 'value': i} for i in year_list],
                value=1980
            )
        ]
    ),

    html.Div([
        html.Div(id='output-container', className='output', style={'display': 'flex', 'flexWrap': 'wrap'})
    ])
])

# Callback to show/hide year dropdown
@app.callback(
    Output('year-container', 'style'),
    Input('report-type', 'value')
)
def update_input_container(selected_statistics):
    return {'display': 'block'} if selected_statistics == 'yearly' else {'display': 'none'}

# Callback to update charts
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='report-type', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'recession':
        recession_data = data[data['Recession'] == 1]

        # Plot 1
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales fluctuation over Recession Period")
        )

        # Plot 2
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicles Sold by Vehicle Type during Recession")
        )

        # Plot 3
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, names='Vehicle_Type', values='Advertising_Expenditure',
                          title="Total Expenditure Share by Vehicle Type During Recession")
        )

        # Plot 4
        unemp_data = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='Unemployment_Rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'Unemployment_Rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title="Effect of Unemployment Rate on Vehicle Type and Sales")
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]

    elif selected_statistics == 'yearly' and selected_year:
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x="Year", y="Automobile_Sales", title="Yearly Automobile Sales Trend"))

        # Plot 2
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x="Month", y="Automobile_Sales", title="Total Monthly Automobile Sales"))

        # Plot 3
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x="Vehicle_Type", y="Automobile_Sales",
                                           title="Average Vehicles Sold by Vehicle Type in {}".format(selected_year)))

        # Plot 4
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, names="Vehicle_Type", values="Advertising_Expenditure",
                                           title="Total Advertisement Expenditure by Vehicle Type in {}".format(selected_year)))

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
