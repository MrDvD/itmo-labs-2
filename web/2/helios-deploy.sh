rm -rf public
npm run format
npm run build
ssh helios "rm -r wildfly-37.0.1.Final/resources"
scp -r public helios:wildfly-37.0.1.Final/resources