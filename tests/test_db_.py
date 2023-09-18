from python.dbclasses import DBConnection
from python.ozonattributes import ColorAttribute, NameAttribute, PhotoProductSizeAttribute, SearchTagsAttribute
from python.ozonproduct import OzonDimensionUnit, OzonGeneralProduct, OzonProductCategory, OzonProductDimensions, OzonProductGeneralInfo, OzonProductMedia, OzonProductWeight, OzonWeightUnit


dimensions1 = OzonProductDimensions(OzonDimensionUnit.MM, 10, 100, 1000)
weight1 = OzonProductWeight(OzonWeightUnit.GRAMMS, 1000)
media1 = OzonProductMedia(['asdf', 'qwerty'])
attributes1 = set(
    [NameAttribute("asdf"), SearchTagsAttribute("amogus, sus, bebra")])
general_info1 = OzonProductGeneralInfo("asdf", "amogus", "4206942069")

product1 = OzonGeneralProduct(dimensions1, weight1, media1,
                              attributes1, [
                                  [ColorAttribute(["серый"]),
                                   ColorAttribute(["белый"])],
                                  [PhotoProductSizeAttribute(
                                      '62'), PhotoProductSizeAttribute('64')]
                              ], general_info1)

category1 = OzonProductCategory("asdf", "qwerty", [product1])
category2 = OzonProductCategory("bebrasus", "deltaplan", [product1])


db = DBConnection(db_name='test_OZWBSync')
db.clear_db()


def test_new_category():
    db.save_product_category(category1)
    loaded_category = db.load_product_category(category1.category_name)

    assert loaded_category == category1
    db.clear_db()


def test_replace_category():
    db.save_product_category(category1)
    category1.category_type = 'bebra'
    db.save_product_category(category1)

    loaded_category = db.load_product_category(category1.category_name)
    assert loaded_category == category1
    db.clear_db()


def test_get_categories():
    db.save_product_category(category1)
    db.save_product_category(category2)

    loaded_categories = db.load_product_categories()
    assert loaded_categories != []
