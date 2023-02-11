import json
import logging

import aiohttp as aiohttp
import sseclient
import urllib3

import settings
from controller.lightning_backend.lightning_backend_interface import LightningBackendInterface
from model.invoice import Invoice


def with_urllib3(url, headers):
    """Get a streaming response for the given event feed using urllib3."""

    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False, headers=headers)


class LNBits(LightningBackendInterface):

    def __init__(self):
        self.base_url = settings.LNBITS_BASE_URL
        self.invoice_key = settings.LNBITS_INVOICE_KEY

    async def get_invoice(self, price: int) -> Invoice:
        endpoint = 'api/v1/payments'
        data = {"out": False, "amount": price, "memo": 'LNBeerTAP', "unit": 'sat',
                "internal": False}
        headers = {
            'X-Api-Key': self.invoice_key
        }
        data = await self._post(endpoint, data, headers)
        logging.debug(data)
        return Invoice(**data)

    async def check_for_payments(self, callback) -> None:
        headers = {'Accept': 'text/event-stream', 'x-api-key': self.invoice_key}
        url = self.base_url + 'api/v1/payments/sse'
        response = with_urllib3(url, headers)
        client = sseclient.SSEClient(response)
        for event in client.events():
            logging.debug(f'Event: {event.data}')
            if event.event == 'ping':
                continue
            try:
                payment = json.loads(event.data)
                if not payment['pending']:
                    logging.info("Payment received")
                    await callback(payment['payment_hash'])

            except Exception as e:
                logging.error(e)
                pass

    async def _post(self, endpoint, data, headers) -> any:
        async with aiohttp.ClientSession() as session:
            try:
                logging.debug(f"Posting to: {self.base_url + endpoint}")
                async with session.post(self.base_url + endpoint, json=data, headers=headers) as response:
                    if int(str(response.status)[:1]) == 2:
                        return await response.json()
                    else:
                        logging.error(f'connection error: {response.status}')
            except aiohttp.ClientConnectorError as e:
                logging.error(e)

    async def get_price_in_sats(self, price) -> int:
        endpoint = 'api/v1/conversion'
        data = {
            "from": "eur",
            "amount": price,
            "to": "sat"
        }
        headers = {}
        data = await self._post(endpoint, data, headers)
        return data['sats']
