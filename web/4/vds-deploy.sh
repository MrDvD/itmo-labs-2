npm i && \
scalafmt && \
npm run clean
npm run build && \
mvn clean package

ssh_ctl=./ssh-ctl

ssh -fNM -o ControlPath=$ssh_ctl vdska
ssh -o ControlPath=$ssh_ctl vdska << EOF
  source .bashrc
  rm -rf \$ITMO_LABS/itmo-labs-2
  cd \$ITMO_LABS
  git clone git@github.com:MrDvD/itmo-labs-2.git --branch web-4
EOF
WEB_4=$(ssh -o ControlPath=$ssh_ctl vdska 'source .bashrc; echo $WEB_4')
scp -ro ControlPath=$ssh_ctl dist "vdska:$WEB_4" && \
ssh -o ControlPath=$ssh_ctl vdska "mkdir -p $WEB_4/target" && \
scp -o ControlPath=$ssh_ctl target/lab-4-1.0.jar "vdska:$WEB_4/target/" && \
ssh -o ControlPath=$ssh_ctl vdska << EOF
  source .bashrc
  cd \$WEB_4
  docker compose down
  cp ./docker/Dockerfile.main ./Dockerfile && \
  chown -R 1000:1000 ./dist ./target
  chmod -R u+rwX ./dist ./target
  POSTGRES_HOST=$POSTGRES_HOST POSTGRES_DB=$POSTGRES_DB POSTGRES_USER=$POSTGRES_USER POSTGRES_PASSWORD=$POSTGRES_PASSWORD APP_SECRET=$APP_SECRET docker compose up
EOF
ssh -o ControlPath=$ssh_ctl -O exit vdska