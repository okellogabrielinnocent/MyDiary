""" Tests module """
import unittest
from flask import json
from run import app

class TestBase(unittest.TestCase):
    """ Base class for all test classes """

    app.app_context().push()
    client = app.test_client()
    
    
