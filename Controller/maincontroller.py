from Controller.Payments.paymentcontroller import PaymentController
from Controller.acutator.beerTap import BeerTap
from util.EventChannel import EventChannel


class MainController:
    def __init__(self):
        self.eventChannel = EventChannel()
        self.paymentController = PaymentController(self.eventChannel)
        self.beer_tap = BeerTap(self.eventChannel)

