#!/usr/bin/env python
# coding: utf-8

# In[28]:
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = (r"C:\Users\Marcus\Documents\School Documents\Python Environments\Unit_4\sample1percent.osm")
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
postcodes_re = re.compile(r'^\D*(\d{5}).*')
cities_re = re.compile(r'.+', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

#Makes a dictionary of all of the street types to allow us to create a list to update

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

#If the element key for 'k' is 'addr:street', return the associated value pair
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


""" Here we create a dictionary of type set called street_types, 
and turn the open function into a variable for ease of use in the future 
Next is my pride and joy, instead of using "for et.iterparse" to iterate directly line by line
through the file instead we use the osm_file var to open the file in memory, and 
then turn it into an iterable. This saves a TON of time, as we can iterate on the file
in memory instead of iterating the file line by line. Once we do this, we then iterate through and
for each tag that matches "node" or "way", we check if it is a street name, and if so we run the audit_street_types function.
we then clear the root tree, saving memory and time, close the file, and return the updated street_types dict.
"""

def audit_s(osmfile):
    street_types = defaultdict(set)
    osm_file = open(osmfile, "r")

    # get an iterable
    iterable = ET.iterparse(osm_file, events=("start", "end"))

    # turn it into an iterator
    iterable = iter(iterable)

    # get the root element
    event, root = iterable.next()

    for event, elem in iterable:
        if event == "end" and (elem.tag == "node" or elem.tag == "way"):
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
        root.clear()
    
    osm_file.close()
    return street_types
""" The update_street function takes the information we learned from the audit_s function
and utilizes that to check a manually created mapping dictionary and DONT_UPDATE tuple.
These two objects are created by reading the report from audit_s and choosing how we want to standardize the types.
to go above and beyond, we also standardized prefixes such as N for North. Unfortunely this caused an issue where Highway or Route, 
which often had the suffix N would be incorrectly corrected to North, such as Route North.
Therefore we created the DON_UPDATE tuple, and check each value against the tuple, and if there is a match
the value is not updated. To fix the street types, we broke the value into parts
seperated by whitespace using .split(), then change the value if it matches the key found in mapping, to the paired value.
Finally, the seperated parts are then rejoined with a space inbetween using the .join() function.
"""
def update_street(name):
    mapping = {"St": "Street",
           "Rd.": "Road",
           "Rd": "Road",
           "N.": "North",
           "N": "North",
           "S.": "South",
           "Blvd": "Boulevard",
           "Blvd.": "Boulevard",
           "Expy": "Expressway",
           "Ln": "Lane",
           "Ctr": "Center",
           "Ctr.": "Center",
           "5th": "Fifth",
           "4th": "Fourth",
           "3rd": "Third",
           "2nd": "Second",
           "1st": "First",
           #There was a street named just dade...that's it..so I went on google to find the real address, so this corrects that occurance.
           "Dade": "South Dade Avenue",
           "MO-94": "Highway 94"
          }

    DONT_UPDATE = ('route','suite')

    if name.lower().startswith(DONT_UPDATE):
        return name
    else: 
        return ' '.join(mapping.get(part, part).title() for part in name.split())


def dicti(data, item):
    """This function creates a dictionary where postcodes can be held.
    The dictionary key will be the postcode itself and the dictionary value
    is a count of postcodes that were repeated throughout the dataset."""
    data[item] += 1

#This function returns the elem if 'k' matches "addr:postcode"
def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

#This codes is identical in function the the street function of similar name
def audit_p(osmfile):
    osm_file = open(OSMFILE, "r")
    data = defaultdict(int)

    # get an iterable
    iterable = ET.iterparse(osm_file, events=("start", "end"))

    # turn it into an iterator
    iterable = iter(iterable)

    # get the root element
    event, root = iterable.next()

    for event, elem in iterable:
        if event == "end" and (elem.tag == "node" or elem.tag == "way"):
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    dicti(data, tag.attrib['v'])
        root.clear()
    osm_file.close()
    return data

# This is the function that actually changes the post code to the proper values
# It is called in the OSM_to_XML file, when writing the changes to the .csv

def update_postcode(postcodes):
    output = list()
    
    if re.search(postcodes_re, postcodes):
        new_zip = re.search(postcodes_re, postcodes).group(1)
        output.append(new_zip)

    return ', '.join(str(x) for x in output)


#Once again, this is similar in function to audit_street
def audit_city(city_dict, city_ex):
    m = cities_re.search(city_ex)
    if m:
        city_group = m.group()
        city_dict[city_group].add(city_ex)

#Same function as is_postcode, but for addr:city
def is_city(elem):
    return (elem.attrib['k'] == "addr:city")

#Same function as audit_s, but for city values.
def audit_C(osmfile):
    city_dict = defaultdict(set)
    osm_file = open(osmfile, "r")

    # get an iterable
    iterable = ET.iterparse(osm_file, events=("start", "end"))

    # turn it into an iterator
    iterable = iter(iterable)

    # get the root element
    event, root = iterable.next()

    for event, elem in iterable:
        if event == "end" and (elem.tag == "node" or elem.tag == "way"):
            for tag in elem.iter("tag"):
                if is_city(tag):
                    audit_city(city_dict, tag.attrib['v'])
        root.clear()
    osm_file.close()
    return city_dict

""" Same function as the update_street, except instead of it skipping the
the matched tuple, instead it instead uses the ofallon_mapping dict to correct the
inconsistency of some cities being listed as O'fallon and some as O fallon. 
"""
def update_city(name):
    OFALLON = ('o')
    ofallon_mapping = {"O": "O'"}
    city_mapping = {"St": "Saint",
                "St.": "Saint",
                "bridgeton" : "Bridgeton",
                "drive-through": "O'Fallon",
                "Bass": "Saint",
                "Pro": "Charles",
                "Drive": "",
                "UNINCORPORATED": "Saint Peters",
                }

    if name.lower().startswith(OFALLON):
        return ''.join((ofallon_mapping.get(part, part)).title() for part in name.split())
    return ' '.join((city_mapping.get(part, part)).title() for part in name.split())



def test():

    street_types = audit_s(OSMFILE)
    pprint.pprint(dict(street_types))


    postcodes = audit_p(OSMFILE)
    pprint.pprint(dict(postcodes))

    c_names = audit_C(OSMFILE)
    pprint.pprint(dict(c_names))

    for st_type, ways in street_types.items():
        for name in ways: 
            better_name = update_street(name)
            print (name, "=>", better_name)
            if name == "N. Main Ctr.":
                assert better_name == "North Main Center"
            if name == "Zumbehl Rd":
                assert better_name == "Zumbehl Road"
            if name == "N 3rd St":
                assert better_name == "North Third Street"
            if name == "Route N":
                assert better_name == "Route N"

    for postcode, nums in postcodes.items():
        better_code = update_postcode(postcode)
        print(postcode, "=>", better_code)

    for c_name, ways in c_names.items():
        for name in ways:
            better_city_name = update_city(name)
            print (name, "=>", better_city_name)


if __name__ == '__main__':
    test()


# In[ ]:




