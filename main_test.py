import unittest
import os
import sqlite3 as sql

from main import app, create_db, excel_to_db

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()    
        create_db()

    def tearDown(self):
        os.remove('enodo.db')

    def test_create_db(self):
        self.assertTrue(os.path.exists('enodo.db'))
        self.db = sql.connect('enodo.db')
        tables = self.db.cursor().execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall()
        self.assertTrue(table in tables for table in ['addresses', 'addresses_fts'])        

    def test_search_properties(self):
        response = self.app.get('/searchProperties')
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/searchProperties?query=210')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(data), list) 
        self.assertTrue(key in data[0] for key in ['Full Address', 'CLASS_DESCRIPTION', 'PIN', 'SELECTED'])

    def test_select_property(self):
        response = self.app.get('/selectProperty')
        self.assertEqual(response.status_code, 405)

        response = self.app.post('/selectProperty')
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/selectProperty?PIN=17071230240000')
        self.assertEqual(response.status_code, 200)

    def test_deselect_property(self):
        response = self.app.get('/deselectProperty')
        self.assertEqual(response.status_code, 405)

        response = self.app.post('/deselectProperty')
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/deselectProperty?PIN=17071230240000')
        self.assertEqual(response.status_code, 200)

    def test_get_selected_properties(self):
        response = self.app.get('/getSelectedProperties')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(data), list)  
        self.assertEqual(len(data), 0)
        
        self.test_select_property()

        response = self.app.get('/getSelectedProperties')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(data), list)  
        self.assertEqual(len(data), 1)
        self.assertTrue(key in data[0] for key in ['Full Address', 'CLASS_DESCRIPTION', 'PIN'])

        self.test_deselect_property()

        response = self.app.get('/getSelectedProperties')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(data), list)  
        self.assertEqual(len(data), 0)
    

if __name__ == '__main__':
    unittest.main()