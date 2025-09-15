mvn clean package && \
rm -rf public && \
npm run format && \
npm run build && \
sudo docker compose up