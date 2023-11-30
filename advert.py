import json
import keyword
from typing import Any, Union


class ColorizeMixin:
    """
    This is a mixin class that colors
    the string representation of class.

    Attributes:
        repr_color_code: int number of text color.
    """

    def __init_subclass__(cls, repr_color_code, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.repr_color_code = repr_color_code

    def __repr__(self):
        return (
            f'\033[{self.repr_color_code}m'
            f'{self.title} | {self.price}\033[0m'
        )


class DictToAttr:
    """
    This is a class that converts
    dictionary elements to class attributes.
    """

    @staticmethod
    def process_val(v: Any) -> Any:
        """
        Function process given value
        based on its type.
        dict: makes an object of DictToAttr class;
        list: process each element of list;
        other type: does nothing.
        :param v: input value to process
        :return: processed value
        """
        if isinstance(v, dict):
            return DictToAttr(v)
        if isinstance(v, list):
            return [
                DictToAttr.process_val(elem)
                for elem in v
            ]
        return v

    def __init__(self, dictionary: dict):
        for key, val in dictionary.items():
            if keyword.iskeyword(key):
                key += '_'
            processed_val = self.process_val(val)
            setattr(self, key, processed_val)


class BaseAdvert(DictToAttr):
    """
    This is a base class for converting
    dict elements to attributes. Input dictionary
    should have title in its keys.
    """

    def __init__(self, dictionary: dict):
        self._price = 0
        super().__init__(dictionary)
        if not hasattr(self, 'title'):
            raise ValueError('should contain title')

    @property
    def price(self) -> Union[int, float]:
        return self._price

    @price.setter
    def price(self, val: Union[int, float]) -> None:
        if val < 0:
            raise ValueError('must be >= 0')
        self._price = val

    def __repr__(self):
        return f'{self.title} | {self.price}'


class Advert(ColorizeMixin, BaseAdvert, repr_color_code=32):
    pass


if __name__ == '__main__':
    lesson_str = """{
        "title": "python",
        "price": 0,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": [
                {
                    "metro": "Белорусская",
                    "line": [
                        {
                            "color": ["green", "brown"],
                            "name": ["Кольцевая", "Замоскворецкая"]
                        }
                    ]
                }
            ]
        }
    }"""

    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad.location.address)
    print(lesson_ad.location.metro_stations[0].metro)
    print(lesson_ad)
