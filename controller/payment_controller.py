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

    def check_payments(self) -> None:
        self.lightning_backend.check_for_payments(self._on_payment)

    async def _on_payment(self, payment_hash: str) -> None:
        await self.event_channel.publish('PAYMENT', payment_hash)
        await self.generate_invoice()

    async def _on_invoice(self, invoice: Invoice) -> None:
        await self.event_channel.publish('INVOICE', invoice)

    async def generate_invoice(self) -> None:
        price: int = await self.lightning_backend.get_price_in_sats(settings.PRICE_IN_EUROCENTS/100)
        await self._on_invoice(await self.lightning_backend.get_invoice(price))
