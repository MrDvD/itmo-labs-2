ssh_ctl=./ssh-ctl

rm -rf public
npm run format
npm run build

ssh -fNM -o ControlPath=$ssh_ctl helios
ssh -o ControlPath=$ssh_ctl helios "rm -rf itmo-labs-2"
ssh -o ControlPath=$ssh_ctl helios "git clone https://github.com/MrDvD/itmo-labs-2.git && cd itmo-labs-2 && git checkout web-2"

WILDFLY_HOME=$(ssh -o ControlPath=$ssh_ctl helios 'source ~/.bashrc; echo $WILDFLY_HOME')
WEB_2=$(ssh -o ControlPath=$ssh_ctl helios 'source ~/.bashrc; echo $WEB_2')

ssh -o ControlPath=$ssh_ctl helios "rm -r $WILDFLY_HOME/resources"
scp -ro ControlPath=$ssh_ctl public "helios:$WILDFLY_HOME/resources"
ssh -fo ControlPath=$ssh_ctl helios "source ~/.bashrc; _JAVA_OPTIONS='-XX:MaxHeapSize=1G -XX:MaxMetaspaceSize=128m' bash $WEB_2/helios-run.sh" 
ssh -o ControlPath=$ssh_ctl -O exit helios