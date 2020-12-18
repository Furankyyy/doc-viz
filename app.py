import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from plot import Plot_Embedding
from dash.dependencies import Input, Output, State
import nltk
from nltk.tokenize import sent_tokenize
from dash.exceptions import PreventUpdate

nltk.download('punkt')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='DocViz'),

    html.Div(children='''
        DocViz: A document visualization tool based on BERT.
    '''),
    html.Br(),
    html.Br(),


    html.I("Input document text into the boxes below. Supports up to 4 documents for visualization."),
    html.Br(),
    html.Div(['Document name (Required):', dcc.Input(id='document_text', value='', type='text'), 
              "Input (Required): ", dcc.Input(id='input_text', value='', type='text')]),
    html.Br(),
    html.Div(['Document 2 name (Optional):', dcc.Input(id='document_text2', value='', type='text'), 
              "Input 2 (Optional): ", dcc.Input(id='input_text2', value='', type='text')]),
    html.Br(),
    html.Div(['Document 3 name (Optional):', dcc.Input(id='document_text3', value='', type='text'), 
              "Input 3 (Optional): ", dcc.Input(id='input_text3', value='', type='text')]),
    html.Br(),
    html.Div(['Document 4 name (Optional):', dcc.Input(id='document_text4', value='', type='text'), 
              "Input 4 (Optional): ", dcc.Input(id='input_text4', value='', type='text')]),
    html.Br(),
    html.Button('Plot', id='submit-val', n_clicks=0),

    html.P(id='err', style={'color': 'red'}),

    dcc.Graph(
        id='output_graph'
    )
])


@app.callback(
    Output('output_graph', 'figure'),
    Output('err', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('input_text', 'value')],
    [State('input_text2', 'value')],
    [State('input_text3', 'value')],
    [State('input_text4', 'value')],
    [State('document_text', 'value')],
    [State('document_text2', 'value')],
    [State('document_text3', 'value')],
    [State('document_text4', 'value')],
    # prevent_initial_call=True
)
def update_output_div(n_clicks, text1, text2, text3, text4, doc1, doc2, doc3, doc4):
    text = [text1, text2, text3, text4]
    doc = [doc1, doc2, doc3, doc4]
    if len(sent_tokenize(' '.join(text))) < 3:
        return dash.no_update, 'Please input more than 3 sentences!'
        #raise PreventUpdate
    
    data = [(doc[n],text[n]) for n in range(len(text))]
    m = Plot_Embedding()
    fig = m.plot(*data)
    return fig, ''


if __name__ == '__main__':
    app.run_server(debug=True)
