# This document describes how to configure backend development environment 

## Prerequisites

### PostgreSQL

PostgreSQL database instance local or remote. In case of fresh installation make sure that remote access is configured. Verify that command line access to PosgreSQL is working.
> psql -h /hostname/ -U /username/ 

Create database schema and make sure that user is authorized to access the database.

https://github.com/backpacktraveling/backpacktraveling/blob/main/docs/createdatabase.md

### PostgreSQL connector

PostgreSQL JDBC driver is installed and accessible.

https://jdbc.postgresql.org/


### Java 11

Java 11 installed.

> java --version
```bash
openjdk 11.0.18 2023-01-17 LTS
OpenJDK Runtime Environment (Red_Hat-11.0.18.0.10-3.el9) (build 11.0.18+10-LTS)
OpenJDK 64-Bit Server VM (Red_Hat-11.0.18.0.10-3.el9) (build 11.0.18+10-LTS, mixed mode, sharing)
```

### Python3

> python3
```
Python 3.9.16 (main, Dec  8 2022, 00:00:00) 
[GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] on linux
Type "help", "copyright", "credits" or "license" for more information.
```

Install sqlalchemy

https://www.sqlalchemy.org/

### Maven

Install Maven

> mvn -v
```
Apache Maven 3.6.3 (Red Hat 3.6.3-15)
Maven home: /usr/share/maven
Java version: 11.0.18, vendor: Red Hat, Inc., runtime: /usr/lib/jvm/java-11-openjdk-11.0.18.0.10-3.el9.x86_64
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "5.14.0-177.el9.x86_64", arch: "amd64", family: "unix"
```

## Installation and configuration

### Clone repository

> git clone https://github.com/backpacktraveling/backpacktraveling.git

Verify

> ls backpacktraveling/
```
docs  README.md  server  src  template
```
### Define maven access to GitHub

> vi ~/.m2/settings.xml 
```XML
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
                      http://maven.apache.org/xsd/settings-1.0.0.xsd">

  <activeProfiles>
    <activeProfile>github</activeProfile>
  </activeProfiles>

  <servers>
    <server>
      <id>github</id>
      <username>your name</username>
      <password>your GutHib access key</password>
    </server>
  </servers>
</settings>
```
### Create Java server

> cd backpacktraveling/server<br>
> mvn package

Verify that build is successful

> ls target
```
archive-tmp  
backpacktravelling-1.0-SNAPSHOT.jar  
backpacktravelling-1.0-SNAPSHOT-jar-with-dependencies.jar  
lib  
maven-archiver
```
### Configure

> cd backpacktraveling/server<br>
> cp ../template/* .

> vi env.rc
```
PORT=7999
PROP=rest.properties
JDBC=/usr/share/java/postgresql-jdbc.jar
```
| Parameter | Description
| ---- | ---- | 
| PORT | Java server endpoint port
| PROP | Do not change
| JDBC | Path to PostgreSQL JDBC driver

> vi rest.properties
```
jdir=../src/restdir
plugins=RESOURCE,SQL,PYTHON3,RESOURCEDIR
resdir=../src/resoudir
pythonhome=../src/python
reqparams=user,sessionid

url=jdbc:postgresql://localhost:5432/backpack
user=backuser
password=secret

alchemyconnect=postgresql+psycopg2://backuser:secret@localhost:5432/backpack
```
| Parameter | Description
| ---- | ---- | 
| jdir | Do not change
| plugins | Do not change
| resdir | Do not change
| pythonhome | Do not change
| reqparams | do not change
| url | JDBC URL access to PostgreSQL backpacktraveling database
| user | Authorized user
| password | Password
| alchemyconnect | SQL alchemy connection string. Should reflect JDBC URL access string.

## Run or die

> ./run.sh
```
/home/btest/backpacktraveling/server
[2023-06-13 21:05:02] INFO: jdir value read:../src/restdir  
[2023-06-13 21:05:02] INFO: multithread no value found but not mandatory  
[2023-06-13 21:05:02] INFO: Single thread  
[2023-06-13 21:05:02] INFO: plugins value read:RESOURCE,SQL,PYTHON3,RESOURCEDIR  
[2023-06-13 21:05:02] INFO: pythonhome value read:../src/python  
[2023-06-13 21:05:02] INFO: resdir value read:../src/resoudir  
[2023-06-13 21:05:02] INFO: resdir value read:../src/resoudir  
[2023-06-13 21:05:02] INFO: url value read:jdbc:postgresql://localhost:5432/backpack  
[2023-06-13 21:05:02] INFO: user value read:backuser  
[2023-06-13 21:05:02] INFO: password value read:XXXXXXXX  
[2023-06-13 21:05:02] INFO: Connecting to jdbc:postgresql://localhost:5432/backpack user backuser  
[2023-06-13 21:05:03] INFO: Connected  
[2023-06-13 21:05:03] INFO: RestService 1.2 (r:6), 2023/05/21  
[2023-06-13 21:05:03] INFO: Start HTTP Server, listening on port 7999  
[2023-06-13 21:05:03] INFO: Register service: restversion  
[2023-06-13 21:05:03] INFO: Register service: {root}  
```

Test from another console or browser

> curl /hostname/:7999/restversion
```
{"restver":"RestService 1.2 (r:5), 2023/05/18","jsonapiver":"RestAPIJSON version 1.4 (r:4) 2023/05/18"}
```
