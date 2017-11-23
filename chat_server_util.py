import socket, pdb

MAX_CLIENTS = 30
PORT = 0
host = ""
room_ref = 100
student_id = 14315530


def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    host = address[0]
    print "HOST$$: " + str(host)
    print "Listening at " + str(address) + "\n" 
    return s

class Server:
    
    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.room_client_map = {} # {clienJoinID: roomName}
        self.room_ref = room_ref
        self.rooms_dict = {} # {room_ref: Room}

    def read_message(self, client, msg):
        print "-*- " + client.name + " join_id is: " + str(client.join_id)
        print("--> " + client.name + " says: \n" + msg)
        
        
        if "JOIN_CHATROOM:" in msg:
            #print "&&&&&& HOST " + host 
            same_room = False
            new_room = 0
            if len(msg.split()) >= 2: # error check
                room_name = msg.split()[1]
                client.name = msg.split()[7]
                #print "CLIENT NAME$$$: " + client.name
                #if client.name in self.room_client_map: # switching?
                #
                #    if self.room_client_map[client.name] == room_name:	# already in this room
                #        client.socket.sendall("You are already in room: " + room_name + "\n")
                #        same_room = True
                #        
                #    else: # switching room
                #        old_room = self.room_client_map[client.name]
                #        old_room_ref = self.rooms[old_room].room_ref
                #        self.rooms[old_room].remove_client(client, old_room_ref)
                #        #self.check_empty_room(old_room)
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name, self.room_ref)
                        self.rooms[room_name] = new_room	# create a new room
                        self.rooms[room_name].room_ref = self.room_ref  # Attach room reference
                        client.room_refs.append(self.room_ref)
                        self.rooms_dict[self.room_ref] = room_name
                        #print "APPENDED CLIENT REF LIST: " + str(client.room_refs)
                        new_room = 1
                        self.room_ref = self.room_ref + 1
                    self.rooms[room_name].clients.append(client)	# add client to the room
                    if new_room == 0:
                        client.room_refs.append(self.rooms[room_name].room_ref)
                        #print "APPENDED CLIENT REF LIST: " + str(client.room_refs)
                        #new_room = 1
                    joined_string = "JOINED_CHATROOM: " + room_name \
                    + "\nSERVER_IP: " + host \
                    + "\nPORT: " + str(PORT) \
                    + "\nROOM_REF: " + str(self.rooms[room_name].room_ref) \
                    + "\nJOIN_ID: " + str(client.join_id) + "\n"
                    client.socket.sendall(joined_string)
                    #print "SENT$$: " + joined_string
                    
                    self.rooms[room_name].welcome_new(client, str(self.rooms[room_name].room_ref))
                    self.room_client_map[self.rooms[room_name].room_ref + (client.join_id*10)] = room_name
                    msg = " "             
        
        elif "LEAVE_CHATROOM:" in msg:
            
            leave_room_ref = msg.split()[1]
            leave_join_id = msg.split()[3]
            leave_client_name = msg.split()[5]
            leave_msg = "LEFT_CHATROOM: " + leave_room_ref + "\nJOIN_ID: " + leave_join_id + "\n"
            client.socket.sendall(leave_msg)
            #print "CLIENT REF LIST: " + str(client.room_refs)
            
            #print "SENT LEAAVE$$" + leave_msg
            
            old_room = self.rooms_dict[int(leave_room_ref)]
            #old_room = self.room_client_map[int(leave_join_id)]    # get name of room to leave
            self.rooms[old_room].remove_client(client, leave_room_ref)      # remove client from the room
            client.room_refs.remove(int(leave_room_ref))
            #print "REMOVED CLIENT REF LIST: " + str(client.room_refs)
            #int_leave_id = 
            del self.room_client_map[int(leave_room_ref) + (int(leave_join_id)*10)]
            #self.check_empty_room(old_room)
           
        elif "DISCONNECT:" in msg:
            for room_ref in client.room_refs:
                old_room = self.rooms_dict[int(room_ref)]
                self.rooms[old_room].remove_client(client, room_ref)
            client.socket.shutdown(socket.SHUT_RDWR)    # terminate the client's connection
            #self.remove_client(client)
            

        elif "CHAT:" in msg:
            # check if in a room or not first
            
            recv_room_ref = msg.split()[1]
            recv_client_name = msg.split()[5]
            recv_message = msg.split("MESSAGE: ")[1]    # get the message          
            
            if len(client.room_refs) != 0: 
                       
                msg_to_send = "CHAT: " + recv_room_ref \
                + "\nCLIENT_NAME: " + recv_client_name \
                + "\nMESSAGE: " + recv_message
                self.rooms[self.room_client_map[int(recv_room_ref) + (client.join_id*10)]].broadcast(client, msg_to_send)
                print "SERVER SENT:\n" + msg_to_send + "\n"
            
        elif "HELO" in msg:
            text = msg.split()[1]
            msg = "HELO " + text \
            + "\nIP:" + str(host) \
            + "\nPort:" + str(PORT) \
            + "\nStudentID:" + str(student_id) + "\n"
            client.socket.sendall(msg)
        elif "KILL_SERVICE" in msg:
            for room_ref in client.room_refs:
                old_room = self.rooms_dict[int(room_ref)]
                self.rooms[old_room].remove_client(client, room_ref)
            client.socket.shutdown(socket.SHUT_RDWR)    # terminate the client's connection
            self.remove_client(client)
            
        else:
            print msg
    
    def remove_client(self, client):
        for room_ref in client.room_refs:
            self.rooms[self.room_client_map[int(room_ref) + (client.join_id*10)]].remove_client(client)
            del self.room_client_map[client.join_id]
        print("Client: " + client.name + " has left\n")

    #def check_empty_room(self, room_name):
    #     if len(self.rooms[room_name].clients) == 0:      # check if this room is now empty
    #        print room_name + " is empty, deleting...\n"
    #        del self.rooms[room_name]        # delete empty room from rooms list
    
    
class Room:
    def __init__(self, name, room_ref):
        self.clients = [] # a list of sockets
        self.name = name
        self.room_ref = room_ref

    def welcome_new(self, from_client, room_ref):     # welcome message when joining a room
        msg = from_client.name + " has joined this chatroom"
        msg_to_send = "CHAT: " + room_ref \
        + "\nCLIENT_NAME: " + from_client.name \
        + "\nMESSAGE:" + msg + "\n\n"
        
        
        for client in self.clients:
            client.socket.sendall(msg_to_send)      # send welcome message to all clients in room
        #print "Welcome"
        
    def broadcast(self, from_client, msg):
        #msg = from_client.name + b": " + msg    # add clients name
        for client in self.clients:
            #if client is not from_client:       # broadcast to all except the client who sent it
            client.socket.sendall(msg)

    def remove_client(self, client, leave_room_ref):
        
        leave_msg = client.name + " has left the room\n"
        msg_to_send = "CHAT: " + str(leave_room_ref) \
        + "\nCLIENT_NAME: " + client.name \
        + "\nMESSAGE:" + leave_msg + "\n"
        self.broadcast(client, msg_to_send)
        self.clients.remove(client)
        print "SERVER SENT:\n" + msg_to_send + "\n"

class Client:
    
    def __init__(self, socket, name, join_id):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
        self.join_id = join_id
        self.room_refs = []

    def fileno(self):
        return self.socket.fileno()
