from nfc import ContactlessFrontend
from nfc.clf import RemoteTarget
from nfc.tag import Tag
from lnurl import Lnurl
from ndef import Record, UriRecord, TextRecord

class NfcController:
    def __init__(self, event_channel):
        self.event_channel = event_channel
        self.stopped = True

    def listen(self):
        # TODO: Figure out how to get the path
        self.stopped = False
        with ContactlessFrontend('usb') as clf:
            while self.stopped == False:
                print("NfcController.listen: start connecting to NFC.")
                has_connected = clf.connect(rdwr={
                    'on-discover': self.on_discover,
                    'on-connect': self.on_connect,
                    'on-release': self.on_release,
                    'beep-on-connect': True,
                })
                print("NfcController.listen: done connecting to NFC. has connected:", has_connected)

    def stop_listening(self):
        self.stopped = True

    def on_discover(self, target: RemoteTarget):
        print("NfcController.on_discover:", target)
        return True

    def on_connect(self, tag: Tag):
        print("NfcController.on_connect:", tag)

        if tag.ndef is None:
            print("NfcController.on_connect: Tag is not NDEF.")
            return True

        records: list[Record] = tag.ndef.records
        for record in records:
            lnurl = self.extract_lnurl_from_record(record)
            if lnurl is not None:
                print("NfcController.on_connect: lnurl found:", lnurl)
                self.event_channel.publish('LNURLW', lnurl)
                return True

        print("NfcController.on_connect: No lnurl found.")
        # return True to make `clf.connect` wait until card is released.
        # return False to make `clf.connect` return immediately
        return True

    def on_release(self, tag: Tag):
        print("NfcController.on_release: ", tag)

    def extract_lnurl_from_record(self, record: Record):
        if isinstance(record, UriRecord):
            ur: UriRecord = record
            return self.extract_lnurl_from_string(ur.iri)
        
        if isinstance(record, TextRecord):
            tr: TextRecord = record
            return self.extract_lnurl_from_string(tr.text)

        try:
            yolo = record.data.decode('utf-8')
            return self.extract_lnurl_from_string(yolo)
        except:
            pass

        return None

    def extract_lnurl_from_string(self, str: str):
        if str is None:
            return None
        
        str = str.strip()
        lower = str.lower()
        if lower.startswith('lnurlw://'):
            t = str.split('://', 1)[1]
            if lower.endswith('.onion'):
                return 'http://' + t
            
            return 'https://' + t
        
        if lower.startswith('https://'):
            return str

        if lower.startswith('http://') and (
            lower.endswith('.onion')
            or lower.find('.onion/') > 0
            or lower.find('.onion?') > 0
        ):
            return str

        try:
            lnurl = Lnurl(str)
            return lnurl.url
        except:
            pass
        
        return None
