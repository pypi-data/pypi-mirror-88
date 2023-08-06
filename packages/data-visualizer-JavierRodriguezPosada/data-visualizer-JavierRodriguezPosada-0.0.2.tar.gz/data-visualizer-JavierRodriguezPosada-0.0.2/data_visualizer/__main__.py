import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
   
    dcc.Dropdown(
        id='graph-dropdown',
        options=[
            {'label': '3D Axis', 'value': '3d-axis'},
            {'label': '3D Scatter', 'value': '3d-scatter'},
            {'label': 'Surface', 'value': 'surface'}
        ],
        value='3d-axis',
        placeholder='Select a plot'
    ),

    html.Button('Toggle animation', id='toggle-animation'),

    dcc.Graph(
        figure=px.scatter_3d(),
        style={'height': 900},
        id='graph'
    ),

    dcc.RangeSlider(
        id='my-range-slider',
        min=1,
        max=1,
        step=1,
        value=[1,1],
        marks={
            1: { 'label': '1' }
        },
        allowCross=False
    ),

    dcc.Interval(
        id='range-interval',
        disabled=True,
        n_intervals=0
    ),

    # Data cache
    html.Div(id='panda_dataframe', style={'display': 'none'})
])

def file_to_dataframe(contents, filename, date):
    df = pd.DataFrame()

    _, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'xls' in filename or 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        df = pd.DataFrame()
        print(e)

    return df.to_json(date_format='iso', orient='split')

@app.callback(Output('panda_dataframe', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True)
def process_files(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            file_to_dataframe(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output('my-range-slider', 'max'),
    Input('panda_dataframe', 'children'),
    prevent_initial_call=True)
def update_range_max(data):
    max_value = 1
    
    if data:
        df = pd.read_json(data[0], orient='split')

        if not df.empty:
            max_value = df.shape[0]

    return max_value

@app.callback(
    Output('my-range-slider', 'marks'),
    Input('my-range-slider', 'max'),
    State('panda_dataframe', 'children'),
    prevent_initial_call=True)
def update_range_marks(max_value, data):
    marks = {}
    
    if data:
        df = pd.read_json(data[0], orient='split')

        if not df.empty:
            for index in range(1,max_value + 1,1):
                marks[index] = { 'label': str(index) }

    return marks

@app.callback(
    Output('my-range-slider', 'value'),
    Input('my-range-slider', 'max'),
    Input('range-interval', 'n_intervals'),
    State('my-range-slider', 'value'),
    prevent_initial_call=True)
def update_range_value(max_value, n_intervals, current_range_value):
    ctx = dash.callback_context
    
    range_value = [1,1]
    
    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'range-interval':
        range_value[1] = current_range_value[1] + 1
    else:
        range_value[1] = max_value

    if range_value[1] > max_value:
        range_value[1] = 1

    return range_value

@app.callback(
    Output('graph', 'figure'),
    Input('panda_dataframe', 'children'),
    Input('my-range-slider', 'value'),
    Input('graph-dropdown', 'value'),
    prevent_initial_call=True)
def generate_graph(data, range_value, value):
    fig = px.scatter_3d()
    x, y, z = [], [], []

    if data:
        df = pd.read_json(data[0], orient='split')

        if not df.empty:
            for column in df.columns.values[1:]:
                for row in df.index[(range_value[0]-1):range_value[1]]:
                    x.append(column)
                    y.append(df.at[row,df.columns.values[0]])
                    z.append(df.at[row,column])

            if (value == '3d-axis'):
                fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z, opacity=0.5)])
            elif (value == '3d-scatter'):
                fig = px.scatter_3d(x=x, y=y, z=z)
            elif (value == 'surface'):
                fig = go.Figure(data=[go.Surface(z=df.values[(range_value[0]-1):range_value[1]])])
             
            z_min = df.min(axis=1).min()
            z_max = df.max(axis=1).max()
            
            z_length = z_max - z_min
            z_min -= z_length * 0.05
            z_max += z_length * 0.05

            # Calculate ratio in reference to x_ratio=1
            y_ratio = df.shape[0] / df.shape[1]

            fig.update_layout(
                uirevision=1,
                scene_aspectmode='manual',
                scene_aspectratio=dict(x=1,y=y_ratio,z=1),
                scene = dict(
                    xaxis=dict(
                        ticks='outside',
                        nticks=df.shape[1]
                    ),
                    yaxis=dict(
                        ticks='outside',
                        nticks=df.shape[0],
                        range=[0,df.shape[0]]
                    ),
                    zaxis=dict(
                        ticks='outside',
                        range=[z_min,z_max]
                    )
                )
            )

    return fig

@app.callback(
    Output('range-interval', 'disabled'),
    Input('toggle-animation', 'n_clicks'),
    State('range-interval', 'disabled'),
    prevent_initial_call=True)
def toggle_animation(n_clicks, disabled):
    return not disabled


if __name__ == '__main__':
    app.run_server(debug=True)