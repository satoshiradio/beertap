import asyncio

from gpiozero import LED, Device
from gpiozero.pins.mock import MockFactory

import settings


def calculate_poor_time_in_seconds() -> int:
    return (60/settings.MILLILITER_PER_HOUR*settings.MILLILITER_PER_GLASS*60)+settings.TAP_TIME_ADJUSTMENT_SECONDS


class GPIOActuator:
    def __init__(self, event_channel):
        if settings.EMULATE_GPIO:
            Device.pin_factory = MockFactory()

        self.pin = LED(settings.GPIO_TAP_PIN)
        self.event_channel = event_channel
        self.event_channel.subscribe('PAYMENT', self._on_payment)
        pass

    async def _on_payment(self, hash) -> None:
        await self.pour()

    async def pour(self) -> None:
        self.pin.on()
        print("GPIO HIGH")
        await asyncio.sleep(calculate_poor_time_in_seconds())
        self.pin.off()
        print("GPIO LOW")


