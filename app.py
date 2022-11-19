# Acevedo Jauergui Jose Alberto
# Mechato Lara Salvador Leonardo
# Rojas Ruiz Cristopher Edison 




#import plotly.express as px
from whitenoise import WhiteNoise
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static')

#app._favicon = "assets/favicon.ico"
app.title = "Sensores IA"

# Data - CSV
csv = 'https://github.com/Hocklaint/Parcial_IA_render/blob/f9daed8698f55e1dacadbaece5a870562cadd5c3/src/Magnetometro.csv?raw=true'
csv_luz= 'https://github.com/Hocklaint/Parcial_IA_render/blob/f9daed8698f55e1dacadbaece5a870562cadd5c3/src/Luz.csv?raw=true'
csv_acelerometro= 'https://github.com/Hocklaint/Parcial_IA_render/blob/f9daed8698f55e1dacadbaece5a870562cadd5c3/src/Acelerometro.csv?raw=true'

#CSS

tabs_styles = {
    "flexDirection": "row",
}
tab_style = {
    "padding": "1.3vh",
    "color": 'black',
    "fontSize": '.9vw',
    "backgroundColor": 'rgba(242, 242, 242, 0.0)',
    'borderBottom': '1px black solid',
    
}

tab_selected_style = {
    "fontSize": '.9vw',
    "color": 'black',
    "padding": "1.3vh",
    'fontWeight': 'bold',
    "backgroundColor": '#b6c0c8',
    'borderTop': '1px black solid',
    'borderLeft': '1px black solid',
    'borderRight': '1px black solid',
    'borderRadius': '0px 0px 0px 0px',
}

background_div_style = {
    "position": "absolute",
    "top": "0px",
    "right": "0px",
    "left": "0px",
    "bottom": "0px",
}

backgroundImage_style = {
    "height": "167vh"
}

header_div_style = {
    "position": "relative",
    "top": "101vh"
}

content_div_style = {
    "position": "relative",
    "top": "111vh"
}

tab_selected_style1 = {
    "fontSize": '.9vw',
    "color": '#F4F4F4',
    "padding": "1.3vh",
    'fontWeight': 'bold',
    "backgroundColor": '#566573',
    'borderTop': '1px white solid',
    'borderLeft': '1px white solid',
    'borderRight': '1px white solid',
    'borderRadius': '0px 0px 0px 0px',
}

# Umbrales de tolerancia, y razonables
limite_luz = 30

limite_inferior_aceleXY = -1
limite_superior_aceleXY = 1
limite_inferior_aceleZ = 9.7
limite_superior_aceleZ = 9.9

limite_magnetometro = 40

def kpi_color(valor, umbral_minimo, umbral_maximo, color_izquierdo="red", color_central="#FCDE22",
              color_derecho="#109D55"):
    if valor < umbral_minimo:
        color = color_izquierdo
    elif valor > umbral_maximo:
        color = color_derecho
    else:
        color = color_central
    return color

def kpi_color2(valor, umbral, color_izquierdo="red", color_derecho="#109D55"):
    if valor < umbral:
        color = color_izquierdo
    elif valor > umbral:
        color = color_derecho
    
    return color

def semaforo_factory(limite_inferior, limite_superior,
                     titulo_izquierdo="Peligro", titulo_central="Alerta", titulo_derecho="Correcto",
                     color_izquierdo="red", color_central="#FCDE22", color_derecho="#109D55"
                     ):
    semaforo = html.Div([
        html.Div([
            html.Div([html.H5(titulo_izquierdo, style={"marginBottom": '0px', 'color': 'black'})],
                     className="cell cell-header cell-header-red  card_container four columns",
                     style={"backgroundColor": color_izquierdo}),
            html.Div([html.H5(titulo_central, style={"marginBottom": '0px', 'color': 'black'})],
                     className="cell cell-header cell-header-green  card_container four "
                               "columns", style={"backgroundColor": color_central}),
            html.Div([html.H5(titulo_derecho, style={"marginBottom": '0px', 'color': 'black'})],
                     className="cell cell-header cell-header-red card_container four columns",
                     style={"backgroundColor": color_derecho}
                     )
        ], className="row flex display"
        ),
        html.Div([
            html.Div([html.H5(f"< {limite_inferior}", style={"marginBottom": '0px', 'color': color_izquierdo})],
                     className="cell cell-body cell-body-red danger card_container four columns"),
            html.Div(
                [html.H5(f"{limite_inferior} - {limite_superior}",
                         style={"marginBottom": '0px', 'color': color_central})],
                className="cell cell-body cell-body-yellow warning card_container four "
                          "columns"),
            html.Div([html.H5(f"{limite_superior} <", style={"marginBottom": '0px', 'color': color_derecho})],
                     className="cell cell-body cell-body-green success card_container four columns")
        ], className="row flex display"
        )
    ], className="table row flex display")
    return semaforo

