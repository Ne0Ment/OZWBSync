from python.ozonattributes import NameAttribute, SearchTagsAttribute, AttributeSerializer, AttributeVerifier
from python.productclasses import Product, ProductDimensions, DimensionUnit, ProductWeight, WeightUnit, ProductMedia, ProductGeneralInfo, ProductSerializer

dimensions1 = ProductDimensions(DimensionUnit.MM, 10, 100, 1000)
weight1 = ProductWeight(WeightUnit.GRAMMS, 1000)
media1 = ProductMedia(['asdf', 'qwerty'])
attributes1 = set(
    [NameAttribute("asdf"), SearchTagsAttribute("amogus, sus, bebra")])
general_info1 = ProductGeneralInfo("asdf", "amogus", "4206942069")

dimensions2 = ProductDimensions(DimensionUnit.MM, 10, 100, 1000)
weight2 = ProductWeight(WeightUnit.GRAMMS, 1000)
media2 = ProductMedia(['asdf', 'qwerty'])
attributes2 = set(
    [NameAttribute("asdf"), SearchTagsAttribute("amogus, sus, bebra")])
general_info2 = ProductGeneralInfo("asdf", "amogus", "4206942069")

product1 = Product(dimensions1, weight1, media1, attributes1, general_info1)
product2 = Product(dimensions2, weight2, media2, attributes2, general_info2)

attributeSerializer = AttributeSerializer(AttributeVerifier('ms_attrib_dict.pickle'))
productSerializer = ProductSerializer(attributeSerializer)


def test_product_serialization():
    serialized1 = productSerializer.to_dict(product1)
    serialized2 = productSerializer.to_dict(product2)
    assert serialized1 == serialized2
