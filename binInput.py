#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT
import pandas as pd
import datetime
import time

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
steplength= 40 # length op step input

# initialising arrays
data= pd.DataFrame({'Time': 0,'Temperature': 0,'Humidity': 0, 'rTime':0}, columns=['Time','Temperature','Humidity','rTime'],index=range(0,steplength/Ts))
i=1
Time=0
In=pd.read_csv('bininp.csv',squeeze=True, header=0)

for i in range(steplength/Ts):
    n1=datetime.datetime.now()  # Start timing

    if In[i] == 1:   # Set output
        GPIO.output(relayPin,GPIO.LOW)
        print('On')
    else:
        GPIO.output(relayPin,GPIO.HIGH)
        print('Off')
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensorPin)
    data.loc[i]=pd.Series({'Time': datetime.datetime.now(),'Temperature': temperature,'Humidity': humidity,'rTime':Time})
    i=i+1
    Time=Time+Ts
    n2=datetime.datetime.now()
    elapsedTime=(n2.microsecond-n1.microsecond)/1e6
    
    if Ts-elapsedTime>0:
        time.sleep(Ts-elapsedTime)

data=pd.concat([data, In], axis=1)
with open("/media/pi/715F-106E/IDexperimentoutput.csv", "w") as f:
    data.to_csv(f, header=True, index=False)

GPIO.cleanup()
