# OpenStreetMap Data Wrangling with SQL

OpenStreetMap data of St Charles, MO is audited, cleaned and stored in an SQLite database. The database is then queried to extract information related to users contributing to the database & the amenities in the region. 

## About
In this project, wrangling and cleaning of a large dataset (>50MB) are performed. The data is then imported into SQLite for querying. The data was extracted from OpenStreetMap.

## Objectives Addressed:
For the area of study, download an XML-OSM raw dataset from OpenStreetMap.

Audit and clean your dataset, converting it from XML to CSV format.

Import the cleaned .csv files into a SQL database.

Explore the data using SQL queries.

Report the findings.

Since the size of the original data was very large (176mb), steps 2-4 were performed with a sample of the source data. After the code was checked, it was then verified and ran on the source data.

## Learning Outcome
The project helped me learn to write code to assess the quality of data for validity, accuracy, completeness, consistency, and uniformity. This is also my first project involving cleaning data to this extent and it was a very educational experience on the potential ways data can be "dirty".

## Files
* OpenStreetMap Data Wrangling with SQL.ipynb - the jupyter notebook you're currently reading.
* Audit.py - includes the update functions, as well as the intial audit used to create the update functions.
* OSM_to_CSV.py - iterates through the OSM file, calls the update functions from the audit.py file and then seperates the values into their appropriate csv file. The csv file is then checked against the schema.py for proper database schema.
* schema.py - this is a file that is the python equivelant of the database_wrangling_schema.sql that is used to verify the data is formatted properly for database upload.
* data_wrangling_schema.sql - the file that schema.py is based off, is not used but is included for reference.
* creating_db.py - this file creates the database and the tables inside. As well as checking for duplicate tables and then inserts the data from the converted .csv files into their proper table.
* queries.py - this file contains the queries used for our data exploration phase.
* sample1percent.osm - a sample of the dataset that is 1% of the size or every 100 top level lines.
* nodes.csv, nodes_tags.csv, ways.csv, ways_nodes.csv, ways_tags.csv - the csv files created from the OSM_to_CSV.py file after being run on the source document.

## Requirements
To download the dataset, use the Overpass API to download a custom square area. The following link is a direct link to the coordinates used with the api:

https://overpass-api.de/api/map?bbox=-90.7189,38.7013,-90.3117,38.8884

This project requires Python 2 and was developed using Anaconda, a pre-packaged Python distribution that contains all of the necessary libraries and software for data related projects, as well as using Jupyter Notebook for the report, and Visual Studio Code for development.
