# meta-dataclasses
A minimal implementation of a dataclass metaclass. Inspired from [dataklasses](https://github.com/dabeaz/dataklasses)

# Usage
    from meta_dataclass import dataclass
    class Name(metaclass=dataclass):
        first: str
        last: str

Name will automagically get reasonable definitions of the `__init__`, `__repr__`, `__eq__`, `__iter__` and `__hash__` methods.

    >>> don = Name("Donald", "Knuth")
    >>> don.first
    'Donald'
    >>> don
    Name(first='Donald', last='Knuth')
    >>> don == Name('Donald', 'Knuth')
    True
