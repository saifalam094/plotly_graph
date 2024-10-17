# Import necessary packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import json

# Load and incorporate the JSON data
with open('table-data.json') as f:
    data = json.load(f)

df = pd.json_normalize(data)

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My App with US Census Data', style={'textAlign': 'center'}),
    html.Hr(),
    
    dcc.RadioItems(
        options=[
            {'label': 'Total Population', 'value': 'Total'},
            {'label': 'White Total Population', 'value': 'WhiteTotal'},
            {'label': 'Black Total Population', 'value': 'BlackTotal'},
            {'label': 'Hispanic Population', 'value': 'Hispanic'}
        ],
        value='Total',  # default selection
        id='my-radio-item-example'
    ),
    
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    
    # Layout for the five graphs with centered headings
    html.Div([
        html.Div([
            html.H4('Bar Chart: Population by State', style={'textAlign': 'center'}),  # Centered Heading for Bar Chart
            dcc.Graph(figure={}, id='my-bar-graph')
        ], style={'margin-bottom': '40px'}),  # Add some space below the graph

        html.Div([
            html.H4('Pie Chart: Population Distribution by State', style={'textAlign': 'center'}),  # Centered Heading for Pie Chart
            dcc.Graph(figure={}, id='my-pie-chart', style={'height': "600px"})
        ], style={'margin-bottom': '40px'}),  # Add some space below the graph

        html.Div([
            html.H4('Scatter Plot: Population vs Total', style={'textAlign': 'center'}),  # Centered Heading for Scatter Plot
            dcc.Graph(figure={}, id='my-scatter-plot', style={'height': "600px"})
        ], style={'margin-bottom': '40px'}),  # Add some space below the graph

        html.Div([
            html.H4('Box Plot: Population Distribution by State', style={'textAlign': 'center'}),  # Centered Heading for Box Plot
            dcc.Graph(figure={}, id='my-box-plot', style={'height': "600px"})
        ], style={'margin-bottom': '40px'}),  # Add some space below the graph

        html.Div([
            html.H4('Line Chart: Trend of Population by State', style={'textAlign': 'center'}),  # Centered Heading for Line Chart
            dcc.Graph(figure={}, id='my-line-chart', style={'height': "600px"})  # New line chart
        ], style={'margin-bottom': '40px'})  # Add some space below the graph
    ])
])

# Add controls to update all five graphs
@callback(
    [Output('my-bar-graph', 'figure'),
     Output('my-pie-chart', 'figure'),
     Output('my-scatter-plot', 'figure'),
     Output('my-box-plot', 'figure'),
     Output('my-line-chart', 'figure')],  # New output for line chart
    Input('my-radio-item-example', 'value')
)
def update_graphs(col_chosen):
    # Bar chart
    bar_fig = px.bar(df, x='State', y=col_chosen, title=f'{col_chosen} by State')
    
    # Pie chart
    pie_fig = px.pie(df, names='State', values=col_chosen, title=f'{col_chosen} Distribution by State')

    # Scatter plot
    scatter_fig = px.scatter(df, x='Total', y=col_chosen, title=f'{col_chosen} vs Total Population', 
                             labels={'Total': 'Total Population', col_chosen: col_chosen})  # Label customization
    
    # Box plot
    box_fig = px.box(df, x='State', y=col_chosen, title=f'Distribution of {col_chosen} by State')

    # Line chart
    line_fig = px.line(df, x='State', y=col_chosen, title=f'Trend of {col_chosen} by State',
                       labels={'State': 'State', col_chosen: col_chosen})  # Label customization

    return bar_fig, pie_fig, scatter_fig, box_fig, line_fig  # Return all five figures

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
