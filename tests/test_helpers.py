import unittest

from ocsw.utils import helpers


class TestHelpers(unittest.TestCase):
    def test_helper_get_from_dict(self):
        obj = {"a": [{"b": {"c": 3}}]}
        value = helpers.get(obj, "a.0.b.c")
        self.assertEqual(value, 3)

        value = helpers.get(obj, "a.foo.b.c", "bar")
        self.assertEqual(value, "bar")

    def test_helper_get_from_list(self):
        obj = [{}, {"a": [{"b": {"c": 3}}]}]
        value = helpers.get(obj, "1.a.0.b.c")
        self.assertEqual(value, 3)

        value = helpers.get(obj, "a.foo.b.c", "bar")
        self.assertEqual(value, "bar")


if __name__ == "__main__":
    unittest.main()
