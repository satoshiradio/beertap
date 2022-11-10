from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", default=False)
EMULATE_GPIO = env.bool("EMULATE_GPIO", default=False)
FULLSCREEN = env.bool("FULLSCREEN", default=True)

GPIO_TAP_PIN = env.int("GPIO_TAP_PIN")

PRICE_IN_EUROCENTS = env.int("PRICE_IN_EUROCENTS")

LNBITS_BASE_URL = env.str("LNBITS_BASE_URL")
LNBITS_INVOICE_KEY = env.str("LNBITS_INVOICE_KEY")
LIGHTNING_BACKEND = env.str("LIGHTNING_BACKEND", default=None)



