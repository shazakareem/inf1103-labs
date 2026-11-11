from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        if type(quantity) is not int or quantity < 1:
            raise ValueError("Order quantity must be a positive whole number.")
        self.__order_lines.append(OrderLine(product, quantity))

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def calculate_total(self) -> float:
        return sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)