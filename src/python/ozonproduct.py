from enum import Enum
from typing import List

from ozonattributes import Attribute, AttributeSerializer
from itertools import product as iter_product


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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OzonProductDimensions):
            return self.dimension_unit == other.dimension_unit and \
                self.height == other.height and \
                self.width == other.width and \
                self.depth == other.depth
        return False

    def __str__(self) -> str:
        return f'height: {self.height} width: {self.width} depth: {self.depth} unit: {self.dimension_unit}\n'


class OzonProductWeight():
    def __init__(self, weight_unit: OzonWeightUnit, weight: int) -> None:
        self.weight_unit = weight_unit
        self.weight = weight

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OzonProductWeight):
            return self.weight == other.weight and \
                self.weight_unit == other.weight_unit
        return False

    def __str__(self) -> str:
        return f'unit: {self.weight_unit} weight: {self.weight}\n'


class OzonProductPrices():
    def __init__(self, old_price: str, price: str, min_price: str) -> None:
        self.old_price = old_price
        self.price = price
        self.min_price = min_price

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OzonProductPrices):
            return self.old_price == other.old_price and \
                self.price == other.price and \
                self.min_price == other.min_price
        return False

    def __str__(self) -> str:
        return f'price: {self.price} old_price: {self.old_price} min_price: {self.min_price}\n'


class OzonProductMedia():
    def __init__(self, images: List[str]) -> None:
        self.images = images

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OzonProductMedia):
            return self.images == other.images
        return False

    def __str__(self) -> str:
        return f'images: {[" ".join(self.images)]}\n'


class OzonProductGeneralInfo():
    def __init__(self, name: str, offer_id: str, category_id: int) -> None:
        self.name = name
        self.offer_id = offer_id
        self.category_id = category_id

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OzonProductGeneralInfo):
            return self.name == other.name and \
                self.offer_id == other.offer_id and \
                self.category_id == other.category_id
        return False

    def __str__(self) -> str:
        return f'name: {self.name} offer_id: {self.offer_id} category_id: {self.category_id}\n'


class OzonProduct():
    def __init__(self, dimensions: OzonProductDimensions, weight: OzonProductWeight,
                 media: OzonProductMedia, attributes: set[Attribute], info: OzonProductGeneralInfo) -> None:
        self.dimensions = dimensions
        self.weight = weight
        self.media = media
        self.attributes = attributes
        self.info = info

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OzonProduct):
            return self.dimensions == other.dimensions and \
                self.weight == other.weight and \
                self.media == other.media and \
                self.attributes == other.attributes and \
                self.info == other.info
        return False

    def __str__(self) -> str:
        attributes_str = '\n' + \
            '\n    '.join([str(i) for i in self.attributes]) + '\n'
        return 'ozonproduct\n' + \
            'info: ' + str(self.info) + \
            'weight: ' + str(self.weight) + \
            'media: ' + str(self.media) + \
            'dimensions: ' + str(self.dimensions) + \
            'attributes: ' + attributes_str


class OzonGeneralProduct(OzonProduct):
    def __init__(self, dimensions: OzonProductDimensions, weight: OzonProductWeight,
                 media: OzonProductMedia, attributes: List[Attribute],
                 varying_attributes: List[List[Attribute]],
                 info: OzonProductGeneralInfo) -> None:
        super().__init__(dimensions, weight, media, attributes, info)
        self.varying_attributes = varying_attributes

    def expand_into_products(self) -> List[OzonProduct]:
        products = []
        attribute_variations = iter_product(*self.varying_attributes)
        for attribute_variation in attribute_variations:
            products.append(OzonProduct(self.dimensions,
                                        self.weight,
                                        self.media,
                                        self.attributes | set(
                                            attribute_variation),
                                        self.info))
        return products


class ProductSerializer():
    def __init__(self, attributeSerializer: AttributeSerializer) -> None:
        self.attributeSerializer = attributeSerializer

    def to_dict(self, product: OzonProduct):
        return {
            'name': product.info.name,
            'offer_id': product.info.offer_id,
            'category_id': product.info.category_id,
            'weight': {
                'weight_unit': product.weight.weight_unit.name,
                'weight': product.weight.weight
            },
            'media': {
                'images': product.media.images
            },
            'dimensions': {
                'dimension_unit': product.dimensions.dimension_unit.name,
                'depth': product.dimensions.depth,
                'width': product.dimensions.width,
                'height': product.dimensions.height
            },
            'attributes': [self.attributeSerializer.to_dict(i) for i in product.attributes]}

    def from_dict(self, data) -> OzonProduct:
        attributeSerializer = AttributeSerializer()
        return OzonProduct(
            dimensions=OzonProductDimensions(OzonDimensionUnit(data['dimensions']['dimension_unit']),
                                             data['dimensions']['height'],
                                             data['dimensions']['width'],
                                             data['dimensions']['depth']),

            weight=OzonProductWeight(OzonWeightUnit(data['weight']['weight_unit']),
                                     data['weight']['weight']),

            media=OzonProductMedia(data['media']['images']),

            attributes=set([attributeSerializer.from_dict(i)
                           for i in data['attributes']]),

            info=OzonProductGeneralInfo(
                data['name'], data['offer_id'], data['category_id'])

        )
