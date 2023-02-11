import asyncio
from tkinter import *
from functools import wraps
import logging
import os

import telegram_handler
from telegram_handler import TelegramHandler

import settings
from app import App
from view.gui import GUI


async def run_tk(root, interval=0.05):
    """
    Run a tkinter app in an asyncio event loop.
    """
    try:
        while True:
            root.update()
            await asyncio.sleep(interval)
    except TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


logging_handlers = []

logging_handlers.append(logging.StreamHandler())
if settings.TELEGRAM_ENABLED:
    telegram_logger = TelegramHandler(token=settings.TELEGRAM_TOKEN, chat_id=settings.TELEGRAM_CHAT)
    telegram_logger.formatter = telegram_handler.HtmlFormatter("%(asctime)s [%(module)s] %(levelname)s: %(message)s")
    logging_handlers.append(telegram_logger)
    logging_handlers.append(logging.FileHandler('logs.log'))


async def main() -> None:
    logging.basicConfig(
        level=settings.LOGLEVEL,
        format="%(asctime)s [%(module)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=logging_handlers
    )
    app = App()
    root = Tk()
    GUI(root, app.event_channel)
    asyncio.ensure_future(app.exec())
    await run_tk(root)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
