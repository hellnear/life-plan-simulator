""" Application entry point. """

import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format

from simulator.simulation import simulate

with open('test.json', 'r') as f:
    params = json.load(f)

df = simulate(params=params, num_years=100)
display_unit = params['settings']['display unit']['unit']

app = dash.Dash()
app.title = 'My Life Plan'

app.layout = html.Div(
    children=[
        html.H1('My Life Plan'),

        dcc.Graph(
            id='Savings',
            figure={
                'data': [
                    {'x': df.columns, 'y': df.loc['balance', 'savings'],
                     'type': 'bar', 'name': 'savings'}
                ],
                'layout': {
                    'title': 'Savings',
                    'xaxis': {'title': 'Year'},
                    'yaxis': {'title': display_unit, 'tickformat': 'digit'}
                }
            }
        ),

        dash_table.DataTable(
            id='data_table',
            columns=\
                [{'id': f'level_{i}', 'name': ''} for i in range(2)] + \
                [{'id': f'{year}',
                  'name': f'{year}',
                  'type': 'numeric'}
                 for year in df.columns],
            data=df.reset_index().to_dict('record'),
            fixed_columns={'headers': True, 'data': 2},
            style_table={'width': '100%', 'minWidth': '100%'}
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
