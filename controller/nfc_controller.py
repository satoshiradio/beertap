import logging
import time
from nfc import ContactlessFrontend
from nfc.clf import RemoteTarget
from nfc.tag import Tag
from lnurl import Lnurl
from ndef import Record, UriRecord, TextRecord
from utils.EventChannel import EventChannel
from controller.lnurlw_controller import LnurlwController
from settings import NFC_PATH, NFC_TARGETS

class NfcController:
    def __init__(self, event_channel: EventChannel, lnurlw_controller: LnurlwController):
        self.event_channel = event_channel
        self.lnurlw_controller = lnurlw_controller
        self.stopped = True

    def listen(self):
        self.stopped = False
        with ContactlessFrontend(NFC_PATH) as clf:
            while self.stopped == False:
                logging.info("NfcController.listen: start connecting to NFC.")
                has_connected = clf.connect(rdwr={
                    'targets': NFC_TARGETS,
                    'on-discover': self.on_discover,
                    'on-connect': self.on_connect,
                    'on-release': self.on_release,
                    'beep-on-connect': True,
                })

                print("NfcController.listen: done connecting to NFC. has connected:", has_connected)
                logging.warning("Sleeping 60 seconds to avoid burning cpu on failure.")
                time.sleep(60)

    def stop_listening(self):
        self.stopped = True

    def on_discover(self, target: RemoteTarget):
        logging.info("NfcController.on_discover:", target)
        return True

    def on_connect(self, tag: Tag):
        logging.info("NfcController.on_connect:", tag)

        if tag.ndef is None:
            print("NfcController.on_connect: Tag is not NDEF.")
            return True

        records: list[Record] = tag.ndef.records
        for record in records:
            lnurl = self.extract_lnurl_from_record(record)
            if lnurl is not None:
                logging.info("NfcController.on_connect: lnurl found:", lnurl)
                self.lnurlw_controller.on_lnurlw(lnurl)
                return True

        logging.info("NfcController.on_connect: No lnurl found.")
        # return True to make `clf.connect` wait until card is released.
        # return False to make `clf.connect` return immediately
        return True

    def on_release(self, tag: Tag):
        logging.info("NfcController.on_release: ", tag)

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
