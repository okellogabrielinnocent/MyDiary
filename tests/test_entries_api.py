from .test_base import TestBase
import unittest
from flask import json
from .test_data import entry1, entry2, entry3


class TestEntries(TestBase):
    """ Defines tests for the view methods of for rides """

    def setUp(self):
        pass

    
    def test_create_entry(self):
        """
        Test API can create a dialy entry/ idea (POST request)
        """
        
        response = self.client.post('/api/v1/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))
        
        self.assertEqual(response.status_code, 500)
        self.assertIn('Either the server is overloaded or there is an error in the application', str(response.data))
    
     
    
    
    def test_get_all_entries(self):
        """
        Test API can view all entries.
        """

        response = self.client.get('/api/v1/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Technical Leader', str(response.data))
        
    
    def test_get_entry(self):
        """
        Test API that can get a single entry by using it's id.
        """
        # post data
        response = self.client.post('/api/v1/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))

        self.assertEqual(response.status_code, 500)
        # get data
        response = self.client.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)
        
        results = json.loads(response.data.decode())
        
        for entry in results:
            result = self.client.get(
                'api/v1/entries/{}'.format(entry[1]),
                content_type='application/json',
                data=json.dumps(entry1))
                
        self.assertEqual(result.status_code, 200)
        self.assertIn(entry[1], str(result.data), 404)


    '''def test_update_entry(self):
        response = self.client.put('/API/v1/entries/1', data=json.dumps(
            dict(title="Software Engineer", body="Technical Leadership to learn from your ego and teach others the new technologies")),
                         content_type='application/json')

        # get data
        response = self.client.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)
        
        results = json.loads(response.data.decode())
        
        for entry in results:
            result = self.client.get(
                'api/v1/entries/{}'.format(entry[2]),
                content_type='application/json',
                data=json.dumps(entry1))
                
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Software Engineer", result.data)'''