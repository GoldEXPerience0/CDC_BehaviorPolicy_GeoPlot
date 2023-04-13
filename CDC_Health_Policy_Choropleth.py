#!/usr/bin/env python
# coding: utf-8

# In[1]:
#import dependencies
import numpy as np
import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, Input, Output

#Read cleaned, combined dataframe of behavior and policy
cdcdata = pd.read_csv('cdcdata.csv')

#Run the application
app = Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Health Behavior within the United States',
            style={'text-align':'center','color': '#004C54'}),
    html.Div(children='CDC Adult Data on Physical Activity, Nutrition, and Obesity (2011-2020) and related Policy Data (2011-2017)',
             style={'text-align':'center','color': '#004C54'}),
    
    html.Hr(),
    html.Br(),
    
    dcc.Slider(
        min=cdcdata['Year'].min(),
        max=cdcdata['Year'].max(),
        step=None,
        value=cdcdata['Year'].min(),
        marks={str(year):str(year) for year in cdcdata['Year'].unique()},
        id='year_slider'),
    
    html.Br(),
    
    html.Div(children='Topic:',style={'text-align':'left','color': '#004C54'}),
    dcc.Dropdown(options=[{'label':s,'value':s} for s in (cdcdata['Topic'].unique())],
                 value='Physical Activity',
                 id='topic_dropdown',
                placeholder='Select Topic',
                clearable=False),
    
    html.Br(),
    
    html.Div(children='Question:',style={'text-align':'left','color': '#004C54'}),
    dcc.Dropdown(id='question_dropdown',
                placeholder='Select Question',
                clearable=False),
    
    html.Br(),
    html.Hr(),
    
    dcc.Graph(id='my_map',figure={})
])

@app.callback(Output('question_dropdown','options'),
             Input('topic_dropdown','value'))
def set_question_options(selected_topic):
    dff = cdcdata[cdcdata['Topic']==selected_topic]
    return [{'label': i,'value': i} for i in (dff['Question'].unique())]


@app.callback(Output('question_dropdown','value'),
             Input('question_dropdown','options'))
def set_question_values(available_options):
    return [k['value'] for k in available_options][0]


@app.callback(
    Output('my_map','figure'),
    [Input('year_slider','value'),
    Input('topic_dropdown','value'),
    Input('question_dropdown','value')]
)
def update_map_by_slider(selected_year,selected_topic,selected_question):
    dff = cdcdata.copy()
    dff = dff[dff['Year']==selected_year]
    dff = dff[dff['Topic']==selected_topic]
    dff = dff[dff['Question']==selected_question]
    
    fig = px.choropleth(data_frame=dff,locationmode='USA-states',locations='LocationAbbr',
                        scope='usa',color='Data_Value',
                        hover_data=['High_Confidence_Limit','Data_Value','Low_Confidence_Limit','Sample_Size','NumPolicies'],
                        labels={'LocationAbbr':'Location',
                               'Low_Confidence_Limit':'Low Confidence Limit (%)',
                               'Data_Value':'Value in Question (%)',
                               'High_Confidence_Limit':'High Confidence Limit (%)',
                               'Sample_Size':'Sample Size',
                               'NumPolicies':'Number of Enacted Policies'},
                       template='plotly_dark')
    return fig


if __name__ == '__main__':
    app.run_server()
    
#viewer.show(app)

