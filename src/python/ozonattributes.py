from typing import List
from utility import same_class


class Attribute():
    def __init__(self, _id, name, value):
        self._id = _id
        self.name = name
        self.value = value

    def verify(self):
        return True

    @same_class
    def __eq__(self, other: object) -> bool:
        return self._id == other._id and \
            self.name == other.name and \
            self.value == other.value

    def __hash__(self) -> int:
        return hash(hash(self._id) + hash(self.name) + hash(self.value))

    def __str__(self) -> str:
        return f'id: {self._id} name: {self.name} value: {self.value}'


class StringAttribute(Attribute):
    def __init__(self, _id, name, value):
        super().__init__(_id, name, value)

    def verify(self):
        return super().verify() and type(self.value) == str and self.value != ""


class IntAttribute(Attribute):
    def __init__(self, _id, name, value):
        super().__init__(_id, name, value)

    def verify(self):
        return super().verify() and type(self.value) == int


class FloatAttribute(Attribute):
    def __init__(self, _id, name, value):
        super().__init__(_id, name, value)

    def verify(self):
        return super().verify() and type(self.value) == float


class BoolAttribute(Attribute):
    def __init__(self, _id, name, value):
        super().__init__(_id, name, value)

    def verify(self):
        return super().verify() and type(self.value) == bool


class MultiAttribute(Attribute):
    def __init__(self, _id, name, value):
        if not isinstance(value, list):
            raise ValueError(value)
        super().__init__(_id, name, value)

    def verify(self):
        return self.value != []

    def __hash__(self) -> int:
        s = hash(self._id) + hash(self.name)
        for val in self.value:
            s += hash(val)
        return hash(s)


class MultiStringAttribute(MultiAttribute):
    def __init__(self, _id, name, value):
        super().__init__(_id, name, value)

    def verify(self):
        return super().verify() and all([(type(i) == str and i != "") for i in self.value])


class MultiIntAttribute(MultiAttribute):
    def __init__(self, _id, name, value):
        super().__init__(_id, name, value)

    def verify(self):
        return super().verify() and all([type(i) == int for i in self.value])


class MultiNumberAttribute(MultiAttribute):
    def __init__(self, _id, name, value):
        super().__init__(_id, name, value)

    def verify(self):
        return super().verify() and all([(type(i) == int or type(i) == float) for i in self.value])


class BrandAttribute(StringAttribute):
    def __init__(self, value="Нет бренда"):
        super().__init__(31, "Бренд", value)


class RuSizeAttribute(MultiStringAttribute):
    def __init__(self, value: List[str]):
        super().__init__(4295, "Российский размер", value)


class TypeAttribute(StringAttribute):
    def __init__(self, value: str):
        super().__init__(8229, "Тип", value)


class GroupingAttribute(StringAttribute):
    def __init__(self, value: str):
        super().__init__(8292, "Объединить на одной карточке", value)


class GenderAttribute(MultiStringAttribute):
    def __init__(self, value: List[str]):
        super().__init__(9163, "Пол", value)


class ColorAttribute(MultiStringAttribute):
    def __init__(self, value: List[str]):
        super().__init__(10096, "Цвет товара", value)


class SeriesAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(33, 'Серия в одежде и обуви', value)


class NameAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4180, "Название", value)


class AnnotationAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4191, 'Аннотация', value)


class PackageTypeAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4300, 'Тип упаковки одежды', value)


class ProducerCountryAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4389, 'Страна-изготовитель', value)


class MaterialAttribute(MultiStringAttribute):
    def __init__(self, value: List[str]):
        super().__init__(4496, 'Материал', value)


class PackagedWeightAttribute(FloatAttribute):
    def __init__(self, value):
        super().__init__(4497, 'Вес с упаковкой, г', value)


class PhotoProductSizeAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4508, 'Размер товара на фото', value)


class SleeveLengthAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4596, 'Длина рукава', value)


class MaterialCompositionAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4604, 'Состав материала', value)


class SleeveTypeAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4621, 'Вид рукава', value)


class CareInstructionsAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(4655, 'Инструкция по уходу', value)


class ProducerArticleAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(9024, 'Артикул', value)

    def verify(self):
        return self.value != ''


class AdultAttribute(BoolAttribute):
    def __init__(self, value: bool):
        super().__init__(9070, 'Признак 18+', value)


class TargetAudienceAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(9390, 'Целевая аудитория', value)


class PrintTypeAttribute(MultiStringAttribute):
    def __init__(self, value: List[str]):
        super().__init__(9437, 'Вид принта', value)


class ProducerSizeAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(9533, 'Размер производителя', value)


class ProductsPerPackageAttribute(IntAttribute):
    def __init__(self, value):
        super().__init__(9661, 'Количество в упаковке', value)


class ColorNameAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(10097, 'Название цвета', value)


class NeckShapeAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(11071, 'Форма воротника/горловины', value)


class RichContentAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(11254, 'Rich-контент JSON', value)


class JsonSizeTableAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(13164, 'Таблица размеров JSON', value)


class SearchTagsAttribute(StringAttribute):
    def __init__(self, value):
        super().__init__(22336, 'Ключевые слова', value)


id2class = {9070: AdultAttribute,
            4191: AnnotationAttribute,
            31: BrandAttribute,
            4655: CareInstructionsAttribute,
            10096: ColorAttribute,
            10097: ColorNameAttribute,
            9163: GenderAttribute,
            8292: GroupingAttribute,
            13164: JsonSizeTableAttribute,
            4496: MaterialAttribute,
            4604: MaterialCompositionAttribute,
            4180: NameAttribute,
            11071: NeckShapeAttribute,
            4300: PackageTypeAttribute,
            4497: PackagedWeightAttribute,
            4508: PhotoProductSizeAttribute,
            9437: PrintTypeAttribute,
            9024: ProducerArticleAttribute,
            4389: ProducerCountryAttribute,
            9633: ProducerSizeAttribute,
            9661: ProductsPerPackageAttribute,
            11254: RichContentAttribute,
            4295: RuSizeAttribute,
            22336: SearchTagsAttribute,
            33: SeriesAttribute,
            4596: SleeveLengthAttribute,
            4621: SleeveTypeAttribute,
            9390: TargetAudienceAttribute,
            8229: TypeAttribute
            }

class2id = {'AdultAttribute': 9070,
            'AnnotationAttribute': 4191,
            'BrandAttribute': 31,
            'CareInstructionsAttribute': 4655,
            'ColorAttribute': 10096,
            'ColorNameAttribute': 10097,
            'GenderAttribute': 9163,
            'GroupingAttribute': 8292,
            'JsonSizeTableAttribute': 13164,
            'MaterialAttribute': 4496,
            'MaterialCompositionAttribute': 4604,
            'NameAttribute': 4180,
            'NeckShapeAttribute': 11071,
            'PackageTypeAttribute': 4300,
            'PackagedWeightAttribute': 4497,
            'PhotoProductSizeAttribute': 4508,
            'PrintTypeAttribute': 9437,
            'ProducerArticleAttribute': 9024,
            'ProducerCountryAttribute': 4389,
            'ProducerSizeAttribute': 9633,
            'ProductsPerPackageAttribute': 9661,
            'RichContentAttribute': 11254,
            'RuSizeAttribute': 4295,
            'SearchTagsAttribute': 22336,
            'SeriesAttribute': 33,
            'SleeveLengthAttribute': 4596,
            'SleeveTypeAttribute': 4621,
            'TargetAudienceAttribute': 9390,
            'TypeAttribute': 8229}
