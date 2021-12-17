from ftdc import structs
from ftdc.trader import trader_api, TraderSpi
from settings.settings import USERINFO


if __name__ == '__main__':
    appinfo = structs.ReqAuthenticateField(
        BrokerID='9999', UserID='195076', UserProductInfo="", AuthCode="0000000000000000", AppID="simnow_client_test"
    )
    userinfo = structs.UserLoginField(BrokerID='9999', UserID='195076', Password='Asin#940213')
    api = trader_api.CThostFtdcTraderApi_CreateFtdcTraderApi(f'{USERINFO}/')
    print(api.GetApiVersion())
    spi = TraderSpi(api, userinfo, appinfo)
    api.RegisterFront("tcp://180.168.146.187:10201")
    api.RegisterSpi(spi)
    api.Init()
    # api.Join()
    api.Release()
