rm -rf public && \
npm run format && \
npm run build && \
scp -r public helios:wildfly-37.0.1.Final/resources