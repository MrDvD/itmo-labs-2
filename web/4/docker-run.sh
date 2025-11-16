npm i && \
# scalafmt && \
npm run clean
npm run build && \
# mvn clean package
cp ./docker/Dockerfile.dev ./Dockerfile && \
sudo docker compose build && \
sudo -E docker compose up