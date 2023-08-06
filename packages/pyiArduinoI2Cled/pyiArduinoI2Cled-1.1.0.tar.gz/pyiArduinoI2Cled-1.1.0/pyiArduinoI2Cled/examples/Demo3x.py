#!/usr/bin/python3
# ПРИМЕР ВЫВОДИТ ТЕКУЩИЙ КУРС ДОЛЛАРА США, ЕВРО И ТЕМПЕРАТУРУ В МОСКВЕ
# Необходима установленная библиотека forex-python и pyowm
# pip3 install forex-python
# pip3 install pyowm

from forex_python.converter import CurrencyRates
from pyowm.owm import OWM
from datetime import datetime
from time import sleep

OWMKEY = 'ВАШ КЛЮЧ OWM'
# Подключаем библиотеку для работы с индикатором I2C-flash.
from pyiArduinoI2Cled import *

# Объявляем объект библиотеки forex_python
c = CurrencyRates()

# Объявляем объект библиотеки pyiArduinoI2Cled, указывая адрес модуля на шине I2C.
disp1 = pyiArduinoI2Cled(0x09, NO_BEGIN)
disp2 = pyiArduinoI2Cled(0x0a, NO_BEGIN)
disp3 = pyiArduinoI2Cled(0x0b, NO_BEGIN)

#print('after obj')
#disp1.setPull

# Объект OpenWeatherMap с ключом
owm = OWM(OWMKEY)

# Объект менеджера OpenWeatherMap
mgr = owm.weather_manager()

while not disp1.begin():
    print("waiting module 1")
    sleep(.5)
    pass
while not disp2.begin():
    print("waiting module 2")
    sleep(.5)
    pass
while not disp3.begin():
    print("waiting module 3")
    sleep(.5)
    pass

disp1.clear()
disp2.clear()
disp3.clear()

# Указываем двоеточию не мигать (если оно выводится на индикатор).
disp1.blink(0, False)
disp2.blink(0, False)
disp3.blink(0, False)

try:

    while True:

        observation = mgr.weather_at_place("Moscow,ru").weather
        one_call = mgr.one_call(lat=55.7512, lon=37.6184)
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
        disp1.print(t, RIGHT, POS4)
        disp2.print(s, RIGHT, POS4)
        disp3.print(w, LEFT, TEMP)
        sleep(10)

except:

    # Очищаем дисплей если сценарий был прерван из-за исключения
    disp1.clear()
    disp2.clear()
    disp3.clear()
    disp1.reset()
    disp2.reset()
    disp3.reset()
