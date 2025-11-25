import numpy as np
from .event import MarketEvent


class Engine:
    def __init__(self, data, strategy, portfolio, execution):
        # DataHandler: 하루씩 가격을 공급
        self.data = data

        # Strategy: 매수/매도 신호를 만드는 알고리즘
        self.strategy = strategy

        # Portfolio: 현금/보유량/수익률 계산
        self.portfolio = portfolio

        # ExecutionHandler: 주문을 체결해주는 역할 (시뮬레이션)
        self.execution = execution

    def run(self):
        """
        전체 백테스트를 실행하는 메인 루프.
        실제 트레이딩 시스템의 이벤트 흐름을 흉내낸 구조.
        """
        while True:
            # 1) 새로운 시장 데이터(캔들) 1개 전달 (하루 전진)
            event = self.data.next()

            # 데이터 끝이면 종료
            if event is None:
                break

            # 들어온 이벤트가 '시장 데이터 도착'일 경우
            if isinstance(event, MarketEvent):
                # 오늘의 주가(종가) 가져오기
                price = self.data.get_price()

                # 2) 전략 실행 → 매수/매도 Signal 생성
                signal = self.strategy.generate()

                # 3) Signal이 있으면 → Portfolio에서 Order 생성
                if signal:
                    order = self.portfolio.on_signal(signal, price)

                    # 4) Order가 있으면 → Execution(시뮬레이터)에서 FillEvent 생성
                    if order:
                        fill = self.execution.execute(order, price)

                        # 5) FillEvent로 포트폴리오 갱신 (주문 체결 반영)
                        self.portfolio.on_fill(fill)

                # 6) 마지막으로 오늘자 자산 가치 업데이트
                self.portfolio.update_equity(price)

        # ==========================
        # 날짜 인덱스를 equity curve에 연결
        # ==========================

        # 가격 데이터의 날짜 인덱스
        dates = self.data.data.index[:len(self.portfolio.equity_curve)]

        # equity curve를 날짜 인덱스로 생성
        equity = self.portfolio.get_equity_curve(dates)

        # 일별 수익률 계산 (pct_change = 퍼센트 변화율)
        returns = equity.pct_change().dropna()

        # 샤프 비율 = 연간화 수익률 / 연간화 변동성
        sharpe = (np.sqrt(252) * returns.mean() / returns.std()).round(3)

        # MDD = 최대 낙폭
        mdd = ((equity.cummax() - equity) / equity.cummax()).max().round(3)

        return {
            "final_capital": equity.iloc[-1],
            "sharpe": sharpe,
            "mdd": mdd,
            "equity_curve": equity
        }
