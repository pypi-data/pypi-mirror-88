# Fake W1 thermometer

**README**

This package wil generate a fake DS18B20 temperature sensor like on a raspberry Pi so developement on other devices is possible without the actual connecting of a temperature sensor. It mimics the behaviour of this sensor. The sensor takes a min and max temperature and oscillates between this given range by 0.1 degrees celcius.

**Version:**
0.1

**Usage:**
Import an instantaniate the class, the class takes an minimum and maximum temperature, an output dir and sensor number. This sensornumber makes it possible to instantaniate a number of sensors. On initialize the class will generate a random temperature between the min and max temperature so you get different readings per sensor. I've added a example.py to give you an idea on how to run this package.

**Author**
This package is created by me, Ted van Roon, if you have any questions don't hesitate to contact me via DM.

**Licence**
This package is licensed under GNU GPLv3.

**Language**
This package is written in Python 3.9, not doing anything fancy, so I think this wil work for Python 3.x.