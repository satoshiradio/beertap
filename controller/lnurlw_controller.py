import requests

class LnurlwController:
    def __init__(self, event_channel) -> None:
        self.event_channel = event_channel
        event_channel.subscribe('INVOICE', self.on_invoice)
        event_channel.subscribe('LNURLW', self.on_invoice)
    
    def on_invoice(self, invoice):
        self.invoice = invoice
    
    def on_lnurlw(self, lnurlw):
        try:
            resp1 = requests.get(lnurlw)
            json1 = resp1.dict()
            callback = json1['callback']
            k1 = json1['k1']
            reason1 = json1['reason']
            status1 = json1['status']
            if status1 == 'ERROR':
                # TODO: Show feedback to user, server returned error
                print('LnurlwController.on_lnurlw: Server returned error: ', reason1)
                return
            
            if callback is None or not isinstance(callback, str) or k1 is None or not isinstance(k1, str):
                print('LnurlwController.on_lnurlw: Server response invalid: ', json1)
            
            sep = '?'
            if callback.find('?') > 0:
                sep = '&'
            
            url = callback + sep + 'k1=' + k1 + "&pr=" + self.invoice
            resp2 = requests.get(url)
            json2 = resp2.dict()
            status2 = json2['status']
            if status2 == 'OK':
                # TODO: Maybe show to the user that they're going to initiate the payment now. But maybe not, time will be short before it will actually be paid
                return
            
            if status2 == 'ERROR':
                # TODO: Show feedback to user, server returned error
                print('LnurlwController.on_lnurlw: Server returned error: ', json2['reason'])
            
            print('server sent invalid response. doing nothing.', json2)
        except:
            # TODO: Show something to the user, this is a failure on our side.
            pass

    
