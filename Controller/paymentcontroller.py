import settings


class PaymentController:
    def __init__(self):
        print("init payment controller")
        settings.LIGHTNING_BACKEND.generate_invoice()
