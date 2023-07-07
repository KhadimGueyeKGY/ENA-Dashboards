# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 16:52:51 2023

@author: khadim
"""

'''
favicon.ico pour l'icone 
add comment lines

genaral stattistcs 11, 12 , 116
CohortDashbord 31 and 32
main linge 95
'''


import dash
#from flask
from dash import Dash, dcc, html, Input, Output , dash_table, State, MATCH, dash_table
import dash_bootstrap_components as dbc
#import plotly.express as px
#import geopandas as gpd
import pandas as pd
from datetime import datetime
from ENA_Cohort_Dashboard.recoDID_COVID_19_dashboard.modules.header import Header
from ENA_Cohort_Dashboard.recoDID_COVID_19_dashboard.modules.body_contain import Contain
from ENA_Cohort_Dashboard.recoDID_COVID_19_dashboard.modules.general_statistics import General_Statistics
from ENA_Cohort_Dashboard.recoDID_COVID_19_dashboard.modules.CohortDashboard import CohortDashboard
import json
from ENA_Cohort_Dashboard.recoDID_COVID_19_dashboard.modules.geo import geoM
from django_plotly_dash import DjangoDash


##################  https://www.ebi.ac.uk/biosamples/download?count=100000&format=json (to download the biosamples metadata)
df = pd.read_excel('ENA_Cohort_Dashboard/recoDID_COVID_19_dashboard/assets/data/ReCoDID_EMCpilot_sampleIDs.xlsx', header=3, index_col= 'top-level accession', usecols=[col for col in range(22, 30) if col != 23])
df = df.dropna(axis=0, how='all')

with open('ENA_Cohort_Dashboard/recoDID_COVID_19_dashboard/assets/data/samples.json', 'r') as f:
    json_data = f.read()
data = json.loads(json_data)

lt_id = []
for i in range(len(data)):
            lt_id.append(data[i]['accession'])
#List_init= html.Div([html.P(html.A(lt_id[i],href='https://www.ebi.ac.uk/biosamples/samples/'+str(lt_id[i]) )) for i in range(len(lt_id))],style={'margin-left':'40px','font-size':'20px'})

# Top-level accession (150 samples)
lt_id = [acc for acc in df.index]

table_List_init = html.Div([ dash_table.DataTable(
    id='table',
    columns=[{'name': 'Accessions', 'id': 'Accession', 'type': 'text', 'presentation': 'markdown'}],
    data=[{'Accession': f"[{id}](https://www.ebi.ac.uk/biosamples/samples/{id})"} for id in lt_id],
    editable=False,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    row_selectable="multi",
    row_deletable=False,
    selected_rows=[],
    page_action="native",
    page_current=0,
    page_size=110,
    style_cell={
                'textAlign': 'center',
                'backgroundColor': '#D0D0CE'
            }
        )
], style={
     'textAlign': 'center',
    'font-size': '20px'
})

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    #'static/main.css'
]
app = DjangoDash('ena_cohort_dashboard', external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True,
                )

app.title = 'Cohort Dashboard'

tabs = dbc.Tabs(
    [
        dbc.Tab(label="Cohort Dashboard",tab_id = 'tab_0',style={'font-size': '20px'}),
        #dbc.Tab(label="Over View",tab_id = 'tab_1'),
        #dbc.Tab( label="General Statistics",tab_id = 'tab_2'),
        dbc.Tab( label="Map",tab_id = 'tab_3',style={'font-size': '20px'})
    ],
    id="tabs",
    active_tab="tab_0",
    style={'font-size': '20px'}
)

sarch = dbc.Input(id="search", placeholder="Search...", type="text",style={'font-size':'20px','text-align': 'center'})
header = Header.header()

app.layout = html.Div([
    #header,
    dcc.Location(id='url', refresh=False),
    html.Hr(),
    tabs,
    html.Div(id = 'tab_content'),
    html.Br(),
    html.Br(),
    html.Br(), 
])

def list_ID(search):
    id = []
    if search : #=='' or search =='Search...':
        for i in range(len(data)):
            if str(data[i]['accession']).upper().find(str(search).upper()) != -1 :
                id.append(data[i]['accession'])
    else:
        for i in range(len(data)):
            id.append(data[i]['accession'])
    List= html.Div([html.P(html.A(id[i],href='https://www.ebi.ac.uk/biosamples/samples/'+str(id[i]))) for i in range(len(id))],style={'text-align': 'center','font-size':'20px'})
    return List, len(id)

#---------------------------contain 
def contain():
    contain = html.Div([
            html.Div([Contain.contain(item) 
                    ,
                    html.Div(dbc.Button("More Info >>>" , color="primary"),style={'margin-bottom': '7px','margin-left': '85%'}),
                    html.Div([
                    #html.H1('Counter App'),
                    #html.Button('more info',id={'type': 'more-info-button', 'index': index}),
                    #html.Div(id={'type': 'counter', 'index': index}, children='0')
                    ]),
                    
                ], style={'margin-left':'7px','margin-top': '7px','margin-right':'7px','border-style': 'solid','border-width': '1px','border-radius': '10px'})
          for  item in data ])
    return contain



#--------------- body cohort

def body_cohort():
    res = html.Div([
        CohortDashboard.cohortStudy(data,lt_id),
        html.Div([
            #html.Div([dbc.Input(id="search_2", placeholder="SAMEXXXX...", type="text",style={'margin': 'auto','width':'50%','font-size':'30px','text-align': 'center','align':'center','justify':'center'}),
            #          ] ,style = {'width':'100%','text-align': 'center'}),
            #html.Br(),
                dcc.Tabs(id='bc_tabs', value='bc_tab_1', children=[
                dcc.Tab(label='Heatmap', value='bc_tab_1',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
                dcc.Tab(label='Scatter Plot', value='bc_tab_2',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
                dcc.Tab(label='Relationships', value='bc_tab_3',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
            ]),
            html.Div(id='bc_tabs_output')
        ], style={'margin-left':'100px','margin-top': '50px','margin-right':'100px','text-align':'center'})
    ])
    return res



@app.callback(
        Output('bc_tabs_output', 'children'),
        Input('bc_tabs', 'value'), 
        #Input("search_2", "value"),
        )
def render_content(tab): # search_2
            '''
            id = []
            index = list(df.index)
            if search_2 : #== is not '' or search =='Search...':
                for i in range(len(index)):
                    if str(index[i]).upper().find(str(search_2).upper()) != -1 :
                        id.append(index[i])
                filtered_df = df[df.index.isin(id)]
            else:'''
            filtered_df = df
            fig4 = General_Statistics.heatmap(filtered_df)
            fig5 = General_Statistics.scatter_heatmap(filtered_df)
            if tab == 'bc_tab_1':
                    return html.Div([
                                html.H3('Heatmap',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
                                html.Div('data types = [ 1. antibody profile\n2. viral Seq\t3. B-cell\t4. T-cell\t5. Clin-Epi ]',style = {'font-size': '15px','text-align':'center','font-style': 'italic'}),
                                dcc.Graph(figure=fig4), 
                        ],style={'width': '100%', 'text-align': 'center'})
                
            elif tab == 'bc_tab_2':
                    return html.Div([
                                html.H3('Scatter Plot',style = {'font-weight': 'bold','font-size': '20px','text-align':'center'}),
                                html.Div('data types = [ 1. antibody profile\n2. viral Seq\t3. B-cell\t4. T-cell\t5. Clin-Epi ]',style = {'font-size': '15px','text-align':'center','font-style': 'italic'}),
                                dcc.Graph(figure=fig5), 
                        ],style={'width': '100%', 'text-align': 'center'})
            elif tab == 'bc_tab_3':
                 return html.Div([
                      html.H3('Relationships',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
                      General_Statistics.Relationships(data,lt_id)
                 ])
            
#-----------------------------------------------------------map

def map ():
    code_3 = pd.read_csv('assets/Officially_assigned_code_elements.csv',sep= '\t')
    country = []
    for item in data:
        if ('geographic location (country and/or sea)' in item['characteristics']) and ('text' in item['characteristics']['geographic location (country and/or sea)'][0]):
            country.append(item['characteristics']['geographic location (country and/or sea)'][0]['text'])
        else : 
            country.append('')
    code = []
    for i in country :
        if i != '':
             for j in range(len(code_3.country)) : 
                  if str(code_3.country[j]).find(i) != -1 :
                       code.append(code_3.code[j])
    df_map = {'code':[],'size':[]}
    code_uniq = list(set(code))
    for i in code_uniq :
         df_map['code'].append(i)
         df_map['size'].append(code.count(i))
    df_map = pd.DataFrame(df_map)
    fig = geoM.Choropleth_map(df_map)
    res = html.Div([
            html.H3('Geographical Distribution of Biosamples from the Multidisciplinary COVID-19 Study',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
            html.H2('(Top-level BioSamples)',style = {'font-size': '15px','text-align':'center'}),
            dcc.Graph(figure=fig), 
          ])
     
    return res

#------------------------------------------------------------main
@app.callback(Output("tab_content", "children"),
              Output('url', 'pathname'),
              #Output("list_id", "children"),
              #Output("num_bio", "children"),
              [Input("tabs", "active_tab"),
               Input('url', 'pathname')
               #Input("search", "value"),
               ]
              )
def switch_tab(at,pathname) :#,search):
    current_dateTime = datetime.now()
    print('\033[92m'+'[ '+str(current_dateTime)+' ] Action ...')
    print('\033[0m')
    #lt,len_id = list_ID(search)
    #if at == "tab_1":
    #    return contain() ,lt,'Number of Biosamples: '+str(len_id)
    #elif at == "tab_2":
    #    return general_statistics(data),lt,'Number of Biosamples: '+str(len_id)
    if at == 'tab_3':
        return map() ,'/Cohort-Dashboard' # ,lt,'Number of Biosamples: '+str(len_id)
    elif at == 'tab_0':
        return body_cohort() , '/Cohort-Dashboard'  # ,lt,'Number of Biosamples: '+str(len_id)


'''
@app.callback(Output('url', 'pathname'),
              [Input('url', 'pathname')])
def update_url(pathname):
    return '/Cohort-Dashboard'



if __name__=='__main__':
    app.run_server(host='0.0.0.0', debug=True, use_reloader=False, port=8050) # use_reloader=False
    #app.run_server(host="0.0.0.0", port=8050)

'''








