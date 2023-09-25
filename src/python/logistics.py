from utility import same_class


class RawProduct():
    def __init__(self, product_type, product_size, product_color, stock) -> None:
        self.product_type = product_type
        self.product_size = product_size
        self.product_color = product_color
        self.stock = stock

    def reduce_stock(self, by=1):
        self.stock -= by

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.product_type == other.product_type and \
            self.product_size == other.product_size and \
            self.product_color == other.product_color and \
            self.stock == other.stock

    def __str__(self) -> str:
        return f'type: {self.product_color} size: {self.product_size} color: {self.product_color}'
