from ftdc import structs
from ftdc.user import user_api, MdUserApi
from broker.redis_broker import RedisBroker, RedisBrokerConfig
from settings.settings import USERINFO


if __name__ == '__main__':
    userinfo = structs.UserLoginField(BrokerID='9999', UserID='195076', Password='Asin#940213')
    api = user_api.CThostFtdcMdApi_CreateFtdcMdApi(f'{USERINFO}/')
    spi = MdUserApi(api, userinfo)
    spi.set_contracts(['ni2201', 'cu2201'])
    broker = RedisBroker(RedisBrokerConfig('10.170.139.12'))
    broker.register('redis', spi)
    '''以下是7*24小时环境'''
    api.RegisterFront("tcp://180.168.146.187:10211")
    # api.RegisterFront("tcp://180.168.146.187:10131")
    api.RegisterSpi(spi)
    api.Init()
    try:
        api.Join()
    except Exception as e:
        print(e)
    print('停止')
    api.Release()
