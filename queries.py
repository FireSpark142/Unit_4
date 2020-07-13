import sqlite3
import csv
from pprint import pprint

# Put the path to your sqlite database.
# If no database is available, a new one will be created.
sqlite_file = 'osm_stchas.sqlite'

# Connecting to the database.
con = sqlite3.connect(sqlite_file)
cursor = con.cursor()

# Number of Nodes
def number_of_nodes():
    output = cursor.execute('SELECT COUNT(*) FROM nodes')
    return output.fetchone()[0]
print('Number of nodes: %d' % (number_of_nodes()))

# Number of Ways
def number_of_ways():
    output = cursor.execute('SELECT COUNT(*) FROM ways')
    return output.fetchone()[0]
print('Number of ways: %d' %(number_of_ways()))

# Number of Unique Users
def number_of_unique_users():
    output = cursor.execute('SELECT COUNT(DISTINCT e.uid) FROM \
                         (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e')
    return output.fetchone()[0]
print('Number of unique users: %d' %(number_of_unique_users()))

# Query for Top 10 Amenities in St Charles
query = "SELECT value, COUNT(*) as num FROM nodes_tags \
            WHERE key='amenity' \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10"

# Top 10 Amenities in St Charles
def top_ten_amenities_in_st_charles():
    output = cursor.execute(query)
    pprint(output.fetchall())
    return None

print('Top 10 Amenities:\n')
top_ten_amenities_in_st_charles()

# Type of religions that each place_of_worship value returned
query = "SELECT value, COUNT(*) as num FROM nodes_tags \
            WHERE key='religion' \
            GROUP BY value"

def types_of_religion():
    output = cursor.execute(query)
    pprint(output.fetchall())
    return None

print('Different types of shops:\n')
types_of_religion()