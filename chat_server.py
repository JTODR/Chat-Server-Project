import select, socket, sys, pdb
from chat_server_util import Server, Room, Client
import chat_server_util
import time

READ_BUFFER = 4096
join_id = 1

chat_server_util.host = sys.argv[1] if len(sys.argv) >= 2 else ''
chat_server_util.PORT = (int)(sys.argv[2])
listen_sock = chat_server_util.create_socket((chat_server_util.host, chat_server_util.PORT))

server = Server()
connection_list = []
connection_list.append(listen_sock)

while True:
    read_sockets, write_sockets, error_sockets = select.select(connection_list, [], [])
    for client in read_sockets:		# check all connected sockets
        if client is listen_sock: # new connection, client is a socket
            new_socket, add = client.accept()
            new_client = Client(new_socket, "new", join_id)     # add a new client
            connection_list.append(new_client)
            join_id = join_id + 1

        else: # already a client, read the message
            msg = client.socket.recv(READ_BUFFER)

            if msg:			# check for message
                server.read_message(client, msg)	# interpret message
            

    for sock in error_sockets: # close error sockets
    	error_code = 1
    	error_message = "ERROR_CODE: " + str(error_code) \
    	+ "\nERROR_DESCRIPTION: Socket pushed to error list"
        sock.sendall(error_message)
        sock.close()
        connection_list.remove(sock)
