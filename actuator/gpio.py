import time

import settings

# if settings.EMULATE_GPIO:
#     from RPiSim import GPIO
# else:
#     try:
#         import RPi.GPIO as GPIO
#     except RuntimeError:
#         print('ERROR: importing RPi.GPIO! This is probably because you need superuser privileges.')

from gpiozero import LED, Device
from gpiozero.pins.mock import MockFactory


class GPIOActuator:
    def __init__(self, event_channel):
        if settings.EMULATE_GPIO:
            Device.pin_factory = MockFactory()

        self.pin = LED(settings.GPIO_TAP_PIN)
        self.event_channel = event_channel
        self.event_channel.subscribe('payment', self.pour)
        # self.event_channel.publish('payment', 'test')
        print("GPIO SETUP")
        pass

    def pour(self, hash):
        self.pin.on()
        print("GPIO HIGH")
        time.sleep(1)
        self.pin.off()
        print("GPIO LOW")
