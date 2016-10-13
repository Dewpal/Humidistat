#!/usr/bin/python
import sys
import time
import datetime
import Adafruit_DHT
import plotly
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# Parse command line parameters.
sensor = Adafruit_DHT.DHT11
pin = 21

# connect to plotly
plotly.tools.set_credentials_file(username='bramDeJaeg', api_key='jemhzjyun0')

# Parameters for data storage
Ts= 1; # sampling time (s)
nStore= 5 # number of datapoints to store
i=1

data= pd.DataFrame({'Time': 0,'Temperature': 0,'Humidity': 0}, columns=['Time','Temperature','Humidity'],index=range(0,nStore-1))

#while True:
for i in range(0,nStore-1):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        data.loc[i]=pd.Series({'Time': datetime.datetime.now(),'Temperature': temperature,'Humidity': humidity}) 
    else:
        print('missed reading')
    print(data)
    time.sleep(Ts)
    i=i+1

trace=go.Scatter(
  x= data.Time,
  y= data.Humidity,
  stream=dict( 
      token= "0f1psssxtu",
      maxpoints= 200
      )
)

layout = go.Layout(
    title='RPi, DHT-sensor Data'
)
fig=go.Figure(data=[trace], layout=layout)

py.plot(fig,filename = 'basic_TH',)
      
stream=py.Stream('0f1psssxtu')
stream.open()

##while True:
##    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
##    i=i+1
##    stream.write({'x': datetime.datetime.now(), 'y': humidity})
##    time.sleep(Ts)
