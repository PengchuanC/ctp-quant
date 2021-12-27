import time

from ftdc import structs
from ftdc.md import user_api, MdSPi
from broker.redis_broker import RedisBroker, RedisBrokerConfig
from settings.settings import USERINFO


if __name__ == '__main__':
    spi = MdSPi()
    spi.set_contracts(['ni2201', 'cu2201'])
    broker = RedisBroker(RedisBrokerConfig('10.170.139.12'))
    spi.register_broker('redis', broker)

    spi.init()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            spi.logout()
            time.sleep(5)
            api.Release()
            exit()
