#!/usr/bin/python

#import RPi.GPIO as GPIO
#import Adafruit_DHT
import pandas as pd
import datetime
import time
import threading
try:
    import Queue
except:
    import queue as Queue

class virtualSystem:
    def __init__(self,humidityFrame):
        self.humidityFrame=humidityFrame
        self.dt=10
    def read_retry(self,sensor, sensorPin):
        humidity = (100-self.humidityFrame[0]+self.humidityFrame[1])/self.dt
        temperature = 25
        self.humidityFrame.pop()
        self.humidityFrame.insert(0, humidity)
        return self.humidityFrame[0], temperature

class Controller:
    def __init__(self,relayPin):
        self.Ts=1   # (s) sampling time
        self.LL=90  # lower limit humidity
        self.relayPin=relayPin
        self.Time=0
    def run(self):
        global stopTime
        global q
        while time.clock() < stopTime:
            if abs(time.clock()-self.Time) >= self.Ts:
                humidity=q.get()    # take from queue
                q.put(humidity)     # put it back as there is no .peek() method apparently
                if humidity <= self.LL:
                    #GPIO.output(relayPin,GPIO.LOW)
                    print('Humidifier: on')
                else:
                    #GPIO.output(relayPin,GPIO.HIGH)
                    print('Humidifier: off')
                self.Time=time.clock()
                print('Controller time: '+ str(self.Time))

class Sensor:
    def __init__(self,sensorPin,sensor,Ts,sensorObject):
        global stopTime
        self.Ts=Ts  # (s) sampling time
        self.sensorPin=sensorPin
        self.sensor=sensor
        self.i=0
        self.sensorObject=sensorObject
        self.Time=0
        self.f=open('test','w')
        self.f.write('Time, Temperature, Humidity, relative Time \n')

    def run(self):
        global q
        global stopTime
        while time.clock() < stopTime:
            if abs(time.clock()-self.Time) >= self.Ts:
                humidity, temperature = v.read_retry(self.sensor, self.sensorPin) # change to
                self.f.write(str(datetime.datetime.now()) + ',' + str(temperature) + ',' + str(humidity) + ',' + str(time.clock()) + '\n')
                self.i+=1
                void=q.get()
                q.put(humidity)
                self.Time=time.clock()
                print('Sensor time: '+ str(self.Time))
        self.f.close()
        return ()

if __name__ == '__main__':

    # Initialisation
    stopTime=60                 # (s)
    humidityFrame=[40, 40] # current humidity and previous humidity
    q=Queue.Queue(1)
    q.put(40)

    # Initialising GPIOs of the rasberryPi
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(relayPin,GPIO.OUT)
    #GPIO.output(relayPin,GPIO.HIGH) # K1 is off

    # Creating objects
    c=Controller(relayPin=26)
    v=virtualSystem(humidityFrame=humidityFrame)    # for virtual System

    # v=Adafruit_DHT()                              # for real System
    s=Sensor(sensorPin=21,sensor='None',Ts=v.dt,sensorObject=v)         # sensor normally Adafruit_DHT.DHT22

    # Main multithread program
    ct=threading.Thread(target=c.run,args=())
    st=threading.Thread(target=s.run,args=())

    print('Starting sensor thread')
    st.start()

    print('Starting controller thread')
    ct.start()

   # data=pd.concat([data, In], axis=1)
   # with open("/media/pi/715F-106E/IDexperimentoutput.csv", "w") as f:
   #     data.to_csv(f, header=True, index=False)

    # Controlled shutdown
#    GPIO.cleanup()
