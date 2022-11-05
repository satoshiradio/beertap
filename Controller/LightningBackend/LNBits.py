import asyncio
import json

import requests
import sseclient
import urllib3

import settings


def with_urllib3(url, headers):
    """Get a streaming response for the given event feed using urllib3."""

    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False, headers=headers)


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

    async def check_payment(self, callback):
        headers = {'Accept': 'text/event-stream', 'x-api-key': self.invoice_key}
        url = self.base_url + 'api/v1/payments/sse/'
        response = with_urllib3(url, headers)
        client = sseclient.SSEClient(response)
        for event in client.events():
            try:
                payment = json.loads(event.data)
                if not payment['pending']:
                    callback(payment['payment_hash'])

            except Exception as e:
                # print(e)
                pass