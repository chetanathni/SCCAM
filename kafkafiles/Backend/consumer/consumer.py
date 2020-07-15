import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import random
import dash_daq as daq
import plotly
import plotly.graph_objs as go
from collections import deque
from kafka import KafkaConsumer,KafkaProducer
import threading ,queue
import json
#Change to External IP
bootstrap_servers = ['34.71.243.135:9092']

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

    print(q.queue)
    print(t.queue)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def dash_thread(q,r,t,out_pr):


    X = deque(maxlen=20)
    X.append(1)
    Y = deque(maxlen=20)
    Y.append(1)


    available_indicators = ['Bangalore North','Bangalore South','Mumbai North', 'Mumbai South']
    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Bangalore North'
                ),
            ],
            style={'width': '40%', 'display': 'inline-block'}),
        ]),
        dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1")
        ),

        dcc.Graph(id='indicator-graphic',style={'width':700}),
        dcc.Interval(id='graph-update',interval=5100),
        dcc.Interval(id='gauge-update',interval=5000),
        html.Div([
        dcc.Input(id="input_text", type="text", placeholder="Enter the filename", debounce=True),
        html.Div(id="output"),]),

        html.Div(id="system_usage", children=[
            ] ),

    ])

    def empty_graph(X,Y,xaxis_column_name):

        out_pr.put(xaxis_column_name)

        Y.clear()
        Y.append(0)
        X.clear()
        X.append(0)

        

    @app.callback(Output('indicator-graphic', 'figure'),Output("loading-output-1", "children"),[Input('xaxis-column', 'value'),Input('graph-update', 'n_intervals')])

    def update_graph(xaxis_column_name,n_inter):
        prev = r.get()
        if(xaxis_column_name!=prev):
            empty_graph(X,Y,xaxis_column_name)
            q.queue.clear()
            t.queue.clear()

        r.put(xaxis_column_name)

        ppmval = q.get()
        X.append(X[-1]+1)
        Y.append(ppmval)

        data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode= 'lines+markers',
        fill = 'tonexty',
        marker={'color': 'red',})

        return {'data': [data],'layout' : go.Layout(xaxis={'title':'TIME', 'showgrid':False,'range':[min(X),max(X)],'color':'black'},yaxis={'range':[min(Y),max(Y)],'title':'PPM', 'showgrid':False,'color':'black'},plot_bgcolor = 'rgba(0,0,0,0)',
paper_bgcolor = 'rgba(0,0,0,0)',)}


    @app.callback(Output('system_usage', 'children'),[Input(component_id='gauge-update',component_property='n_intervals')])
    def update_output(w):
        l_items = t.get()
        cpu_usage = l_items[0]
        total_ram = l_items[1]
        used_ram = l_items[2]
        disk_usage = l_items[3]
        return  daq.Gauge(showCurrentValue=True,id='my-gauge',label="CPU",units="%",max=100,min=0,value=cpu_usage),daq.Gauge(showCurrentValue=True,id='my-gauge2',label="Disk",units="%",max=100,min=0,value=disk_usage ),html.P('Total RAM :{}'.format(total_ram)) , html.P('Used RAM :{}'.format(used_ram))

    @app.callback(Output("output", "children"), [Input("input_text", "value")],)
    def update_filename(input_text):
        docker_image.put(input_text)
        return u'Input File:- {}'.format(input_text)

if __name__ == "__main__":

    # creating thread 
    q = queue.Queue()
    r = queue.Queue()
    t = queue.Queue()
    docker_image = queue.Queue()
    pr = queue.Queue()
    r.put('Bangalore North')
    pr.put('Bangalore North')

    t1 = threading.Thread(target=dash_thread ,args=(q,r,t,pr,docker_image))
    t2 = threading.Thread(target=graph_info ,args=(q,t))
    t3 = threading.Thread(target=user_ch , args=(pr,))
    t4 = threading.Thread(target=docker_data , args=(docker_image,))

    t1.start()
    t3.start()
    t2.start()
    t4.start()
    

    app.run_server(debug=True,host='0.0.0.0')
    # starting thread 2 

    # wait unti
                
