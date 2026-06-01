import unittest

from qautils import slugify


class TestSlugify(unittest.TestCase):
    def test_examples_from_spec(self):
        cases = [
            ("Hello, World!", "hello-world"),
            ("  multiple   spaces  ", "multiple-spaces"),
            ("Already_Slug", "already-slug"),
            ("---A---B---", "a-b"),
            ("!!!", ""),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)


if __name__ == "__main__":
    unittest.main()

