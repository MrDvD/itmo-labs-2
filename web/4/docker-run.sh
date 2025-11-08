npm i && \
scalafmt && \
npm run clean
npm run build && \
mvn clean package && \
sudo -E docker compose up