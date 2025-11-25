import pandas as pd


class Portfolio:
    """
    Portfolio (포트폴리오 / 계좌 관리)

    - 내가 가진 현금
    - 보유한 주식 수량(position)
    - 현재 자산 가치(equity)
    - 매수 가격(entry price)

    등을 관리하며,
    주문을 체결했을 때 계좌에 반영하고,
    매일매일 자산 변화율을 저장해서 분석할 수 있게 해준다.
    """

    def __init__(self, initial_capital=1000):
        # 시작 현금 (초기 자본: 예 100,000달러)
        self.cash = initial_capital

        # 현재 보유 주식 수량 (처음엔 0)
        self.position = 0

        # 매수한 가격(평단가). 매수할 때 기록됨.
        self.entry_price = None

        # 매일 업데이트되는 총 자산 가치(equity) 기록
        self.equity_curve = []

    def on_signal(self, event, price):
        """
        전략이 만든 SignalEvent를 받아
        어떤 주문(OrderEvent)을 낼지 결정한다.

        LONG  → 매수 주문 생성 (position이 없을 때만)
        EXIT  → 매도 주문 생성 (position이 있을 때만)

        Return:
            ("BUY", qty)   또는   ("SELL", qty)
        """
        # 매수 시그널 + 현재 보유 없음 → BUY 주문
        if event.direction == "LONG" and self.position == 0:
            # current cash로 몇 주 살 수 있는지 계산
            qty = int(self.cash / price)
            return ("BUY", qty)

        # 포지션 종료 시그널 + 보유 있음 → SELL 주문
        elif event.direction == "EXIT" and self.position > 0:
            return ("SELL", self.position)

        # 조건에 맞지 않으면 주문 없음
        return None

    def on_fill(self, event):
        """
        FillEvent(체결 이벤트)를 받아서
        실제 계좌 상태에 반영하는 함수.

        BUY → 현금 감소 + 포지션 증가
        SELL → 현금 증가 + 포지션 0으로 변경
        """
        if event.direction == "BUY":
            # 전체 매수 비용
            cost = event.quantity * event.price

            # 현금에서 차감
            self.cash -= cost

            # 보유 주식 증가
            self.position += event.quantity

            # 매수 가격 기록 (평단가 역할)
            self.entry_price = event.price

        elif event.direction == "SELL":
            # 매도해서 들어온 돈
            gain = event.quantity * event.price

            # 현금 증가
            self.cash += gain

            # 주식 보유량 0으로 초기화
            self.position = 0

    def update_equity(self, price):
        """
        하루가 지났을 때 총 자산 가치 계산.

        총 자산 = 현금 + (보유 주식 수량 × 현재 주가)
        """
        total = self.cash + self.position * price

        # 자산 기록
        self.equity_curve.append(total)
        return total

    def get_equity_curve(self, dates):
        """
        지금까지 저장된 자산 가치 리스트를
        Pandas Series로 변환하여 반환.

        → 샤프지수, MDD, 수익률 계산에 사용됨.
        """
        return pd.Series(self.equity_curve, index=dates)
