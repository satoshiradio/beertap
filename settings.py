import importlib

from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", default=False)
LNBITS_ENDPOINT = env.str("LNBITS_ENDPOINT")
LNBITS_INVOICE_KEY = env.str("LNBITS_INVOICE_KEY")

lightning_backend_module = importlib.import_module('Controller.LightningBackend')

lightning_backend_class = getattr(
    lightning_backend_module, env.str("LIGHTNING_BACKEND", default=None)
)

LIGHTNING_BACKEND = lightning_backend_class()


