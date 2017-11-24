# Python Chat Server  
# CS4400 Internet Applications Assigment 1
**Name:** Joseph O'Donovan  
**Student Number:** 14315530

## Dependencies
This project is written in **Python 2.7**  
This project must be compiled and run on a **UNIX machine**  
Run this project with: **./start.sh PORTNUMBER**  

## Project Overview
This project is a multi-roomed chat server written in Python.  
Clients must join a chatroom to chat with other clients.  
Clients can join multiple chatrooms.  
Clients can leave chatrooms.  
A client may leave the server by sending "KILL_SERVICE\n"

----

Clients can join a chatroom by sending a join message:  
**JOIN\_CHATROOM: [chatroom name]  
CLIENT\_IP: [IP address of client]  
PORT: [port number of client]  
CLIENT\_NAME: [name of client]**

----

Clients can leave a chatroom by sending a leave message:  
**LEAVE\_CHATROOM: [room reference]  
JOIN\_ID: [client's assigned join id]  
CLIENT\_NAME: [name of client]**

----

Clients can send a message to their chatroom by sending:  
**CHAT: [room reference]   
JOIN\_ID: [client's assigned join id]  
CLIENT\_NAME: [name of client]  
MESSAGE: [string terminated with '\n\n']**


