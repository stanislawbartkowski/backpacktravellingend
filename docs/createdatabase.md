 ## How to create database from scratch
 
 ### Login as postgres user
 
 As root
 
 ```
 su - postgres
 psql
 ```
 
 Create user and database (user, password and database name can be changed later)
 
 ```SQL
CREATE USER backuser  WITH PASSWORD 'secret';
create database backpack with owner backuser;
``` 
### Verify using psql command line

(password: secret)

```
psql -h /hostname/ -U backuser backpack
Password for user backuser: 
psql (14.7 (Homebrew))
Type "help" for help.

backpack=> 
```
### Create database schema using psql command line

> psql -h /hostname/ -U backuser backpack -f createschema.sql
