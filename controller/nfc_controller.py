from nfc import ContactlessFrontend
from nfc.clf import RemoteTarget
from nfc.tag import Tag

class NfcController:
    def __init__(self):
        self.__stopped = True

    def listen(self):
        # TODO: Figure out how to get the path
        with ContactlessFrontend('usb') as clf:
            while self.__stopped == False:
                print("NfcController.listen: start connecting to NFC.")
                has_connected = clf.connect(rdwr={
                    'on-discover': self.on_discover,
                    'on-connect': self.on_connect,
                    'on-release': self.on_release,
                    'beep-on-connect': True,
                })
                print("NfcController.listen: done connecting to NFC. has connected: ", has_connected)

    def on_discover(self, target: RemoteTarget):
        print("NfcController.on_discover: ", target)
        return True

    def on_connect(self, tag: Tag):
        print("NfcController.on_connect: ", tag)

        # return true to make `clf.connect` wait until card is released.
        # return false to make `clf.connect` return immediately
        return True

    def on_release(self, tag: Tag):
        print("NfcController.on_release: ", tag)
