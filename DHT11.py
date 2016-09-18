#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import Adafruit_DHT
import plotly
import pandas as pd

# Parse command line parameters.
sensor = Adafruit_DHT.DHT11
pin = 21

# connect to plotly
# plotly.tools.set_credentials_file(username='Beramos', api_key='jemhzjyun0')

# Parameters for data storage
Ts= 1; # sampling time (s)
nStore= 10 # number of datapoints to store
i=1

data= pd.DataFrame({'Time': 0,'Temperature': 0,'Humidity': 0}, columns=['Time','Temperature','Humidity'],index=range(0,nStore-1))

# while True:
for i in range(0,10):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print(temperature)
        print(humidity)
        data.loc[i]=pd.Series({'Time': 0,'Temperature': temperature,'Humidity': humidity})
        
    else:
        print('missed reading')
    print(data)
    time.sleep(Ts)
    i=i+1
