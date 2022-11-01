#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, Input, Output
#Behavior DataFrame
behavior = pd.read_csv('cdcbehavior.csv')
#load policy data
policy = pd.read_csv('cdcpolicy.csv')


# In[2]:


#Dropping data
behavior.drop(['YearEnd','Datasource','Class','Data_Value_Unit','Data_Value_Type','Data_Value_Alt',
               'ClassID','TopicID','QuestionID','DataValueTypeID','LocationID',
               'Data_Value_Footnote_Symbol','Data_Value_Footnote',
               'GeoLocation','Age(years)', 'Education', 'Gender', 'Income','Race/Ethnicity',
               'StratificationCategory1', 'Stratification1','StratificationID1','StratificationCategoryId1'],
              axis=1,inplace=True)

behavior= behavior[behavior['LocationAbbr']!= 'PR'] 
behavior= behavior[behavior['LocationAbbr']!= 'GU']
behavior= behavior[behavior['LocationAbbr']!= 'VI']
behavior= behavior[behavior['LocationAbbr']!= 'DC'] #can remove or not remove

behavior= behavior[behavior['Total']=='Total']

#Rename and replace
behavior.rename(columns={'YearStart':'Year','High_Confidence_Limit ':'High_Confidence_Limit'},inplace=True)
behavior['Topic'].replace(to_replace='Physical Activity - Behavior',value='Physical Activity',inplace=True)
behavior['Topic'].replace(to_replace='Obesity / Weight Status',value='Obesity',inplace=True)
behavior['Topic'].replace(to_replace='Fruits and Vegetables - Behavior',value='Nutrition',inplace=True)

behavior['Question'].replace(to_replace='Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
                             value='% of adults with >= 150 min/wk of moderate aerobic or 75 min/wk of vigorous aerobic activity (or an = mix)',inplace=True)
behavior['Question'].replace(to_replace='Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
                             value='% of adults with >= 300 min/wk of moderate aerobic or 150 min/wk of vigorous aerobic activity (or an = mix)',inplace=True)
behavior['Question'].replace(to_replace='Percent of adults who engage in no leisure-time physical activity',
                             value='% of adults with no leisure-time physical activity',inplace=True)
behavior['Question'].replace(to_replace='Percent of adults aged 18 years and older who have obesity',
                             value='% of adults aged >= 18 years with obesity',inplace=True)
behavior['Question'].replace(to_replace='Percent of adults aged 18 years and older who have an overweight classification',
                             value='% of adults aged >= 18 years with an overweight classification',inplace=True)
behavior['Question'].replace(to_replace='Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
                             value='% of adults with muscle-strengthening activities >= 2 days/wk',inplace=True)
behavior['Question'].replace(to_replace='Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
                             value='% of adults with >= 150 min/wk of moderate aerobic or 75 min/wk of vigorous aerobic physical activity & muscle-strengthening activities on >= 2 days/wk',inplace=True)
behavior['Question'].replace(to_replace='Percent of adults who report consuming fruit less than one time daily',
                             value='% of adults who report consuming fruit < once/day',inplace=True)
behavior['Question'].replace(to_replace='Percent of adults who report consuming vegetables less than one time daily',
                             value='% of adults who report consuming vegetables < once/day',inplace=True)

#Drop
#behavior = behavior[behavior['Year']<2018] #get the year range
behavior.drop('Total',axis=1,inplace=True) #finished selecting total as total

#Organize 
behavior.sort_values(by=['Year','LocationAbbr','Topic'],inplace=True)
behavior.reset_index(drop=True,inplace=True)
behavior = behavior[['Year','LocationAbbr','LocationDesc','Topic','Question','Low_Confidence_Limit','Data_Value','High_Confidence_Limit',
                     'Sample_Size']]

behaviorUS = behavior[behavior['LocationAbbr']=='US']
behaviorUS.reset_index(drop=True,inplace=True)


# In[3]:


#Dropping data
policy.drop(['Quarter','DataSource','Title','Comments','GeoLocation','Citation','StatusAltValue','DataType','EnactedDate','EffectiveDate',
             'DisplayOrder','PolicyTypeID','HealthTopicID','PolicyTopicID','SettingID','ProvisionID'],axis=1,inplace=True)
policy = policy[policy['LocationAbbr']!='DC']
#Organizing 
policy.sort_values(['Year','LocationAbbr','LocationDesc','HealthTopic'],inplace=True)
policy.reset_index(drop=True,inplace=True)

#Create policyEnacted
#copy to prevent assigning and selecting at once
policyEnacted = policy.loc[policy.Status == 'Enacted',:].copy()
policyEnacted.drop(['Status','LocationDesc'],axis=1,inplace=True)
policyEnacted.sort_values(['Year','LocationAbbr','HealthTopic'],inplace=True)
policyEnacted.reset_index(drop=True,inplace=True)
policyEnacted.set_index(['Year','LocationAbbr','HealthTopic'],inplace=True)
policyEnactedgb = policyEnacted.groupby(['Year','LocationAbbr','HealthTopic'])
policyEnacted['NumPolicies']= policyEnactedgb.PolicyTopic.count().copy()
policyEnacted.reset_index(inplace=True)

#create cdcdata
cdcdata = behavior.merge(policyEnacted,how='left',left_on=['Year','LocationAbbr','Topic'],right_on=['Year','LocationAbbr','HealthTopic'])
cdcdata['NumPolicies'].replace(to_replace=np.nan,value='N/A',inplace=True)
cdcdata.drop(['HealthTopic','PolicyTopic','Setting'],axis=1,inplace=True)


# In[ ]:


app = Dash(__name__)

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
        marks={str(year):str(year) for year in behavior['Year'].unique()},
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

