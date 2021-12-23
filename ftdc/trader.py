"""
@author：chuanchao.peng
@date: 2021-12-09
@desc:
实现交易所CThostFtdcTraderSpi类，处理交易所指令
"""

import thosttraderapi as trader_api

from ftdc import structs, order
from logger.logger import logger


class TraderSpi(trader_api.CThostFtdcTraderSpi):

    def __init__(
            self, api: "CThostFtdcTraderApi", userinfo: structs.UserLoginField, appinfo: structs.ReqAuthenticateField
    ):
        trader_api.CThostFtdcTraderSpi.__init__(self)
        self._api = api
        self._info = userinfo
        self._app = appinfo

    def _auth(self):
        """登陆"""
        auth_field: structs.ReqAuthenticateField = trader_api.CThostFtdcReqAuthenticateField()
        auth_field.BrokerID = self._app.BrokerID
        auth_field.UserID = self._app.UserID
        auth_field.AppID = self._app.AppID
        auth_field.AuthCode = self._app.AuthCode
        self._api.ReqAuthenticate(auth_field, 0)
        logger.info("交易端-已发送客户端认证请求")

    def _login(self):
        login_field: structs.UserLoginField = trader_api.CThostFtdcReqUserLoginField()
        login_field.BrokerID = self._info.BrokerID
        login_field.UserID = self._info.UserID
        login_field.Password = self._info.Password
        login_field.UserProductInfo = "python dll"
        ret = self._api.ReqUserLogin(login_field, 0)
        if ret != 0:
            logger.error(f'交易端-登陆请求发送失败')
            return
        logger.info(f'交易端-登陆请求发送成功')

    def _qry_settlement_info(self):
        """发送投资结果查询请求"""
        qry_info_field: structs.QrySettlementInfoField = trader_api.CThostFtdcQrySettlementInfoField()
        qry_info_field.BrokerID = self._info.BrokerID
        qry_info_field.InvestorID = self._info.UserID
        qry_info_field.TradingDay = self._api.GetTradingDay()
        self._api.ReqQrySettlementInfo(qry_info_field, 0)
        logger.info("交易端-已发送投资结果查询请求")

    def trade(self, order_info: order.InputOrderField):
        """执行交易，对不同的策略，此函数一定要重写！！！"""
        logger.info(f'交易端-执行交易')
        ret = self._api.ReqOrderInsert(order_info, 0)
        if ret:
            logger.error(f'交易端-报单请求失败,ErrorCode={ret}')

    def qry_investor_position(self, instrument_id: str, exchange_id: str):
        """查询投资者持仓明细"""
        logger.info(f'交易端-持仓查询,InstrumentID={instrument_id},ExchangeID={exchange_id}')
        field: order.QryInvestorPositionField = trader_api.CThostFtdcQryInvestorPositionField()
        field.BrokerID = self._info.BrokerID
        field.InvestorID = self._info.UserID
        field.ExchangeID = exchange_id
        field.InstrumentID = instrument_id
        self._api.ReqQryInvestorPosition(field, 0)

    def OnFrontConnected(self):
        """当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。"""
        logger.info(f'服务端-交易服务器已连接,即将进行客户端认证')
        self._auth()

    def OnFrontDisconnected(self, nReason: int):
        """
        当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
        :param nReason:
        """
        logger.info(f'交易服务器已断开连接，连接断开原因 {nReason}')

    def OnHeartBeatWarning(self, nTimeLapse: int):
        """
        心跳超时警告。当长时间未收到报文时，该方法被调用。
        :param nTimeLapse:
        """
        logger.warning(f'交易端-长时间没有收到报文警告，最后一次接收时间为：{nTimeLapse}')

    def OnRspAuthenticate(
            self,
            pRspAuthenticateField: "CThostFtdcRspAuthenticateField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """客户端认证响应"""
        if pRspInfo.ErrorID != 0:
            logger.error(f'交易端-客户端认证失败,ErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}')
            return
        logger.info(f'交易端-客户端认证成功,即将进行用户登陆')
        self._login()

    def OnRspUserLogin(
            self,
            pRspUserLogin: "CThostFtdcRspUserLoginField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """登录请求响应"""
        logger.info(
            f"交易端-收到登陆请求返回信息, SessionID={pRspUserLogin.SessionID},ErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}"
        )
        self._qry_settlement_info()

    def OnRspUserLogout(
            self,
            pUserLogout: "CThostFtdcUserLogoutField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """登出请求响应"""
        logger.info('交易端-用户已登出')

    def OnRspUserPasswordUpdate(
            self,
            pUserPasswordUpdate: "CThostFtdcUserPasswordUpdateField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        用户口令更新请求响应
        :param pUserPasswordUpdate:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        """
        pass

    def OnRspTradingAccountPasswordUpdate(
            self,
            pTradingAccountPasswordUpdate: "CThostFtdcTradingAccountPasswordUpdateField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """资金账户口令更新请求响应"""
        pass

    def OnRspUserAuthMethod(
            self,
            pRspUserAuthMethod: "CThostFtdcRspUserAuthMethodField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        查询用户当前支持的认证模式的回复
        :param pRspUserAuthMethod:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        """
        print("OnRspUserAuthMethod")

    def OnRspGenUserCaptcha(
            self,
            pRspGenUserCaptcha: "CThostFtdcRspGenUserCaptchaField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        获取图形验证码请求的回复
        :param pRspGenUserCaptcha:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        """
        pass

    def OnRspGenUserText(
            self,
            pRspGenUserText: "CThostFtdcRspGenUserTextField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        获取短信验证码请求的回复
        :param pRspGenUserText:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        pass

    def OnRspOrderInsert(
            self,
            pInputOrder: order.InputOrderField,
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """报单录入请求响应"""
        logger.info(f'交易端-报单录入请求响应\n\tErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}')

    def OnRspParkedOrderInsert(
            self,
            pParkedOrder: "CThostFtdcParkedOrderField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        预埋单录入请求响应
        :param pParkedOrder:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        """
        pass

    def OnRspParkedOrderAction(
            self,
            pParkedOrderAction: "CThostFtdcParkedOrderActionField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        预埋撤单录入请求响应
        :param pParkedOrderAction:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        """
        pass

    def OnRspOrderAction(
            self,
            pInputOrderAction: "CThostFtdcInputOrderActionField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        报单操作请求响应
        :param pInputOrderAction:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        """

    def OnRspQueryMaxOrderVolume(
            self,
            pQueryMaxOrderVolume: 'CThostFtdcQueryMaxOrderVolumeField',
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        查询最大报单数量响应
        :param pQueryMaxOrderVolume:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        pass

    def OnRspSettlementInfoConfirm(
            self,
            pSettlementInfoConfirm: structs.SettlementInfoConfirmField,
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """投资者结算结果确认响应"""
        logger.info("交易端-投资者结算结果确认完成")
        # TODO 进行具体交易

    def OnRspRemoveParkedOrder(
            self,
            pRemoveParkedOrder: "CThostFtdcRemoveParkedOrderField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """
        删除预埋单响应
        :param pRemoveParkedOrder:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        """
        pass

    def OnRspRemoveParkedOrderAction(
            self,
            pRemoveParkedOrderAction: "CThostFtdcRemoveParkedOrderActionField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """删除预埋撤单响应"""
        pass

    def OnRspExecOrderInsert(
            self,
            pInputExecOrder: "CThostFtdcInputExecOrderField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """执行宣告录入请求响应"""
        pass

    def OnRspExecOrderAction(
            self,
            pInputExecOrderAction: "CThostFtdcInputExecOrderActionField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """执行宣告操作请求响应"""
        pass

    def OnRspForQuoteInsert(
            self, pInputForQuote: "CThostFtdcInputForQuoteField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """询价录入请求响应"""
        pass

    def OnRspQuoteInsert(
            self, pInputQuote: "CThostFtdcInputQuoteField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """报价录入请求响应"""
        pass

    def OnRspQuoteAction(
            self, pInputQuoteAction: "CThostFtdcInputQuoteActionField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """报价操作请求响应"""
        pass

    def OnRspBatchOrderAction(
            self, pInputBatchOrderAction: "CThostFtdcInputBatchOrderActionField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """批量报单操作请求响应"""
        pass

    def OnRspOptionSelfCloseInsert(
            self, pInputOptionSelfClose: "CThostFtdcInputOptionSelfCloseField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """期权自对冲录入请求响应"""
        pass

    def OnRspOptionSelfCloseAction(
            self, pInputOptionSelfCloseAction: "CThostFtdcInputOptionSelfCloseActionField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """期权自对冲操作请求响应"""
        pass

    def OnRspCombActionInsert(
            self, pInputCombAction: "CThostFtdcInputCombActionField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """申请组合录入请求响应"""
        pass

    def OnRspQryOrder(
            self, pOrder: "CThostFtdcOrderField", pRspInfo: structs.RspInfoField, nRequestID: int,
            bIsLast: bool
    ):
        """请求查询报单响应"""
        pass

    def OnRspQryTrade(
            self, pTrade: "CThostFtdcTradeField", pRspInfo: structs.RspInfoField, nRequestID: int,
            bIsLast: bool
    ):
        """请求查询成交响应"""
        pass

    def OnRspQryInvestorPosition(
            self, pInvestorPosition: structs.InvestorPositionField,
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询投资者持仓响应"""
        p = pInvestorPosition
        logger.info(
            f'交易端-投资者持仓明细(OnRspQryInvestorPosition)\n\tInstrumentID={p.InstrumentID}\n\tPosition={p.Position}'
            f'\n\tLongFrozen={p.LongFrozen},LongFrozenAmount={p.LongFrozenAmount}'
            f'\n\tShortFrozen={p.ShortFrozen},ShortFrozenAmount={p.ShortFrozenAmount}'
            f'\n\tTradingDay={p.TradingDay}'
        )
        data = {name: getattr(pInvestorPosition, name) for name in structs.InvestorPositionField._fields}
        # todo 处理持仓数据

    def OnRspQryTradingAccount(
            self, pTradingAccount: "CThostFtdcTradingAccountField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询资金账户响应"""
        pass

    def OnRspQryInvestor(
            self, pInvestor: "CThostFtdcInvestorField", pRspInfo: structs.RspInfoField, nRequestID: int,
            bIsLast: bool
    ):
        """请求查询投资者响应"""
        pass

    def OnRspQryTradingCode(
            self, pTradingCode: "CThostFtdcTradingCodeField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询交易编码响应"""
        pass

    def OnRspQryInstrumentMarginRate(
            self, pInstrumentMarginRate: "CThostFtdcInstrumentMarginRateField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询合约保证金率响应"""
        pass

    def OnRspQryInstrumentCommissionRate(
            self, pInstrumentCommissionRate: "CThostFtdcInstrumentCommissionRateField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询合约手续费率响应"""
        pass

    def OnRspQryExchange(
            self, pExchange: "CThostFtdcExchangeField", pRspInfo: structs.RspInfoField, nRequestID: int,
            bIsLast: bool
    ):
        """请求查询交易所响应"""
        pass

    def OnRspQryProduct(
            self,
            pProduct: "CThostFtdcProductField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """请求查询产品响应"""
        pass

    def OnRspQryInstrument(
            self,
            pInstrument: "CThostFtdcInstrumentField",
            pRspInfo: structs.RspInfoField,
            nRequestID: int,
            bIsLast: bool
    ):
        """请求查询合约响应"""
        pass

    def OnRspQryDepthMarketData(
            self, pDepthMarketData: "CThostFtdcDepthMarketDataField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询行情响应"""
        pass

    #
    def OnRspQrySettlementInfo(
            self, pSettlementInfo: structs.SettlementInfoField, pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询投资者结算结果响应"""
        if pSettlementInfo is not None:
            logger.info(f"结算结果查询为：{pSettlementInfo.Content}")
        else:
            logger.info("结算结果查询为空")
        confirm: structs.SettlementInfoConfirmField = trader_api.CThostFtdcSettlementInfoConfirmField()
        confirm.BrokerID = self._info.BrokerID
        confirm.InvestorID = self._info.UserID
        self._api.ReqSettlementInfoConfirm(confirm, 0)
        logger.info("交易端-发送结算结果确认请求成功")

    #
    def OnRspQryTransferBank(
            self, pTransferBank: "CThostFtdcTransferBankField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询转帐银行响应"""
        pass

    def OnRspQryInvestorPositionDetail(
            self, pInvestorPositionDetail: "CThostFtdcInvestorPositionDetailField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询投资者持仓明细响应"""
        logger.info('OnRspQryInvestorPositionDetail')

    def OnRspQryNotice(
            self, pNotice: "CThostFtdcNoticeField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询客户通知响应"""
        pass

    def OnRspQrySettlementInfoConfirm(
            self, pSettlementInfoConfirm: "CThostFtdcSettlementInfoConfirmField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询结算信息确认响应"""
        raise NotImplementedError('')

    def OnRspQryInvestorPositionCombineDetail(
            self,
            pInvestorPositionCombineDetail: "CThostFtdcInvestorPositionCombineDetailField",
            pRspInfo: structs.RspInfoField, nRequestID: int,
            bIsLast: bool
    ):
        """请求查询投资者持仓明细响应"""
        logger.info('OnRspQryInvestorPositionCombineDetail')

    def OnRspQryCFMMCTradingAccountKey(
            self, pCFMMCTradingAccountKey: "CThostFtdcCFMMCTradingAccountKeyField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """查询保证金监管系统经纪公司资金账户密钥响应"""
        pass

    def OnRspQryEWarrantOffset(
            self, pEWarrantOffset: "CThostFtdcEWarrantOffsetField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询仓单折抵信息响应"""
        pass

    def OnRspQryInvestorProductGroupMargin(
            self, pInvestorProductGroupMargin: "CThostFtdcInvestorProductGroupMarginField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询投资者品种/跨品种保证金响应"""
        pass

    def OnRspQryExchangeMarginRate(
            self, pExchangeMarginRate: "CThostFtdcExchangeMarginRateField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询交易所保证金率响应"""
        pass

    def OnRspQryExchangeMarginRateAdjust(
            self, pExchangeMarginRateAdjust: "CThostFtdcExchangeMarginRateAdjustField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询交易所调整保证金率响应"""
        pass

    def OnRspQryExchangeRate(
            self, pExchangeRate: "CThostFtdcExchangeRateField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询汇率响应"""
        pass

    def OnRspQrySecAgentACIDMap(
            self, pSecAgentACIDMap: "CThostFtdcSecAgentACIDMapField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询二级代理操作员银期权限响应"""
        pass

    def OnRspQryProductExchRate(
            self, pProductExchRate: "CThostFtdcProductExchRateField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询产品报价汇率"""
        pass

    def OnRspQryProductGroup(
            self, pProductGroup: "CThostFtdcProductGroupField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询产品组"""
        pass

    def OnRspQryMMInstrumentCommissionRate(
            self, pMMInstrumentCommissionRate: "CThostFtdcMMInstrumentCommissionRateField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询做市商合约手续费率响应"""
        pass

    def OnRspQryMMOptionInstrCommRate(
            self, pMMOptionInstrCommRate: "CThostFtdcMMOptionInstrCommRateField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询做市商期权合约手续费响应"""
        pass

    def OnRspQryInstrumentOrderCommRate(
            self, pInstrumentOrderCommRate: "CThostFtdcInstrumentOrderCommRateField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询报单手续费响应"""
        pass

    def OnRspQrySecAgentTradingAccount(
            self, pTradingAccount: "CThostFtdcTradingAccountField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询资金账户响应"""
        pass

    def OnRspQrySecAgentCheckMode(
            self, pSecAgentCheckMode: "CThostFtdcSecAgentCheckModeField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询二级代理商资金校验模式响应"""
        pass

    def OnRspQrySecAgentTradeInfo(
            self, pSecAgentTradeInfo: "CThostFtdcSecAgentTradeInfoField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询二级代理商信息响应"""
        pass

    def OnRspQryOptionInstrTradeCost(
            self, pOptionInstrTradeCost: "CThostFtdcOptionInstrTradeCostField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询期权交易成本响应"""
        pass

    def OnRspQryOptionInstrCommRate(
            self, pOptionInstrCommRate: "CThostFtdcOptionInstrCommRateField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询期权合约手续费响应"""
        pass

    def OnRspQryExecOrder(
            self, pExecOrder: "CThostFtdcExecOrderField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询执行宣告响应"""
        pass

    def OnRspQryForQuote(
            self, pForQuote: "CThostFtdcForQuoteField", pRspInfo: structs.RspInfoField, nRequestID: int,
            bIsLast: bool
    ):
        """请求查询询价响应"""
        pass

    def OnRspQryQuote(
            self, pQuote: "CThostFtdcQuoteField", pRspInfo: structs.RspInfoField, nRequestID: int,
            bIsLast: bool
    ):
        """请求查询报价响应"""
        pass

    def OnRspQryOptionSelfClose(
            self, pOptionSelfClose: "CThostFtdcOptionSelfCloseField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询期权自对冲响应"""
        pass

    def OnRspQryInvestUnit(
            self, pInvestUnit: "CThostFtdcInvestUnitField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询投资单元响应"""
        pass

    def OnRspQryCombInstrumentGuard(
            self, pCombInstrumentGuard: "CThostFtdcCombInstrumentGuardField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询组合合约安全系数响应"""
        pass

    def OnRspQryCombAction(
            self, pCombAction: "CThostFtdcCombActionField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询申请组合响应"""
        pass

    def OnRspQryTransferSerial(
            self, pTransferSerial: "CThostFtdcTransferSerialField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询转帐流水响应"""
        pass

    def OnRspQryAccountregister(
            self, pAccountregister: "CThostFtdcAccountregisterField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询银期签约关系响应"""
        pass

    def OnRspError(self, pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool):
        """错误应答"""
        logger.error(f'交易端-请求返回结果错误,ErrorID={pRspInfo.ErrorID},ErrorMsg={pRspInfo.ErrorMsg}')

    def OnRtnOrder(self, pOrder: order.OrderField):
        """报单通知"""
        logger.info(
            f'交易端-报单通知\n\tOrderStatus={pOrder.OrderStatus}\n\t'
            f'StatusMsg={pOrder.StatusMsg}\n\tLimitPrice={pOrder.LimitPrice}'
        )

    def OnRtnTrade(self, pTrade: order.TraderField):
        """成交通知"""
        logger.info(
            f'交易端-成交通知\n\tInstrumentID={pTrade.InstrumentID}\n\tTradeID={pTrade.TradeID}'
            f'\n\tPrice={pTrade.Price}\n\tVolume={pTrade.Volume}\n\tTradeDate={pTrade.TradeDate}'
            f'\n\tTradeTime={pTrade.TradeTime}'
        )

    def OnErrRtnOrderInsert(self, pInputOrder: order.InputOrderField, pRspInfo: structs.RspInfoField):
        """报单录入错误回报"""
        logger.info(f'交易端-报单录入错误,OnErrRtnOrderInsert')

    def OnErrRtnOrderAction(self, pOrderAction: "CThostFtdcOrderActionField", pRspInfo: structs.RspInfoField):
        """报单操作错误回报"""
        pass

    def OnRtnInstrumentStatus(self, pInstrumentStatus: "CThostFtdcInstrumentStatusField"):
        """合约交易状态通知"""
        pass

    def OnRtnBulletin(self, pBulletin: "CThostFtdcBulletinField"):
        """交易所公告通知"""
        pass

    def OnRtnTradingNotice(self, pTradingNoticeInfo: "CThostFtdcTradingNoticeInfoField"):
        """交易通知"""
        pass

    def OnRtnErrorConditionalOrder(self, pErrorConditionalOrder: "CThostFtdcErrorConditionalOrderField"):
        """提示条件单校验错误"""
        pass

    def OnRtnExecOrder(self, pExecOrder: "CThostFtdcExecOrderField"):
        """执行宣告通知"""
        pass

    def OnErrRtnExecOrderInsert(
            self, pInputExecOrder: "CThostFtdcInputExecOrderField",
            pRspInfo: structs.RspInfoField):
        """执行宣告录入错误回报"""
        pass

    def OnErrRtnExecOrderAction(
            self, pExecOrderAction: "CThostFtdcExecOrderActionField",
            pRspInfo: structs.RspInfoField):
        """执行宣告操作错误回报"""
        pass

    def OnErrRtnForQuoteInsert(
            self, pInputForQuote: "CThostFtdcInputForQuoteField",
            pRspInfo: structs.RspInfoField
    ):
        """询价录入错误回报"""
        pass

    def OnRtnQuote(self, pQuote: "CThostFtdcQuoteField"):
        """报价通知"""
        pass

    def OnErrRtnQuoteInsert(self, pInputQuote: "CThostFtdcInputQuoteField", pRspInfo: structs.RspInfoField):
        """报价录入错误回报"""
        pass

    def OnErrRtnQuoteAction(self, pQuoteAction: "CThostFtdcQuoteActionField", pRspInfo: structs.RspInfoField):
        """报价操作错误回报"""
        pass

    def OnRtnForQuoteRsp(self, pForQuoteRsp: "CThostFtdcForQuoteRspField"):
        """询价通知"""
        pass

    def OnRtnCFMMCTradingAccountToken(self, pCFMMCTradingAccountToken: "CThostFtdcCFMMCTradingAccountTokenField"):
        """保证金监控中心用户令牌"""
        pass

    def OnErrRtnBatchOrderAction(
            self, pBatchOrderAction: "CThostFtdcBatchOrderActionField",
            pRspInfo: structs.RspInfoField
    ):
        """批量报单操作错误回报"""
        pass

    def OnRtnOptionSelfClose(self, pOptionSelfClose: "CThostFtdcOptionSelfCloseField"):
        """期权自对冲通知"""
        pass

    def OnErrRtnOptionSelfCloseInsert(
            self, pInputOptionSelfClose: "CThostFtdcInputOptionSelfCloseField",
            pRspInfo: structs.RspInfoField
    ):
        """期权自对冲录入错误回报"""
        pass

    def OnErrRtnOptionSelfCloseAction(
            self, pOptionSelfCloseAction: "CThostFtdcOptionSelfCloseActionField",
            pRspInfo: structs.RspInfoField
    ):
        """期权自对冲操作错误回报"""
        pass

    def OnRtnCombAction(self, pCombAction: "CThostFtdcCombActionField"):
        """申请组合通知"""
        pass

    def OnErrRtnCombActionInsert(
            self, pInputCombAction: "CThostFtdcInputCombActionField",
            pRspInfo: structs.RspInfoField
    ):
        """申请组合录入错误回报"""
        pass

    def OnRspQryContractBank(
            self, pContractBank: "CThostFtdcContractBankField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询签约银行响应"""
        pass

    def OnRspQryParkedOrder(
            self, pParkedOrder: "CThostFtdcParkedOrderField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询预埋单响应"""
        pass

    def OnRspQryParkedOrderAction(
            self, pParkedOrderAction: "CThostFtdcParkedOrderActionField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool):
        """请求查询预埋撤单响应"""
        pass

    def OnRspQryTradingNotice(
            self, pTradingNotice: "CThostFtdcTradingNoticeField", pRspInfo: structs.RspInfoField,
            nRequestID: int, bIsLast: bool
    ):
        """请求查询交易通知响应"""
        pass

    def OnRspQryBrokerTradingParams(
            self, pBrokerTradingParams: "CThostFtdcBrokerTradingParamsField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """请求查询经纪公司交易参数响应"""
        pass

    def OnRspQryBrokerTradingAlgos(
            self, pBrokerTradingAlgos: "CThostFtdcBrokerTradingAlgosField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool

    ):
        """请求查询经纪公司交易算法响应"""
        pass

    def OnRspQueryCFMMCTradingAccountToken(
            self,
            pQueryCFMMCTradingAccountToken: "CThostFtdcQueryCFMMCTradingAccountTokenField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool):
        """请求查询监控中心用户令牌"""
        pass

    def OnRtnFromBankToFutureByBank(self, pRspTransfer: "CThostFtdcRspTransferField"):
        """银行发起银行资金转期货通知"""
        pass

    def OnRtnFromFutureToBankByBank(self, pRspTransfer: "CThostFtdcRspTransferField"):
        """银行发起期货资金转银行通知"""
        pass

    def OnRtnRepealFromBankToFutureByBank(self, pRspRepeal: "CThostFtdcRspRepealField"):
        """银行发起冲正银行转期货通知"""
        pass

    def OnRtnRepealFromFutureToBankByBank(self, pRspRepeal: "CThostFtdcRspRepealField"):
        """银行发起冲正期货转银行通知"""
        pass

    def OnRtnFromBankToFutureByFuture(self, pRspTransfer: "CThostFtdcRspTransferField"):
        """期货发起银行资金转期货通知"""
        pass

    def OnRtnFromFutureToBankByFuture(self, pRspTransfer: "CThostFtdcRspTransferField"):
        """期货发起期货资金转银行通知"""
        pass

    def OnRtnRepealFromBankToFutureByFutureManual(self, pRspRepeal: "CThostFtdcRspRepealField"):
        """系统运行时期货端手工发起冲正银行转期货请求，银行处理完毕后报盘发回的通知"""
        pass

    def OnRtnRepealFromFutureToBankByFutureManual(self, pRspRepeal: "CThostFtdcRspRepealField"):
        """系统运行时期货端手工发起冲正期货转银行请求，银行处理完毕后报盘发回的通知"""
        pass

    def OnRtnQueryBankBalanceByFuture(self, pNotifyQueryAccount: "CThostFtdcNotifyQueryAccountField"):
        """期货发起查询银行余额通知"""
        pass

    def OnErrRtnBankToFutureByFuture(
            self, pReqTransfer: "CThostFtdcReqTransferField",
            pRspInfo: structs.RspInfoField
    ):
        """期货发起银行资金转期货错误回报"""
        pass

    def OnErrRtnFutureToBankByFuture(
            self, pReqTransfer: "CThostFtdcReqTransferField",
            pRspInfo: structs.RspInfoField
    ):
        """期货发起期货资金转银行错误回报"""
        pass

    def OnErrRtnRepealBankToFutureByFutureManual(
            self, pReqRepeal: "CThostFtdcReqRepealField",
            pRspInfo: structs.RspInfoField
    ):
        """系统运行时期货端手工发起冲正银行转期货错误回报"""
        pass

    def OnErrRtnRepealFutureToBankByFutureManual(
            self, pReqRepeal: "CThostFtdcReqRepealField",
            pRspInfo: structs.RspInfoField
    ):
        """系统运行时期货端手工发起冲正期货转银行错误回报"""
        pass

    def OnErrRtnQueryBankBalanceByFuture(
            self, pReqQueryAccount: "CThostFtdcReqQueryAccountField",
            pRspInfo: structs.RspInfoField
    ):
        """期货发起查询银行余额错误回报"""
        pass

    def OnRtnRepealFromBankToFutureByFuture(self, pRspRepeal: "CThostFtdcRspRepealField"):
        """期货发起冲正银行转期货请求，银行处理完毕后报盘发回的通知"""
        pass

    def OnRtnRepealFromFutureToBankByFuture(self, pRspRepeal: "CThostFtdcRspRepealField"):
        """期货发起冲正期货转银行请求，银行处理完毕后报盘发回的通知"""
        pass

    def OnRspFromBankToFutureByFuture(
            self, pReqTransfer: "CThostFtdcReqTransferField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """期货发起银行资金转期货应答"""
        pass

    def OnRspFromFutureToBankByFuture(
            self, pReqTransfer: "CThostFtdcReqTransferField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """期货发起期货资金转银行应答"""
        pass

    def OnRspQueryBankAccountMoneyByFuture(
            self,
            pReqQueryAccount: "CThostFtdcReqQueryAccountField",
            pRspInfo: structs.RspInfoField, nRequestID: int, bIsLast: bool
    ):
        """期货发起查询银行余额应答"""
        pass

    def OnRtnOpenAccountByBank(self, pOpenAccount: "CThostFtdcOpenAccountField"):
        """银行发起银期开户通知"""
        pass

    def OnRtnCancelAccountByBank(self, pCancelAccount: "CThostFtdcCancelAccountField"):
        """银行发起银期销户通知"""
        pass

    def OnRtnChangeAccountByBank(self, pChangeAccount: "CThostFtdcChangeAccountField"):
        """银行发起变更银行账号通知"""
        pass
