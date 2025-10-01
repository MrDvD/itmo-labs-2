test -z $APP_DOMAIN || test -z $APP_PORT && {
  echo "Environment variables are not set!"
  exit 1
}

npm i && \
npm run build

ssh_ctl=./ssh-ctl
remote=helios

test ! -S $ssh_ctl && {
  echo "Creating a new ssh connection..."
  ssh -fNM -o ControlPath=$ssh_ctl $remote
}
ssh -o ControlPath=$ssh_ctl $remote "rm -r bin"
scp -ro ControlPath=$ssh_ctl public "$remote:~" && \
scp -ro ControlPath=$ssh_ctl bin "$remote:~" && \
ssh -o ControlPath=$ssh_ctl $remote "APP_DOMAIN=$APP_DOMAIN APP_PORT=$APP_PORT ./bin/server"
ssh -o ControlPath=$ssh_ctl -O exit $remote