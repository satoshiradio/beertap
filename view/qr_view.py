import tkinter as tk
import qrcode
from PIL import ImageTk


class QRView(tk.Frame):
    def __init__(self, root, event_channel):
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="top")
        self.event_channel = event_channel
        self.event_channel.subscribe('INVOICE', self.update_qr)
        tk.Label(self, text="This is the QR page").pack(side="top", fill="x", pady=10)

    def update_qr(self, invoice):
        self.generate_qr(invoice)
        print(invoice)
        pass

    def generate_qr(self, invoice):
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=1
        )
        qr.add_data(invoice)
        qr.make(fit=True)
        img = qr.make_image(
            fill_color='#201200',
            back_color='#FF9900'
        )
        #
        #
        img_element = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 150, image=img_element)
        self.canvas.image = img_element
        self.update()
