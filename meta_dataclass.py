from functools import reduce
import itertools

class dataclass(type):
    def __new__(cls, name, bases, dict):
        annots = cls.parse_annotations(bases, dict)
        init = cls.create_init(annots)
        repr = cls.create_repr(annots)
        eq = cls.create_eq(annots)
        it = cls.create_iter(annots)
        hsh = cls.create_hash(annots)
        return super().__new__(type, name, bases, {
            **dict, '__init__': init, '__repr__': repr, '__eq__': eq,
            '__hash__': hsh, '__iter__': it,
        })

    @classmethod
    def create_init(cls, annots):
        args = "self" + "".join([f", {i}" for i in annots])
        bodylines = "".join([f"    self.{i} = {i}\n" for i in annots])
        code_str = f"def __init__({args}):\n{bodylines}"

        exec(code_str, globals(), d:={})
        return d.popitem()[1]

    @classmethod
    def create_repr(cls, annots):
        repr_args = ", ".join([f"{i}={{self.{i}}}" for i in annots])
        bodylines = f"return f\"{{type(self).__name__}}({repr_args})\""
        code_str = f"def __repr__(self):\n    {bodylines}"

        exec(code_str, globals(), d:={})
        return d.popitem()[1]

    @classmethod
    def create_eq(cls, annots):
        own_vals = ",".join(f"self.{a}" for a in annots)
        other_vals = ",".join(f"other.{a}" for a in annots)

        code_str = f"def __eq__(self, other):\n    if self.__class__ is other.__class__:\n" \
                   f"        return ({own_vals},) == ({other_vals},)\n    return False"

        exec(code_str, globals(), d:={})
        return d.popitem()[1]

    @classmethod
    def create_hash(cls, annots):
        own_vals = ", ".join(f"self.{a}" for a in annots)
        code_str = f"def __hash__(self):\n    return hash(({own_vals},))"

        exec(code_str, globals(), d:={})
        return d.popitem()[1]

    @classmethod
    def create_iter(cls, annots):
        own_vals = ", ".join(f"self.{a}" for a in annots)
        code_str = f"def __iter__(self):\n    return (i for i in ({own_vals},))"

        exec(code_str, globals(), d:={})
        return d.popitem()[1]

    @classmethod
    def parse_annotations(cls, bases, dict):
        reversed_mro = itertools.chain.from_iterable([b.__mro__[-2::-1] for b in bases[::-1]])
        annotations_dict = reduce(lambda x, y: x | getattr(y, '__annotations__', {}), reversed_mro, {}) | dict['__annotations__']
        return annotations_dict


if __name__ == '__main__':
    class Name(metaclass=dataclass):
        first: str
        last: str
