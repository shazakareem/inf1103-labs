from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = NoDiscount() if discount is None else discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def calculate_total(self) -> float:
        total = sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)
        return self.discount.apply(total)
