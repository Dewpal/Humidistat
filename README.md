# Dewpal Software

## Humidity controller 
### Hardware components
* Combined humidity and temperature sensor (DHT22)
* 8 channel 5V relay board
* Humidifier

![Overview](HumidityController/Figures/experimentalSetupIGem.png)

### Software
* __bangBangController.py__ implements a multithread controller for the system discussed above

* __DHTxx.py__ provides hardware/software interfaces for the humidity sensors using adafruit software

* __DHTlog__ is a simple HTML page displaying the humidity and temperature.
