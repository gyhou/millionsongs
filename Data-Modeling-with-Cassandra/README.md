# Data Modeling with Cassandra

## Summary

## ETL Pipeline Processing
- Created `event_data_new.csv` file
- Used the appropriate datatype within the CREATE statement

## Data Modeling
- Created the Apache Cassandra tables for three queries
- The CREATE TABLE statement includes the appropriate table
- Followed the one table per query rule of Apache Cassandra
- Not replicating the same table for all three queries, which defies that rule
- Have three distinct tables with unique tables names and used appropriate CREATE table statements
- The SELECT statement does NOT use ALLOW FILTERING to generate the results

- In query 3, SELECT statement selected only the name of the user, even though the data in the table is partitioned with a PARTITION KEY and CLUSTERING COLUMN for this specific query

- Table names reflect the query and the result it will generate
- Table names include alphanumeric characters and underscores, and table names must start with a letter

- The sequence in which columns appear reflect how the data is partitioned and the order of the data within the partitions

- Apache Cassandra is a partition row store, which means the partition key determines which node a particular row is stored on
- With the Primary key (which includes the Partition Key and any clustering columns), the partitions are distributed across the nodes of the cluster
- It determines how data are chunked for write purposes. Any clustering column(s) would determine the order in which the data is sorted within the partition

## PRIMARY KEYS
- The combination of the PARTITION KEY and CLUSTERING COLUMNS are used to uniquely identify each row

- Implemented the PRIMARY KEY with a COMPOSITE Partition for both the CREATE and INSERT statements

- In query 1, each row is uniquely identified with the combination of userId, sessionId and clustering column itemInSession
