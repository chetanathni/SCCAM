import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
from kafka import KafkaConsumer,KafkaProducer
import threading ,queue
import plotly
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from collections import deque
import datetime
import time
import json
import dash_daq as daq
import queue,threading
bootstrap_servers = ['34.71.243.135:9092']

def rec_agg(agg_rec):
        topicName5 = 'aggVal'
        consumer5= KafkaConsumer (topicName5, group_id = 'group3', bootstrap_servers = bootstrap_servers, api_version = (0,10,0), auto_offset_reset = 'latest')
        consumer5.subscribe(topicName5)
        for aggval in consumer5:
                agg_val=(aggval.value).decode('utf-8')
                agg_rec.put(agg_val)
              

def send_agg(agg_send):

    topicName4 ='functionName'
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers,api_version=(0,10,0))
    while(1):
        func_text=agg_send.get()
        producer.send(topicName4 , func_text.encode('utf-8'))
        producer.flush()
def docker_data(docker_image):

    topicName3 ='InputImage'
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers,api_version=(0,10,0))
    while(1):
        docker_text=docker_image.get()
        producer.send(topicName3 , docker_text.encode('utf-8'))
        producer.flush()

def user_ch(in_pr):

    topicName2 ='LocationReq'
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers,api_version=(0,10,0))
    while(1):
        choice_us=in_pr.get()
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
places=['Bangalore','Delhi','Mumbai','Hyderabad']
app = dash.Dash(external_stylesheets=[BS])
def dash_thread(q,r,t,pr,docker_image,agg_send,agg_rec):

    X = deque(maxlen=20)
    X.append(1)
    Y = deque(maxlen=20)
    Y.append(1)

    

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="#")),
            dbc.NavItem(dbc.NavLink("About Us", href="#")),
            dbc.NavItem(dbc.NavLink("Products", href="#")),
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
        color="dark",
        dark=True,
        fluid =True,
        sticky="top",
    )
    hello = dbc.Container(
        dbc.Alert("We're still under construction. Our services will begin soon!", color="success"),
        className="p-5",
        style = {'textAlign':'center'},
    )
    jumbotron = dbc.Jumbotron(
        [
            html.P(
                "Welcome to Smart City Control and Management! ",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "We deliver to you the information you need from our sensors ranging from its log data to the analytics that you might need. "
            ),
        ],
        style = {'textAlign' : 'center'}
    )
    jumbo=dbc.Jumbotron(
            [
            dbc.Badge("USER", pill=True, color="warning", className="mr-1"),
            html.Div( id="graph",
            children=[
                    dbc.Row(
                    [
                    dbc.Card(
                    [
                    dcc.Dropdown(
                        id='my_ticker_symbol',
                        options=[{'label': i, 'value': i} for i in places], #places,
                        value= 'Bangalore',#=['Bangalore'],
                        style = {'height': '2px', 'width':'900px'},
                    ),
                    html.P(),
                    dcc.Graph(id='live-graph', animate=True,style={'width':900,'align':'center',
                    'plot_bgcolor': '#114111',
                    'paper_bgcolor': '#111671'
                    },),
                    dcc.Interval(id='graph-update',interval=1000),
                    ],
                    style={"width" : "70rem"},
    ),
    dbc.Card(
    [
    dbc.ButtonGroup(
        [
            dbc.Button("Graph",href="#"),
            #dbc.Button("Upload Function",href="#"),
                    dbc.Button("Upload Function", id="open-centered"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Upload Function"),
                            dbc.ModalBody(
                            [
                                dcc.Input(id="input_text", type="text", placeholder="Enter the filename", debounce=True),
                                html.Div(id="output"),
                            ],
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close", id="close-centered", className="ml-auto"
                                )
                            ),
                        ],
                        id="modal-centered",
                        centered=True,
                    ),
            #dbc.Button("CPU/RAM Usage",href="#"),
            dbc.DropdownMenu(
                [dbc.DropdownMenuItem(".json"), dbc.DropdownMenuItem(".csv"), dbc.DropdownMenuItem(".xls")],
                label="Download Data",
                group=True,
            ),
            html.P(),
            dcc.Dropdown(
            id='aggregate-dropdown',
            options=[
                {'label': 'Minimum', 'value': 'min'},
                {'label': 'Maximum', 'value': 'max'},
                {'label': 'Average', 'value': 'avg'}
            ],
            value='min',style={'width':'25rem'}
        ),
        html.Div(id='aggregate-output-container'),
        ],
        vertical=True,
        style = {'height':'120px'},
    ),
    #html.P("Average:- "),
    ],
    style = {'height':'120px','width':'30rem'},
    ),],),
    ],),],)
    jumbo_admin = dbc.Jumbotron(
    [
    dbc.Badge("ADMIN", pill=True, color="warning", className="mr-1"),
            html.Div(id="cpu",
            children=[
            dbc.Card(
            [
            #dcc.Graph(id='cpu-graph', animate=True,),
            #dcc.Interval(id='cpu-update',interval=1000),
            ],
            style={"width" : "40rem"},),],),
        html.Div(id="ram",
        children=[
        dbc.Card(
        [
        #dcc.Graph(id='ram-graph', animate=True,),
        #dcc.Interval(id='ram-update',interval=1000),
        ],
        style={"width" : "40rem"},
    ),],),],)


    
    @app.callback(
        dash.dependencies.Output('aggregate-output-container', 'children'),
        [dash.dependencies.Input('aggregate-dropdown', 'value')])
    def update_output2(value):
            agg_send.put('{}'.format(value))
            computed_val=agg_rec.get()
            return '{} : {}'.format(value,computed_val)
    @app.callback(
        Output("modal-centered", "is_open"),
        [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
        [State("modal-centered", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
    app.layout = html.Div([navbar,hello,jumbotron,jumbo,jumbo_admin,],)
    @app.callback(Output("output", "children"),[Input("input_text", "value")],)
    def update_output(input_text):
        docker_image.put('{}'.format(input_text))
        return u'Input File:- {}'.format(input_text)

    def empty_graph(X,Y,xaxis_column_name):

        pr.put(xaxis_column_name)

        Y.clear()
        Y.append(0)
        X.clear()
        X.append(0)

    @app.callback(Output('live-graph', 'figure'),[Input('graph-update', 'n_intervals')],[State('my_ticker_symbol','value')])
    def update_graph_scatter(input_data,key):
        prev = r.get()
        if(input_data!=prev):
            empty_graph(X,Y,input_data)
            q.queue.clear()
            t.queue.clear()

        r.put(input_data)

        ppmval = q.get()
        X.append(X[-1]+1)
        Y.append(ppmval)


        data = plotly.graph_objs.Scatter(
                x=list(X),
                y=list(Y),
                name='Scatter',
                mode= 'lines+markers',
                fill='tonexty',
                #marker={'color': 'red' ,}
                )
        return {'data': [data],'layout' : go.Layout(xaxis={'title':'Time (in seconds)', 'showgrid':False,'range':[min(X),max(X)],'color':'white',},
                                                    yaxis={'range':[0,max(Y)+100],'title':'PPM', 'showgrid':False,'color':'white',},
                                                    plot_bgcolor = 'rgba(1,1,0,0)',
                                                    paper_bgcolor = 'rgba(1,1,0,0)',
                                                )}
if __name__ == "__main__":

    # creating thread 
    q = queue.Queue()
    r = queue.Queue()
    t = queue.Queue()
    docker_image = queue.Queue()
    pr = queue.Queue()
    agg_send = queue.Queue()
    agg_rec = queue.Queue()
    agg_send.put('min')
    r.put('Bangalore North')
    pr.put('Bangalore North')

    t1 = threading.Thread(target=dash_thread ,args=(q,r,t,pr,docker_image,agg_send,agg_rec))
    t2 = threading.Thread(target=graph_info ,args=(q,t))
    t3 = threading.Thread(target=user_ch , args=(pr,))
    t4 = threading.Thread(target=docker_data , args=(docker_image,))
    t5 = threading.Thread(target=send_agg , args=(agg_send,))
    t6 = threading.Thread(target=rec_agg , args=(agg_rec,))

    t1.start()
    t3.start()
    t2.start()
    t4.start()
    t5.start()
    t6.start()
    
    app.run_server(debug=True,host='0.0.0.0')
