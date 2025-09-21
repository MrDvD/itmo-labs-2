npm i && \
mvn clean package && \
npm run clean && \
npm run format && \
npm run build && \
sudo docker compose up