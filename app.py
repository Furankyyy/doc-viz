import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from plot import Plot_Embedding
from dash.dependencies import Input, Output
from nltk.tokenize import sent_tokenize
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Div(["Input: ",
              dcc.Input(id='input_text', value='Input text', type='text')]),


    dcc.Graph(
        id='output_graph'
    )
])


@app.callback(
    Output('output_graph', 'figure'),
    Input('input_text', 'value')
    # prevent_initial_call=True
)
def update_output_div(text):
    if len(sent_tokenize(text)) < 3:
        raise PreventUpdate
    m = Plot_Embedding()
    fig = m.plot(text)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)