# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import TypeVar, Generic

from azureml.exceptions._azureml_exception import UserErrorException

K = TypeVar('K')
V = TypeVar('V')


class _AttrDict(Generic[K, V], dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __getattr__(self, name: K) -> V:
        try:
            return self[name]
        except KeyError:
            ue = UserErrorException('Key {} not found'.format(name))
            raise ue

    def __setattr__(self, name: K, value: V):
        self[name] = value

    # For Jupyter Notebook auto-completion
    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]

    def __deepcopy__(self, memo=None, _nil=[]):
        # Object of dictionary type needed to be copied recursively.
        # Here we use memo to avoid infinite recursion by recording the object being copied.
        # See more about copy.deepcopy <https://docs.python.org/3/library/copy.html#copy.deepcopy>
        if memo is None:
            memo = {}
        d = id(self)
        y = memo.get(d, _nil)
        if y is not _nil:
            return y

        from copy import deepcopy
        attr_dict = _AttrDict()
        memo[d] = id(attr_dict)
        for key in self.keys():
            attr_dict.__setattr__(deepcopy(key, memo=memo),
                                  deepcopy(self.__getattr__(key), memo=memo))
        return attr_dict
