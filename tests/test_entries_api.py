from .test_base import TestBase
import unittest
from flask import json, request
from api.models import Entry
from .test_data import entry1, entry2, entry3


class TestEntries(TestBase):
    """ Defines tests for the view methods of for rides """

    def setUp(self):
        pass

    
    def test_get_entries(self):
        """
        Test API that view all entries.
        Check whether Technical leader is in tittle
        
        """
        
        response = self.client.get('/api/v1/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Technical Leader', str(response.data))
        

    def test_get_entry(self):
        """
        Test API that view all entries.
        Check whether Technical leader is in tittle
        
        """
        
        response = self.client.get('/api/v1/entries',
                                      content_type='application/json',
                                      data=json.dumps(entry1))

        self.assertEqual(response.status_code, 200)
        self.assertIn('1', str(response.data))

        response = self.client.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)
        
        results = json.loads(response.data.decode())
        
        for entry in results:
            result = self.client.get(
                '/api/v1/entries/{}'.format(entry[1]),
                content_type='application/json',
                data=json.dumps(entry1))
                
        self.assertEqual(result.status_code, 200)
        self.assertIn(entry[1], str(result.data), 404)

        for entry in Entry.entries:
            if (entry['id'] == 1):
                
                response = self.client.get(
                    'api/v1/entries/{}'.format(entry[1]),
                    content_type='application/json',
                    data=json.dumps(entry1))

                self.assertEqual(result.status_code, 200)
        
        
             


    def test_update_entry(self):
        '''data = request.get_json()
        response = [ entry for entry in Entry.entries if (entry['id'] == 1) ]
        if  not 'tittle' in data:
            error = 'Please wrong tittle'
            self
            return error
        elif 'tittle' in data:
            en[0]['tittle'] = data['tittle']

        if not 'body' in data:
            error = 'Please wrong body'
            return error    
        elif 'body' in data:
            en[0]['body'] = data['body']

        
        if 'date' in data : 
            en[0]['date'] = data['date']'''
        pass