# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 14:36:15 2020

@author: qwerdf
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input,Output
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app=dash.Dash("Reddit Post Cluster",external_stylesheets=external_stylesheets)
data=pd.read_csv(r"tsne.csv")
data=data.dropna(axis=0)

app.layout=html.Div([
    dcc.Slider(
        id="Slider",
        min=0,
        max=data['group'].max(),
        value=0,
        marks={str(group):str(group) for group in data['group'].unique()},
        step=None
        ),
    dcc.Graph(id='main_post')]
    )

@app.callback(
    Output('main_post','figure'),
    [Input('Slider','value')])
def update_figure(select_group):
    traces=[]
    for group in sorted(data['group'].unique()):
        sub_data=data[data['group']==group]
        if group ==select_group:
            traces.append(
                dict(
                    x=sub_data['TSNE component 1'],
                    y=sub_data["TSNE component 2"],
                    text=sub_data["title"],
                    customdata=sub_data['web_link'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size':5,
                        'color':"purple"
                        },
                    name=group,
                    hovertemplate="<b>Title:%{text}</b><br><br>Web Link:%{customdata}<br><br>TSNE Component 1: %{x:.2f}<br><br>TSNE Component 2: %{y:.2f}"
                )
                ) 
        else:
            traces.append(
                dict(
                    x=sub_data['TSNE component 1'],
                    y=sub_data["TSNE component 2"],
                    text=sub_data["title"],
                    mode='markers',
                    opacity=0.3,
                    marker={
                        'size':3
                        },
                    name=group,
                    hovertemplate="<b>%{text}</b>"
                )
                ) 
    return {
        'data':traces,
        'layout':dict(
            title="Clustering Reddit Post in /r/dataisbeautiful Using TSNE",
            xaxis={'type':'linear','title':"TSNE comoponet 1"},
            yaxis={'type':'linear','title':"TSNE component 2"},
            legend={'x':0,"y":1},
            hovermode='closest',
            height=1000,
            transition={'duration':500}
            ),
        'config':dict(
            responsive=True
            )
        }


    

if __name__ == '__main__':
    app.run_server(debug=False)
