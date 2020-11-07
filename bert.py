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


def plot_embeddings(pairs, dimension = 2):

    sentences, embeddings = pairs[0], pairs[1]
    dim_reduc = PCA(n_components=dimension)
    reduced_emb = dim_reduc.fit_transform(embeddings)

    if dimension == 2:
        data = {'sentences': sentences, 'dim1': reduced_emb[:,0], 'dim2': reduced_emb[:,1]}
        data = pd.DataFrame(data)

        fig = px.scatter(data, x='dim1', y='dim2',
                         title='Visualized embedding space',
                         labels={'0': 'Dimension 1', '1': 'Dimension 2'}
                         )

        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        #fig.add_trace



    if dimension == 3: 
        data = {'sentences': sentences, 'dim1': reduced_emb[:,0], 'dim2': reduced_emb[:,1],
                'dim3': reduced_emb[:,2]}
        data = pd.DataFrame(data)
        """
        fig = px.scatter_3d(data, x='dim1', y='dim2', z='dim3',
                            title='Visualized embedding space',
                            labels={'0': 'Dimension 1', '1': 'Dimension 2', '2': 'Dimension 3'}
                            )
        """
        fig = go.Figure(go.Scatter3d(
                        x = data['dim1'],
                        y = data['dim2'],
                        z = data['dim3'],
                        text = data['sentences'],
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

    fig.show()
        

if __name__ == '__main__':

    m = SentenceEncoder()

    with open('sample.txt','r') as f:
        t = f.read().replace("\n", " ")
        f.close()

    e = m.encode(t)

    plot_embeddings(e,3)
        