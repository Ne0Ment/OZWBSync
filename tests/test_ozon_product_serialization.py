from python.dbclasses import DBConnection
from python.ozonattributes import ColorAttribute, NameAttribute, PhotoProductSizeAttribute, SearchTagsAttribute
from python.ozonproduct import OzonGeneralProduct, OzonProductCategory, OzonProductDimensions, OzonDimensionUnit, OzonProductPrice, OzonProductWeight, OzonWeightUnit, OzonProductMedia, OzonProductGeneralInfo
from python.serializers import OzonAttributeSerializer, OzonGeneralProductSerializer, OzonProductCategorySerializer

dimensions1 = OzonProductDimensions(OzonDimensionUnit.MM, 10, 100, 1000)
weight1 = OzonProductWeight(OzonWeightUnit.GRAMMS, 1000)
media1 = OzonProductMedia(['asdf', 'qwerty'])
attributes1 = set(
    [NameAttribute("asdf"), SearchTagsAttribute("amogus, sus, bebra")])
general_info1 = OzonProductGeneralInfo("asdf", "amogus", "4206942069")
price1 = OzonProductPrice(2000, 1500, 1000)

dimensions2 = OzonProductDimensions(OzonDimensionUnit.MM, 10, 100, 1000)
weight2 = OzonProductWeight(OzonWeightUnit.GRAMMS, 1000)
media2 = OzonProductMedia(['asdf', 'qwerty'])
attributes2 = set(
    [NameAttribute("asdf"), SearchTagsAttribute("amogus, sus, bebra")])
general_info2 = OzonProductGeneralInfo("asdf", "amogus", "4206942069")
price2 = OzonProductPrice(2000, 1500, 1000)

product1 = OzonGeneralProduct(dimensions1, weight1, media1,
                              attributes1, [
                                  [ColorAttribute(["серый"]),
                                   ColorAttribute(["белый"])],
                                  [PhotoProductSizeAttribute(
                                      '62'), PhotoProductSizeAttribute('64')]
                              ], general_info1, price1)
product2 = OzonGeneralProduct(dimensions2, weight2, media2,
                              attributes2, [
                                  [ColorAttribute(["серый"]),
                                   ColorAttribute(["белый"])],
                                  [PhotoProductSizeAttribute(
                                      '62'), PhotoProductSizeAttribute('64')]
                              ], general_info2, price2)

attributeSerializer = OzonAttributeSerializer(DBConnection().init_verifier())
product_serializer = OzonGeneralProductSerializer(attributeSerializer)

serialized1 = product_serializer.serialize(product1)
serialized2 = product_serializer.serialize(product2)
deserialized1 = product_serializer.deserialize(serialized1)
deserialized2 = product_serializer.deserialize(serialized2)

category1 = OzonProductCategory("asdf", "qwerty", [product1])
category2 = OzonProductCategory("asdf", "qwerty", [product1])

category_serializer = OzonProductCategorySerializer(product_serializer)

serialized_category1 = category_serializer.serialize(category1)
serialized_category2 = category_serializer.serialize(category2)

deserialized_category1 = category_serializer.deserialize(serialized_category1)
deserialized_category2 = category_serializer.deserialize(serialized_category2)


def test_same_product_serialization():
    assert serialized1 == serialized2


def test_same_product_deserialization():
    assert deserialized1 == deserialized2


def test_correct_product_serialization_deserialization():
    assert deserialized1 == product1
    assert deserialized2 == product2


def test_correct_category_serialization():
    assert deserialized_category1 == deserialized_category2
    assert category1 == deserialized_category1
    assert category2 == deserialized_category2
