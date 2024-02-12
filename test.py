import unittest
from meta_dataclass import dataclass

class TestMetaDataClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Parent(metaclass=dataclass):
            a: int
            b: int
        
        class FirstChild(Parent, metaclass=dataclass):
            c: int
            d: int
        
        class SecondChild(Parent, metaclass=dataclass):
            e: int
            f: int
        
        class GrandChild(FirstChild, SecondChild, metaclass=dataclass):
            g: int
            h: int

        cls.parent = Parent
        cls.first_child = FirstChild
        cls.second_child = SecondChild
        cls.grand_child = GrandChild

    def test_init_simple(self):
        p = self.parent(1,2)
        self.assertEqual([p.a, p.b], [1,2]) 

    def test_init_inheritance(self):
        g = self.grand_child(1, 2, 3, 4, 5, 6, 7, 8)
        self.assertEqual([g.a, g.b, g.e, g.f, g.c, g.d, g.g, g.h], list(range(1, 9)))

    def test_repr(self):
        p = self.parent(1,2)
        self.assertEqual(repr(p), "Parent(a=1, b=2)")

    def test_eq(self):
        p = self.parent(1,2)
        class AnotherParent(metaclass=dataclass):
            a: int
            b: int
        p_other = AnotherParent(1,2)

        self.assertNotEqual(p, p_other)
        self.assertNotEqual(p, (1,2,))
        self.assertEqual(p, self.parent(1,2))
        
    def test_hash(self):
        p = self.parent(1,2)
        self.assertEqual(hash(p), hash((1,2,)))

    def test_iter(self):
        class SingleParent(metaclass=dataclass):
            a: int

        s = SingleParent(23)
        it = iter(s)
        self.assertEqual(next(it), 23)
        with self.assertRaises(StopIteration):
            next(it)

if __name__ == '__main__':
    unittest.main()
