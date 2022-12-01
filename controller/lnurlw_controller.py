import requests
from utils.EventChannel import EventChannel
from model.invoice import Invoice

class LnurlwController:
    def __init__(self, event_channel: EventChannel) -> None:
        self.event_channel = event_channel
        event_channel.subscribe('INVOICE', self.on_invoice)
        event_channel.subscribe('LNURLW', self.on_lnurlw)

    def on_invoice(self, invoice: Invoice):
        self.invoice = invoice
    
    def on_lnurlw(self, lnurlw: str):
        print('LnurlwController.on_lnurlw')
        try:
            print('sending lnurlw get request 1 to:', lnurlw)
            resp1 = requests.get(lnurlw)
            json1 = resp1.json()
            print('LnurlwController.on_lnurlw: got response1:', json1)
            callback = json1.get('callback')
            k1 = json1.get('k1')
            reason1 = json1.get('reason')
            status1 = json1.get('status')
            if status1 == 'ERROR':
                # TODO: Show feedback to user, server returned error
                print('LnurlwController.on_lnurlw: Server returned error:', reason1)
                return

            if callback is None or not isinstance(callback, str) or k1 is None or not isinstance(k1, str):
                print('LnurlwController.on_lnurlw: Server response invalid:', json1)
            
            sep = '?'
            if callback.find('?') > 0:
                sep = '&'
            
            url = callback + sep + 'k1=' + k1 + "&pr=" + self.invoice.payment_request
            print('sending lnurlw get request 1 to:', url)
            resp2 = requests.get(url)
            json2 = resp2.json()
            print('LnurlwController.on_lnurlw: got response2:', json2)
            status2 = json2.get('status')
            if status2 == 'OK':
                # TODO: Maybe show to the user that they're going to initiate the payment now. But maybe not, time will be short before it will actually be paid
                return
            
            if status2 == 'ERROR':
                # TODO: Show feedback to user, server returned error
                reason2 = json2.get('reason')
                print('LnurlwController.on_lnurlw: Server returned error reason:', reason2)
            
            print('server sent invalid response. doing nothing.', json2)
        except Exception as e: 
            print('LnurlwController.on_lnurlw error:', e)
            # TODO: Show something to the user, this is a failure on our side.

    
