from .event import FillEvent


class ExecutionHandler:
    """
    ExecutionHandler (체결 핸들러)

    실제 시장에서는 주문을 넣으면,
    - 매수 체결



    - 매도 체결
    - 부분 체결
    - 미체결
    이런 다양한 상황이 발생한다.

    그러나 백테스트에서는 "가정"을 사용한다:
    → 주문을 넣으면 항상 즉시, 그 가격(price)으로 체결된다고 가정.

    이 역할을 수행하는 것이 ExecutionHandler다.
    즉, 백테스트용 체결 시뮬레이터(simulator).
    """

    def execute(self, order, price):
        """
        주문(OrderEvent)을 받아서 체결(FillEvent) 이벤트를 생성한다.

        Parameters
        ----------
        order : (direction, quantity) 형태의 튜플
            direction : BUY 또는 SELL
            quantity : 주문 수량

        price : float
            주문을 체결할 가격 (백테스트에서는 보통 종가 Close 값)

        Returns
        -------
        FillEvent
            direction, quantity, price를 담고 있는 체결 이벤트 객체
        """

        # order는 튜플 형태 → (direction, qty)
        direction, qty = order

        # FillEvent 생성 후 반환
        # → "주문이 체결되었다"는 의미의 이벤트
        return FillEvent(direction=direction, quantity=qty, price=price)
