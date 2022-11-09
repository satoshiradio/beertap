import asyncio
import importlib

import settings
from controller.lightning_backend.lightning_backend_interface import LightningBackendInterface
from model.invoice import Invoice


class PaymentController:
    def __init__(self, event_channel):
        self.event_channel = event_channel
        lightning_backend_module = importlib.import_module('controller.lightning_backend')

        lightning_backend_class = getattr(
            lightning_backend_module, settings.LIGHTNING_BACKEND
        )
        self.lightning_backend: LightningBackendInterface = lightning_backend_class()

    def check_payments(self):
        asyncio.get_event_loop().create_task(self.lightning_backend.check_for_payments(self._on_payment))

    async def _on_payment(self, payment_hash: str):
        await self.event_channel.publish('PAYMENT', payment_hash)
        await self.generate_invoice()

    async def _on_invoice(self, invoice: Invoice):
        await self.event_channel.publish('INVOICE', invoice)

    async def generate_invoice(self):
        price: int = await self.lightning_backend.get_price_in_sats()
        await self._on_invoice(await self.lightning_backend.get_invoice(price))
