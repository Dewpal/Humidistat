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
    def __init__(self):
        self.humidityFrame=[40, 40] # current and previous humidity
        self.inputFrame=[0, 0] # current and previous control action
        self.dt=10
    def read_retry(self,sensor, sensorPin):
        u=qInput.get()
        qInput.put(u)
        self.inputFrame.pop()
        self.inputFrame.insert(0,u)
        humidity = (100-0.001*self.humidityFrame[0]+0.001*self.inputFrame[0]-0.001*self.inputFrame[1])*2*self.dt+self.humidityFrame[1]
        temperature = 25
        self.humidityFrame.pop()
        self.humidityFrame.insert(0, humidity)
        return self.humidityFrame[0], temperature

class Controller:
    def __init__(self,relayPin,actionLength):
        self.Ts=0.5   # (s) sampling time
        self.LL=90  # lower limit humidity
        self.relayPin=relayPin
        self.Time=0.5
        self.actionLength=actionLength
        self.actionTime=2
        self.cooldownLength=8
        self.cooldownTime=8
    def run(self):
        global stopTime
        global q
        while time.clock() < stopTime:
            if abs(time.clock()-self.Time) >= self.Ts:
                humidity=q.get()    # take from queue
                q.put(humidity)     # put it back as there is no .peek() method apparently
                if (humidity <= self.LL) and (self.actionTime>0):  # control action up
                    #GPIO.output(relayPin,GPIO.LOW)
                    void=qInput.get()
                    qInput.put(1)
                    self.actionTime-=self.Ts
                    self.cooldownTime=self.cooldownLength # reset cooldown
                    print('Humidifier: on')
                elif (self.actionTime<=0) and (self.cooldownTime>=0):                        # cooldownLength control action
                    self.cooldownTime-=self.Ts
                    void=qInput.get()
                    qInput.put(1)
                    print('Humidifier: off' + 'cooldown time: ' + str(self.cooldownTime))
                else:                                             # control action down
                    #GPIO.output(relayPin,GPIO.HIGH)
                    void=qInput.get()
                    qInput.put(0)
                    self.actionTime=self.actionLength # reset control action
                    self.cooldownTime=self.cooldownLength # reset cooldown
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

    # Initialisation of parameters and queues
    stopTime=60                 # (s)
    q=Queue.Queue(1)
    qInput=Queue.Queue(1)
    q.put(40)
    qInput.put(1)


    # Initialising GPIOs of the rasberryPi
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(relayPin,GPIO.OUT)
    #GPIO.output(relayPin,GPIO.HIGH) # K1 is off

    # Creating objects
    c=Controller(relayPin=26, actionLength=2)
    v=virtualSystem()    # for virtual System

    # v=Adafruit_DHT()                              # for real System
    s=Sensor(sensorPin=21,sensor='None',Ts=v.dt,sensorObject=v)         # sensor normally Adafruit_DHT.DHT22

    # Main multithread program
    ct=threading.Thread(target=c.run,args=())
    st=threading.Thread(target=s.run,args=())

    print('Starting sensor thread')
    st.start()

    print('Starting controller thread')
    ct.start()

    # Controlled shutdown
#    GPIO.cleanup()
