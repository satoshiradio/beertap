from actuators.gpio import GPIOActuator
from controller.payment_controller import PaymentController
from utils.EventChannel import EventChannel


class App:
    def __init__(self):
        self.event_channel = EventChannel()
        self.paymentController = PaymentController(self.event_channel)
        self.actuator = GPIOActuator(self.event_channel)

    async def exec(self):
        await self.paymentController.generate_invoice()
        self.paymentController.check_payments()
