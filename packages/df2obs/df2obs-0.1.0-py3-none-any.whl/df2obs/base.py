# -*- coding: utf-8 -*-
"""Base class to map data class attributes to pandas DataFrame columns
"""
import pandas as pd
from typing import Any, List, Iterable


class ColumnMappingError(Exception):
    pass


class NonUniformTypeError(Exception):
    pass


class BaseType(type):
    def __new__(cls, name, bases, attrs):
        attributes = {k: v for k, v in attrs.items() if not k.startswith('__') and not callable(v)}
        attrs['__mapped_columns__'] = attributes
        return type.__new__(cls, name, bases, attrs)


class Base(object):
    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__

    def df2obs(self, df) -> Iterable[Any]:
        # check if mapped column names are in df.columns.values; throw exception if not
        if not set(self.__mapped_columns__.values()).issubset(set(df.columns.values.tolist())):
            diff = set(self.__mapped_columns__.values()).difference(set(df.columns.values.tolist()))
            raise ColumnMappingError(f"{diff} does not exist in columns of passed-in DataFrame; please double check mapping")

        for _, row in df.iterrows():
            instance = self.__class__()
            for k, v in self.__mapped_columns__.items():
                setattr(instance, k, row[v])
            yield instance

    def obs2df(self, obs: List[Any]) -> pd.DataFrame:
        # first check if all instances in obs are of the same type; if not, raise exception
        if not all(isinstance(ob, self.__class__) for ob in obs):
            raise NonUniformTypeError(f"Different types found in passed-in object list; they have to be of the same type")
        data_list = list()
        for ob in obs:
            data_list.append(ob.__dict__)
        return pd.DataFrame(data_list)