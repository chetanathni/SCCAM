import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from collections import deque
import requests
import numpy as np
import datetime
import time
import random
import string
import json
import dash_daq as daq
import queue,threading
from plotly import tools
from plotly import subplots
from kafka import KafkaConsumer,KafkaProducer

bootstrap_servers = ['kafka:9092']
def rec_agg(agg_rec):
        topicName5 = 'aggVal'
        consumer5= KafkaConsumer (topicName5, group_id = 'group3', bootstrap_servers = bootstrap_servers, api_version = (0,10,0), auto_offset_reset = 'latest')
        consumer5.subscribe(topicName5)
        for aggval in consumer5:
                agg_val=(aggval.value).decode('utf-8')
                agg_rec.put(agg_val)
                
def docker_data(docker_image):

    topicName3 ='OptionName'
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers,api_version=(0,10,0))
    while(1):
        docker_text=docker_image.get()
        producer.send(topicName3 , docker_text.encode('utf-8'))
        producer.flush()
        
def user_ch(pr):

    topicName2 ='LocationReq'
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers,api_version=(0,10,0))
    while(1):
        choice_us=pr.get()
        producer.send(topicName2 , choice_us.encode('utf-8'))
        producer.flush()

def graph_info(q,t):

    topicName = 'filtered'
    consumer = KafkaConsumer (topicName, group_id = 'test-consumer-group',bootstrap_servers = bootstrap_servers,api_version=(0,10,0),auto_offset_reset = 'latest',value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    consumer.subscribe(topicName)
    for message in consumer:
        y=message.value
        q.put(y[0])
        t.put(y[1:5])


BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/solar/bootstrap.min.css"
app = dash.Dash(__name__,external_stylesheets=[BS])
app.config['suppress_callback_exceptions'] = True

def dash_thread(q,r,t,pr,docker_image,agg_rec):
    
    X = deque(maxlen=20)
    X.append(1)
    Y = deque(maxlen=20)
    Y.append(1)
    U = deque(maxlen=20)
    U.append(1)
    V = deque(maxlen=20)
    V.append(1)
    A = deque(maxlen=20)
    A.append(1)
    B = deque(maxlen=20)
    B.append(1)
    M = deque(maxlen=3)
    
    navbar = dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="#")),
                    dbc.NavItem(dbc.NavLink("Contact Us", href="#")),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Login",href="#"),
                            dbc.DropdownMenuItem("Sign Up", href="#"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Login",
                    ),
                ],
                brand="SCCAM",
                brand_href="#",
                color="#186e98",
                dark=True,
                fluid =True,
                sticky="top",
                style={'fontSize':18,"color":"white"} )
    
    tabs_content = dbc.Tabs(
                    [
                        dbc.Tab(label="User", tab_id="tab-1",tab_style={'width':'50%'},label_style={'text-align':'center'}),
                        dbc.Tab(label="Admin", tab_id="tab-2",tab_style={'width':'50%'},label_style={'text-align':'center'}),
                    ],
                    id="tabs",
                    active_tab="tab-1",
                    style={'display':'flex','font-size':20},
                )
    output_tab = html.Div(id="content")
    output_tab2 = html.Div(id="output_content")
    user_tab =  dbc.Container(

                dbc.FormGroup(
                [
                    
                    daq.ToggleSwitch(
                        label={'label':'Default Graphs',"style":{"fontSize":20,"padding":10}},
                        labelPosition='right',
                        size=50,
                        id="switches-input",
                        value=False,
                        color= 'yellow',
                        
                        style={'justify-content':'space-between','display': 'inline-block','padding-top':20}
                    ),
                    
                
                dbc.Button("Upload Function", color="success",size="lg", className="mr-1",outline=True    ,id="open-centered",style={"margin-left":'50%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Upload Function"),
                        dbc.ModalBody(
                        [
                            dcc.Input(id="input_text", type="text", placeholder="DockerImage name", debounce=True,style={"margin-left":"5%","padding":10,"width":"70%","border":"1px solid white","background-color":"rgba(0,0,0,0)","color":"white"}),
                            html.Div(id="output",style={"padding":20,"font-size":20}),
                        ],
                        ),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close", id="close-centered", className="ml-auto",outline=True, color="warning"
                            )
                        ),
                    ],
                    id="modal-centered",
                    centered=True,
                ),],),
                className="p-1",style = {'textAlign':'center','width':'100%','padding':20},)
    default_graphs = dbc.Jumbotron(
        [
                    dbc.Row(
                    [
                    dbc.Col(
                    [
                    dbc.Card(
                    [
                    
                    html.Div([
                        
                        dcc.Dropdown(
                        id='loc-dropdown',
                        options=[
                            {'label': 'HSR Layout', 'value': 'HSR'},
                            {'label': 'Bellanduru', 'value': 'Bellandur'},
                        ],
                        value='HSR',
                        style={'width':'50%',"background-color": 'rgba(0,0,0,0)',"display":'inline-block',"color":"black"}),
                
                    dcc.Dropdown(
                        id='demo-dropdown',
                        options=[
                            {'label': 'Line Chart', 'value': 'Line'},
                            {'label': 'Bubble Chart', 'value': 'Bubble'},
                            {'label': 'Scatter Plot', 'value': 'Scatter'},
                            {'label': 'Dot Plot', 'value': 'Dot'},
                            {'label': 'Strip Chart', 'value': 'Strip'},
                            {'label': 'Candlestick Chart', 'value': 'Candlestick'},
                        ],
                        value='Line',
                        style={'width':'50%',"background-color": 'rgba(0,0,0,0)',"display":'inline-block',"color":"black"}),
                    ],style={"float":"left","display":'inline-block',"justify-content":"space-between","background-color": 'rgb(191, 191, 191)'}),
                        html.P('Air-Quality',style={"font-size":30,"margin-left":"15%","margin-top":"5%"}),
                        dcc.Graph(id='live-graph', animate=True ,style={'width': 700,'height' : 550, 'align':'center' }),
                        dcc.Interval(
                            id='graph-update',
                            interval=1*5000),
                    ],
                    style={'width':'100%'}),
                    ],),
                    dbc.Col(
                    [
                    dbc.Card(
                    [
                    html.Div([],id="current_ppmval"),
                    
                        html.Br(),html.Hr(style={'border':'5px solid black'}),
                            dbc.Row([
                                html.P('Aggregate Values',style={"font-size":30,"margin-left":"15%"}),
                                html.Div([
                            #html.P('Aggregate Values',style={"font-size":20,"margin-left":"15%"}),
                            dcc.Graph(id='live-update-graph-bar'),
                            dcc.Interval(
                            id='interval-component4',
                            interval=1*10000)])
                        ],style={"margin-left":"10%"}),],
                        style={'width':'100%',"height":"100%"}),
                        ],),],),
            ]
        ),
    #default_body = html.Div(id="default_body",children=['Your graphs appear here'])
    default_body = dbc.Jumbotron(html.Div(id="default_body",children=[
                    html.P('Your graphs appear here')],style={'fontSize':50,'textAlign':'center','margin-top':'200px'}),style={'height':600})
    fig = subplots.make_subplots(rows=1, cols=2,print_grid=False,horizontal_spacing=0.15,subplot_titles=("CPU usage", "Disk Usage"))
    admin_tab = dbc.Jumbotron(
        [
        dbc.Card(
        dbc.CardBody(
            [
                html.P("Admin only", className="card-text",style={'fontSize':15}),
                dcc.Graph(id='sys-graph',figure=fig,style={'width':'100%', 'height':'100%'},),
                dcc.Interval(id='graph-update2',interval=1*5000),
                html.Div(id="ram-used-div",className="ram-used-div",children=
                    [
                        html.P('RAM Usage', style={'fontSize':25,'margin-left':'40.5    %'}),
                        html.P(f'{random.randint(1,8)} of 8 GB '  , style={'fontSize':35,'margin-left':'40%'},id="ram_used_val")
                    ],style={
                        'padding':5,
                    }
                )
            ],style={"justify-content":"space-around","margin-left":"3%"}
        ),
        className="mt-3",
    ),],)
    app.layout = html.Div([navbar,tabs_content,output_tab,output_tab2,],)
    
    
    @app.callback(Output("modal-centered", "is_open"),[Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],[State("modal-centered", "is_open")],)
    def toggle_modal(n1, n2, is_open):
        
        if n1 or n2:
            return not is_open
        return is_open
    
    
    @app.callback(Output("output", "children"),[Input("input_text", "value")],)
    def update_output(input_text):
        
        docker_image.put('{}'.format(input_text))
        return u'Input File:- {}'.format(input_text)
    
    @app.callback(Output("output_content", "children"),[Input("switches-input", "value"),],)
    def on_form_change(switches_value):
        if switches_value == True:
            return default_graphs
        else:
            return default_body
        
    @app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
    def switch_tab(at):
        if at == "tab-1":
            return user_tab
        elif at == "tab-2":
            return admin_tab
        return html.P("This shouldn't ever be displayed...")
    
    
    
    
    def empty_graph(X,Y,xaxis_column_name):

        pr.put(xaxis_column_name)

        Y.clear()
        Y.append(0)
        X.clear()
        X.append(0)

    
    @app.callback([Output('live-graph', 'figure'),Output('current_ppmval',"children")],[Input('graph-update', 'n_intervals'),Input('demo-dropdown', 'value')])
    def update_graph_scatter(input_data,value):
        
        #prev = r.get()
        #if(input_data!=prev):
            #empty_graph(X,Y,input_data)
            #q.queue.clear()
            #t.queue.clear()

        r.put(input_data)

        ppmval = q.get()
        X.append(X[-1]+1)
        Y.append(ppmval)
        
        curr_ppm = daq.LEDDisplay( id='my-LED-display',
                                label="PPM",
                                value=ppmval,backgroundColor="rgba(0,0,0,0)",color="red",style={'align':'center',},),
        
        size = list(Y)
        if value == 'Bubble':
            data=go.Scatter(
            x=list(X),
            y=list(Y),
            name = 'PPM',
            mode='markers',
            marker=dict(
                color=['rgb(255, 128, 128)', 'rgb(255, 159, 128)', 'rgb(255, 191, 128)', 'rgb(255, 223, 128)', 'rgb(255, 255, 128)', 'rgb(191, 255, 128)','rgb(159, 255, 128)','rgb(128, 255, 128)','rgb(128, 255, 159)','rgb(128, 255, 191)','rgb(128, 255, 223)','rgb(128, 255, 255)','rgb(128, 223, 255)','rgb(128, 191, 255)','rgb(128, 128, 255)','rgb(223, 128, 255)','rgb(255, 128, 223)','rgb(255, 128, 191)','rgb(255, 128, 159)','rgb(255, 128, 128)',],
                size=[x /20 for x in list(Y)],
                opacity = [0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7],
                sizeref=2.*max(size)/(40.**2),
                ),
            fill='none',
                )
        if value == 'Line':
            data = go.Scatter(
                    x=list(X),
                    y=list(Y),
                    name='PPM',
                    mode= 'lines',
                    fill='tonexty',
                    )
        return [{'data': [data],'layout' : go.Layout(xaxis={'title':'TIME (seconds) ', 'showgrid':False,'range':[min(X),(max(X)+2)],'color':'white'},
                yaxis={'range':[(min(Y)-50),(max(Y)+100)],'title':'PPM', 'showgrid':False,'color':'white'},plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = 'rgba(0,0,0,0)',)} , curr_ppm]
        
        
        
    @app.callback([Output('sys-graph', 'figure'),Output('ram-used-div',"children")],[Input('graph-update2', 'n_intervals')])
    def update_graph_scatter2(n_intervals):
            
            system_usage = t.get()
            cpu=system_usage[0]
            total_ram = system_usage[1]
            used_ram = system_usage[2]
            disk_pct = system_usage[3]
            
            U.append(U[-1]+1)
            V.append(disk_pct)
            
            A.append(A[-1]+1)
            B.append(cpu)
            
            fig.append_trace(go.Scatter(x=list(A),y=list(B),name='CPU',mode= 'lines',marker_color='rgb(179, 179, 255)',fill='tonexty'),1,1)
            fig.append_trace(go.Scatter(x=list(U),y=list(V),name='Disk',mode= 'lines',marker_color='rgb(217, 179, 255)',fill='tonexty'),1,2)
            fig.update_layout(height=500, width=1600, title_text="System Usage",showlegend=False,paper_bgcolor = 'rgba(0,0,0,0)',plot_bgcolor = 'rgba(0,0,0,0)',font_color='white')
            fig.update_xaxes(gridcolor='rgba(0,0,0,0)',title_text="Percentage (%)")
            fig.update_yaxes(gridcolor='rgba(0,0,0,0)',title_text="Time (seconds)")
            
            new_val = html.P(f'{used_ram} of {total_ram} GB '  , style={'fontSize':35,'margin-left':'40%'},id="ram_used_val")
            
            return [fig , new_val]
        
    @app.callback(Output('live-update-graph-bar', 'figure'), [Input('interval-component4', 'n_intervals')])
    def update_graph_bar(n_intervals2):
        
        agg_vals = agg_rec.get()
        M.append(agg_vals[0])
        M.append(agg_vals[2])
        M.append(agg_vals[1])
        data_bar = go.Bar(
                x=list(M),
                y=['Min', 'Avg', 'Max'],
                orientation='h',
                text=list(M),
                marker=dict(color=['rgb(0, 204, 204)','rgb(140, 26, 255)','rgb(255, 26, 83)']
                            #color=['#df5e5e','#b60808','#e7553b']
                            ),
                textposition='auto')
        return {'data': [data_bar],'layout' : go.Layout(xaxis={'title':'PPM', 'showgrid':False,'color':'white'},yaxis={'title':'Category', 'showgrid':False,'color':'white'},plot_bgcolor = 'rgba(0,0,0,0)',
    paper_bgcolor = 'rgba(0,0,0,0)',)}
        
        
        
if __name__ == "__main__":

    # creating thread 
    q = queue.Queue()
    r = queue.Queue()
    t = queue.Queue()
    docker_image = queue.Queue()
    pr = queue.Queue()
    agg_rec = queue.Queue()
    r.put('HSR')
    pr.put('HSR')

    t1 = threading.Thread(target=dash_thread ,args=(q,r,t,pr,docker_image,agg_rec))
    t2 = threading.Thread(target=graph_info ,args=(q,t))
    t3 = threading.Thread(target=user_ch , args=(pr,))
    t4 = threading.Thread(target=docker_data , args=(docker_image,))
    t6 = threading.Thread(target=rec_agg , args=(agg_rec,))

    t1.start()
    t3.start()
    t2.start()
    t4.start()
    t6.start()
    
    app.run_server(debug=True,host='0.0.0.0')
