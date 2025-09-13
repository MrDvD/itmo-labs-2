mvn clean package && \
rm -rf public && \
npm run build && \
sudo docker compose up