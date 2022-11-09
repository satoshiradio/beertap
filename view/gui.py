import settings
from view.qr_view import QRView


class GUI:
    def __init__(self, root, event_channel):
        self.event_channel = event_channel
        self.root = root
        self.set_screen_size()
        self._frame = None
        self.switch_frame(QRView)

    def switch_frame(self, frame_class) -> None:
        new_frame = frame_class(self.root, self.event_channel)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def set_screen_size(self) -> None:
        self.root.resizable(False, False)
        if settings.FULLSCREEN:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(str(screen_width) + 'x' + str(screen_height))
            self.root.wm_attributes('-type', 'splash')
            self.root.attributes('-fullscreen', True)
        else:
            self.root.geometry('800x480')
