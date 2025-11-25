class Event:
    """
    모든 이벤트의 부모 클래스.
    실제 기능은 없고,
    MarketEvent / SignalEvent / OrderEvent / FillEvent 의 공통 기반 역할을 한다.
    """
    pass


class MarketEvent(Event):
    """
    시장 데이터(캔들)가 새로 들어왔음을 알리는 이벤트.
    DataHandler.next()가 한 날짜(하루치 OHLCV)를 불러올 때 이 이벤트가 발생한다.
    """
    def __init__(self):
        self.type = "MARKET"   # 이벤트 종류 표시


class SignalEvent(Event):
    """
    전략(Strategy)이 '사라/팔라' 같은 매매 신호를 만들 때 생성되는 이벤트.
    direction: LONG(매수), EXIT(포지션 종료) 등 전략의 의사결정 결과.
    """
    def __init__(self, direction):
        self.type = "SIGNAL"
        self.direction = direction  # LONG / EXIT


class OrderEvent(Event):
    """
    Portfolio(계좌 관리)가 매수/매도 주문을 만들 때 생성되는 이벤트.
    direction: BUY(매수), SELL(매도)
    quantity: 주문 수량
    """
    def __init__(self, direction, quantity):
        self.type = "ORDER"
        self.direction = direction  # BUY / SELL
        self.quantity = quantity    # 주문 수량


class FillEvent(Event):
    """
    ExecutionHandler(체결 시스템)가 주문을 실제로 체결했다고 가정하고 반환하는 이벤트.
    direction: BUY 또는 SELL
    quantity: 체결된 수량
    price: 체결 가격 (백테스트에서는 종가로 체결한다고 가정)
    """
    def __init__(self, direction, quantity, price):
        self.type = "FILL"
        self.direction = direction
        self.quantity = quantity   # 체결 수량
        self.price = price         # 체결 가격
