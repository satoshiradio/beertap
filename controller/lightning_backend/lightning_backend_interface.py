from abc import ABC, abstractmethod

from model.invoice import Invoice


class LightningBackendInterface(ABC):

    @abstractmethod
    async def get_invoice(self, price: int) -> Invoice:
        raise NotImplementedError

    @abstractmethod
    async def check_for_payments(self, callback):
        raise NotImplementedError

    @abstractmethod
    async def get_price_in_sats(self, price) -> int:
        raise NotImplementedError
