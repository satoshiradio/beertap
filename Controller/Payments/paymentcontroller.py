import asyncio
import importlib

import settings


class PaymentController:
    def __init__(self, channel):
        self.event_channel = channel
        lightning_backend_module = importlib.import_module('Controller.LightningBackend')

        lightning_backend_class = getattr(
            lightning_backend_module, settings.LIGHTNING_BACKEND
        )
        self.loop = asyncio.get_event_loop()
        self.lightning_backend = lightning_backend_class()
        self.check_payments()

    def check_payments(self):
        self.loop.create_task(self.lightning_backend.check_payment(self._on_payment))

    def _on_payment(self, payment_hash: str):
        self.event_channel.publish('payment', payment_hash)
