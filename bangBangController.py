#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT
import pandas as pd
import datetime
import time
import threading
try:
    import Queue
except:
    import queue as Queue

class virtualSystem:
    def __init__(self):
        self.humidityFrame=[40, 40] # current and previous humidity
        self.inputFrame=[0, 0] # current and previous control action
        self.dt=10
    def read_retry(self,sensor, sensorPin):
        u=qInput.get()
        qInput.put(u)
        self.inputFrame.pop()
        self.inputFrame.insert(0,u)
        humidity = (100-0.001*self.humidityFrame[0]+0.001*self.inputFrame[0]-0.001*self.inputFrame[1])*2*self.dt+self.humidityFrame[1] # first order difference equation
        temperature = 25 # constant temperature
        self.humidityFrame.pop()
        self.humidityFrame.insert(0, humidity)
        return self.humidityFrame[0], temperature

class Controller:
    def __init__(self,relayPin,GPIO):
        self.Ts=5   # (s) sampling time controller
        self.LL=95  # lower limit humidity
        self.Time=0 # initialisation
        self.relayPin=relayPin
	    self.GPIO=GPIO
    def run(self):
        global stopTime
        global q
        while time.clock() < stopTime:
            if abs(time.clock()-self.Time) >= self.Ts:
                humidity=q.get()            # take from queue
                q.put(humidity)             # put it back as there is no .peek() method apparently
                if (humidity <= self.LL):   # control action up
                    GPIO.output(self.relayPin,self.GPIO.LOW)
                    void=qInput.get()
                    qInput.put(1)
                    print('Humidifier: on')
                else:                       # control action down
                    GPIO.output(self.relayPin,self.GPIO.HIGH)
                    void=qInput.get()
                    qInput.put(0)
                    print('Humidifier: off')
                self.Time=time.clock()
	GPIO.output(self.relayPin,self.GPIO.HIGH)

class Sensor:
    def __init__(self,sensorPin,sensor,Ts,sensorObject,fileName):
        global stopTime
        self.sensorPin=sensorPin
        self.sensor=sensor
        self.Ts=Ts  # (s) sampling time
        self.sensorObject=sensorObject
        self.f=open(fileName,'w')
        self.f.write('Time, Temperature, Humidity, relative Time \n')
        self.i=0    # initialisation
        self.Time=0 # initialisation

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

    # Initialisation of parameters and queues
    stopTime=18000          # run program for stopTime seconds
    q=Queue.Queue(1)        # controller/sensor queue
    qInput=Queue.Queue(1)   # controller/virtualsystem queue

    q.put(40)
    qInput.put(1)

    # Initialising GPIOs of the Rasberry Pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26,GPIO.OUT)
    GPIO.output(26,GPIO.HIGH) # K1 is off

    c=Controller(relayPin=26,GPIO=GPIO) # controller object
    s=Sensor(sensorPin=21,sensor=v.DHT22,Ts=10,sensorObject=Adafruit_DHT,fileName='data12_9')       # sensorObject = Adafruit_DHT when running with hardware attached,

    # Main program
    ct=threading.Thread(target=c.run,args=())
    st=threading.Thread(target=s.run,args=())

    print('Starting sensor thread')
    st.start()

    print('Starting controller thread')
    ct.start()

    # Controlled shutdown when threads are finished
    st.join()
    ct.join()
    GPIO.cleanup()
