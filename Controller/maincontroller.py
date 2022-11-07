import asyncio

from Controller.Payments.paymentcontroller import PaymentController
from actuator.gpio import GPIOActuator
# from Controller.acutator.beerTap import BeerTap
from util.EventChannel import EventChannel
from view.main_window import Window


class MainController:
    def __init__(self):
        self.eventChannel = EventChannel()
        self.actuator = GPIOActuator(self.eventChannel)
        self.window = Window(asyncio.get_event_loop(), self.eventChannel)
        self.paymentController = PaymentController(self.eventChannel)
        self.paymentController.generate_invoice()
        # self.view = MainView(self.eventChannel)
        # self.root = self.view.root

    async def exec(self):
        await self.window.show()

