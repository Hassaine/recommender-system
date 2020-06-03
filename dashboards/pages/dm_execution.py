import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime
import os,json
import pandas as pd
import dash_table
from app import app
import os,sys,inspect
import base64
import io

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
#os.chdir(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir+"\\dataMining")

df = pd.read_csv('../dataSource/market/marketBool.csv')
#print(sys.path)

from dataMining.pso import BPSO
from dataMining.fpGrowth import Fp_Growth


layout = html.Div(children=[

    dbc.Row(html.H1('Execute Rule Association Mining',className="mx-auto mt-20")),
    html.Hr(),
     dbc.Row(

     dbc.Col(
         dbc.Card(
             dbc.CardBody([
                   dbc.Row(dbc.Col(dcc.Upload([
                            'Drag and Drop or ',
                            html.A('Select a dataset')
                        ], style={
                            'width': '100%',
                            'height': '120px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                        },multiple=True,id="upload"))),
                        dbc.Row(dbc.Col(html.Hr())),
                        dbc.Row(dbc.Col([dbc.Label("algorithm-selector",className="mx-auto mt-40"),
                                    dcc.Dropdown(
                                        id='algorithm-selector',
                                        options=[{'label': i, 'value': i} for i in ['fp-Growth','BPSO','parallel-fp-growth']],
                                        value="fp-Growth",
                                        searchable=False,
                                        clearable=False
                                    ),]),className="my-auto"),
                        dbc.Row([dbc.Col(dbc.Label('mesure :')),
                                 dbc.Col( dcc.Dropdown(
                                        id='mesure-selector',
                                        options=[{'label': i, 'value': i} for i in ['confidence','lift','leverage','conviction']],
                                        value="confidence",
                                        searchable=False,
                                        clearable=False
                                    ))]),
                        dbc.Row([
 
                            dbc.Col( dbc.Input(
                                id="input_max_iter",
                                type='text',
                                placeholder="number of iteration",
                            )),
                            dbc.Col(
                               
                                dbc.Input(
                                id="input_particule_number",
                                type='text',
                                placeholder="number of particule",
                            )
                            ),
                            dbc.Col( dbc.Input(
                                id="input_m",
                                type='text',
                                placeholder="number association rule",
                            ))
                            ]
                            ,id="BPSO-params"
                        ),
                            dbc.Row([
                            dbc.Col(
                                dbc.Input(
                                id="input_support",
                                type='text',
                                placeholder="support",
                                
                            )
                            ),
                            dbc.Col( dbc.Input(
                                id="input_confidence",
                                type='text',
                                placeholder="confidence",
                                
                            ))],id="fp-growth-params"),
                            dbc.Row(dbc.Col(html.Hr())),
                             ]
                    )
                                
                 ,body=True),
                width=12)
         )
       ,
        html.Hr()
        
        ,dcc.Loading(html.Div(id="dataframe_output"))
      
       
      
   
    ])








@app.callback(
   [Output(component_id='fp-growth-params', component_property='style'),Output(component_id='BPSO-params', component_property='style')],
   [Input(component_id='algorithm-selector', component_property='value')])

def show_hide_element(visibility_state):
    if visibility_state == 'BPSO':
        return [{'display': 'none'},{'display': 'block'}]
    if visibility_state == 'fp-Growth' or visibility_state =="parallel-fp-growth":
        return [{'display': 'block'},{'display': 'none'}]







def parse_contents(contents, filename, date,support,confidence,particule_number,m,max_iter,algo,mesure):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'txt' in filename:
            file=open('..\\dataSource\\{}'.format(filename),'w')
            file.write(decoded.decode('utf-8'))
            file.close()
            
            if(algo=="parallel-fp-growth"):
                curentDir =os.getcwd()
                os.chdir('../largeScale/parallelFp_growth')

                dataConfig={'support':float(support),'confidence':float(confidence),'input':"..\\..\\dataSource\\{}".format(filename),
                                'output' :"..\\..\\output\\dataMining\\parallel-fp-growth_ar_test.csv"}
                with open('configuration.json', 'w') as outfile: 
                    json.dump(dataConfig, outfile)  
                os.system('%SPARK_HOME%/bin/pyspark < fp_growth.py')
                os.chdir(curentDir)
                df = pd.read_csv('../output/dataMining/{}_ar_test.csv'.format(algo))
            
            #

            

        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            data = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            if(algo=="fp-Growth"):
                print("confidence : {}".format(float(confidence)))
                df_tmp = Fp_Growth.fp_growth(data,confidence=float(confidence),support=float(support))
            elif(algo=="BPSO"):
                df_tmp = BPSO.association_rule_mining(df=data,particule_count=int(particule_number),max_iter=int(max_iter),mesure=mesure, m=int(m))
           

            df_tmp.to_csv('../output/dataMining/{}_ar_test.csv'.format(algo),index=False)
            df = pd.read_csv('../output/dataMining/{}_ar_test.csv'.format(algo))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),

       dbc.Row(dbc.Col(dash_table.DataTable(
            id="table-exec",
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            page_action="native",
            page_current= 0,
            page_size= 10,
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
                ],
            style_header={
                     'backgroundColor': 'rgb(230, 230, 230)',
                     'fontWeight': 'bold'
               }
        ))),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('dataframe_output', 'children'),
              [Input('upload', 'contents')],
              [State('upload', 'filename'),
               State('upload', 'last_modified'),
               State('input_support', 'value'),
               State('input_confidence', 'value'),
               State('input_particule_number', 'value'),
               State('input_m', 'value'),
               State('input_max_iter', 'value'),
               State('algorithm-selector', 'value'),
               State('mesure-selector', 'value')
               ])
def update_output(list_of_contents, list_of_names, list_of_dates,support,confidence,particule_number,m,max_iter,algo,mesure):
    
    if list_of_contents is not None:
        #print(list_of_contents)
        children = [
            parse_contents(c, n, d,support,confidence,particule_number,m,max_iter,algo,mesure) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children[0]
    else:
        return "None"



# @app.callback(Output('result_table', 'children'),
#               [Input('submit-button-state', 'n_clicks')],
#               [State('input_support', 'value'),
#                State('input_confidence', 'value'),
#                State('input_m', 'value'),
#                State('input_particule_number', 'value'),
#                State('input_max_iter', 'value'),
#                State('algorithm-selector', 'value')
#                ]
               
#                )
# def update_output(n_clicks, support, confidence,m,particule_number,max_iter,algorithm):
#     if(algorithm=="BPSO"):
#         return "BPSO"
#     if(algorithm=="fp-Growth"):
     
#         result=Fp_Growth.fp_growth(df,confidence=float(confidence),support=float(support))
#         if(result.empty):
#             return "None" 
#         data = result .to_dict("rows")
#         cols = [{"name": i, "id": i} for i in result.columns]

#         child = html.Div([
#                 dash_table.DataTable(
#                                 id='table',
#                                 data=data, 
#                                 columns=cols,
#                                 style_cell={'width': '50px',
#                                             'height': '30px',
#                                             'textAlign': 'left'}
#                                       )
#                            ])
#         return child
        # result.reset_index(level=0, inplace=True)
        # result.rename(columns={'index':'col_name'}, inplace=True)
        # child=html.Div(dash_table.DataTable(
        # id='datatable-paging',
        # columns=[{"name": i, "id": i} for i in result.columns],
        # data=result.to_dict("records"),
        # editable=False,
        # filter_action="native",
        # sort_action="native",
        # sort_mode="multi",
        # page_action="native",
        # page_current= 0,
        # page_size= 10,
        # style_data_conditional=[
        # {
        #     'if': {'row_index': 'odd'},
        #     'backgroundColor': 'rgb(248, 248, 248)'
        # }
        # ],
        # style_header={
        # 'backgroundColor': 'rgb(230, 230, 230)',
        # 'fontWeight': 'bold'
        # }
        # ))
        # return child
        
    