import unittest

from netutils import parse_port


class TestParsePort(unittest.TestCase):
    def test_valid_int_boundaries(self):
        for value in [1, 2, 65534, 65535]:
            with self.subTest(value=value):
                self.assertEqual(parse_port(value), value)

    def test_valid_string_values_are_stripped_and_converted(self):
        cases = [("1", 1), (" 80 ", 80), ("65535", 65535), ("0002", 2)]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_port(raw), expected)

    def test_out_of_range_values_raise_value_error(self):
        for value in [0, 65536, "0", "65536"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_port(value)

    def test_invalid_strings_raise_value_error(self):
        for value in ["", "   ", "+80", "-1", "abc", "80/tcp"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_port(value)

    def test_invalid_types_raise_type_error(self):
        for value in [None, [], {}, 3.14, True, False]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    parse_port(value)


if __name__ == "__main__":
    unittest.main()

