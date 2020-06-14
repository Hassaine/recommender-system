import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
from collections import defaultdict
import dash_daq as daq
import dash_table
import pandas as pd
from app import app,df_movies,evaluator,df_rating
import os,sys,inspect
import pickle
from imdb import IMDb
ia = IMDb()
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


df_links = pd.read_csv('../dataSource/moviesLen/newLinks.csv')

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
   dcc.Loading(html.Div(id="movies-output"), type="default"),
   html.Hr(),
  dbc.Row(html.Div(
      html.Div(
      dbc.Button("show Poster", color="primary", className="mr-1",id="show-poster"),className="col-sm-10"),
    className="form-group row")),
   html.Div(id="movies-poster")
])




@app.callback(
   [Output(component_id='movies-rated', component_property='children'),
   Output(component_id='movies-output', component_property='children'),
  # Output(component_id='movies-poster', component_property='children')
   ],
   [Input(component_id='submit-rec', component_property='n_clicks')],
   [         State('algorithm-selector-fc', 'value'),
               State('userId', 'value'),
               State('context-selector', 'value'),
               ])

def recommandeMovies(n_clicks,algo,userId,context):

 
  if(n_clicks==None):
    return ["No movies","No recommandation"]#,"No recommandation"]
  
  
  movies= recommande(userId=userId,algorithm=algo)
  df_recommended_movies = pd.DataFrame(movies, columns =['movieId', 'estimatedRating'])
  
  #tmp_links=df_recommended_movies.set_index('movieId').join(df_links.set_index('movieId'))


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
    ),
    #html.H1('hello world')

    #  dbc.Row([dbc.Col(dbc.Card(
    # dbc.CardBody(
    #     [
            
    #         #html.H6("imdb id={}".format(tmp_links.loc[movie[0],'imdbId']), className="card-subtitle"),

    #        #dbc.CardImg(src=tmp_links.loc[movie[0],'poster_url'], top=True),
    #        dbc.CardImg(src=ia.get_movie(tmp_links.loc[movie[0],'imdbId'])['full-size cover url'], top=True),
    #        dbc.CardImgOverlay([ 
    #          html.H3(dbc.Badge("8.1 imdb",color="warning"), className="card-title"),
    #          dbc.CardLink("Card link", href="#"),
    #         dbc.CardLink("External link", href="https://google.com"),
    #         ])
           
    #     ]
    # ),
    # style={"width": "18rem"},className="text-white"
    #   )) for movie in movies[:2]])
    
    ]
  


@app.callback(
   Output(component_id='movies-poster', component_property='children'),
   [Input(component_id='show-poster', component_property='n_clicks')],
   [ State('userId', 'value'), State('algorithm-selector-fc', 'value') ])

def showPoster(n_clicks,userId,algo):
  if(n_clicks==None):
      return ["No movies"]
  
  #print(userId)
  movies= recommande(userId=userId,algorithm=algo)

  
  df_recommended_movies = pd.DataFrame(movies, columns =['movieId', 'estimatedRating'])
  #print(movies)

  
  tmp_links=df_recommended_movies.set_index('movieId').join(df_links.set_index('movieId'))
  # dictMovies=defaultdict(dict)
  # for movie in movies:
  #   movieMatrix=ia.get_movie(tmp_links.loc[movie[0],'imdbId'])
  #   dictMovies[movie[0]]={'full-size cover url':movieMatrix['full-size cover url'],"rating":movieMatrix['rating']}
    
  return dbc.Row([dbc.Col(dbc.Card(
    dbc.CardBody(
        [
            
            #html.H6("imdb id={}".format(tmp_links.loc[movie[0],'imdbId']), className="card-subtitle"),

           #dbc.CardImg(src=tmp_links.loc[movie[0],'poster_url'], top=True),
           dbc.CardImg(src=tmp_links.loc[movie[0],'img_url'], top=True),
           dbc.CardImgOverlay([ 
             html.H3(dbc.Badge("{} imdb".format(tmp_links.loc[movie[0],'imdb_rating']),color="warning"), className="card-title")
            ])
           
        ]
    ),
    style={"width": "18rem"},className="text-white"
      )) for movie in movies])

