import sqlite3

def create_connection():
  conn = sqlite3.connect('database.db')
  return conn

def init_db():
  attractions_table = '''
    create table if not exists attractions (
      
    ); 
  '''
