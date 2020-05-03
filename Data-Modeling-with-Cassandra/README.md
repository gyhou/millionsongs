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

Student demonstrates good understanding of data modeling by generating correct SELECT statements to generate the result being asked for in the question.

The SELECT statement should NOT use ALLOW FILTERING to generate the results.

Awesome work! Your data is modeled correctly to generate the exact responses posed in the questions. For e.g., in query 3, SELECT statement you have selected only the name of the user, even though your data in the table is partitioned with a PARTITION KEY and CLUSTERING COLUMN for this specific query.

Student should use table names that reflect the query and the result it will generate. Table names should include alphanumeric characters and underscores, and table names must start with a letter.

Nice work! Each of your table names indicate what the respective query is about.

The sequence in which columns appear should reflect how the data is partitioned and the order of the data within the partitions.

Excellent work! This is probably one of the most important learnings that I want you to walk away with from this lesson. Apache Cassandra is a partition row store, which means the partition key determines which node a particular row is stored on. With the Primary key (which includes the Partition Key and any clustering columns), the partitions are distributed across the nodes of the cluster. It determines how data are chunked for write purposes. Any clustering column(s) would determine the order in which the data is sorted within the partition.

## PRIMARY KEYS
The combination of the PARTITION KEY alone or with the addition of CLUSTERING COLUMNS should be used appropriately to uniquely identify each row.

Excellent work at understanding and then implementing the PRIMARY KEY with a COMPOSITE Partition for both the CREATE and INSERT statements. I am so glad you took the time to understand this and make this change. For e.g., in query 1, each row is uniquely identified with the combination of userId, sessionId and clustering column itemInSession. Nice work taking the time to look through the data and figuring this out. This is a very important lesson takeaway regarding how COMPOSITE PARTITION key works to uniquely identify each row.
