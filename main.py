import sqlite3 as sql
import pandas as pd
import json
from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/getSelectedProperties')
def get_selected_properties():
    '''Return selected properties
    Query all selected properties (SELETED = 1)
    Convert results into json format using sqlite3.Row and iterating with a dictionary
    '''
    with sql.connect('enodo.db') as db:
        db.row_factory = sql.Row
        results = db.cursor().execute('SELECT rowid, `Full Address`, CLASS_DESCRIPTION, SELECTED FROM addresses WHERE SELECTED = 1').fetchall()
        results_json = json.dumps([dict(row) for row in results])
        return Response(results_json, mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})

@app.route('/searchProperties')
def search_properties():
    ''' Return properties based on search query for autocomplete suggestions
    Remove leading and trailing whitespaces from the query, then split by space character to get individual terms
    Add a wildcard (*) at the end of each term to handle missing characters, then join the terms using space separator 
    Connect to database, query fts table for address and return results from original table (addresses)
    Convert results into json format using sqlite3.Row and iterating with a dictionary
    '''
    terms = request.args['query'].strip().split(' ')
    query = ' '.join([term + '*' for term in terms])
    with sql.connect('enodo.db') as db:
        db.row_factory = sql.Row
        results = db.cursor().execute('SELECT rowid, `Full Address`, CLASS_DESCRIPTION, SELECTED FROM addresses WHERE PIN IN (SELECT rowid FROM addresses_fts WHERE SELECTED = 0 AND `Full Address` MATCH ?)', (query,)).fetchall()
        results_json = json.dumps([dict(row) for row in results])
        return Response(results_json, mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})

@app.route('/selectProperty', methods=['POST'])
def select_property():
    '''Select property using PIN
    Update property as selected (SELECTED = 1) using PIN
    '''
    with sql.connect('enodo.db') as db:
        db = sql.connect('enodo.db')
        db.execute('UPDATE addresses SET SELECTED = 1 WHERE PIN = ?', (request.args['PIN'],))
        db.commit()
        return Response(status=200, headers={'Access-Control-Allow-Origin': '*'})

@app.route('/deselectProperty', methods=['POST'])
def deselect_property():
    '''Deselect property using PIN
    Update property as deselected (SELECTED = 0) using PIN
    '''
    with sql.connect('enodo.db') as db:
        db = sql.connect('enodo.db')
        db.execute('UPDATE addresses SET SELECTED = 0 WHERE PIN = ?', (request.args['PIN'],))
        db.commit()
        return Response(status=200, headers={'Access-Control-Allow-Origin': '*'})

def excel_to_db(io, db, sheet_name=None, index=False):
    workbook = pd.read_excel(io, sheet_name=sheet_name)
    for sheet in workbook:
        workbook[sheet].to_sql(sheet, db, index=index, if_exists='replace')

def create_db():
    ''' Create SQLite database and addresses table
    Convert Excel file to table
    Set PIN as Primary Key
    Create an external-content VIRTUAL TABLE for full-text search
    '''
    db = sql.connect('enodo.db')
    excel_to_db('Enodo_Skills_Assessment_Data_File.xlsx', db)
    db.executescript('''
        CREATE TABLE IF NOT EXISTS addresses(
            PIN INTEGER PRIMARY KEY,
            `Full Address` TEXT,
            CLASS_DESCRIPTION TEXT,
            SELECTED INTEGER NOT NULL
        );

        REPLACE INTO addresses SELECT PIN, `Full Address`, CLASS_DESCRIPTION, 0 FROM Sheet1;

        DROP TABLE Sheet1;

        CREATE VIRTUAL TABLE IF NOT EXISTS addresses_fts USING fts5(`Full Address`, content=addresses, content_rowid=PIN);
        INSERT INTO addresses_fts(addresses_fts) VALUES('rebuild');
    ''')
    db.commit()
    db.close()

def main():
    create_db()
    app.run()

if __name__ == "__main__":
    main()
