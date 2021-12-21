# CTP Wrapper

基于swig和CTP api封装python版，目标是实现Python接入期货公司交易系统，实现量化交易

开发进度
- [x] 完成MdUserApi接口封装，可以获取行情数据
- [x] 添完成redis broker，可以将行情数据缓存至redis
- [ ] grpc broker
- [x] redis dispatcher，通过redis分发数据，目前仅分发到sqlite
- [x] TraderUserApi接口封装，目前仅完成常用功能重写
- [ ] 开发并接入策略，模拟盘交易策略
- [ ] 基于FastApi的后端接口

特点：
 - 以Python namedtuple来定义c++中的struct类型
 - 采用pub/sub机制处理数据和事件，方便自定义subscriber
 - type hints
 - Windows下基于Python3.8，其他版本python需要swig重新处理ctp api
 - 依赖于redis

后续目标：
- [ ] 以C++实现数据订阅和交易后端
- [ ] 以Python实现策略、下单指令和web后端
- [ ] 实现web前端

使用：
1. 安装Redis、Python3.8及相关依赖；
2. 删除`./userinfo`下的全部文件，在命令行中执行`python command.py database migrate`来迁移数据库；
3. 挂载MdSpi实例，监听行情数据，可以参考`./demos/md_api.py`中的示例；
4. (可选)编写Dispatcher实例，处理行情数据，可以用于保存数据或发送给行情，可以参考`./demos/database_dispatcher.py`中的示例；
5. 编写交易策略并挂载到TraderSpi实例，执行交易策略，可以参考`./demos/td_api.py`中的实示例。