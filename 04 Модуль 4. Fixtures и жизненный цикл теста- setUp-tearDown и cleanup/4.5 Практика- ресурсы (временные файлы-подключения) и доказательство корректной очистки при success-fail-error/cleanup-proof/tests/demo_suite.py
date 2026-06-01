import sqlite3
import tempfile
import unittest


TMP_DIRS = []
CONNS = []


class _BaseWithResources(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        TMP_DIRS.append(tmp.name)
        self.addCleanup(tmp.cleanup)

        conn = sqlite3.connect(":memory:")
        CONNS.append(conn)
        self.addCleanup(conn.close)
        conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO items (name) VALUES ('demo')")
        self.conn = conn


class InnerPass(_BaseWithResources):
    def test_passes(self):
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM items").fetchone()[0], 1)


class InnerFail(_BaseWithResources):
    def test_fails(self):
        self.assertEqual(1, 2)


class InnerError(_BaseWithResources):
    def test_errors(self):
        raise RuntimeError("inner error")


class InnerSetupError(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        TMP_DIRS.append(tmp.name)
        self.addCleanup(tmp.cleanup)

        conn = sqlite3.connect(":memory:")
        CONNS.append(conn)
        self.addCleanup(conn.close)
        conn.execute("CREATE TABLE setup_items (id INTEGER PRIMARY KEY)")
        raise RuntimeError("setup failed")

    def test_never_runs(self):
        self.fail("setUp should stop this test")

