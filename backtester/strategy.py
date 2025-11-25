from .event import SignalEvent


class MovingAverageCrossStrategy:
    """
    20일 / 50일 이동평균 골든크로스 전략(MACD의 단순 버전)

    핵심 원리:
    - 최근 20일 평균 가격(short MA)이
      최근 50일 평균 가격(long MA)보다 올라가면 → 상승 추세 진입이라고 판단 → 매수
    - 반대로 20일 MA < 50일 MA → 추세 약화로 보고 → 매도(포지션 종료)
    """

    def __init__(self, data):
        # DataHandler 객체. 가격 데이터를 history로 받기 위해 사용됨.
        self.data = data

        # 현재 포지션 보유 여부 (True = 매수 포지션 있음)
        self.in_position = False

    def generate(self):
        """
        전략 신호(SignalEvent)를 생성하는 핵심 함수.
        매일 실행되며, 매수/매도 신호를 판단한다.
        """
        # 최근 50일 종가 히스토리 불러오기
        prices = self.data.get_history(50)

        # 데이터가 충분하지 않으면(초반 50일 전) 신호 없음
        if prices is None:
            return None

        # 단기(20일) 평균
        short = prices.tail(20).mean()

        # 장기(50일) 평균
        long = prices.tail(50).mean()

        # 단기 > 장기 → 상승 추세 시작 → 매수
        if short > long and not self.in_position:
            self.in_position = True
            return SignalEvent("LONG")

        # 단기 < 장기 → 추세 꺾임 → 매도(포지션 종료)
        elif short < long and self.in_position:
            self.in_position = False
            return SignalEvent("EXIT")

        return None



class MomentumStrategy:
    """
    모멘텀 전략 (Momentum)
    - 최근 12개월(252 거래일) 동안 가격이 상승했으면 → LONG
    - 최근 12개월 동안 하락했으면 → EXIT

    기본 원리:
    "오르는 종목은 계속 오른다"라는 모멘텀 효과에 근거.
    """

    def __init__(self, data):
        self.data = data
        self.in_position = False

    def generate(self):
        # 252일(약 1년) 종가 데이터 필요
        prices = self.data.get_history(252)
        if prices is None:
            return None

        # 모멘텀 = 최근가격 - 1년 전 가격
        momentum = prices.iloc[-1] - prices.iloc[0]

        # 가격이 1년 동안 상승했다 → 상승 모멘텀 → 매수
        if momentum > 0 and not self.in_position:
            self.in_position = True
            return SignalEvent("LONG")

        # 모멘텀이 음수 → 장기 하락 추세 → 포지션 청산
        elif momentum < 0 and self.in_position:
            self.in_position = False
            return SignalEvent("EXIT")

        return None



class MeanReversionStrategy:
    """
    평균회귀 전략 (Mean Reversion)

    원리:
    - 가격은 평균에서 너무 벗어났다가 다시 평균으로 돌아오는 성질이 있다.

    구현:
    - 최근 20일 평균보다 3% 이상 떨어지면 → '과하게 떨어짐' → 매수
    - 평균보다 3% 이상 올라가면 → '과하게 상승' → 매도
    """

    def __init__(self, data):
        self.data = data
        self.in_position = False

    def generate(self):
        # 최근 20일 종가 데이터
        prices = self.data.get_history(20)
        if prices is None:
            return None

        # 20일 평균 가격
        mean = prices.mean()

        # 오늘 종가
        price = prices.iloc[-1]

        # 평균보다 3% 아래 → 과매도 구간 → 매수
        if price < mean * 0.97 and not self.in_position:
            self.in_position = True
            return SignalEvent("LONG")

        # 평균보다 3% 위 → 과매수 구간 → 매도
        elif price > mean * 1.03 and self.in_position:
            self.in_position = False
            return SignalEvent("EXIT")

        return None
