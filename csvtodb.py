import sqlite3
import pandas

# This file was used once to create the albums database, using a .csv file and the pandas library

# load data file
data = pandas.read_csv('CleanAlbumDB.csv')

# create or connect to a sqlite db
connection = sqlite3.connect('albums.db')

# load data to SQLite
data.to_sql('albums', connection, if_exists='replace')