from python.ozonattributes import NameAttribute, SearchTagsAttribute
from python.ozonproduct import OzonProduct, OzonProductDimensions, OzonDimensionUnit, OzonProductWeight, OzonWeightUnit, OzonProductMedia, OzonProductGeneralInfo


dimensions1 = OzonProductDimensions(OzonDimensionUnit.MM, 10, 100, 1000)
weight1 = OzonProductWeight(OzonWeightUnit.GRAMMS, 1000)
media1 = OzonProductMedia(['asdf', 'qwerty'])
attributes1 = set(
    [NameAttribute("asdf"), SearchTagsAttribute("amogus, sus, bebra")])
general_info1 = OzonProductGeneralInfo("asdf", "amogus", "4206942069")

dimensions2 = OzonProductDimensions(OzonDimensionUnit.MM, 10, 100, 1000)
weight2 = OzonProductWeight(OzonWeightUnit.GRAMMS, 1000)
media2 = OzonProductMedia(['asdf', 'qwerty'])
attributes2 = set(
    [NameAttribute("asdf"), SearchTagsAttribute("amogus, sus, bebra")])
general_info2 = OzonProductGeneralInfo("asdf", "amogus", "4206942069")

dimensions3 = OzonProductDimensions(OzonDimensionUnit.MM, 10, 999, 1000)
weight3 = OzonProductWeight(OzonWeightUnit.GRAMMS, 10)
media3 = OzonProductMedia(['asdf', 'qty'])
attributes3 = set([NameAttribute("asasdads"),
                  SearchTagsAttribute("amogus, sus")])
general_info3 = OzonProductGeneralInfo("asdf", "amos", "420694")


product1 = OzonProduct(dimensions1, weight1, media1, attributes1, general_info1)
product2 = OzonProduct(dimensions2, weight2, media2, attributes2, general_info2)
product3 = OzonProduct(dimensions3, weight3, media3, attributes3, general_info3)


def test_dimensions_equality():
    assert dimensions1 == dimensions2
    assert dimensions1 != dimensions3


def test_weight_equality():
    assert weight1 == weight2
    assert weight1 != weight3


def test_media_equality():
    assert media1 == media2
    assert media1 != media3


def test_attribute_equality():
    assert attributes1 == attributes2
    assert attributes1 != attributes3


def test_generalinfo_equality():
    assert general_info1 == general_info2
    assert general_info1 != general_info3


def test_product_equality():
    assert product1 == product2
    assert product1 != product3
