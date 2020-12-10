# -*- coding: utf-8 -*-

"""__init__ unit tests."""

import pytest
import os
from flask import Flask
from loglan_db import app_lod, run_with_context


@pytest.mark.usefixtures("db")
def test_run_with_context():

    @run_with_context
    def run_test():
        pass

    result = run_test()
    assert result is None


def test_app_lod():
    assert isinstance(app_lod(), Flask)


def test_run_with_context_no_uri():
    os.environ['LOD_DATABASE_URL'] = "None"

    @run_with_context
    def run_test():
        pass

    result = run_test()
    assert result is None
