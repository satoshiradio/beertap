from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", default=False)
EMULATE_GPIO = env.bool("EMULATE_GPIO", default=False)
FULLSCREEN = env.bool("FULLSCREEN", default=True)

GPIO_TAP_PIN = env.int("GPIO_TAP_PIN")

LNURL_URL = env.str('LNURL_URL')

LNBITS_ENDPOINT = env.str("LNBITS_ENDPOINT")
LNBITS_INVOICE_KEY = env.str("LNBITS_INVOICE_KEY")
LIGHTNING_BACKEND = env.str("LIGHTNING_BACKEND", default=None)



