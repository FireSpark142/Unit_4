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

most_contributing_users()


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

# Different Types of Shops
query = "SELECT value, COUNT(*) as num FROM nodes_tags \
            WHERE key='shop' \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10"

def shops_in_st_charles():
    output = cursor.execute(query)
    pprint(output.fetchall())
    return None

print('Different types of shops:\n')
shops_in_st_charles()

# Popular Cafes in St Charles
def most_popular_cafes():
    output = cursor.execute('SELECT nodes_tags.value, COUNT(*) as num \
                          FROM nodes_tags \
                            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="coffee_shop") AS cafes \
                            ON nodes_tags.id = cafes.id \
                            WHERE nodes_tags.key="name"\
                            GROUP BY nodes_tags.value \
                            ORDER BY num DESC \
                            LIMIT 10' )
    pprint(output.fetchall())
    return output.fetchall()

print('Most popular cafes in St Charles: \n')
most_popular_cafes()