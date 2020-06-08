import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc

import dash_daq as daq
import dash_table
import pandas as pd
from app import app,df_movies,evaluator,df_rating
import os,sys,inspect
import pickle

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#print(currentdir)
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
#os.chdir(currentdir)
# sys.path.append(parentdir)
sys.path.append(parentdir+"\\algorithms")
#print(sys.path)

from HybridAlgorithm import HybridAlgorithm
from RBMAlgorithm import RBMAlgorithm

def recommande(userId=85,algorithm='FC',n=10):
  recommendations=[]
  if algorithm=='FC':
    model = pickle.load(open('../savedModels/finalized_svdpp.sav', 'rb'))
  elif algorithm=='FC-CF':
    model = pickle.load(open('../savedModels/finalized_hybrid_FC_CF.sav', 'rb'))
  elif algorithm=='DL-FC-RAs':
    model = pickle.load(open('../savedModels/finalized_rbm.sav', 'rb'))
  else:
    model = pickle.load(open('../savedModels/finalized_svdpp_ra.sav', 'rb'))

  testSet = evaluator.dataset.GetAntiTestSetForUser(userId)
  predictions = model.test(testSet)
  for userID, movieID, actualRating, estimatedRating, _ in predictions:
    intMovieID = int(movieID)
    recommendations.append((intMovieID, estimatedRating))
  recommendations.sort(key=lambda x: x[1], reverse=True)

  return recommendations[:n]


#print(recommande())

layout=html.Div(children=[
     dbc.Row(html.H1('Recommandation',className="mx-auto mt-20")),
    html.Hr(),
      html.Div ([html.Label(htmlFor ="staticEmail",className="col-sm-2 col-form-label", children="User Id"),
    html.Div( dcc.Input(type="text" , className="form-control",  id="userId" ,value="1"),
     className="col-sm-10"
     
      )],className="form-group row"
    ),
     html.Div ([html.Label(htmlFor ="algorithm-selector-fc",className="col-sm-2 col-form-label", children="Algorithm to Use "),
     html.Div(dcc.Dropdown(
                                        id='algorithm-selector-fc',
                                        options=[{'label': i, 'value': i} for i in ['FC','FC-RAs','FC-CF','DL-FC-RAs']],
                                        value="FC",
                                        searchable=False,
                                        clearable=False,
                                        className="form-control"
                                        
                                    ) ,className="col-sm-10")],className="form-group row"
    ),html.Div ([html.Label(htmlFor ="context-selector",className="col-sm-2 col-form-label", children="Context to Use "),
     html.Div(dcc.Dropdown(
                                        id='context-selector',
                                        options=[{'label': i, 'value': i} for i in ['Big Data','Classic']],
                                        value="Classic",
                                        searchable=False,
                                        clearable=False,
                                        className="form-control"
                                        
                                    ) ,className="col-sm-10")],className="form-group row"
    ),
    
    dbc.Row(html.Div(
      html.Div(
      dbc.Button("submit", color="primary", className="mr-1",id="submit-rec"),className="col-sm-10"),
    className="form-group row")),
     html.Hr(),
     dbc.Row(html.H2('Movies rated by the user',className="mx-auto mt-20")),
       dcc.Loading(html.Div(id="movies-rated"),
            type="default"),
      html.Hr(),
   dbc.Row(html.H2('Movies recommended for the user',className="mx-auto mt-20")),
       dcc.Loading(   html.Div(id="movies-output"), type="default")
])




@app.callback(
   [Output(component_id='movies-rated', component_property='children'),
   Output(component_id='movies-output', component_property='children')],
   [Input(component_id='submit-rec', component_property='n_clicks')],
   [         State('algorithm-selector-fc', 'value'),
               State('userId', 'value'),
               State('context-selector', 'value'),
               ])

def recommandeMovies(n_clicks,algo,userId,context):

 
  if(n_clicks==None):
    return ["No movies","No recommandation"]
  
  
  movies= recommande(userId=userId,algorithm=algo)
  df_recommended_movies = pd.DataFrame(movies, columns =['movieId', 'estimatedRating'])
  #df_recommended_movies=df_recommended_movies.join(df_movies,on="movieId")
  df_recommended_movies=df_recommended_movies.set_index('movieId').join(df_movies.set_index('movieId'))


  df_rated=df_movies[df_movies.movieId.isin(df_rating[df_rating.userId==int(userId)]['movieId'].values)]
  return[
    dash_table.DataTable(
        id="datatable-movies-rated",
        columns=[{"name": i, "id": i} for i in df_rated.columns],
        data=df_rated.to_dict("records"),
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
         "backgroundColor": "rgb(25, 161, 185)",
        "color": "white",
        "textAlign": "center",
        'fontWeight': 'bold'
        }
    ),
     dash_table.DataTable(
        id="datatable-movies-result",
        columns=[{"name": i, "id": i} for i in df_recommended_movies.columns],
        data=df_recommended_movies.to_dict("records"),
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
         "backgroundColor": "rgb(25, 161, 185)",
        "color": "white",
        "textAlign": "center",
        'fontWeight': 'bold'
        }
    )
    
    ]
  
#     if visibility_state == 'BPSO':
#         return [{'display': 'none'},{'display': 'block'}]
#     if visibility_state == 'fp-Growth' or visibility_state =="parallel-fp-growth":
#         return [{'display': 'block'},{'display': 'none'}]
