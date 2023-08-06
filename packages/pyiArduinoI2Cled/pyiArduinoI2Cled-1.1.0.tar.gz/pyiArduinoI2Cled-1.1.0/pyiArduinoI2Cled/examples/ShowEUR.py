#!/usr/bin/python3
# ПРИМЕР ВЫВОДИТ ТЕКУЩИЙ КУРС ЕВРО
# Необходима установленная библиотека forex-python
# pip3 install forex-python

from forex_python.converter import CurrencyRates
from datetime import datetime
from time import sleep

# Подключаем библиотеку для работы с индикатором I2C-flash.
from pyiArduinoI2Cled import *

# Объявляем объект библиотеки forex_python
c = CurrencyRates()
# Объявляем объект библиотеки pyiArduinoI2Cled, указывая адрес модуля на шине I2C.
disp = pyiArduinoI2Cled(0x09)

# Если объявить объект без указания адреса, то адрес будет найден автоматически.
#disp = pyiArduinoI2Cled()

# Указываем двоеточию не мигать (если оно выводится на индикатор).
disp.clear();
disp.blink(0, False)

try:

    while True:

        eur= c.get_rate('EUR', 'RUB')
        t = "EU:"+str(eur)

        # Выводим значения
        disp.print(t, RIGHT, POS4)
        sleep(1)

except:

    # Очищаем дисплей если сценарий был прерван из-за исключения
    disp.clear()
