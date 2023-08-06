from jesse.strategies import Strategy
from jesse import utils


# test_route_capital_isolation
class TestRouteCapitalIsolation1(Strategy):
    def should_long(self) -> bool:
        print(self.symbol, self.price, self.capital)
        return self.index == 0

    def should_short(self) -> bool:
        return False

    def go_long(self):
        qty = utils.size_to_qty(1000, self.price)
        self.buy = qty, self.price

    def go_short(self):
        pass

    def should_cancel(self):
        return False

    def update_position(self):
        print(self.capital)
