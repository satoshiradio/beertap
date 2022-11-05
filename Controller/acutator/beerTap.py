class BeerTap:
    def __init__(self, channel):
        self.event_channel = channel
        self.event_channel.subscribe('payment', self.tap)

    def tap(self, payment_hash):
        print("LAAT HET BIER MAAR LOPEN!")
