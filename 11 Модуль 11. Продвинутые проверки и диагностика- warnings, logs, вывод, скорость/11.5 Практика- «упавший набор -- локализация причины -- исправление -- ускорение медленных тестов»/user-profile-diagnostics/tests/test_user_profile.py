import unittest
from unittest.mock import Mock, patch

from app.user_profile import build_profile, normalize_username, wait_until_ready


class TestUserProfileDiagnostics(unittest.TestCase):
    maxDiff = None

    def test_build_profile_table_is_explicit(self):
        cases = [
            ({"username": " Alice ", "role": "ADMIN"}, {"username": "alice", "role": "admin"}),
            ({"username": " Bob ", "role": "User"}, {"username": "bob", "role": "user"}),
        ]
        for payload, expected in cases:
            with self.subTest(payload=payload):
                self.assertEqual(build_profile(payload), expected, msg="profile fields must be normalized")

    def test_short_username_emits_deprecation_warning(self):
        with self.assertWarnsRegex(DeprecationWarning, "short usernames"):
            self.assertEqual(normalize_username(" Al "), "al")

    def test_build_profile_logs_info(self):
        with self.assertLogs("app.user_profile", level="INFO") as logs:
            build_profile({"username": "Alice", "role": "ADMIN"})
        self.assertIn("building profile", logs.output[0])

    def test_wait_until_ready_success_without_real_sleep(self):
        check_status = Mock(side_effect=[False, True])
        with patch("app.user_profile.time.monotonic", side_effect=[0, 0, 1]), patch("app.user_profile.time.sleep") as sleep:
            with self.assertNoLogs("app.user_profile", level="ERROR"):
                self.assertTrue(wait_until_ready(check_status, timeout=10, interval=1))
        sleep.assert_called_once_with(1)

    def test_wait_until_ready_timeout_logs_error_without_real_sleep(self):
        check_status = Mock(return_value=False)
        with patch("app.user_profile.time.monotonic", side_effect=[0, 0, 1, 2, 3]), patch("app.user_profile.time.sleep") as sleep:
            with self.assertLogs("app.user_profile", level="ERROR") as logs:
                self.assertFalse(wait_until_ready(check_status, timeout=3, interval=1))
        self.assertIn("timed out", logs.output[0])
        self.assertEqual(sleep.call_count, 3)

