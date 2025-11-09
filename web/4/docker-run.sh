npm i && \
scalafmt && \
npm run clean
npm run build && \
mvn clean package
sudo docker compose build && \
sudo -E docker compose up