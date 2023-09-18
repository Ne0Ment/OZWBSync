import pickle

import ozonattributes as ozon
from ozonproduct import OzonProductCategory, OzonDimensionUnit, OzonProductDimensions, OzonProductGeneralInfo, OzonProductMedia, OzonProductWeight, OzonWeightUnit, OzonGeneralProduct, OzonProduct

OZON_ATTRIB_DICT_FILENAME = 'ms_attrib_dict.pickle'


class OzonAttributeVerifier():
    def __init__(self, dict_path=OZON_ATTRIB_DICT_FILENAME) -> None:
        with open(dict_path, 'rb') as f:
            self.attrib_dict: dict = pickle.load(f)

    def _verify_value(self, attribute_id: int, value):
        if attribute_id not in self.attrib_dict:
            raise ValueError(attribute_id)
        if self.attrib_dict[attribute_id]['values'] == []:
            return True
        if ozon.id2class[attribute_id] == ozon.BrandAttribute and value == 'Нет бренда':
            return True
        return len([i for i in self.attrib_dict[attribute_id]['values'] if i['value'] == value]) != 0

    def verify_attribute(self, attribute: ozon.Attribute):
        if not attribute.verify():
            return False
        if type(attribute.value) == list:
            return all([self._verify_value(attribute._id, i) for i in attribute.value])

        return self._verify_value(attribute._id, attribute.value)


class OzonAttributeSerializer():
    def __init__(self, verifier: OzonAttributeVerifier) -> None:
        self.verifier = verifier

    def serialize(self, attribute: ozon.Attribute):
        return {
            'id': attribute._id,
            'name': attribute.name,
            'value': attribute.value
        }

    def deserialize(self, data) -> ozon.Attribute:
        attr: ozon.Attribute = ozon.id2class[data['id']](data['value'])
        if self.verifier.verify_attribute(attr):
            return attr
        raise ValueError(attr.value)


class OzonGeneralProductSerializer():
    def __init__(self, attribute_serializer: OzonAttributeSerializer) -> None:
        self.attribute_serializer = attribute_serializer

    def serialize(self, product: OzonGeneralProduct):
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
            'attributes': [self.attribute_serializer.serialize(i) for i in product.attributes],
            'varying_attributes': [
                [self.attribute_serializer.serialize(attribute_variety)
                 for attribute_variety in varying_attribute]
                for varying_attribute in product.varying_attributes]
        }

    def deserialize(self, data) -> OzonProduct:
        return OzonGeneralProduct(
            dimensions=OzonProductDimensions(OzonDimensionUnit[data['dimensions']['dimension_unit']],
                                             data['dimensions']['height'],
                                             data['dimensions']['width'],
                                             data['dimensions']['depth']),

            weight=OzonProductWeight(OzonWeightUnit[data['weight']['weight_unit']],
                                     data['weight']['weight']),

            media=OzonProductMedia(data['media']['images']),

            attributes=set([self.attribute_serializer.deserialize(i)
                           for i in data['attributes']]),

            varying_attributes=[[self.attribute_serializer.deserialize(attribute_variety)
                                 for attribute_variety in varying_attribute]
                                for varying_attribute in data['varying_attributes']],

            info=OzonProductGeneralInfo(
                data['name'], data['offer_id'], data['category_id'])

        )


class OzonProductCategorySerializer():
    def __init__(self, general_product_serializer: OzonGeneralProductSerializer) -> None:
        self.general_product_serializer = general_product_serializer

    def serialize(self, product_category: OzonProductCategory):
        return {
            'category_name': product_category.category_name,
            'category_type': product_category.category_type,
            'category_products': [self.general_product_serializer.serialize(general_product)
                                  for general_product in product_category.category_products]
        }

    def deserialize(self, data):
        return OzonProductCategory(
            category_name=data['category_name'],
            category_type=data['category_type'],
            category_products=[self.general_product_serializer.deserialize(general_product)
                               for general_product in data['category_products']]
        )
