#!/bin/bash

# WARNING: This project must be run on a UNIX machine

# Get machine IP address
IP=$(hostname -I)

# Compile and run the server on the IP at the port number provided by the command line
python chat_server.py $IP $1