def semaforo_factory2(limite,
                     titulo_izquierdo="Correcto", titulo_derecho="Peligro",
                     color_izquierdo="red", color_derecho="#109D55"
                     ):
    semaforo = html.Div([
        html.Div([
            html.Div([html.H5(titulo_izquierdo, style={"marginBottom": '0px', 'color': 'black'})],
                     className="cell cell-header cell-header-red  card_container six columns",
                     style={"backgroundColor": color_izquierdo}),
            
            html.Div([html.H5(titulo_derecho, style={"marginBottom": '0px', 'color': 'black'})],
                     className="cell cell-header cell-header-red card_container six columns",
                     style={"backgroundColor": color_derecho}
                     )
        ], className="row flex display"
        ),
        html.Div([
            html.Div([html.H5(f"< {limite}", style={"marginBottom": '0px', 'color': color_izquierdo})],
                     className="cell cell-body cell-body-red danger card_container six columns"),
            
            html.Div([html.H5(f"{limite} <", style={"marginBottom": '0px', 'color': color_derecho})],
                     className="cell cell-body cell-body-green success card_container six columns")
        ], className="row flex display"
        )
    ], className="table row flex display")
    return semaforo

#html
app.layout = html.Div([
    html.Div(id='background_image', style=background_div_style),
    html.Div([
        dcc.Interval(id='update_date_time',
                     interval=1000,
                     n_intervals=0),
        
    ]),

    html.Div([

        # Cabecera
        html.Div([
            html.Div([
                html.Div([
                    html.Img(src="/assets/uni_logo.png",
                             title="Logo",
                             style={
                                 "height": "100px",
                                 "width": "auto",
                                 'marginBottom': "25px"
                             }, id="logo_ocad", className="six columns"),
                    html.H6('Parcial SI077U',
                            style={
                                'lineHeight': '1',
                                'color': 'white',
                                'marginLeft': '20px', 'fontSize': '50px', 'paddingTop': '20px'},
                            className='adjust_title six columns'
                            ),
                ], className="six columns row flex display"),

                html.Div([
                    html.Div(id='update',
                             className='image_grid six columns'),
                    html.H6(id='get_date_time',
                            style={
                                'lineHeight': '1',
                                'color': 'white', 'paddingTop': '7%', 'marginRight': '30px'},
                            className='adjust_date_time'
                            )
                ], className='temp_card1', style={'textAlign': 'right'}),
            ], className='adjust_title_and_date_time_two_columns')
        ], className='container_title_date_time twelve columns')
    ], className="row flex-display", style=header_div_style),
    
    html.Div([
        dcc.Interval(id='update_chart',
                     interval=1000,
                     n_intervals=0),
    ]),

    html.Div([
                  
            
            #Tabs
            html.Div([
                dcc.Tabs( id="tabs-styled-with-inline", children=[
                    dcc.Tab(
                        children=[
                            
                            # Gráfico de lineas + KPI + Semáforo + Imagen
                            html.Div([
                                # 7 columnas
                                html.Div([
                                    # Gráfico de lineas
                                    dcc.Graph(id='lux-chart',
                                            animate=True,
                                            config={'displayModeBar': 'hover'},
                                            className='chart_width'),
                                ], className="seven columns"),
                               
                                # 5 columnas
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            # KPI
                                            html.Div([
                                                html.Div(id='text1_1', className='grid_height'),
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Semáforo
                                        html.Div([
                                            html.Div([
                                                semaforo_factory2(f"{limite_luz} lx",
                                                                 "Insuficiente", "Suficiente",
                                                                color_izquierdo="red",
                                                                color_derecho="#109D55")
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Imagen
                                        #--
                                    ], className="row flex display"),
                                ], className="five columns"),
                            ], className="row flex display", style={"padding":"7.5vh"}),

                            

                            
                        ],
                        label='Escenario 1',                               
                        style=tab_style,
                        selected_style=tab_selected_style,
                        className='font_size'
                    ),
                    dcc.Tab(
                        children=[
                            #Podometro
                            # Gráfico de lineas + KPI + Semáforo + Imagen
                            html.Div([
                                # 7 columnas
                                html.Div([
                                    # Gráfico de lineas
                                    dcc.Graph(id='acele-chart-x',
                                            animate=True,
                                            config={'displayModeBar': 'hover'},
                                            className='chart_width'),
                                ], className="seven columns"),
                                
                                # 5 columnas
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            # KPI
                                            html.Div([
                                                html.Div(id='text2x', className='grid_height'),
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Semáforo
                                        html.Div([
                                            html.Div([
                                                semaforo_factory(f"{limite_inferior_aceleXY}m/s2",
                                                                f"{limite_superior_aceleXY}m/s2",
                                                                "Incorrecto", "Correcto",
                                                                "Incorrecto", color_izquierdo="red",
                                                                color_central="#109D55", color_derecho="red")
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Imagen
                                        #--
                                        
                                    ], className="row flex display"),
                                ], className="five columns"),
                            ], className="row flex display"),

                            # Gráfico de lineas + KPI + Semáforo + Imagen
                            html.Div([
                                                               
                                # 5 columnas
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            # KPI
                                            html.Div([
                                                html.Div(id='text2y', className='grid_height'),
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Semáforo
                                        html.Div([
                                            html.Div([
                                                semaforo_factory(f"{limite_inferior_aceleXY}m/s2",
                                                                f"{limite_superior_aceleXY}m/s2",
                                                                "Incorrecto", "Correcto",
                                                                "Incorrecto", color_izquierdo="red",
                                                                color_central="#109D55", color_derecho="red")
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Imagen
                                       #--                                       
                                    ], className="row flex display"),
                                ], className="five columns"),
                                # 7 columnas
                                html.Div([
                                    # Gráfico de lineas
                                    dcc.Graph(id='acele-chart-y',
                                            animate=True,
                                            config={'displayModeBar': 'hover'},
                                            className='chart_width'),
                                ], className="seven columns"),
                            ], className="row flex display"),

                            # Gráfico de lineas + KPI + Semáforo + Imagen
                            html.Div([
                                # 7 columnas
                                html.Div([
                                    # Gráfico de lineas
                                    dcc.Graph(id='acele-chart-z',
                                            animate=True,
                                            config={'displayModeBar': 'hover'},
                                            className='chart_width'),
                                ], className="seven columns"),
                                
                                # 5 columnas
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            # KPI
                                            html.Div([
                                                html.Div(id='text2z', className='grid_height'),
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Semáforo
                                        html.Div([
                                            html.Div([
                                                semaforo_factory(f"{limite_inferior_aceleZ}m/s2",
                                                                f"{limite_superior_aceleZ}m/s2",
                                                                "En movimiento", "En reposo",
                                                                "En movimiento", color_izquierdo="#109D55",
                                                                color_central="red", color_derecho="#109D55")
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Imagen
                                        #--
                                    ], className="row flex display"),
                                ], className="five columns"),
                            ], className="row flex display"),
                        ],
                        label='Escenario 2',                               
                        style=tab_style,
                        selected_style=tab_selected_style,
                        className='font_size'
                    ),
                    dcc.Tab(
                        children=[
                            
                            # Gráfico de lineas + KPI + Semáforo + Imagen
                            html.Div([
                                # 7 columnas
                                html.Div([
                                    # Gráfico de lineas
                                    dcc.Graph(id='magnetic-chart',
                                            animate=True,
                                            config={'displayModeBar': 'hover'},
                                            className='chart_width'),
                                ], className="seven columns"),
                               
                                # 5 columnas
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            # KPI
                                            html.Div([
                                                html.Div(id='text3', className='grid_height'),
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Semáforo
                                        html.Div([
                                            html.Div([
                                                semaforo_factory2(f"{limite_magnetometro} μT",
                                                                "Estándar", "Detección metálica",
                                                                color_izquierdo="red",
                                                                color_derecho="#109D55")
                                            ], className="twelve columns"),
                                        ], className="row flex display"),
                                        # Imagen
                                        #--
                                    ], className="row flex display"),
                                ], className="five columns"),
                            ], className="row flex display", style={"padding":"7.5vh"}),
                            
                            
                            #Por eje
                            html.Div([
                                html.Div([
                                    # Eje x
                                    dcc.Graph(id='magnetic-chart-x',
                                            animate=True,
                                            config={'displayModeBar': 'hover'},
                                            className='chart_width'),
                                ], className="twelve columns"),
                                html.Div([
                                    # Eje y
                                    dcc.Graph(id='magnetic-chart-y',
                                            animate=True,
                                            config={'displayModeBar': 'hover'},
                                            className='chart_width'),
                                ], className="twelve columns"),
                                html.Div([
                                    # Eje z
                                    dcc.Graph(id='magnetic-chart-z',
                                            animate=True,
                                            config={'displayModeBar': 'hover'},
                                            className='chart_width'),
                                ], className="twelve columns"),
                            ], className="row flex display"),
                        ],
                        label='Escenario 3',                               
                        style=tab_style,
                        selected_style=tab_selected_style,
                        className='font_size'
                    ),
                ]),
            ], className='create_container3 nine columns'),
            
        
    ], className="row flex-display", style=content_div_style),
], id="mainContainer", style={"display": "flex", "flexDirection": "column"})


#DateTime
@app.callback(Output('get_date_time', 'children'),
              [Input('update_date_time', 'n_intervals')])
def update_graph(n_intervals):
    now = datetime.now()
    dt_string = now.strftime("Fecha: %d/%m/%Y, Hora: %H:%M:%S %p")
    if n_intervals == 0:
        raise PreventUpdate

    return [
        html.Div(dt_string),
    ]

#Clima
@app.callback(Output('lux-chart', 'figure'), 
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    
    df = pd.read_csv(csv_luz)
    df = df.drop_duplicates(subset = "Time (s)")
    get_time = df['Time (s)'].tail(50)
    categoria = 'Luz'
    get_lux = df['Illuminance (lx)'].tail(50)
    if n_intervals == 0:
        raise PreventUpdate
    
       
        #Luz
    lux_chart = go.Figure(
        {
            'data': [go.Scatter(
                x=get_time,
                y=get_lux,
                mode='markers+lines',
                line=dict(width=3, color='#CA23D5'),
                marker=dict(size=7, symbol='circle', color='#CA23D5',
                            line=dict(color='#CA23D5', width=2)
                            ),

                hoverinfo='text',
                hovertext=
                '<b>Tiempo(s)</b>: ' + get_time.astype(str) + '<br>' +
                '<b>' + categoria + '</b>: ' + [f'{x:,.2f} lx' for x in get_lux] + '<br>'

            )],

            'layout': go.Layout(
                plot_bgcolor='rgba(255, 255, 255, 0.0)',
                paper_bgcolor='rgba(255, 255, 255, 0.0)',
                title={
                    'text': 'Luminosidad',

                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'black',
                    'size': 17},

                hovermode='closest',
                margin=dict(t=25, r=0, l=50),

                xaxis=dict(range=[min(get_time), max(get_time)],
                           title='<b>Tiempo (s)</b>',
                           color='black',
                           showline=True,
                           showgrid=False,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                yaxis=dict(range=[min(get_lux) - 0.1, max(get_lux) + 0.1],
                           title=('<b>%s</b>' % categoria),
                           color='black',
                           showline=True,
                           showgrid=True,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                legend={
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='black')

            )

        }
    )
    return lux_chart

#Podómetro
@app.callback(Output('acele-chart-x', 'figure'),Output('acele-chart-y', 'figure'),Output('acele-chart-z', 'figure'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    
    df = pd.read_csv(csv_acelerometro)
    df = df.drop_duplicates(subset = "Time(ms)")
    get_time = df['Time(ms)'].tail(50)
    categoria = 'Aceleración (m/s2)'
    get_acele_x = df['X'].tail(50)
    get_acele_y = df['Y'].tail(50)
    get_acele_z = df['Z'].tail(50)
    if n_intervals == 0:
        raise PreventUpdate
    
    #En X
    acele_chart_x = go.Figure(
        {
            'data': [go.Scatter(
                x=get_time,
                y=get_acele_x,
                mode='markers+lines',
                line=dict(width=3, color='#CA23D5'),
                marker=dict(size=7, symbol='circle', color='#CA23D5',
                            line=dict(color='#CA23D5', width=2)
                            ),

                hoverinfo='text',
                hovertext=
                '<b>Tiempo (ms)</b>: ' + get_time.astype(str) + '<br>' +
                '<b>' + categoria + '</b>: ' + [f'{x:,.2f} m/s2' for x in get_acele_x] + '<br>'

            )],

            'layout': go.Layout(
                plot_bgcolor='rgba(255, 255, 255, 0.0)',
                paper_bgcolor='rgba(255, 255, 255, 0.0)',
                title={
                    'text': 'Acelerómetro X',

                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'black',
                    'size': 17},

                hovermode='closest',
                margin=dict(t=25, r=0, l=50),

                xaxis=dict(range=[min(get_time), max(get_time)],
                           title='<b>Tiempo(ms)</b>',
                           color='black',
                           showline=True,
                           showgrid=False,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                yaxis=dict(range=[min(get_acele_x) - 0.1, max(get_acele_x) + 0.1],
                           title=('<b>%s</b>' % categoria),
                           color='black',
                           showline=True,
                           showgrid=True,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                legend={
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='black')

            )

        }
    )
    #En Y
    acele_chart_y = go.Figure(
        {
            'data': [go.Scatter(
                x=get_time,
                y=get_acele_y,
                mode='markers+lines',
                line=dict(width=3, color='#CA23D5'),
                marker=dict(size=7, symbol='circle', color='#CA23D5',
                            line=dict(color='#CA23D5', width=2)
                            ),

                hoverinfo='text',
                hovertext=
                '<b>Tiempo (ms)</b>: ' + get_time.astype(str) + '<br>' +
                '<b>' + categoria + '</b>: ' + [f'{x:,.2f} m/s2' for x in get_acele_y] + '<br>'

            )],

            'layout': go.Layout(
                plot_bgcolor='rgba(255, 255, 255, 0.0)',
                paper_bgcolor='rgba(255, 255, 255, 0.0)',
                title={
                    'text': 'Acelerómetro Y',

                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'black',
                    'size': 17},

                hovermode='closest',
                margin=dict(t=25, r=0, l=50),

                xaxis=dict(range=[min(get_time), max(get_time)],
                           title='<b>Tiempo (ms)</b>',
                           color='black',
                           showline=True,
                           showgrid=False,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                yaxis=dict(range=[min(get_acele_y) - 0.1, max(get_acele_y) + 0.1],
                           title=('<b>%s</b>' % categoria),
                           color='black',
                           showline=True,
                           showgrid=True,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                legend={
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='black')

            )

        }
    )
    #En z
    acele_chart_z = go.Figure(
        {
            'data': [go.Scatter(
                x=get_time,
                y=get_acele_z,
                mode='markers+lines',
                line=dict(width=3, color='#CA23D5'),
                marker=dict(size=7, symbol='circle', color='#CA23D5',
                            line=dict(color='#CA23D5', width=2)
                            ),

                hoverinfo='text',
                hovertext=
                '<b>Tiempo (ms)</b>: ' + get_time.astype(str) + '<br>' +
                '<b>' + categoria + '</b>: ' + [f'{x:,.2f} m/s2' for x in get_acele_z] + '<br>'

            )],

            'layout': go.Layout(
                plot_bgcolor='rgba(255, 255, 255, 0.0)',
                paper_bgcolor='rgba(255, 255, 255, 0.0)',
                title={
                    'text': 'Acelerómetro Z',

                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'black',
                    'size': 17},

                hovermode='closest',
                margin=dict(t=25, r=0, l=50),

                xaxis=dict(range=[min(get_time), max(get_time)],
                           title='<b>Tiempo (ms)</b>',
                           color='black',
                           showline=True,
                           showgrid=False,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                yaxis=dict(range=[min(get_acele_z) - 0.1, max(get_acele_z) + 0.1],
                           title=('<b>%s</b>' % categoria),
                           color='black',
                           showline=True,
                           showgrid=True,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                legend={
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='black')

            )

        }
    )
   
    return acele_chart_x, acele_chart_y, acele_chart_z



#Magnetometro
@app.callback(Output('magnetic-chart', 'figure'), Output('magnetic-chart-x', 'figure'), Output('magnetic-chart-y', 'figure'), Output('magnetic-chart-z', 'figure'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    
    df = pd.read_csv(csv)
    df = df.drop_duplicates(subset = "Time (s)")
    get_time = df['Time (s)'].tail(50)
    categoria = 'Inducción magnética (µT)'
    get_magnetic_absolute = df['Absolute field (µT)'].tail(50)
    get_magnetic_x = df['Magnetic Field x (µT)'].tail(50)
    get_magnetic_y = df['Magnetic Field y (µT)'].tail(50)
    get_magnetic_z = df['Magnetic Field z (µT)'].tail(50)
    if n_intervals == 0:
        raise PreventUpdate

    magnetic_chart = go.Figure(
        {
            'data': [go.Scatter(
                x=get_time,
                y=get_magnetic_absolute,
                mode='markers+lines',
                line=dict(width=3, color='#CA23D5'),
                marker=dict(size=7, symbol='circle', color='#CA23D5',
                            line=dict(color='#CA23D5', width=2)
                            ),

                hoverinfo='text',
                hovertext=
                '<b>Tiempo</b>: ' + get_time.astype(str) + '<br>' +
                '<b>' + categoria + '</b>: ' + [f'{x:,.2f} µT' for x in get_magnetic_absolute] + '<br>'

            )],

            'layout': go.Layout(
                plot_bgcolor='rgba(255, 255, 255, 0.0)',
                paper_bgcolor='rgba(255, 255, 255, 0.0)',
                title={
                    'text': 'Magnetómetro Absoluto',

                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'black',
                    'size': 17},

                hovermode='closest',
                margin=dict(t=25, r=0, l=50),

                xaxis=dict(range=[min(get_time), max(get_time)],
                           title='<b>Tiempo (s)</b>',
                           color='black',
                           showline=True,
                           showgrid=False,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                yaxis=dict(range=[min(get_magnetic_absolute) - 0.1, max(get_magnetic_absolute) + 0.1],
                           title=('<b>%s</b>' % categoria),
                           color='black',
                           showline=True,
                           showgrid=True,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                legend={
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='black')

            )

        }
    )
    #En X
    magnetic_chart_x = go.Figure(
        {
            'data': [go.Scatter(
                x=get_time,
                y=get_magnetic_x,
                mode='markers+lines',
                line=dict(width=3, color='#CA23D5'),
                marker=dict(size=7, symbol='circle', color='#CA23D5',
                            line=dict(color='#CA23D5', width=2)
                            ),

                hoverinfo='text',
                hovertext=
                '<b>Tiempo(s)</b>: ' + get_time.astype(str) + '<br>' +
                '<b>' + categoria + '</b>: ' + [f'{x:,.2f} µT' for x in get_magnetic_x] + '<br>'

            )],

            'layout': go.Layout(
                plot_bgcolor='rgba(255, 255, 255, 0.0)',
                paper_bgcolor='rgba(255, 255, 255, 0.0)',
                title={
                    'text': 'Magnetómetro X',

                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'black',
                    'size': 17},

                hovermode='closest',
                margin=dict(t=25, r=0, l=50),

                xaxis=dict(range=[min(get_time), max(get_time)],
                           title='<b>Tiempo (s)</b>',
                           color='black',
                           showline=True,
                           showgrid=False,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                yaxis=dict(range=[min(get_magnetic_x) - 0.1, max(get_magnetic_x) + 0.1],
                           title=('<b>%s</b>' % categoria),
                           color='black',
                           showline=True,
                           showgrid=True,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                legend={
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='black')

            )

        }
    )
    #En Y
    magnetic_chart_y = go.Figure(
        {
            'data': [go.Scatter(
                x=get_time,
                y=get_magnetic_y,
                mode='markers+lines',
                line=dict(width=3, color='#CA23D5'),
                marker=dict(size=7, symbol='circle', color='#CA23D5',
                            line=dict(color='#CA23D5', width=2)
                            ),

                hoverinfo='text',
                hovertext=
                '<b>Tiempo(s)</b>: ' + get_time.astype(str) + '<br>' +
                '<b>' + categoria + '</b>: ' + [f'{x:,.2f} µT' for x in get_magnetic_y] + '<br>'

            )],

            'layout': go.Layout(
                plot_bgcolor='rgba(255, 255, 255, 0.0)',
                paper_bgcolor='rgba(255, 255, 255, 0.0)',
                title={
                    'text': 'Magnetómetro Y',

                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'black',
                    'size': 17},

                hovermode='closest',
                margin=dict(t=25, r=0, l=50),

                xaxis=dict(range=[min(get_time), max(get_time)],
                           title='<b>Tiempo (s)</b>',
                           color='black',
                           showline=True,
                           showgrid=False,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                yaxis=dict(range=[min(get_magnetic_y) - 0.1, max(get_magnetic_y) + 0.1],
                           title=('<b>%s</b>' % categoria),
                           color='black',
                           showline=True,
                           showgrid=True,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                legend={
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='black')

            )

        }
    )
    #En z
    magnetic_chart_z = go.Figure(
        {
            'data': [go.Scatter(
                x=get_time,
                y=get_magnetic_z,
                mode='markers+lines',
                line=dict(width=3, color='#CA23D5'),
                marker=dict(size=7, symbol='circle', color='#CA23D5',
                            line=dict(color='#CA23D5', width=2)
                            ),

                hoverinfo='text',
                hovertext=
                '<b>Tiempo(s)</b>: ' + get_time.astype(str) + '<br>' +
                '<b>' + categoria + '</b>: ' + [f'{x:,.2f} µT' for x in get_magnetic_z] + '<br>'

            )],

            'layout': go.Layout(
                plot_bgcolor='rgba(255, 255, 255, 0.0)',
                paper_bgcolor='rgba(255, 255, 255, 0.0)',
                title={
                    'text': 'Magnetómetro Z',

                    'y': 0.97,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'black',
                    'size': 17},

                hovermode='closest',
                margin=dict(t=25, r=0, l=50),

                xaxis=dict(range=[min(get_time), max(get_time)],
                           title='<b>Tiempo (s)</b>',
                           color='black',
                           showline=True,
                           showgrid=False,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                yaxis=dict(range=[min(get_magnetic_z) - 0.1, max(get_magnetic_z) + 0.1],
                           title=('<b>%s</b>' % categoria),
                           color='black',
                           showline=True,
                           showgrid=True,
                           linecolor='black',
                           linewidth=1,
                           ticks='outside',
                           tickfont=dict(
                               family='Arial',
                               size=12,
                               color='black')

                           ),

                legend={
                    'orientation': 'h',
                    'bgcolor': '#F2F2F2',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='black')

            )

        }
    )
    return magnetic_chart, magnetic_chart_x, magnetic_chart_y , magnetic_chart_z

#Tarjeta Clima
@app.callback(Output('text1_1', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
   
    df = pd.read_csv(csv_luz)
    df = df.drop_duplicates(subset = "Time (s)")
    get_time = df['Time (s)'].tail(1).iloc[0]
    get_lux_level = df['Illuminance (lx)'].tail(1).iloc[0].astype(float)
    previous_lux_level = df['Illuminance (lx)'].tail(2).iloc[0].astype(float)
    changed_lux_level = get_lux_level - previous_lux_level
    
    if n_intervals == 0:
        raise PreventUpdate

    color_actual = kpi_color2(get_lux_level, limite_luz, color_izquierdo="red", color_derecho="#109D55")
    color_variacion = kpi_color2(changed_lux_level, 0)

  
    return [
        html.H6('Luminosidad',
                style={'textAlign': 'center',
                       'lineHeight': '1',
                       'color': 'black',
                       'fontSize': 30,
                       }
                ),
        # Nivel Actual
        html.P('{0:,.2f} lx'.format(get_lux_level),
               style={'textAlign': 'center',
                      'color': color_actual,
                      'fontSize': 30,
                      'fontWeight': 'bold',
                      'marginTop': '5px',
                      'lineHeight': '1',
                      }, className='paragraph_value_humi'
               ),
        html.P('{0:,.2f} lx'.format(changed_lux_level) + ' ' + 'vs. medición anterior',
               style={'textAlign': 'center',
                      'color': color_variacion,
                      'fontSize': 15,
                      'fontWeight': 'bold',
                      'marginTop': '0px',
                      'marginLeft': '0px',
                      'lineHeight': '1',
                      }, className='change_paragraph_value_humi'
               ),
        html.P(get_time,
               style={'textAlign': 'center',
                      'color': 'black',
                      'fontSize': 14,
                      'marginTop': '0px'
                      }
               ),
    ]



#Tarjeta Podometro
@app.callback(Output('text2x', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
   
    df = pd.read_csv(csv_acelerometro)
    df = df.drop_duplicates(subset = "Time(ms)")
    get_time = df['Time(ms)'].tail(1).iloc[0]
    get_acelX_level = df['X'].tail(1).iloc[0].astype(float)
    previous_acelX_level = df['X'].tail(2).iloc[0].astype(float)
    changed_acelX_level = get_acelX_level - previous_acelX_level
    
    if n_intervals == 0:
        raise PreventUpdate

    color_actual = kpi_color(get_acelX_level, limite_inferior_aceleXY, limite_superior_aceleXY,
                             color_izquierdo="red", color_central="#109D55", color_derecho="red")
    color_variacion = kpi_color(changed_acelX_level, 0, 0, color_central="black")

  
    return [
        html.H6('Aceleración en X',
                style={'textAlign': 'center',
                       'lineHeight': '1',
                       'color': 'black',
                       'fontSize': 30,
                       }
                ),
        # Nivel Actual
        html.P('{0:,.2f} m/s^2'.format(get_acelX_level),
               style={'textAlign': 'center',
                      'color': color_actual,
                      'fontSize': 30,
                      'fontWeight': 'bold',
                      'marginTop': '5px',
                      'lineHeight': '1',
                      }, className='paragraph_value_humi'
               ),
        html.P('{0:,.2f} m/s^2'.format(changed_acelX_level) + ' ' + 'vs. medición anterior',
               style={'textAlign': 'center',
                      'color': color_variacion,
                      'fontSize': 15,
                      'fontWeight': 'bold',
                      'marginTop': '0px',
                      'marginLeft': '0px',
                      'lineHeight': '1',
                      }, className='change_paragraph_value_humi'
               ),
        html.P(get_time,
               style={'textAlign': 'center',
                      'color': 'black',
                      'fontSize': 14,
                      'marginTop': '0px'
                      }
               ),
    ]
 #Z   
@app.callback(Output('text2z', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
   
    df = pd.read_csv(csv_acelerometro)
    df = df.drop_duplicates(subset = "Time(ms)")
    get_time = df['Time(ms)'].tail(1).iloc[0]
    get_acelZ_level = df['Z'].tail(1).iloc[0].astype(float)
    previous_acelZ_level = df['Z'].tail(2).iloc[0].astype(float)
    changed_acelZ_level = get_acelZ_level - previous_acelZ_level
    
    if n_intervals == 0:
        raise PreventUpdate

    color_actual = kpi_color(get_acelZ_level, limite_inferior_aceleZ, limite_superior_aceleZ,
                             color_izquierdo="#109D55", color_central="red", color_derecho="#109D55")
    color_variacion = kpi_color(changed_acelZ_level, 0, 0, color_central="black")

  
    return [
        html.H6('Aceleración en Z',
                style={'textAlign': 'center',
                       'lineHeight': '1',
                       'color': 'black',
                       'fontSize': 30,
                       }
                ),
        # Nivel Actual
        html.P('{0:,.2f} m/s^2'.format(get_acelZ_level),
               style={'textAlign': 'center',
                      'color': color_actual,
                      'fontSize': 30,
                      'fontWeight': 'bold',
                      'marginTop': '5px',
                      'lineHeight': '1',
                      }, className='paragraph_value_humi'
               ),
        html.P('{0:,.2f} m/s^2'.format(changed_acelZ_level) + ' ' + 'vs. medición anterior',
               style={'textAlign': 'center',
                      'color': color_variacion,
                      'fontSize': 15,
                      'fontWeight': 'bold',
                      'marginTop': '0px',
                      'marginLeft': '0px',
                      'lineHeight': '1',
                      }, className='change_paragraph_value_humi'
               ),
        html.P(get_time,
               style={'textAlign': 'center',
                      'color': 'black',
                      'fontSize': 14,
                      'marginTop': '0px'
                      }
               ),
    ]
#Y
@app.callback(Output('text2y', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
   
    df = pd.read_csv(csv_acelerometro)
    df = df.drop_duplicates(subset = "Time(ms)")
    get_time = df['Time(ms)'].tail(1).iloc[0]
    get_acelY_level = df['Y'].tail(1).iloc[0].astype(float)
    previous_acelY_level = df['Y'].tail(2).iloc[0].astype(float)
    changed_acelY_level = get_acelY_level - previous_acelY_level
    
    if n_intervals == 0:
        raise PreventUpdate

    color_actual = kpi_color(get_acelY_level, limite_inferior_aceleXY, limite_superior_aceleXY,
                             color_izquierdo="red", color_central="#109D55", color_derecho="red")
    color_variacion = kpi_color(changed_acelY_level, 0, 0, color_central="black")

  
    return [
        html.H6('Aceleración en Y',
                style={'textAlign': 'center',
                       'lineHeight': '1',
                       'color': 'black',
                       'fontSize': 30,
                       }
                ),
        # Nivel Actual
        html.P('{0:,.2f} m/s^2'.format(get_acelY_level),
               style={'textAlign': 'center',
                      'color': color_actual,
                      'fontSize': 30,
                      'fontWeight': 'bold',
                      'marginTop': '5px',
                      'lineHeight': '1',
                      }, className='paragraph_value_humi'
               ),
        html.P('{0:,.2f} m/s^2'.format(changed_acelY_level) + ' ' + 'vs. medición anterior',
               style={'textAlign': 'center',
                      'color': color_variacion,
                      'fontSize': 15,
                      'fontWeight': 'bold',
                      'marginTop': '0px',
                      'marginLeft': '0px',
                      'lineHeight': '1',
                      }, className='change_paragraph_value_humi'
               ),
        html.P(get_time,
               style={'textAlign': 'center',
                      'color': 'black',
                      'fontSize': 14,
                      'marginTop': '0px'
                      }
               ),
    ]

#Tarjeta texto Magnetometro
@app.callback(Output('text3', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
   
    df = pd.read_csv(csv)
    df = df.drop_duplicates(subset = "Time (s)")
    get_time = df['Time (s)'].tail(1).iloc[0]
    get_magnetic_level = df['Absolute field (µT)'].tail(1).iloc[0].astype(float)
    previous_magnetic_level = df['Absolute field (µT)'].tail(2).iloc[0].astype(float)
    changed_magnetic_level = get_magnetic_level - previous_magnetic_level
    
    if n_intervals == 0:
        raise PreventUpdate

    color_actual = kpi_color2(get_magnetic_level, limite_magnetometro, 
                             color_izquierdo="red", color_derecho="#109D55")
    color_variacion = kpi_color2(changed_magnetic_level, 0)

  
    return [
        html.H6('Magnetómetro',
                style={'textAlign': 'center',
                       'lineHeight': '1',
                       'color': 'black',
                       'fontSize': 30,
                       }
                ),
        # Nivel Actual
        html.P('{0:,.2f} µT'.format(get_magnetic_level),
               style={'textAlign': 'center',
                      'color': color_actual,
                      'fontSize': 30,
                      'fontWeight': 'bold',
                      'marginTop': '5px',
                      'lineHeight': '1',
                      }, className='paragraph_value_humi'
               ),
        html.P('{0:,.2f} µT'.format(changed_magnetic_level) + ' ' + 'vs. medición anterior',
               style={'textAlign': 'center',
                      'color': color_variacion,
                      'fontSize': 15,
                      'fontWeight': 'bold',
                      'marginTop': '0px',
                      'marginLeft': '0px',
                      'lineHeight': '1',
                      }, className='change_paragraph_value_humi'
               ),
        html.P(get_time,
               style={'textAlign': 'center',
                      'color': 'black',
                      'fontSize': 14,
                      'marginTop': '0px'
                      }
               ),
    ]



if __name__=="__main__":
    app.run_server(debug=True)
