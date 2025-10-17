npm i && \
scalafmt && \
mvn clean package && \
npm run clean && \
npm run format && \
npm run build

ssh_ctl=./ssh-ctl

ssh -fNM -o ControlPath=$ssh_ctl vdska
ssh -o ControlPath=$ssh_ctl vdska << EOF
  source .bashrc
  rm -rf \$ITMO_LABS/itmo-labs-2
  cd \$ITMO_LABS
  git clone git@github.com:MrDvD/itmo-labs-2.git --branch web-3-dop
EOF
WEB_3_1=$(ssh -o ControlPath=$ssh_ctl vdska 'source .bashrc; echo $WEB_3_1')
scp -ro ControlPath=$ssh_ctl public "vdska:$WEB_3_1" && \
scp -ro ControlPath=$ssh_ctl app/target "vdska:$WEB_3_1"/app && \
ssh -o ControlPath=$ssh_ctl vdska << EOF
  source .bashrc
  cd \$WEB_3_1
  docker compose down
  chown -R 1000:1000 ./app ./public
  chmod -R u+rwX ./app ./public
  POSTGRES_HOST=$POSTGRES_HOST POSTGRES_DB=$POSTGRES_DB POSTGRES_USER=$POSTGRES_USER POSTGRES_PASSWORD=$POSTGRES_PASSWORD docker compose up
EOF
ssh -o ControlPath=$ssh_ctl -O exit vdska