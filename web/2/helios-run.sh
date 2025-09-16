mvn -f $WEB_2 clean package && \
cp $WEB_2/conf/standalone.xml $WILDFLY_HOME/standalone/configuration/ && \
cp $WEB_2/target/lab-2-1.0.war $WILDFLY_HOME/standalone/deployments/ && \
. $WILDFLY_HOME/standalone.sh