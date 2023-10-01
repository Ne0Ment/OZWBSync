from enum import Enum
from typing import List

from ozonattributes import Attribute
from utility import same_class


class OzonDimensionUnit(Enum):
    MM = 'mm'
    CM = 'cm'
    IN = 'in'


class OzonWeightUnit(Enum):
    GRAMMS = 'g'
    KG = 'kg'
    LB = 'lb'


class OzonCurrencyCode(Enum):
    RUB = 'RUB'
    USD = 'USD'


class OzonNDSValue(Enum):
    ZERO = '0'
    TEN = '0.1'
    TWENTY = '0.2'


class OzonProductDimensions():
    def __init__(self, dimension_unit: OzonDimensionUnit, height: int, width: int, depth: int) -> None:
        self.dimension_unit = dimension_unit
        self.height = height
        self.width = width
        self.depth = depth

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.dimension_unit.value == other.dimension_unit.value and \
            self.height == other.height and \
            self.width == other.width and \
            self.depth == other.depth

    def __str__(self) -> str:
        return f'height: {self.height} width: {self.width} depth: {self.depth} unit: {self.dimension_unit}\n'


class OzonProductWeight():
    def __init__(self, weight_unit: OzonWeightUnit, weight: int) -> None:
        self.weight_unit = weight_unit
        self.weight = weight

    @same_class
    def __eq__(self, other: object) -> bool:
        if other.__class__.__qualname__ == self.__class__.__qualname__:
            return self.weight == other.weight and \
                self.weight_unit.value == other.weight_unit.value
        return False

    def __str__(self) -> str:
        return f'unit: {self.weight_unit} weight: {self.weight}\n'


class OzonProductPrice():
    def __init__(self, old_price: str, price: str, min_price: str) -> None:
        self.old_price = old_price
        self.price = price
        self.min_price = min_price

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.old_price == other.old_price and \
            self.price == other.price and \
            self.min_price == other.min_price

    def __str__(self) -> str:
        return f'price: {self.price} old_price: {self.old_price} min_price: {self.min_price}\n'


class OzonProductMedia():
    def __init__(self, images: List[str]) -> None:
        self.images = images

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.images == other.images

    def __str__(self) -> str:
        return f'images: {[" ".join(self.images)]}\n'


class OzonProductGeneralInfo():
    def __init__(self, name: str, offer_id: str, category_id: int) -> None:
        self.name = name
        self.offer_id = offer_id
        self.category_id = category_id

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.name == other.name and \
            self.offer_id == other.offer_id and \
            self.category_id == other.category_id

    def __str__(self) -> str:
        return f'name: {self.name} offer_id: {self.offer_id} category_id: {self.category_id}\n'


class OzonProduct():
    def __init__(self, dimensions: OzonProductDimensions, weight: OzonProductWeight,
                 media: OzonProductMedia, attributes: set[Attribute], info: OzonProductGeneralInfo, price: OzonProductPrice) -> None:
        self.dimensions = dimensions
        self.weight = weight
        self.media = media
        self.attributes = attributes
        self.info = info
        self.price = price

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.dimensions == other.dimensions and \
            self.weight == other.weight and \
            self.media == other.media and \
            self.attributes == other.attributes and \
            self.info == other.info and \
            self.price == other.price

    def __str__(self) -> str:
        attributes_str = '\n' + \
            '\n    '.join([str(i) for i in self.attributes]) + '\n'
        return 'ozonproduct\n' + \
            'info: ' + str(self.info) + \
            'weight: ' + str(self.weight) + \
            'media: ' + str(self.media) + \
            'dimensions: ' + str(self.dimensions) + \
            'price: ' + str(self.price) + \
            'attributes: ' + attributes_str


class OzonGeneralProduct(OzonProduct):
    def __init__(self, dimensions: OzonProductDimensions, weight: OzonProductWeight,
                 media: OzonProductMedia, attributes: List[Attribute],
                 varying_attributes: List[List[Attribute]],
                 info: OzonProductGeneralInfo, price: OzonProductPrice) -> None:
        super().__init__(dimensions, weight, media, attributes, info, price)
        self.varying_attributes = varying_attributes

    def expand_into_products(self) -> List[OzonProduct]:
        products = []
        for attribute_variation in self.varying_attributes:
            variation_size = [
                a for a in attribute_variation if a._id == 9533][0].value
            products.append(OzonProduct(self.dimensions,
                                        self.weight,
                                        self.media,
                                        self.attributes | set(
                                            attribute_variation),
                                        OzonProductGeneralInfo(
                                            self.info.name, f'{self.info.offer_id}_{variation_size}', self.info.category_id),
                                        self.price))
        return products

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.dimensions == other.dimensions and \
            self.weight == other.weight and \
            self.media == other.media and \
            self.attributes == other.attributes and \
            self.varying_attributes == other.varying_attributes and \
            self.info == other.info and \
            self.price == other.price


class OzonProductCategory():
    def __init__(self, category_name, category_type, category_products: List[OzonGeneralProduct]) -> None:
        self.category_name = category_name
        self.category_type = category_type
        self.category_products = category_products

    @same_class
    def __eq__(self, other: object) -> bool:
        return self.category_name == other.category_name and \
            self.category_type == other.category_type and \
            self.category_products == other.category_products
