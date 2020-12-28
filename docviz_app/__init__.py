import dash
import io
import redis
import uuid
from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job
import os
from base64 import b64encode
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import nltk
from nltk.tokenize import sent_tokenize
from dash.exceptions import PreventUpdate
from .plot import plot_dash
from .core import app, conn, queue

nltk.download('punkt')

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

    dcc.Store(id="submitted-store"),
    dcc.Store(id="finished-store"),
    dcc.Interval(id="interval", interval=500),

    dcc.Graph(
        id='output_graph'
    ),

    html.A(
        html.Button("Download HTML"), 
        id="download",
        href="",
        download="plotly_graph.html"
    )
])


@app.callback(
    Output("submitted-store", "data"),
    Output('err', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('input_text', 'value')],
    [State('input_text2', 'value')],
    [State('input_text3', 'value')],
    [State('input_text4', 'value')],
    [State('document_text', 'value')],
    [State('document_text2', 'value')],
    [State('document_text3', 'value')],
    [State('document_text4', 'value')]
)
def submit(n_clicks, text1, text2, text3, text4, doc1, doc2, doc3, doc4):
    """
    Submit a job to the queue, log the id in submitted-store
    """
    text = [text1, text2, text3, text4]
    doc = [doc1, doc2, doc3, doc4]
    if len(sent_tokenize(' '.join(text))) < 3:
        return {}, 'Please input more than 3 sentences!'
        #raise PreventUpdate
        
    if n_clicks:
        print('start queueueueueueueu')
        id_ = str(uuid.uuid4())
        data = [(doc[n],text[n]) for n in range(len(text))]
        # queue the task
        queue.enqueue(plot_dash, data, job_id=id_,timeout='1h')
        print('finishquququququququ')
        # log process id in dcc.Store
        return {"id": id_}, ''

    return {},''


'''
@app.callback(
    Output('output_graph', 'figure'),
    Output('err', 'children'),
    Output('download','href'),
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
        return dash.no_update, 'Please input more than 3 sentences!', ''
        #raise PreventUpdate
    
    data = [(doc[n],text[n]) for n in range(len(text))]
    m = Plot_Embedding()
    fig = m.plot(*data)

    buffer = io.StringIO()
    fig.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    encoded = b64encode(html_bytes).decode()

    return fig, '', "data:text/html;base64," + encoded
'''



@app.callback(
    [
        Output('output_graph', 'figure'),
        Output('download','href'),
        Output("finished-store", "data"),
    ],
    [Input("interval", "n_intervals")],
    [State("submitted-store", "data")],
)
def retrieve_output(n, submitted):
    """
    Periodically check the most recently submitted job to see if it has
    completed.
    """
    if n and submitted:
        try:
            job = Job.fetch(submitted["id"], connection=conn)
            print(job.get_status())
            print(job.last_heartbeat)
            print(job.exc_info)
            if job.get_status() == "finished":
                # job is finished, return result, and store id
                return job.result[0], job.result[1], {"id": submitted["id"]}

            # job is still running, get progress and update progress bar
            return dash.no_update, dash.no_update, dash.no_update

        except NoSuchJobError:
            # something went wrong, display a simple error message
            return dash.no_update, dash.no_update, dash.no_update
    # nothing submitted yet, return nothing.
    return dash.no_update, None, {}



@app.callback(
    Output("interval", "disabled"),
    [Input("submitted-store", "data"), Input("finished-store", "data")],
)
def disable_interval(submitted, finished):
    if submitted:
        if finished and submitted["id"] == finished["id"]:
            # most recently submitted job has finished, no need for interval
            return True
        # most recent job has not yet finished, keep interval going
        return False
    # no jobs submitted yet, disable interval
    return True

