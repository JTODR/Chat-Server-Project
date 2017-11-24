#!/bin/bash
#need to run following before ./compile_server.py ->>> chmod 755 compile_server.sh

IP=$(hostname -I)
#echo "$IP" 

python chat_server.py $IP $1
