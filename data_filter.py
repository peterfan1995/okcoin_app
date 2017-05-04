from collections import namedtuple


class DataFilter(object):
    __instance = None

    def __init__(self):
        self.__ticker_list = list()
        self.__depth_list_asks = list()
        self.__depth_list_bids = list()
        self.__trades_list = list()
        self.__kline_list = list()

    def __new__(cls, *args, **kwargs):
        if DataFilter.__instance is None:
            DataFilter.__instance = object.__new__(cls, *args, **kwargs)
        return DataFilter.__instance

    def websocket_filter_data(self, data):
        channel = data['channel']
        print(channel)
        if 'ticker' in channel:
            self.__ticker_list.append(data['data'])
            self.__ticker_list.sort(key=lambda d: d['timestamp'])
        elif 'depth' in channel:
            # TODO
            # self.__depth_list.append(data['data'])
            pass
        elif 'trades' in channel:
            # TODO
            # self.__trades_list.extend(data['data'])
            # self.__trades_list.sort(key=lambda l: l[0])
            pass
        elif 'kline' in channel:
            # TODO
            # self.__kline_list.extend(data['data'])
            # self.__kline_list.sort(key=lambda l: l[0])
            pass

    def add_data(self, data, interface):
        if interface == 'websocket':
            self.websocket_filter_data(data)

    def ticker_add_data(self, data):
        # TODO
        # 行情应该有一个就行，最新的。要做比较
        ticker = namedtuple('ticker', ['timestamp', 'buy', 'sell', 'high', 'low', 'last', 'vol'])
        tmp = data['ticker']
        t = ticker(float(data['date']), float(tmp['buy']), float(tmp['sell']), float(tmp['high']), float(tmp['low']),
                   float(tmp['last']), float(tmp['vol']))
        self.__ticker_list.append(t)

    def depth_add_data(self, data):
        # TODO
        # 深度应该合并。读取200条，websocket可能做增量控制比较好。或者有可能是数据直接刷新
        self.__depth_list_asks.extend(data['asks'])
        self.__depth_list_bids.extend(data['bids'])

    def trades_add_data(self, data):
        # TODO
        # 交易记录应该合并才对。
        trades = namedtuple('trades', ['tid', 'price', 'amount', 'timestamp', 'type'])
        for i, d in enumerate(data):
            tmp = trades(int(d['tid']), float(d['price']), float(d['amount']), int(d['date_ms']), d['type'])
            self.__trades_list.append(tmp)

    def kline_add_data(self, data):
        # TODO
        # 根据时间段进行数据合并
        kline = namedtuple('kline', ['timestamp', 'open', 'high', 'low', 'close', 'vol'])
        for i, l in enumerate(data):
            tmp = kline(l[0], l[1], l[2], l[3], l[4], l[5])
            self.__kline_list.append(tmp)

    def get_ticker_list(self):
        return self.__ticker_list

    def get_depth_list_asks(self):
        return self.__depth_list_asks

    def get_depth_list_bids(self):
        return self.__depth_list_bids

    def get_trades_list(self):
        return self.__trades_list

    def get_kline_list(self):
        return self.__kline_list


global global_data_filter
global_data_filter = DataFilter()


def get_global_data_filter():
    return global_data_filter
