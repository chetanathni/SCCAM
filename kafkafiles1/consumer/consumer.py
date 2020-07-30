import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import random
import dash_daq as daq
import plotly
import plotly.graph_objs as go
import plotly.tools as tls
from collections import deque
from kafka import KafkaConsumer,KafkaProducer
import threading ,queue
import json

bootstrap_servers = ['kafka:9092']

def docker_data(u):

    topicName3 ='InputImage'
    producer3 = KafkaProducer(bootstrap_servers = bootstrap_servers,api_version=(0,10,0))
    while(1):
        if(u.empty()):
            pass
        else:
            docker_text=u.get()
            producer3.send(topicName3 , docker_text.encode('utf-8'))
            producer3.flush()

def user_ch(in_pr):

    topicName2 ='LocationReq'
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers,api_version=(0,10,0))
    while(1):
        if(pr.empty()):
            pass
        else:
            choice_us=in_pr.get()
            producer.send(topicName2 , choice_us.encode('utf-8'))
            producer.flush()

def graph_info(q,t):

    #topicName = 'filtered'
    topicName = 'sample'
    consumer = KafkaConsumer (topicName, group_id = 'test-consumer-group',bootstrap_servers = bootstrap_servers,api_version=(0,10,0),auto_offset_reset = 'latest',value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    consumer.subscribe(topicName)

    for message in consumer:

        y=message.value
        q.put(y[0])
        t.put(y[1:5])

    print(q.queue)
    print(t.queue)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def dash_thread(q,r,t,out_pr,u):

    places = ['Bangalore','Mumbai','Hyderabad','Delhi']
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
    sticky="top",)

    hello = dbc.Container(
    dbc.Alert("We're still under construction. Our services will begin soon!", color="success"),
    className="p-5",
    style = {'textAlign':'center'},)

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
    style = {'textAlign' : 'center'})
    
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
                      options=[{'label': i, 'value': i} for i in places],
                      value= 'Bangalore',
                      multi=True,
                      style = {'height': '2px', 'width':'900px'},
                  ),
                  html.P(),
                  dcc.Graph(id='live-graph', animate=True,style={'width':900,'align':'center',
                  'plot_bgcolor': '#114111',
                  'paper_bgcolor': '#111671'
                  },),
                  dcc.Interval(id='graph-update',interval=1000),
                  ],
                  style={"width" : "70rem"},),

    dbc.Card([
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
        
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem(".json"), dbc.DropdownMenuItem(".csv"), dbc.DropdownMenuItem(".xls")],
            label="Download Data",
            group=True,
        ),
        html.P(),
        dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Minimum', 'value': 'min'},
            {'label': 'Maximum', 'value': 'max'},
            {'label': 'Average', 'value': 'avg'}
        ],
        value='min',style={'width':'30rem'}
    ),
    html.Div(id='dd-output-container'),
    ],
    vertical=True,
    style = {'height':'120px'},),],style = {'height':'120px','width':'30rem'},),],),],),],)

    jumbo_admin = dbc.Jumbotron([
        dbc.Badge("ADMIN", pill=True, color="warning", className="mr-1"),
          html.Div(id="stats",
          children=[
          dbc.Card(
          [
          dcc.Graph(id='admin-graph', animate=True,),
          dcc.Interval(id='stats-update',interval=1000),
          ],
          style={"width" : "40rem"},),],),],)

    app.layout = html.Div([navbar,hello,jumbotron,jumbo,jumbo_admin,],)



    
    def empty_graph(X,Y,xaxis_column_name):

        out_pr.put(xaxis_column_name)

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


    @app.callback(Output('system_usage', 'children'),[Input(component_id='gauge-update',component_property='n_intervals')])
    def update_output(w):
        l_items = t.get()
        cpu_usage = l_items[0]
        total_ram = l_items[1]
        used_ram = l_items[2]
        disk_usage = l_items[3]
        return  daq.Gauge(showCurrentValue=True,id='my-gauge',label="CPU",units="%",max=100,min=0,value=cpu_usage),daq.Gauge(showCurrentValue=True,id='my-gauge2',label="Disk",units="%",max=100,min=0,value=disk_usage ),html.P('Total RAM :{}'.format(total_ram)) , html.P('Used RAM :{}'.format(used_ram))

    @app.callback(Output("modal-centered", "is_open"),[Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],[State("modal-centered", "is_open")],)
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
    
    @app.callback(Output("output", "children"),[Input("input_text", "value")],)
    def update_output_inputfile(input_text):
        u.put('{}'.format(input_text))
        return u'Input File :{}'.format(input_text)

if __name__ == "__main__":

    # creating thread 
    q = queue.Queue()
    r = queue.Queue()
    t = queue.Queue()
    u = queue.Queue()
    pr = queue.Queue()
    r.put('Bangalore North')
    pr.put('Bangalore North')

    t1 = threading.Thread(target=dash_thread ,args=(q,r,t,pr,u))
    t2 = threading.Thread(target=graph_info ,args=(q,t))
    t3 = threading.Thread(target=user_ch , args=(pr,))
    t4 = threading.Thread(target=docker_data , args=(u,))

    t1.start()
    t3.start()
    t2.start()
    t4.start()

    

    app.run_server(debug=True,host='0.0.0.0')
    # starting thread 2 

    # wait unti
                
