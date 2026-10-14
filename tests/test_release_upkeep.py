import unittest
from datetime import date, datetime, timezone
from unittest.mock import patch
from zoneinfo import ZoneInfo

from handbook_builder.maintenance import (GitHubResponseTooLarge, emerging_watch,
    release_rows, releases, render_emerging, update_watchlist, utc_today)


class ReleaseUpkeepTests(unittest.TestCase):
    def test_oversized_feed_pages_the_same_history_and_finds_late_prefix(self):
        rows = [{'tag_name': 'Plane-' + str(i), 'published_at': '2026-10-01T00:00:00Z',
                 'html_url': 'https://github.com/example/repo/releases', 'assets': ['unused']}
                for i in range(100)]
        rows[98]['tag_name'] = 'Copter-1'
        calls = []
        def reader(resource):
            calls.append(resource)
            if 'per_page=100' in resource: raise GitHubResponseTooLarge()
            page = int(resource.split('page=')[-1])
            return rows[(page - 1) * 20:page * 20]
        result = update_watchlist({'releases': [{'id': 'Copter', 'repository': 'example/repo',
            'tag_prefix': 'Copter-', 'covered': 'Copter-1', 'sections': []}]}, reader, date(2026, 10, 14))
        self.assertEqual(result['items'][0]['latest'], 'Copter-1')
        self.assertEqual(result['items'][0]['status'], 'version-matches')
        self.assertEqual(len(calls), 6)
        self.assertEqual(len(release_rows(lambda _: rows, 'example/repo')), 100)
        self.assertNotIn('assets', release_rows(lambda _: rows, 'example/repo')[0])

    def test_short_history_stops_without_extra_requests(self):
        calls = []
        def reader(resource):
            calls.append(resource)
            if 'per_page=100' in resource: raise GitHubResponseTooLarge()
            return []
        self.assertEqual(release_rows(reader, 'example/repo'), [])
        self.assertEqual(len(calls), 2)

    def test_asset_heavy_releases_reduce_pages_without_dropping_history(self):
        rows = [{'tag_name': 'v' + str(i), 'published_at': '2026-10-01T00:00:00Z'} for i in range(100)]
        calls = []
        def reader(resource):
            calls.append(resource)
            if 'per_page=100' in resource or 'per_page=20' in resource:
                raise GitHubResponseTooLarge()
            page = int(resource.split('page=')[-1])
            return rows[(page - 1) * 5:page * 5]
        self.assertEqual(len(release_rows(reader, 'example/repo')), 100)
        self.assertEqual(len(calls), 22)

    def test_redirect_and_size_failures_do_not_bypass_safety_limits(self):
        for error in [ValueError('Unexpected API redirect'), GitHubResponseTooLarge()]:
            calls = []
            def reader(resource):
                calls.append(resource)
                raise error
            with self.subTest(error=type(error).__name__), self.assertRaises(ValueError):
                release_rows(reader, 'example/repo')
            self.assertEqual(len(calls), 4 if isinstance(error, GitHubResponseTooLarge) else 1)

    def test_utc_midnight_accepts_an_already_published_release(self):
        instant = datetime(2026, 10, 14, 3, 15, tzinfo=timezone.utc)
        with patch('handbook_builder.maintenance.datetime') as clock:
            # Model a Chicago runner whose local calendar still says Oct 13.
            clock.now.side_effect = lambda tz=None: instant.astimezone(tz or ZoneInfo('America/Chicago'))
            today = utc_today()
        rows = [{'tag_name': 'v1', 'published_at': '2026-10-14T01:00:00Z'},
                {'tag_name': 'v2', 'published_at': '2026-10-15T01:00:00Z'}]
        self.assertEqual(releases(rows, today)[0]['tag_name'], 'v1')

    def watch(self, release_error=None, previous=None):
        item = {'full_name': 'example/drone', 'description': 'MAVLink telemetry library',
                'language': 'Python', 'size': 1, 'pushed_at': '2026-10-14T01:00:00Z'}
        def reader(resource):
            if resource.startswith('search/'): return {'items': [item]}
            if release_error: raise release_error
            return [{'tag_name': 'v2', 'published_at': '2026-10-14T01:00:00Z'}]
        return emerging_watch({'emerging_queries': ['topic:mavlink']}, reader,
                              date(2026, 10, 14), previous)

    def test_failed_emerging_release_check_retains_prior_observation(self):
        previous = {'projects': [{'repository': 'example/drone', 'release': 'v1',
                    'released': '2026-10-01', 'release_observed': '2026-10-12'}]}
        status = self.watch(OSError('unavailable'), previous)
        project = status['projects'][0]
        self.assertEqual((project['release'], project['released']), ('v1', '2026-10-01'))
        self.assertEqual(project['release_observed'], '2026-10-12')
        self.assertEqual(project['release_checked'], '2026-10-14')
        self.assertIn('last observed v1 / 2026-10-01; check unavailable', render_emerging(status))
        self.assertNotIn('none observed', render_emerging(status))
        recovered = self.watch(previous=status)['projects'][0]
        self.assertEqual((recovered['release'], recovered['release_status']), ('v2', 'observed'))

    def test_first_failed_check_is_unknown_rather_than_no_release(self):
        rendered = render_emerging(self.watch(OSError('unavailable')))
        self.assertIn('check unavailable; release unknown', rendered)
        self.assertNotIn('none observed', rendered)
