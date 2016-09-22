#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

# connect to plotly
plotly.tools.set_credentials_file(username='bramDeJaeg', api_key='jemhzjyun0')

# Relay setup
relayPin=26

GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin,GPIO.OUT)
GPIO.output(relayPin,GPIO.HIGH) # K1 is off

# DHT sensor setup
sensor = Adafruit_DHT.DHT22
sensorPin = 21

# Step response parameters
Ts=8 # sampling time
steplength= 80 # length op step input

# initialising arrays
data= pd.DataFrame({'Time': 0,'Temperature': 0,'Humidity': 0, 'rTime':0}, columns=['Time','Temperature','Humidity','rTime'],index=range(0,steplength/Ts))
i=1
Time=0

GPIO.output(relayPin,GPIO.LOW)

for i in range(steplength/Ts):
    n1=datetime.datetime.now()
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensorPin)
    data.loc[i]=pd.Series({'Time': datetime.datetime.now(),'Temperature': temperature,'Humidity': humidity,'rTime':Time})
    
    n2=datetime.datetime.now()
    elapsedTime=(n2.microsecond-n1.microsecond)/1e6
    i=i+1
    Time=Time+Ts
    if Ts-elapsedTime>0:
        time.sleep(Ts-elapsedTime)

GPIO.cleanup()

plt.plot(data.rTime,data.Temperature,'r',data.rTime,data.Humidity,'b')

trace1=go.Scatter(
  x= data.rTime,
  y= data.Humidity,
  stream=dict( 
      token= "0f1psssxtu",
      maxpoints= 200
      )
)

trace2=go.Scatter(
  x= data.rTime,
  y= data.Temperature,
  stream=dict( 
      token= "0f1psssxtu",
      maxpoints= 200
      )
)

layout = go.Layout(
    title='RPi, DHT-sensor Data'
)
fig=go.Figure(data=[trace1,trace2], layout=layout)

py.plot(fig,filename = 'basic_TH',)
      
