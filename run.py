import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import yfinance as yf
import pandas as pd
from backtester.engine import Engine
from backtester.data import DataHandler
from backtester.strategy import (
    MovingAverageCrossStrategy,
    MomentumStrategy,
    MeanReversionStrategy
)
from backtester.portfolio import Portfolio
from backtester.execution import ExecutionHandler


def download_data():
    """
    Yahoo Finance에서 애플(AAPL) 주가 데이터를 다운로드하고,
    백테스터가 읽기 좋은 포맷(CSV)으로 저장한다.
    """
    df = yf.download(
        tickers="AAPL",
        start="2025-01-01",
        end="2025-11-24",
        group_by="ticker",
        auto_adjust=False,
        threads=False
    )

    # 날짜를 일반 컬럼으로 변환
    df = df.reset_index()

    # CSV 컬럼 이름 표준화
    df.columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]

    # 파일 저장
    df.to_csv("data/AAPL.csv", index=False)
    print("AAPL.csv 다운로드 완료")


def run_backtest(strategy_type="mac"):
    """
    전략 선택 → 엔진 실행 → 결과 출력 + 그래프 그리기
    """
    data = DataHandler("data/AAPL.csv", "AAPL")

    # 전략 선택
    if strategy_type == "mac":
        strategy = MovingAverageCrossStrategy(data)
    elif strategy_type == "momentum":
        strategy = MomentumStrategy(data)
    elif strategy_type == "mr":
        strategy = MeanReversionStrategy(data)
    else:
        raise ValueError("지원하지 않는 전략")

    portfolio = Portfolio(initial_capital=1000)  #시작할 때 가진 돈 = 100,000달러
    execution = ExecutionHandler()

    # 엔진 실행
    engine = Engine(data, strategy, portfolio, execution)
    results = engine.run()

    # 결과 출력
    print("\n=== 최종 결과 ===")
    print("최종 자본:", results["final_capital"])
    print("샤프지수:", results["sharpe"])
    print("MDD:", results["mdd"])

    # equity curve 그래프 그리기
    results["equity_curve"].plot(title="Equity Curve")
    import matplotlib.pyplot as plt
    plt.show()


if __name__ == "__main__":
    download_data()   # 최초 1회만 실행
    run_backtest("mac")
