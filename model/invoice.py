class Invoice:
    def __init__(self, payment_hash, payment_request, checking_id, lnurl_response):
        self.payment_hash: str = payment_hash
        self.payment_request: str = payment_request
        self.checking_id: str = checking_id
        self.lnurl_response: str = lnurl_response
