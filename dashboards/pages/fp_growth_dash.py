import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from app import app
df_fp = pd.read_csv('../output/dataMining/FP_Growth_ar.csv')
df_perf = pd.read_csv('../output/dataMining/FP_Growth_performance.csv')
# def generate_table(dataframe, max_rows=10):
#     return dbc.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ],
#         bordered=True,
#         hover=True,
#     responsive=True,
#     striped=True,
#     size="md",id="dtBasicExample")

fig2 = px.scatter(df_perf, x="support", y="time", color="confidence",color_continuous_scale=px.colors.sequential.Viridis,log_x=True, render_mode="webgl")
fig2.layout.paper_bgcolor = '#fafafa'

layout=html.Div(children=[
        dbc.Row(html.H1('FP-growth',style={
            'text-align' : 'center'

        },className="mx-auto mt-20"))
        ,
    html.Hr(),

    dbc.Row(html.H2('rule generated by FP-growth',style={
            'text-align' : 'center'

        },className="mx-auto mt-20")),
         html.Hr(),
        dbc.Row([
            dbc.Col(dbc.Card(
              [
                  
                   dbc.CardBody(
                    [
                        html.H4(str(round(df_fp['confidence'].max(),2)), className="card-title"),
                        html.P("best confidence", className="card-text"),
                    ]
                ),
                
                    ],color="info", outline=True
            
            )),
            dbc.Col(dbc.Card(
              [
                  
                   dbc.CardBody(
                    [
                        html.H4(str(round(df_fp['lift'].max(),2)), className="card-title"),
                        html.P("best lift", className="card-text"),
                    ]
                ),
                
                    ],color="info", outline=True
            
            )),
            dbc.Col(dbc.Card(
              [
                  
                   dbc.CardBody(
                    [
                        html.H4(str(round(df_fp['leverage'].max(),2)), className="card-title"),
                        html.P("best leverage", className="card-text"),
                    ]
                ),
                
                    ],color="info", outline=True
            
            )),
            dbc.Col(dbc.Card(
              [
                  
                   dbc.CardBody(
                    [
                        html.H4(str(round(df_fp['conviction'].max(),2)), className="card-title"),
                        html.P("best conviction", className="card-text"),
                    ]
                ),
                
                    ],color="info", outline=True
            
            ))
            ]),

            html.Hr(),

        html.Div(dash_table.DataTable(
        id='datatable-paging',
        columns=[{"name": i, "id": i} for i in df_fp.columns],
        data=df_fp.to_dict("records"),
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

    dbc.Row(html.H2('line chart of excution time by confidence and support', style={
        'text-align': 'center'

    }, className="mx-auto my-20"))
    ,
    dbc.Row([dbc.Col(dbc.Card([
        dbc.CardHeader(html.H4("Controleur"))
        ,
        dbc.CardBody([
        dbc.FormGroup(
            [
                dbc.Label("transaction number"),
                dcc.Dropdown(
                    id='transaction',
                    options=[{'label': i, 'value': i} for i in list(df_perf['transaction_number'].unique())],
                    value="980",
                    searchable=False,
                    clearable=False
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in ["confidence","support"]
                    ],
                    value="support",
                    searchable=False,
                    clearable=False

                ),
            ]
        )])]),width=3),
        dbc.Col(dcc.Graph(id="line-graph"),width=9)],className="align-items-center"),
        html.Hr(),
          dbc.Row(html.H2("Multi-Varibales scatter plot",className="mx-auto mt-20")),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig2)))
      ])


@app.callback(
    Output('line-graph', 'figure'),
    [Input('transaction', 'value'),
     Input('x-variable', 'value')])
def update_graph(transaction_number, x_variable):

    fig1 = px.line(x=df_perf[df_perf.transaction_number == int(transaction_number)].groupby(x_variable)[['time']].mean().index.tolist(),
                   y=df_perf[df_perf.transaction_number == int(transaction_number)].groupby(x_variable)[['time']].mean().values)
    fig1.update_yaxes(title_text='avrage execution Time(s)')
    fig1.update_xaxes(title_text=x_variable)
    fig1.update_layout(xaxis_type="log")
    fig1.layout.paper_bgcolor = '#fafafa'
    return fig1


#@app.callback(
#    Output("fp_tab", "children"),
#    [Input("input_text", "value")]
#)
#def cb_render(vals):
#   return generate_table(df_fp,max_rows=int(vals))


