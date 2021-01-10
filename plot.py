from sentence_transformers import SentenceTransformer, util
import torch
from nltk.tokenize import sent_tokenize
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


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
        
        for (doc_name, doc) in args:
            if doc is '':
                continue
            pair = self.Encoder.encode(doc)
            data.append(pair)
            names.append(doc_name)
        
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
                    xaxis_title='',
                    yaxis_title='',
                    zaxis_title=''))

        return fig