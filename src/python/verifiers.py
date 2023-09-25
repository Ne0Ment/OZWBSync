class OzonAttributeVerifier():
    def __init__(self, attrib_dict) -> None:
        self.attrib_dict = attrib_dict

    def _verify_value(self, attribute_id: int, value):
        if attribute_id not in self.attrib_dict:
            raise ValueError(attribute_id)
        if self.attrib_dict[attribute_id]['values'] == []:
            return True
        if attribute_id == 31 and value == 'Нет бренда':
            return True
        return len([i for i in self.attrib_dict[attribute_id]['values'] if i['value'] == value]) != 0

    def verify_attribute(self, attribute):
        if not attribute.verify():
            return False
        if type(attribute.value) == list:
            return all([self._verify_value(attribute._id, i) for i in attribute.value])

        return self._verify_value(attribute._id, attribute.value)
