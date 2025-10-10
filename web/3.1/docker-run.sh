npm i && \
scalafmt && \
mvn clean package && \
npm run clean && \
npm run format && \
npm run build && \
sudo -E docker compose up