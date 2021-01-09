from sentence_transformers import SentenceTransformer, util
import torch
from nltk.tokenize import sent_tokenize
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import io
from base64 import b64encode


class SentenceEncoder():

    def __init__(self):
        self.model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    def encode(self, text):
        '''
        text: Long string document input.
        '''
        sentences = sent_tokenize(text)
        embeddings = self.model.encode(sentences)

        return [sentences, embeddings]


### ADD FEATURE TO TAKE IN DOC NAME


class Plot_Embedding():

    def __init__(self):
        self.Encoder = SentenceEncoder()
    
    def plot(self, *args):

        '''
        args: (doc_name, doc)
        '''

        data = [] # [[doc1,embs1],[doc2,embs2],...]
        names = []
        
        print('encoding starts')
        for (doc_name, doc) in args:
            if doc is '':
                continue
            pair = self.Encoder.encode(doc)
            data.append(pair)
            names.append(doc_name)

        print('PCA starts')
        
        dim_reduc = PCA(n_components=3)
        dim_reduc.fit([emb for doc in data for emb in doc[1]])

        embeddings = [] # [embs_for_doc_1, embs_for_doc_2,...]
        sentences = [] # [sents_for_doc_1, sents_for_doc_2,...]

        df = []
        for pair in range(len(data)):
            reduced_embeddings = dim_reduc.transform(data[pair][1])
            df.append({'sentences': data[pair][0], 'dim1': reduced_embeddings[:,0], 
                    'dim2': reduced_embeddings[:,1],'dim3': reduced_embeddings[:,2], 
                    'doc_name': [names[pair]]*len(reduced_embeddings)})
        
        fig = go.Figure()

        for d in df:
            
            plotting = pd.DataFrame(d)
            
            fig.add_trace(go.Scatter3d(
                        x = plotting['dim1'],
                        y = plotting['dim2'],
                        z = plotting['dim3'],
                        text = plotting['sentences'],
                        hovertemplate = "<b>%{text}</b><br><br>"+"<extra></extra>",
                        mode='markers',
                        name=plotting['doc_name'][0]
                        ))
        
        fig.update_layout(scene = dict(
            xaxis = dict(
                showticklabels=False),
            yaxis = dict(
                showticklabels=False),
            zaxis = dict(
                showticklabels=False)
            ),           
            )

        fig.update_layout(autosize=True,
                          #width=1000,
                          height=850,
                          margin=dict(l=50,r=50,b=50,t=50))

        fig.update_layout(scene = dict(
                    xaxis_title='Dimension 1',
                    yaxis_title='Dimension 2',
                    zaxis_title='Dimension 3'))

        return fig


def plot_dash(data):

    print('plotting')

    M = Plot_Embedding()
    fig = M.plot(*data)
    print('plotting finish')
    buffer = io.StringIO()
    fig.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    encoded = b64encode(html_bytes).decode()

    return fig, "data:text/html;base64," + encoded