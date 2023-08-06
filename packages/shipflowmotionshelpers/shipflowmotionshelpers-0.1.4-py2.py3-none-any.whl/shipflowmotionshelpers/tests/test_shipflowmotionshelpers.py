#!/usr/bin/env python

"""Tests for `shipflowmotionshelpers` package."""

import pytest
from shipflowmotionshelpers import shipflowmotionshelpers as helpers
import shipflowmotionshelpers.tests as tests
import os

def test_load_time_series():
    file_path = os.path.join(tests.path_test_project_1,'test_project_1_TS.csv')
    helpers.load_time_series(file_path=file_path)

def test_extract_parameters_from_file():
    
    file_path = os.path.join(tests.path_test_project_1,'test_project_1')
    parameters = helpers.extract_parameters_from_file(file_path=file_path)
    assert parameters['titl']=="M5030-01-A"
    assert parameters['b4l'] == 0.0
    assert parameters['kyy'] == 43.12

