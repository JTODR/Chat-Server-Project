import select, socket, sys, pdb
from chat_server_util import Server, Room, Client
import chat_server_util
import time

READ_BUFFER = 4096
join_id = 1     # set first client join id

# retrieve port number and IP address
chat_server_util.host = sys.argv[1] if len(sys.argv) >= 2 else ''
chat_server_util.PORT = (int)(sys.argv[2])

# set up sockets on port number and IP address
listen_sock = chat_server_util.create_socket((chat_server_util.host, chat_server_util.PORT))

server = Server()	# create an instance of the whole server
connection_list = []
connection_list.append(listen_sock)

while True:

    # select.select() is a unix system call creates lists of waitable objects
    # it returns a 3 lists of objects which are subsets of connection_list, [], and []
    # connection_list will wait until ready for reading from sockets
    read_sockets, write_sockets, error_sockets = select.select(connection_list, [], [])	
    
    for client in read_sockets:		# check all connected sockets
    
        if client is listen_sock: # new connection, client is a socket
            new_socket, add = client.accept()
           
            # add a new client with "NEW_CLIENT" as temporary name and assign a join id
            new_client = Client(new_socket, "NEW_CLIENT", join_id)     
            connection_list.append(new_client)
            join_id = join_id + 1   # increment global join id for next client

        else: # already a client, read the message
            msg = client.socket.recv(READ_BUFFER)

            if msg:	  # check for valid message
                server.read_message(client, msg)	# handle the message
            

    for sock in error_sockets: # close error sockets
    	error_code = 1
    	error_message = "ERROR_CODE: " + str(error_code) \
    	+ "\nERROR_DESCRIPTION: Socket pushed to error list"
        sock.sendall(error_message)
        sock.close()
        connection_list.remove(sock)
