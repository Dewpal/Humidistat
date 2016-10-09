#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT
import pandas as pd
import datetime
import time
import Queue


class virtualSystem:
    def __init__(self,humidityFrame,dt):
        self.humidityFrame=humidityFrame
        self.dt=dt
    return (100-humidity+humidity_prev)/dt

def virtualSystem(humidity, humidity_prev,dt):


class Controller:
    def __init__(self,relayPin):
        self.Ts=1   # (s) sampling time
        self.LL=90  # lower limit humidity
        self.relayPin=relayPin
        def run (self):
            global stopTime
            global q
            while time.clock() < stopTime:
                if time.clock()-Time >= self.Ts:
                    humidity=q.get()
                    q.put(humidity)
                    if #humidity on last step is < then:
                        GPIO.output(relayPin,GPIO.LOW)
                        print('Humidifier: on')
                    else:
                        GPIO.output(relayPin,GPIO.HIGH)
                        print('Humidifier: off')
                    Time=time.clock()
                    print(Controller time:)
                    print(Time) # debugging

class Sensor:
    def __init__(self,sensorPin,sensor):
        global stopTime
        self.Ts=10   # (s) sampling time
        self.sensorPin=sensorPin
        self.sensor=sensor
        self.data=pd.DataFrame({'Time': 0,'Temperature': 0,'Humidity': 0, 'rTime':0}, columns=['Time','Temperature','Humidity','rTime'],index=range(0,round(stopTime/self.Ts)))
        self.i=0
        def run (self):
            global q
            global stopTime
            while time.clock() < stopTime:
                if time.clock()-Time >= self.Ts:
                    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensorPin)
                    self.data.loc[i]=pd.Series({'Time': datetime.datetime.now(),'Temperature': temperature,'Humidity': humidity,'rTime':time.clock()})
                    self.i+=1
                    void=q.get()
                    q.put(humidity)
                    Time=time.clock()
                print(Sensor time:)
                print(Time) # debugging
        return(self.data)
# Global variables
stopTime=60                 # (s)

# Initialise virtualSystem
humidityFrame=[40, 40] # current humidity and previous humidity

if __name__ == "__main__":
    q=Queue.Queue(1)

    c=Controller(relayPin=26)
    s=Sensor(sensorPin=21,sensor=Adafruit_DHT.DHT22)        # normally Adafruit_DHT.DHT22
    v=virtualSystem(humidityFrame=humidityFrame,dt=s.Ts)    # must be the same as the sensor


# Relay setup
relayPin=26 # need to be set at the end
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin,GPIO.OUT)
GPIO.output(relayPin,GPIO.HIGH) # K1 is off

# DHT sensor setup
sensorPin = 21 # needs to be set at the end
sensor = Adafruit_DHT.DHT22



# Initialisation
i=1
Time=0
controlAction= list()


# Controller
for i in range(round(stopTime/Ts)):
    n1=datetime.datetime.now()  # Start timing
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensorPin)

    if humidity < LL & len(controlAction) == 0



            # Set output
        GPIO.output(relayPin,GPIO.LOW)
        print('On')
        GPIO.output(relayPin,GPIO.HIGH)
        print('Off')
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
