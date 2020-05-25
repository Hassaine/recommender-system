import dash_core_components as dcc
import dash_html_components as html
# from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
# import dash_table
# from app import app
# import plotly.graph_objects as go
import plotly.express as px
# import numpy as np
# import plotly.figure_factory as ff
result = pd.read_csv('../output/dataMining/results_compare.csv')



fig = px.line(result, x="transaction_number", y="time", color='algo')
fig.update_layout(xaxis_type="log")
fig.layout.paper_bgcolor = '#fafafa'  


layout=html.Div(children=[
   dbc.Row(html.H1('comparison',className="mx-auto mt-20")),
    html.Hr(),
    dbc.Row(html.H4('time execution comparison graphe for the bpso and fp-growth algorithms',className="mx-auto mt-20")),
    dbc.Row(dbc.Col(dcc.Graph(figure=fig)))
    
])

