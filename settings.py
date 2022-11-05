import importlib

from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", default=False)
LNBITS_ENDPOINT = env.str("LNBITS_ENDPOINT")
LNBITS_INVOICE_KEY = env.str("LNBITS_INVOICE_KEY")
LIGHTNING_BACKEND = env.str("LIGHTNING_BACKEND", default=None)



