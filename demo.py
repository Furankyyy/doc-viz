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


def plot_embeddings(pairs1, pairs2, dimension = 3):

    sentences1, embeddings1 = pairs1[0], pairs1[1]
    sentences2, embeddings2 = pairs2[0], pairs2[1]

    dim_reduc = PCA(n_components=dimension)
    dim_reduc.fit(np.vstack((embeddings1,embeddings2)))
    
    reduced_emb1 = dim_reduc.fit_transform(embeddings1)
    reduced_emb2 = dim_reduc.fit_transform(embeddings2)

    if dimension == 3: 
        data1 = {'sentences': sentences1, 'dim1': reduced_emb1[:,0], 'dim2': reduced_emb1[:,1],
                'dim3': reduced_emb1[:,2]}
        data1 = pd.DataFrame(data1)

        data2 = {'sentences': sentences2, 'dim1': reduced_emb2[:,0], 'dim2': reduced_emb2[:,1],
                'dim3': reduced_emb2[:,2]}
        data2 = pd.DataFrame(data2)
        """
        fig = px.scatter_3d(data, x='dim1', y='dim2', z='dim3',
                            title='Visualized embedding space',
                            labels={'0': 'Dimension 1', '1': 'Dimension 2', '2': 'Dimension 3'}
                            )
        """
        fig = go.Figure(go.Scatter3d(
                        x = data1['dim1'],
                        y = data1['dim2'],
                        z = data1['dim3'],
                        text = data1['sentences'],
                        hovertemplate = "<b>%{text}</b><br><br>"+"<extra></extra>",
                        mode='markers',
                        marker=dict(color = 'blue')
                        ))

        fig.add_trace(go.Scatter3d(
                        x = data2['dim1'],
                        y = data2['dim2'],
                        z = data2['dim3'],
                        text = data2['sentences'],
                        hovertemplate = "<b>%{text}</b><br><br>"+"<extra></extra>",
                        mode='markers',
                        marker=dict(color = 'red')
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

        
if __name__ == '__main__':

    m = SentenceEncoder()

    with open('sample_obama.txt','r') as f:
        obama = f.read().replace("\n", " ")
        f.close()

    with open('sample_trump.txt','r') as f:
        trump = f.read().replace("\n", " ")
        f.close()

    e1 = m.encode(obama)
    e2 = m.encode(trump)


    plot_embeddings(e1,e2,3)
        