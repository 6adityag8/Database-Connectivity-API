# Database-Connectivity-API
(PROBLEM STATEMENT)
Q. Create an api using django-rest framework that will connect to the given database and query the given table. No restriction on any external libraries other than django.

Tables described here are for example it should work for any existing table or database inside the database server. It should connect to the given database and access the given table, assume that there can be multiple  databases in the same database server and inside all these databases there are multiple tables.Create post requests with the payloads given below :

Payload Example:

{
   "database_name": "database1",
   "data": {
       "table_name": "table1",
   }
}

1. The above query should  connect to database `database1` and create an equivalent sql as SELECT * FROM `table1` and return the result like given below :

{
   "column": [
       "userid",
       "uploaded_time",
       "city",
       "price",
       "year",
       "county_name",
       "state_code",
       "state_name"
   ],
   "data": [
       [
           "awadhesh kumar",
           "2020-03-23T12:23:47",
           "marshall",
           11900,
           2010,
           "Lincoln",
           "SD",
           "South Dakota"
       ],
       [
           "awadhesh kumar",
           "2020-03-23T12:23:47",
           "marshall",
           2800,
           2004,
           "Osceola",
           "IA",
           "Iowa"
       ]
   ],
   "length": 2
}

2. We should be able to select only required fields with the following request :

Payload Example:

{
   "database_name": "database1",
   "data": {
       "select_list": [
           {
               "column": "city"
           },
           {
               "column": "price"
           }
       ],
       "worksheet_id": "table1"
   }
}


with equivalent SQL like SELECT `table1`.city, `table1`.price FROM `table1` and the result as :
													
{
   "column": [
       "city",
       "price"
   ],
   "data": [
       [
           "marshall",
           11900
       ],
       [
           "marshall",
           2800
       ]
   ],
   "length": 2
}

3. We should be able to aggregate on different fields and group by on different fields

Payload Example:

 
{
   "database_name": "database1",
   "data": {
       "aggregate": [
           {
               "column": "price",
               "type": "sum"
           }
       ],
       "groupby": [
           {
               "column": "city"
           }
       ],
       "worksheet_id": "table1",
   }
}

With equivalent SQL  
SELECT `table`.city, sum(`table`.price) AS sum_of_price 
FROM `table` 
GROUP BY `table`.city 

Where we can add or delete different columns in aggregate and group by also different aggregate functions like (sum,avg,count,min,max and distinct count ) should work.



Result will be:

{
   "column": [
       "city",
       "sum_of_price"
   ],
   "data": [
       [
           null,
           44.0
       ],
       [
           "chambersburg",
           43200.0
       ]
   ],
   "length": 2
}


