echo $PWD
source ./env.rc
JAVA=java
JAR=target/backpacktravelling-1.0-SNAPSHOT-jar-with-dependencies.jar
$JAVA -Djava.util.logging.config.file=logging.properties -cp $JAR:$JDBC RestMain -c $PROP -p $PORT
