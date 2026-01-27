# ?? 이벤트 기반 주식 백테스트 엔진 (Python)

## 프로젝트 개요
본 프로젝트는 **실제 트레이딩 시스템의 구조를 이해하기 위해**  
**Market → Signal → Order → Fill** 흐름을 갖는  
**이벤트 기반(Event-Driven) 주식 백테스트 엔진**을 Python으로 직접 설계·구현한 개인 프로젝트이다.

단순히 수익률을 계산하는 것이 아니라,  
전략, 데이터, 포트폴리오, 체결 로직을 분리한 **시스템 아키텍처 이해**에 초점을 두었다.

---

## 주요 특징
- 이벤트 기반 구조의 백테스트 엔진 설계
- 전략, 데이터, 포트폴리오, 체결 로직 완전 분리
- 전략 교체가 가능한 구조 (엔진 수정 없이 확장 가능)
- 포트폴리오 자산 추적 및 성과 지표 계산 지원

---

## 시스템 아키텍처
MarketEvent 발생
↓
Strategy → SignalEvent
↓
Portfolio → Order
↓
ExecutionHandler → FillEvent
↓
Portfolio 자산 업데이트

yaml
코드 복사

---

## 프로젝트 구조
backtester
├─ engine.py # 이벤트 흐름 제어 (메인 루프)
├─ data.py # 시세 데이터 스트리밍
├─ event.py # Market / Signal / Order / Fill 이벤트 정의
├─ strategy.py # 매매 전략 모음
├─ portfolio.py # 자산 및 포지션 관리
└─ execution.py # 주문 체결 시뮬레이터

yaml
코드 복사

---

## 구현된 전략

### 이동평균 교차 전략 (Moving Average Cross)
- 20일 / 50일 이동평균 기반
- 골든크로스 발생 시 매수
- 데드크로스 발생 시 포지션 종료

### 모멘텀 전략 (Momentum)
- 최근 12개월(252 거래일) 가격 변화 기준
- 상승 추세 시 매수, 하락 추세 시 포지션 종료

### 평균 회귀 전략 (Mean Reversion)
- 최근 20일 평균 대비 ±3% 이탈 시 매매
- 과매도 구간 매수 / 과매수 구간 매도

---

## 포트폴리오 및 성과 분석

### 관리 항목
- 현금 잔고
- 보유 주식 수량
- 일별 총 자산 가치 (Equity Curve)

### 성과 지표
- Equity Curve
- Sharpe Ratio
- Maximum Drawdown (MDD)

---

## 사용 기술
- **Language**: Python
- **Data Processing**: Pandas, NumPy
- **Market Data**: Yahoo Finance (yfinance)
- **Visualization**: Matplotlib
