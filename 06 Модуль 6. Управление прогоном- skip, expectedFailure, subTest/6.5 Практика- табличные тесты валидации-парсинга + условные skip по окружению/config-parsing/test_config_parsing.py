import importlib.util
import os
import unittest

from config_parsing import parse_bool, parse_csv, parse_port


RUN_SLOW = os.environ.get("RUN_SLOW") == "1"
HAS_YAML = importlib.util.find_spec("yaml") is not None


class TestConfigParsing(unittest.TestCase):
    def test_valid_ports(self):
        for raw, expected in [("1", 1), (" 80 ", 80), ("65535", 65535)]:
            with self.subTest(raw=raw):
                self.assertEqual(parse_port(raw), expected)

    def test_invalid_ports(self):
        cases = [("", ValueError, "digits"), ("0", ValueError, "range"), ("65536", ValueError, "range"), (None, TypeError, "str")]
        for raw, exc_type, msg in cases:
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(exc_type, msg):
                    parse_port(raw)

    def test_valid_bools(self):
        cases = [("1", True), ("0", False), (" YES ", True), ("off", False), ("TrUe", True)]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertIs(parse_bool(raw), expected)

    def test_invalid_bools(self):
        for raw in ["", "maybe", "2", object()]:
            with self.subTest(raw=raw):
                with self.assertRaises((TypeError, ValueError)):
                    parse_bool(raw)

    def test_valid_csv(self):
        cases = [("a,b,c", ["a", "b", "c"]), (" a, , b ,, ", ["a", "b"]), ("", [])]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_csv(raw), expected)

    def test_invalid_csv_type(self):
        with self.assertRaisesRegex(TypeError, "str"):
            parse_csv(["a", "b"])

    @unittest.skipUnless(RUN_SLOW, "set RUN_SLOW=1 to run extended parser cases")
    def test_extended_cases(self):
        port_cases = [("2", 2), ("443", 443), (" 8080", 8080), ("009", 9)]
        bool_cases = [("yes", True), ("no", False), ("on", True), ("OFF", False)]
        csv_cases = [("x,,y", ["x", "y"]), (" one , two ", ["one", "two"]), (",,,", [])]
        for raw, expected in port_cases:
            with self.subTest(parser="port", raw=raw):
                self.assertEqual(parse_port(raw), expected)
        for raw, expected in bool_cases:
            with self.subTest(parser="bool", raw=raw):
                self.assertIs(parse_bool(raw), expected)
        for raw, expected in csv_cases:
            with self.subTest(parser="csv", raw=raw):
                self.assertEqual(parse_csv(raw), expected)


@unittest.skipUnless(HAS_YAML, "pip install PyYAML to run yaml-dependent tests")
class TestOptionalYamlDependency(unittest.TestCase):
    def test_yaml_dependency_is_available(self):
        import yaml

        self.assertEqual(yaml.safe_load("enabled: true")["enabled"], True)

