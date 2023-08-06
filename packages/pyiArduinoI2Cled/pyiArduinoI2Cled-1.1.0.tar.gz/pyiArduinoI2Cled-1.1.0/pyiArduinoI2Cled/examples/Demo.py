#!/usr/bin/python3
# ПРИМЕР ВЫВОДИТ ТЕКУЩИЙ КУРС ДОЛЛАРА США
# Необходима установленная библиотека forex-python
# pip3 install forex-python

from forex_python.converter import CurrencyRates
from pyowm.owm import OWM
from datetime import datetime
from time import sleep

# Подключаем библиотеку для работы с индикатором I2C-flash.
from pyiArduinoI2Cled import *

# Объявляем объект библиотеки forex_python
c = CurrencyRates()
# Объявляем объект библиотеки pyiArduinoI2Cled, указывая адрес модуля на шине I2C.
disp = pyiArduinoI2Cled(0x09)


# Объект OpenWeatherMap с ключом
owm = OWM('3c92aad5b5e883d00a1843310dc98077')

# Объект менеджера OpenWeatherMap
mgr = owm.weather_manager()

# Если объявить объект без указания адреса, то адрес будет найден автоматически.
#disp = pyiArduinoI2Cled()

disp.clear();

# Указываем двоеточию не мигать (если оно выводится на индикатор).
disp.blink(0, False)

try:

    while True:

        observation = mgr.weather_at_place("Moscow,ru").weather
        #one_call = mgr.one_call(lat=55.7512, lon=37.6184)
        temp = observation.temp
        tMoscow = 0
        for value in temp.items():
            tMoscow = value[1]
            break
        tMoscow -= 273.15

        w = round(tMoscow)

        # Получаем курсы валют
        usd = c.get_rate('USD', 'RUB')
        eur = c.get_rate('EUR', 'RUB')
        t = "US:" + str(usd)
        s = "EU:" + str(eur)

        # Выводим значения
        disp.print(t, RIGHT, POS4)
        print(t)
        sleep(1)
        disp.print(s, RIGHT, POS4)
        print(s)
        sleep(1)
        disp.print(w, LEFT, TEMP)
        print(w)
        sleep(1)

except:

    # Очищаем дисплей если сценарий был прерван из-за исключения
    disp.clear()
