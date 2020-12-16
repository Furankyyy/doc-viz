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

        data = [] # [[sents1,embs1],[sents2,embs2],...]
        
        for text in args:
            pair = self.Encoder.encode(text)
            data.append(pair)
        
        dim_reduc = PCA(n_components=3)
        dim_reduc.fit(np.vstack([pair[1] for pair in data]))

        embeddings = [] # [embs_for_doc_1, embs_for_doc_2,...]
        sentences = [] # [sents_for_doc_1, sents_for_doc_2,...]

        df = []
        for pair in data:
            reduced_embeddings = dim_reduc.fit_transform(pair[1])
            df.append({'sentences': pair[0], 'dim1': reduced_embeddings[:,0], 
                    'dim2': reduced_embeddings[:,1],'dim3':reduced_embeddings[:,2]})
        
        fig = go.Figure()

        for d in df:
            
            plotting = pd.DataFrame(d)
            
            fig.add_trace(go.Scatter3d(
                        x = plotting['dim1'],
                        y = plotting['dim2'],
                        z = plotting['dim3'],
                        text = plotting['sentences'],
                        hovertemplate = "<b>%{text}</b><br><br>"+"<extra></extra>",
                        mode='markers'
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

        fig.update_layout(scene = dict(
                    xaxis_title='Dimension 1',
                    yaxis_title='Dimension 2',
                    zaxis_title='Dimension 3'))

        return fig