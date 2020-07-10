import sqlite3
import csv

db = 'osm_stchas.sqlite'

# Connecting to the database
con = sqlite3.connect(db)
con.text_factory = str
cursor = con.cursor()

# Here we drop the nodes_tags table if it exists to save us from data integrity issues when rerunning this file.
cursor.execute('''
    DROP TABLE IF EXISTS nodes_tags
''')
con.commit()

# Here we create nodes_tags table.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT)
''')
con.commit()

with open('nodes_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    iterate_db = [(i[b'id'], i[b'key'], i[b'value'], i[b'type']) for i in dr]

# Lets go ahead and insert the data into the nodes_tags tables from the 'nodes_tags.csv' file.
cursor.executemany('INSERT INTO nodes_tags(id, key, value, type) VALUES(?, ?, ?, ?);', iterate_db)
con.commit()

# Here we drop the ways table if it exists to save us from data integrity issues when rerunning this file
cursor.execute('''
    DROP TABLE IF EXISTS ways
''')
con.commit()

# Now we need to create the ways tables.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ways(id VARCHAR PRIMARY KEY, user TEXT, uid INTEGER, \
    version VARCHAR, changeset INTEGER, timestamp DATETIME)
''')
con.commit()

with open('ways.csv', 'r') as f:
    dr = csv.DictReader(f)
    iterate_db = [(i[b'id'], i[b'user'], i[b'uid'], i[b'version'], \
    i[b'changeset'], i[b'timestamp']) for i in dr]

# Insert the data from 'ways.csv' into the newly created ways table.
cursor.executemany('INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES(?, ?, ?, ?, ?, ?);', iterate_db)
con.commit()

# Here we drop the ways_nodes table if it exists to save us from data integrity issues when rerunning this file
cursor.execute('''
    DROP TABLE IF EXISTS ways_nodes
''')
con.commit()

# Now on to creating the ways_nodes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')
con.commit()

with open('ways_nodes.csv', 'r') as f:
    dr = csv.DictReader(f)
    iterate_db = [(i[b'id'], i[b'node_id'], i[b'position']) for i in dr]

# Insert the data found in the 'ways_nodes.csv' file into the newly created ways_nodes table.
cursor.executemany('INSERT INTO ways_nodes(id, node_id, position) VALUES(?, ?, ?);', iterate_db)
con.commit()

# Here we drop the ways_tags table if it exists to save us from data integrity issues when rerunning this file
cursor.execute('''
    DROP TABLE IF EXISTS ways_tags
''')
con.commit()

# We create the ways_tags table next.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ways_tags(id INTEGER , key TEXT, value TEXT, type TEXT)
''')
con.commit()

with open('ways_tags.csv', 'r') as f:
    dr = csv.DictReader(f)
    iterate_db = [(i[b'id'], i[b'key'], i[b'value'], i[b'type']) for i in dr]

# Insert the data found in 'ways_tags.csv' into the new ways_tags table.
cursor.executemany('INSERT INTO ways_tags(id, key, value, type) VALUES(?, ?, ?, ?);', iterate_db)
con.commit()

# Here we drop the nodes table if it exists to save us from data integrity issues when rerunning this file
cursor.execute('''
    DROP TABLE IF EXISTS nodes
''')
con.commit()

#Finally, we create the nodes table.
cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes(id VARCHAR PRIMARY KEY, lat REAL,
            lon REAL, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp DATE)
        ''')
con.commit()

with open('nodes.csv', 'r') as f:
    dr = csv.DictReader(f)
    iterate_db = [(i[b'id'], i[b'lat'], i[b'lon'], i[b'user'], \
            i[b'uid'], i[b'version'], i[b'changeset'], i[b'timestamp']) for i in dr]

# Insert the data.
cursor.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?,?, ?, ?, ?);", iterate_db)
con.commit()