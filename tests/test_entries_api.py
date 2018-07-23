from .test_base import TestBase
import unittest
from flask import json
from .test_data import entry1, entry2, entry3


class TestEntries(TestBase):
    """ Defines tests for the view methods of for rides """

    def setUp(self):
        pass

    
    def test_get_entries(self):
        """
        Test API that view all entries.
        Check whether Technical leader is in tittle
        Check whether JSON is request
        """

        response = self.client.get('/api/v1/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Technical Leader', str(response.data))

        response = self.client.get('/api/v1/entries', content_type='text')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Bad Request. JSON Request Expected', str(response.data))
        
    
    