import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
import pandas as pd
from app import app,df_movies,df_rating
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff

#df_rating = pd.read_csv('../dataSource/moviesLen/ratings.csv')

df_ra = pd.read_csv('../output/dataMining/rating_association_rule_small.csv')
df_ra.drop(["antecedent support",'consequent support'],axis=1,inplace=True)
df_new_rating = pd.read_csv('../output/recSystem/ratings_ras_big.csv')


tmp_df_2=df_new_rating.head(2000).pivot(index='movieId' , columns='userId', values='rating').fillna(' ').reset_index()
tmp_df=df_rating.head(2000).pivot(index='movieId' , columns='userId', values='rating').fillna(' ').reset_index()

dfg=df_rating.groupby('rating').count().reset_index()
dfg=dfg.rename(columns={"movieId": "count"})

# plot structure
fig = px.bar(dfg,
             x='rating',
             y='count',
             
             #color='Items',
             barmode='stack')

fig.layout.paper_bgcolor = '#fafafa'

layout = html.Div(children=[

    dbc.Row(html.H1('Home Page',className="mx-auto mt-20")),
    html.Hr(),
     dbc.Row(html.H2('MovieLen 100k Rating Matrix'.format(df_movies.shape[0]),className="mx-auto mt-20")),

    html.Div(dash_table.DataTable(

            id="table-rating",
            data=tmp_df.to_dict('records'),
            columns=[{'name': str(i), 'id': str(i)} for i in tmp_df.columns],
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
        ))
        ,
        html.Hr(),
         dbc.Row(html.H2('Movies table and rating count plot',className="mx-auto mt-20")),
         html.Hr(),

             
         dbc.Row([
             dbc.Col(dash_table.DataTable(

            id="table-movies",
            data=df_movies.to_dict('records'),
            columns=[{'name': str(i), 'id': str(i)} for i in df_movies.columns],
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
        ),width=4),
             dbc.Col(
                 dcc.Graph(figure=fig)

             )
         ]),

             html.Hr(),
               dbc.Row(html.H2('optimized association rules extracted from movieLens 100k',className="mx-auto mt-20")),
             dbc.Row(dash_table.DataTable(

            id="table-ra",
            data=df_ra.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_ra.columns],
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
        )),
        html.Hr(),
           dbc.Row(html.H2('The new MovieLen 100k Rating Matrix',className="mx-auto mt-20")),
            dbc.Row(dash_table.DataTable(

            id="table-rating-2",
            data=tmp_df_2.to_dict('records'),
            columns=[{'name': str(i), 'id': str(i)} for i in tmp_df_2.columns],
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
        ))


     
     
     ])