import os
import tkinter as tk

import qrcode
from PIL import ImageTk, Image

import settings
from model.invoice import Invoice


class QRView(tk.Frame):
    def __init__(self, root: tk.Tk, event_channel):
        self.label = None
        self.root = root
        self.root.config(bg="white")

        self.root.update()
        self.height = self.root.winfo_height()
        self.width = self.root.winfo_width()
        tk.Frame.__init__(self, root, width=self.width, height=self.height)
        image_open = Image.open(os.getcwd() + "/assets/background.jpg")
        self.background_image = ImageTk.PhotoImage(image_open)
        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas = tk.Canvas(self, width=430, height=430)
        self.canvas.config(bg="white", border=0)
        self.canvas.place(x=275, y=25, anchor="nw")
        self.event_channel = event_channel
        self.event_channel.subscribe('INVOICE', self.update_qr)
        self.event_channel.subscribe('PAYMENT', self._on_payment)
        # self.draw_paid()

    async def _on_payment(self, invoice):
        self.draw_paid()
        self.label = tk.Label(self.root, font=("Noto Sans Black", 100))
        self.label.place(x=425, y=175, anchor="nw")
        self.label.config(bg="#ff6422")
        self.draw_countdown(settings.DELAY_AFTER_PAYMENT)

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
        image_open = Image.open(os.getcwd() + "/assets/countdown.png")
        self._draw_image(image_open)
        return

    def draw_background(self):
        image_open = Image.open(os.getcwd() + "/assets/background.jpg")
        self.background_image = ImageTk.PhotoImage(image_open)
        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)

    def _draw_image(self, image):
        image_size = 435
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(215, 215, image=photo_image)
        self.canvas.image = photo_image
        self.update()
        return

    def draw_countdown(self, count):
        self.label['text'] = str(count).zfill(2)
        if count > 0:
            self.root.after(1000, self.draw_countdown, count - 1)
        else:
            self.label.destroy()
