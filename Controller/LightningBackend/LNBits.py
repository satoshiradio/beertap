import requests
import settings


class LNBits:
    def __init__(self):
        pass
        self.base_url = settings.LNBITS_ENDPOINT
        self.invoice_key = settings.LNBITS_INVOICE_KEY

    def generate_invoice(self):
        endpoint = '/api/v1/payments'

        response = requests.post(self.base_url + endpoint,
                                 json={"out": False, "amount": 100, "memo": 'LNBeerTAP', "unit": 'sats',
                                       "internal": False},
                                 headers={
                                     "X-Api-Key": self.invoice_key
                                 })
        print(response.json()['payment_request'])
