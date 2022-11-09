import asyncio

from gpiozero import LED, Device
from gpiozero.pins.mock import MockFactory

import settings


class GPIOActuator:
    def __init__(self, event_channel):
        if settings.EMULATE_GPIO:
            Device.pin_factory = MockFactory()

        self.pin = LED(settings.GPIO_TAP_PIN)
        self.event_channel = event_channel
        self.event_channel.subscribe('PAYMENT', self._on_payment)
        pass

    async def _on_payment(self, hash):
        await self.pour()

    async def pour(self):
        self.pin.on()
        print("GPIO HIGH")
        await asyncio.sleep(10)
        self.pin.off()
        print("GPIO LOW")
