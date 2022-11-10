from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", default=False)
FULLSCREEN = env.bool("FULLSCREEN", default=True)

EMULATE_GPIO = env.bool("EMULATE_GPIO", default=False)
GPIO_TAP_PIN = env.int("GPIO_TAP_PIN")

LIGHTNING_BACKEND = env.str("LIGHTNING_BACKEND", default=None)

MILLILITER_PER_HOUR = env.int("MILLILITER_PER_HOUR")
MILLILITER_PER_GLASS = env.int("MILLILITER_PER_GLASS")
TAP_TIME_ADJUSTMENT_SECONDS = env.int("TAP_TIME_ADJUSTMENT_SECONDS", default=0)
PRICE_IN_EUROCENTS = env.int("PRICE_IN_EUROCENTS")

LNBITS_BASE_URL = env.str("LNBITS_BASE_URL")
LNBITS_INVOICE_KEY = env.str("LNBITS_INVOICE_KEY")



