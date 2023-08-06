#!/usr/bin/python3
# ПРИМЕР ВЫВОДИТ ТЕКУЩИЙ КУРС ДОЛЛАРА США
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

disp.clear();

# Указываем двоеточию не мигать (если оно выводится на индикатор).
disp.blink(0, False)

try:

    while True:

        usd = c.get_rate('USD', 'RUB')
        t = "US:"+str(usd)

        # Выводим значения
        #disp.print(usd, RIGHT, POS4)
        disp.print(t, RIGHT, POS4)
        sleep(1)

except:

    # Очищаем дисплей если сценарий был прерван из-за исключения
    disp.clear()
