import asyncio
import tkinter as tk
import qrcode
from PIL import ImageTk, Image


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

    def _on_payment(self, invoice):
        paid_label = tk.Label(self.root, text="PAID")
        paid_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def update_qr(self, invoice):
        self.generate_qr(invoice)
        print(invoice)
        pass

    def generate_qr(self, invoice):
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L
        )
        qr.add_data(invoice)
        qr.make(fit=True)
        qr_image = qr.make_image()
        qr_size = round(self.height * 0.8)
        qr_image = qr_image.resize((qr_size, qr_size), Image.ANTIALIAS)
        qr_image_element = ImageTk.PhotoImage(qr_image)
        self.canvas.create_image(self.width / 2, self.height / 2, anchor=tk.CENTER, image=qr_image_element)
        self.canvas.image = qr_image_element
        self.update()
