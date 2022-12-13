# allbirds-challenge

# PROGRAMMING CHALLENGE

## Problem definition
You receive drops of data files and specification files. Write an application in the language of your choice that will load these files into a database.

## Problem details
Data files will be dropped in a "data/" directory and specification files will be dropped in a "specs/" directory. All files can be assumed to use UTF-8 encoding.

## Specification Files

Specification files will have filenames equal to the file type they specify and extension of ".csv". So "fileformat1.csv" would be the specification for files of type "fileformat1".

Specification files will be csv formatted with columns "column name", "width", and "datatype".


"column name" will be the name of that column in the database table

"width" is the number of characters taken up by the column in the data file

"datatype" is the SQL data type that should be used to store the value in the database table. It will be one of three values: TEXT, BOOLEAN, or INTEGER.

## Data Files

Data files will have filenames equal to their file format type, followed by an underscore, followed by the drop date and an extension of ".txt". For example, "fileformat1_2020-10-01.txt" would be a data file to be parsed using "specs/fileformat1.csv", which arrived on 10/01/2020.

Data files will be flat text files with rows matching single records for the database. Rows are formatted as specified by the associated format file.


## Examples
This is an example file pair; other files may vary in structure while still fitting the structure of the problem details (above):

specs/testformat1.csv

```
"column name",width,datatype

name,10,TEXT

valid,1,BOOLEAN

count,3,INTEGER
```

data/testformat1_2020-06-28.txt

```
Foonyor 1 1

Barzane 0 -12

Quuxitude 1 103
```

Sample table output:


name | valid | count
--- | --- | ---
Foonyor | True | 1 
Barzane | False | -12
Quuxitude | True | 103



## Expectations
Allbirds primarily uses Python on the backend, but your application can be written with any language/libraries of your choosing.

Database type and connection mechanism is left to your discretion.

You should be prepared to discuss implementation decisions and possible extensions to your application.

The expectation is not that you produce a completely optimized solution, but that we have some base of code as a starting point to understand your thought process and tradeoffs.

It’s not required but advisable to create or think of a way to test the solution.

However, most of the work the team is doing is not this but writing SQL queries. Review the document attached and see if any changes are required.

Also, feel free to propose any improvements/updates to the previous challenge.



# SQL CHALLENGE



## Objective 

The purpose of this pre-work is to evaluate your database querying skills.  

We expect you to: 

1. Familiarize yourself with the data model given below 

2. Complete the queries described below using your preferred RDBMS SQL syntax 

3. Be prepared to explain your approach to the queries and the query itself 

4. Be prepared to write new queries on this data model during the onsite interview Feel free to bring your laptop to show the queries running. 

## Schema 

This is written with PostgreSQL, but feel free to change to your preferred RDBMS and phrase answers  with that SQL syntax. 

```sql
CREATE TABLE orders ( 
    id CHARACTER VARYING(19) NOT NULL PRIMARY KEY, 
    email CHARACTER VARYING(255), 
    created_at_pacific_timestamp TIMESTAMP WITHOUT TIME ZONE
); 

CREATE TABLE skus (
    sku CHARACTER VARYING (50) NOT NULL PRIMARY KEY, 
    product_type CHARACTER VARYING (255) NOT NULL, /* "Runner" or "Lounger" */ 
    product_name CHARACTER VARYING (255) NOT NULL,
    size CHARACTER VARYING (50), 
    color_name CHARACTER VARYING (255), 
    color_hex CHARACTER VARYING (50)
); 

CREATE TABLE order_line_items (
    order_id CHARACTER VARYING(19) NOT NULL REFERENCES orders  ON DELETE CASCADE,
    order_line_number INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    sku CHARACTER VARYING(20) NOT NULL REFERENCES skus ON DELETE RESTRICT,
    PRIMARY KEY (order_id, order_line_number)
);
```

## Questions 

1. Report on quantity sold by month and product_type. Order sale date is in the " created_at_pacific_timestamp" column. 

1. List email addresses of customers that ordered Runners before the first time they ordered Loungers. 

1. List email addresses that ordered Runners twice before the first time they ordered Loungers. 

1. List of customers emails and its highest product price whose last order was 5 days ago.

1. Since question #2 and #3 are similar. Do you know any tool, framework or way to create a generic way to resolve this problem? For example dbt, PLSQL, etc.

1. How (if at all) would you change this schema to better support queries of this kind?
