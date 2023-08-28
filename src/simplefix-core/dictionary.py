import collections
from enum import Enum
from typing import List, Callable
from xml.etree.ElementTree import Element

from version.version_controller import VersionController as VC


class Version(Enum):
    FIX_40 = '4.0'
    FIX_41 = '4.1'
    FIX_42 = '4.2'
    FIX_43 = '4.3'
    FIX_44 = '4.4'
    FIX_50 = '5.0'


class BaseElementClass:
    def __init__(self, **kwargs):
        if 'element' not in kwargs:
            raise Exception('Cannot found XML Element in parameters')


class Value(BaseElementClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'element' in kwargs:
            el: Element = kwargs['element']
            self.enum = el.attrib.get('enum')
            self.description = el.attrib.get('description')

    @property
    def enum(self):
        return self._enum

    @enum.setter
    def enum(self, value):
        self._enum = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value


class Field(BaseElementClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        el: Element = kwargs['element']
        self.name = el.get('name')
        self.required = el.get('required')
        self.repeating = el.get('repeating')
        self.type = el.get('type')
        self.number = el.get('number')
        self.values = list(map(lambda ele: Field(element=ele), el.findall('value')))

    @property
    def repeating(self):
        return self._repeating

    @property
    def name(self):
        return self._name

    @property
    def required(self):
        return self._required

    @property
    def type(self):
        return self._type

    @property
    def number(self):
        return self._number

    @name.setter
    def name(self, value):
        self._name = value

    @required.setter
    def required(self, value):
        self._required = value

    @repeating.setter
    def repeating(self, value):
        self._repeating = value

    @type.setter
    def type(self, value):
        self._type = value

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value


class Message(BaseElementClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'element' in kwargs:
            el = kwargs['element']
            self.name = el.attrib.get('name')
            self.msg_type = el.attrib.get('msgtype')
            self.msg_cat = el.attrib.get('msgcat')
            self.fields = list(map(lambda ele: Field(element=ele), el.findall('field')))

    @property
    def name(self) -> str:
        return self._name

    @property
    def msg_type(self) -> str:
        return self._msg_type

    @property
    def msg_cat(self) -> str:
        return self._msg_cat

    @name.setter
    def name(self, value):
        self._name = value

    @msg_type.setter
    def msg_type(self, value):
        self._msg_type = value

    @msg_cat.setter
    def msg_cat(self, value):
        self._msg_cat = value

    @property
    def fields(self) -> List[Field]:
        return self._fields

    @fields.setter
    def fields(self, var):
        self._fields = var


class DataDictionary:
    """Dictionary for FIX protocol message
    Parameters
    ----------
    Attributes
    ----------
    """

    def __init__(self, fix_version: str):
        xml = VC(fix_version).xml_tree
        root = xml.getroot()
        self.header = parse_list_field(root.findall('header')[0].findall('field'))
        self.trailer = parse_list_field(root.findall('trailer')[0].findall('field'))
        self.messages = list(map(lambda e: Message(element=e),
                                 root.findall('messages')[0].findall('message')))
        self.fields = parse_list_field(root.findall('fields')[0].findall('field'))

    @property
    def header(self) -> List[Field]:
        return self._header

    @property
    def trailer(self) -> List[Field]:
        return self._trailer

    @property
    def messages(self) -> List[Message]:
        return self._messages

    @property
    def fields(self) -> List[Field]:
        return self._fields

    @header.setter
    def header(self, value):
        self._header = value

    @trailer.setter
    def trailer(self, value):
        self._trailer = value

    @messages.setter
    def messages(self, value):
        self._messages = value

    @fields.setter
    def fields(self, value):
        self._fields = value


def parse_list_field(attributes: list[Element]) -> List[Field]:
    return list(map(lambda x: Field(element=x), attributes))
