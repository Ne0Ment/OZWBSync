from python.ozonattributes import AdultAttribute, AnnotationAttribute, AttributeVerifier, BrandAttribute, CareInstructionsAttribute, ColorAttribute, ColorNameAttribute, GenderAttribute, GroupingAttribute, JsonSizeTableAttribute, MaterialAttribute, MaterialCompositionAttribute, NameAttribute, NeckShapeAttribute, PackageTypeAttribute, PackagedWeightAttribute, PhotoProductSizeAttribute, PrintTypeAttribute, ProducerArticleAttribute, ProducerCountryAttribute, ProducerSizeAttribute, ProductsPerPackageAttribute, RichContentAttribute, RuSizeAttribute, SearchTagsAttribute, SeriesAttribute, SleeveLengthAttribute, SleeveTypeAttribute, TargetAudienceAttribute, TypeAttribute

attributeVerifier = AttributeVerifier("ms_attrib_dict.pickle")


def test_brand():
    attrib = BrandAttribute('амогус')
    assert attributeVerifier.verify_attribute(attrib) is False

    attrib = BrandAttribute('Нет бренда')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = BrandAttribute('Yamaha')
    assert attributeVerifier.verify_attribute(attrib) is True


def test_rusize():
    attrib = RuSizeAttribute(['62'])
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = RuSizeAttribute(['бебра'])
    assert attributeVerifier.verify_attribute(attrib) is False


def test_type():
    attrib = TypeAttribute('Футболка')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = TypeAttribute('бебра')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_grouping():
    attrib = GroupingAttribute('бебра')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = GroupingAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_gender():
    attrib = GenderAttribute(['Мужской', 'Женский'])
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = GenderAttribute(['бебра'])
    assert attributeVerifier.verify_attribute(attrib) is False


def test_color():
    attrib = ColorAttribute(['черный', 'серый'])
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = ColorAttribute(['бебра'])
    assert attributeVerifier.verify_attribute(attrib) is False


def test_series():
    attrib = SeriesAttribute('Феникс')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = SeriesAttribute('бебра')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_name():
    attrib = NameAttribute('бебрамогус')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = NameAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_annotation():
    attrib = AnnotationAttribute('бебрамогус')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = AnnotationAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_packagetype():
    attrib = PackageTypeAttribute('Пакет')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = PackageTypeAttribute('Дельтаплан с парнаса до кронвы')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_producercountry():
    attrib = ProducerCountryAttribute('Россия')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = ProducerCountryAttribute('Дельтаплан с парнаса до кронвы')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_material():
    attrib = MaterialAttribute(['Хлопок', 'ABS пластик'])
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = MaterialAttribute(['Дельтаплан с парнаса до кронвы'])
    assert attributeVerifier.verify_attribute(attrib) is False


def test_packageweight():
    attrib = PackagedWeightAttribute(1.2)
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = PackagedWeightAttribute('бебра')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_photoproductsize():
    attrib = PhotoProductSizeAttribute('62')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = PhotoProductSizeAttribute('бебра')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_sleevelength():
    attrib = SleeveLengthAttribute('Короткий')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = SleeveLengthAttribute('бебра')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_materialcomposition():
    attrib = MaterialCompositionAttribute('100% хлопок')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = MaterialCompositionAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_sleevetype():
    attrib = SleeveTypeAttribute('Стандартный')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = SleeveTypeAttribute('амогусный')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_careinstructions():
    attrib = CareInstructionsAttribute('стирать при бебре')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = CareInstructionsAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_producerarticle():
    attrib = ProducerArticleAttribute('82716t5vi7qg')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = ProducerArticleAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_adult():
    attrib = AdultAttribute(True)
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = AdultAttribute(1234)
    assert attributeVerifier.verify_attribute(attrib) is False


def test_targetaudience():
    attrib = TargetAudienceAttribute('Взрослая')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = TargetAudienceAttribute('Для бебр')
    assert attributeVerifier.verify_attribute(attrib) is False

    attrib = TargetAudienceAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_printtype():
    attrib = PrintTypeAttribute(['Принт/Логотип'])
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = PrintTypeAttribute(['Для бебр'])
    assert attributeVerifier.verify_attribute(attrib) is False

    attrib = PrintTypeAttribute([])
    assert attributeVerifier.verify_attribute(attrib) is False


def test_producersize():
    attrib = ProducerSizeAttribute('XL')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = ProducerSizeAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_productsperpackage():
    attrib = ProductsPerPackageAttribute(3)
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = ProductsPerPackageAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_colorname():
    attrib = ColorNameAttribute('бебрус')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = ColorNameAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_neckshape():
    attrib = NeckShapeAttribute('Классический (отложной)')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = NeckShapeAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_richcontent():
    attrib = RichContentAttribute('бебрус суссус')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = RichContentAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_hsonsizetable():
    attrib = JsonSizeTableAttribute('бебрус суссус')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = JsonSizeTableAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False


def test_searchtags():
    attrib = SearchTagsAttribute('бебрус суссус')
    assert attributeVerifier.verify_attribute(attrib) is True

    attrib = SearchTagsAttribute('')
    assert attributeVerifier.verify_attribute(attrib) is False
