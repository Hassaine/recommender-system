import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
globalActiveSideBar="active"
from app import app
from pages import fp_growth_dash,BPSO_dash,dm_execution


sideBar = html.Nav(
            id='sidebar',
            children=[
                html.Div(
                    children=html.H3('REC-OPTI'),
                    className='sidebar-header'
                ),
                html.Ul(
                    className='list-unstyled components',
                    

                    children=[
                        html.P('Dashboard'),
                        html.Li(
                            className='active',
                            children=[
                                html.A(
                                    'Execution',
                                    href='#homeSubmenu2',
                                    className = 'dropdown-toggle',
                                    **{'aria-expanded': 'false', 'data-toggle': 'collapse'}
                                ),
                                html.Ul(
                                    className='collapse list-unstyled',
                                    id='homeSubmenu2',
                                    children=[
                                        html.Li(
                                            dbc.NavLink(
                                                'data mining',
                                                href="/execution/data-mining", 
                                            )
                                        ),
                                        html.Li(
                                            dbc.NavLink(
                                                'recommandation',
                                                href="/execution/recommandation", 
                                            )
                                        )                                  
                                    ]
                                )
                            ]
                        ),
                        html.Li(
                            className='active',
                            children=[
                                html.A(
                                    'Performance',
                                    href='#homeSubmenu',
                                    className = 'dropdown-toggle',
                                    **{'aria-expanded': 'false', 'data-toggle': 'collapse'}
                                ),
                                html.Ul(
                                    className='collapse list-unstyled',
                                    id='homeSubmenu',
                                    children=[
                                        html.Li(
                                            dbc.NavLink(
                                                'FP-growth',
                                                href="/performance/fp-growth", id="page-1-link"
                                            )
                                        ),
                                        html.Li(
                                            dbc.NavLink(
                                                'BPSO',
                                                href="/performance/bpso", id="page-2-link"
                                            )
                                        ),
                                        html.Li(
                                            dbc.NavLink(
                                                'comparison',
                                                href="/performance/comparison", id="page-3-link"
                                            )
                                        ),
                                    ]
                                )
                            ]
                        ),
                        html.Li(
                            children=[
                                html.A(
                                    'About',
                                    href='#'
                                )
                            ]
                        ),
                      
                        html.Ul(
                            [html.Li(children=[html.A("download results",href="#",className="download")])],
                            className="list-unstyled CTAs"
                            )
                    ]
                )
            ]


        )

navBar=html.Div(
             children=[
                 html.Nav(
                     className = 'navbar navbar-expand-lg navbar-light bg-light',
                     children=[
                         html.Div(
                             id="buttonNavcontainer",
                             className = 'container-fluid',
                             children = [
                                 html.Button(
                                     type = 'button',
                                     id = 'sidebarCollapse',
                                     className = 'btn btn-info',
                                     children = [
                                         html.I(className='fas fa-align-left'),

                                     ]
                                 )
                             ]
                         )
                     ]
                 )
             ]
         )
app.layout = html.Div([dcc.Location(id="url"), sideBar,html.Div([navBar,html.Div([],id="content-page")],id='content',style={"font-size":"12px"})],className="wrapper")

@app.callback(
    [Output('sidebar', 'className'),Output('content', 'className')],
    [Input('sidebarCollapse', 'n_clicks')])
def clicks(n_clicks):
    global globalActiveSideBar
    if(globalActiveSideBar==""):
        globalActiveSideBar = "active"
        return ['active','active']
    else:
        globalActiveSideBar=""
        return ['','']


@app.callback(Output("content-page", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/performance/fp-growth"]:
        return  fp_growth_dash.layout
    elif pathname == "/performance/bpso":
        return BPSO_dash.layout
    elif pathname == "/performance/comparison":
        return html.P("Oh cool, this is page 3!")
    elif pathname == "/about":
        return html.H1("About")
    elif pathname == "/execution/data-mining":
        return dm_execution.layout
    elif pathname == "/execution/recommandation":
        return html.H1('recommandation')
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)