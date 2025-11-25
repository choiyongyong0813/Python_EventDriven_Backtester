import pandas as pd
from .event import MarketEvent


class DataHandler:
    def __init__(self, csv_path, symbol):
        # 어떤 종목(AAPL 등)을 사용할지 저장
        self.symbol = symbol

        # CSV 파일을 읽어서 판다스 데이터프레임으로 저장
        # index_col=0 → 첫 번째 열을 날짜(Date)로 사용
        # parse_dates=True → 날짜 문자열을 datetime 객체로 자동 변환
        self.data = pd.read_csv(csv_path, index_col=0, parse_dates=True)

        # ptr(pointer) → 현재 몇 번째 캔들까지 읽었는지 추적하는 커서
        self.ptr = 0

        # current_bar → 지금 시점의 단일 캔들(OHLCV) 데이터
        self.current_bar = None

    def next(self):
        """
        데이터에서 '다음 하루(다음 캔들)'를 가져오고
        그 시점이 도착했다는 의미의 MarketEvent를 반환한다.

        백테스팅에서는 과거 데이터를 실제 시장처럼
        '한 줄씩 흘려보내는(streaming)' 구조가 필요하다.
        """
        # ptr이 데이터 길이를 넘어가면 더 이상 데이터 없음 → 종료 신호
        if self.ptr >= len(self.data):
            return None

        # 현재 ptr 위치의 주가 데이터를 하나 꺼냄
        self.current_bar = self.data.iloc[self.ptr]

        # ptr을 다음 위치로 이동 (커서 이동)
        self.ptr += 1

        # "새로운 시장 데이터가 들어왔다"는 이벤트 반환
        return MarketEvent()

    def get_price(self):
        """
        현재 바(current_bar)의 종가(Close)를 반환.
        전략들은 보통 종가를 기준으로 계산을 수행한다.
        """
        if self.current_bar is None:
            return None
        return self.current_bar["Close"]

    def get_history(self, length):
        """
        최근 length개의 종가 데이터를 슬라이싱하여 반환.

        예: length=20이면, 최근 20일간 종가 리스트가 반환됨
        → 이동평균(MA), 모멘텀 등 전략 계산에 사용
        """
        if self.ptr < length:
            # 아직 데이터가 충분히 쌓이지 않음
            return None

        # 예: ptr=100이면 data[80:100] 구간을 반환
        return self.data["Close"].iloc[self.ptr-length:self.ptr]
