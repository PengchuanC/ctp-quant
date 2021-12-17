# CTP Wrapper

基于swig和CTP api封装python版，目标是实现Python接入期货公司交易系统，实现量化交易

开发进度
- [x] 完成MdUserApi接口封装，可以获取行情数据
- [x] 添完成redis broker，可以将行情数据缓存至redis
- [ ] grpc broker
- [ ] redis dispatcher，通过redis分发数据，目前以stream实现，具体数据处理逻辑待开发
- [ ] TraderUserApi接口封装，目前仅完成部分函数的重载
- [ ] 开发并接入策略，模拟盘交易策略
- [ ] 基于FastApi的后端接口

特点：
 - 以Python namedtuple来定义c++中的struct类型
 - 采用pub/sub机制处理数据和事件，方便自定义subscriber
 - type hints
 - Windows下基于Python3.8，其他版本python需要swig重新处理ctp api
