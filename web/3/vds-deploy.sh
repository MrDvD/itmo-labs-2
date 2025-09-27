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
  git clone git@github.com:MrDvD/itmo-labs-2.git --branch web-3
EOF
WEB_3=$(ssh -o ControlPath=$ssh_ctl vdska 'source .bashrc; echo $WEB_3')
scp -ro ControlPath=$ssh_ctl public "vdska:$WEB_3" && \
scp -ro ControlPath=$ssh_ctl target "vdska:$WEB_3" && \
ssh -o ControlPath=$ssh_ctl vdska << EOF
  source .bashrc
  cd \$WEB_3
  docker compose down
  chown -R 1000:1000 ./target ./public ./src
  chmod -R u+rwX ./target ./public ./src
  POSTGRES_HOST=$POSTGRES_HOST POSTGRES_DB=$POSTGRES_DB POSTGRES_USER=$POSTGRES_USER POSTGRES_PASSWORD=$POSTGRES_PASSWORD docker compose up
EOF
ssh -o ControlPath=$ssh_ctl -O exit vdska