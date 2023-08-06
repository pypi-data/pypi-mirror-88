#!/usr/bin/env python

"""Tests for `acdh_abbr_client` package."""


import unittest
from click.testing import CliRunner

from acdh_abbr_client.acdh_abbr_client import yield_abbr
from acdh_abbr_client import cli


class TestAcdh_abbr_client(unittest.TestCase):
    """Tests for `acdh_abbr_client` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_yield_abbr(self):
        """yield_abbr"""

        abbr_generator = yield_abbr()
        self.assertTrue(abbr_generator.__next__().endswith(''))

    def test_002_yield_abbr(self):
        """yield_abbr"""

        abbr_generator = yield_abbr(limit=True)
        self.assertTrue(len(list(abbr_generator)) == 5)

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'acdh_abbr_client.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
