import asyncio
import logging
from time import perf_counter

from gpiozero import LED, Device, OutputDevice
from gpiozero.pins.mock import MockFactory

import settings


def calculate_poor_time_in_seconds() -> int:
    return settings.TAP_TIME


class GPIOActuator:
    def __init__(self, event_channel):
        if settings.EMULATE_GPIO:
            Device.pin_factory = MockFactory()

        self.pin = OutputDevice(settings.GPIO_TAP_PIN, active_high=False, initial_value=False)
        self.event_channel = event_channel
        self.event_channel.subscribe('PAYMENT', self._on_payment)
        pass

    async def _on_payment(self, hash) -> None:
        await asyncio.sleep(settings.DELAY_AFTER_PAYMENT)
        await self.pour()

    async def pour(self) -> None:
        self.pin.on()
        logging.info("GPIO HIGH")
        await asyncio.sleep(calculate_poor_time_in_seconds())
        self.pin.off()
        logging.info("GPIO LOW")
