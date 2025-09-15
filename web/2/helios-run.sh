mvn clean package && \
export PATH=$PATH:~/wildfly-37.0.1.Final/bin && \
cp conf/standalone.xml ~/wildfly-37.0.1.Final/standalone/configuration/ && \
cp target/lab-2-1.0.war ~/wildfly-37.0.1.Final/standalone/deployments/ && \
standalone.sh