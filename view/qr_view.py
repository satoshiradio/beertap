import os
import tkinter as tk

import qrcode
from PIL import ImageTk, Image

from model.invoice import Invoice


class QRView(tk.Frame):
    def __init__(self, root: tk.Tk, event_channel):
        self.root = root
        self.root.update()
        self.height = self.root.winfo_height()
        self.width = self.root.winfo_width()
        tk.Frame.__init__(self, root, width=self.width, height=self.height)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.event_channel = event_channel
        self.event_channel.subscribe('INVOICE', self.update_qr)
        self.event_channel.subscribe('PAYMENT', self._on_payment)

    async def _on_payment(self, invoice):
        self.draw_paid()

    async def update_qr(self, invoice):
        self.generate_qr(invoice)
        pass

    def generate_qr(self, invoice: Invoice):
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L
        )
        qr.add_data(invoice.payment_request)
        qr.make(fit=True)
        qr_image = qr.make_image()
        self._draw_image(qr_image)

    def draw_paid(self):
        image_open = Image.open(os.getcwd() + "/assets/paid.png")
        self._draw_image(image_open)
        return

    def _draw_image(self, image):
        image_size = round(self.height * 0.8)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.width / 2, self.height / 2, anchor=tk.CENTER, image=photo_image)
        self.canvas.image = photo_image
        self.update()
        return
