import asyncio
import threading
from actuators.gpio import GPIOActuator
from controller.payment_controller import PaymentController
from controller.nfc_controller import NfcController
from controller.lnurlw_controller import LnurlwController
from utils.EventChannel import EventChannel

class App:
    def __init__(self):
        self.event_channel = EventChannel()
        self.paymentController = PaymentController(self.event_channel)
        self.actuator = GPIOActuator(self.event_channel)
        self.lnurlwController = LnurlwController(self.event_channel)
        self.nfcController = NfcController(self.event_channel, self.lnurlwController)

    async def exec(self):
        await self.paymentController.generate_invoice()
        self.paymentController.check_payments()
        threading.Thread(target=self.nfcController.listen()).start()
