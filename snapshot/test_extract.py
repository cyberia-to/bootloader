import io
import json
import unittest
from unittest import mock

import extract


class _FakeResponse:
    """a context manager standing in for urllib.request.urlopen's return value"""

    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return io.BytesIO(json.dumps(self._payload).encode())

    def __exit__(self, *exc):
        return False


class GetTests(unittest.TestCase):
    def test_returns_parsed_json_on_first_success(self):
        with mock.patch("extract.urllib.request.urlopen", return_value=_FakeResponse({"ok": True})):
            self.assertEqual(extract.get("/x"), {"ok": True})

    def test_retries_on_transient_failure_then_succeeds(self):
        calls = {"n": 0}

        def flaky(*a, **k):
            calls["n"] += 1
            if calls["n"] < 3:
                raise TimeoutError("boom")
            return _FakeResponse({"ok": True})

        with mock.patch("extract.urllib.request.urlopen", side_effect=flaky), \
             mock.patch("extract.time.sleep") as sleep:
            self.assertEqual(extract.get("/x"), {"ok": True})
        self.assertEqual(calls["n"], 3)
        self.assertEqual(sleep.call_count, 2)

    def test_reraises_the_real_exception_after_five_failed_attempts(self):
        with mock.patch("extract.urllib.request.urlopen", side_effect=TimeoutError("boom")), \
             mock.patch("extract.time.sleep"):
            with self.assertRaises(TimeoutError):
                extract.get("/x")

    def test_backoff_grows_linearly_by_attempt_and_never_sleeps_after_the_last(self):
        with mock.patch("extract.urllib.request.urlopen", side_effect=TimeoutError("boom")), \
             mock.patch("extract.time.sleep") as sleep:
            with self.assertRaises(TimeoutError):
                extract.get("/x")
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [2, 4, 6, 8])


class PagedTests(unittest.TestCase):
    def test_single_page_yields_all_items(self):
        with mock.patch("extract.get", return_value={"items": [1, 2, 3],
                                                       "pagination": {"next_key": None}}) as g:
            self.assertEqual(list(extract.paged("/x", "items")), [1, 2, 3])
        g.assert_called_once()

    def test_follows_next_key_across_pages(self):
        pages = [
            {"items": [1, 2], "pagination": {"next_key": "abc"}},
            {"items": [3], "pagination": {"next_key": None}},
        ]
        with mock.patch("extract.get", side_effect=pages) as g:
            self.assertEqual(list(extract.paged("/x", "items")), [1, 2, 3])
        self.assertEqual(g.call_count, 2)
        self.assertIn("pagination.key=abc", g.call_args_list[1].args[0])

    def test_missing_pagination_block_stops_after_one_page(self):
        with mock.patch("extract.get", return_value={"items": [1]}):
            self.assertEqual(list(extract.paged("/x", "items")), [1])

    def test_missing_key_yields_nothing(self):
        with mock.patch("extract.get", return_value={"pagination": {"next_key": None}}):
            self.assertEqual(list(extract.paged("/x", "items")), [])

    def test_extra_query_string_is_appended(self):
        with mock.patch("extract.get", return_value={"items": [],
                                                       "pagination": {"next_key": None}}) as g:
            list(extract.paged("/x", "items", extra="&status=BOND"))
        self.assertIn("&status=BOND", g.call_args.args[0])

    def test_next_key_is_url_quoted(self):
        # urllib.parse.quote's default safe="/" leaves a base64 next_key's
        # slash literal and only escapes its '+'; harmless in a query value,
        # pinned here rather than assumed
        pages = [
            {"items": [1], "pagination": {"next_key": "a/b+c"}},
            {"items": [], "pagination": {"next_key": None}},
        ]
        with mock.patch("extract.get", side_effect=pages) as g:
            list(extract.paged("/x", "items"))
        self.assertIn("pagination.key=a/b%2Bc", g.call_args_list[1].args[0])


if __name__ == "__main__":
    unittest.main()
