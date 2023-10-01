from utility import same_class
from typing import List


class Stock():
    def __init__(self, size, color, stock) -> None:
        self.size = size
        self.color = color
        self.stock = stock

    def reduce_stock(self, by=1):
        self.stock -= by

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.size == other.size and \
            self.color == other.color and \
            self.stock == other.stock

    def __str__(self) -> str:
        return f'size: {self.size} color: {self.color} stock: {self.stock}'


class CategoryStock():
    def __init__(self, category_name, stocks: List[Stock]) -> None:
        self.category_name = category_name
        self.category_stocks = stocks

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.category_name == other.category_name and \
            self.category_stocks == other.category_stocks

    def __str__(self) -> str:
        return f'category_name: {self.category_name}, stocks: \n ' + [str(s) for s in self.category_stocks]
