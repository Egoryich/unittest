import io
import sqlite3
import unittest
from pathlib import Path

from tests import demo_suite


class TestCleanupProof(unittest.TestCase):
    def test_resources_are_cleaned_for_success_fail_error_and_setup_error(self):
        demo_suite.TMP_DIRS.clear()
        demo_suite.CONNS.clear()
        suite = unittest.TestSuite()
        for case in [
            demo_suite.InnerPass,
            demo_suite.InnerFail,
            demo_suite.InnerError,
            demo_suite.InnerSetupError,
        ]:
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(case))

        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)

        self.assertGreaterEqual(len(result.failures), 1)
        self.assertGreaterEqual(len(result.errors), 1)
        for path in demo_suite.TMP_DIRS:
            with self.subTest(path=path):
                self.assertFalse(Path(path).exists())
        for conn in demo_suite.CONNS:
            with self.subTest(conn=conn):
                with self.assertRaises(sqlite3.ProgrammingError):
                    conn.execute("SELECT 1")
