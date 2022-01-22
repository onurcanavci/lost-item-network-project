import socket
import re
import _thread
import json
import time 
import hashlib
import search
PORT = 12345
UDPPORT = 12345

# Thread lock for threads that update or retreive users dictionary
users_lock = _thread.allocate_lock()
users = {}
lost_items = {}
awaiting_approvals = {}
myName = ""
myIP = ""
splittedIP = ""
s = None
bursts = set()
found_items = {}
notify_items = {}


def print_red(*message):
    print('\033[91m' + " ".join(message) + '\033[0m')

def print_green(*message):
    print('\033[92m' + " ".join(message) + '\033[0m')

def print_cyan(*message):
    print('\033[96m' + " ".join(message) + '\033[0m')

def print_yellow(*message):
    print('\033[93m' + " ".join(message) + '\033[0m')

def validate_and_parse_json(message):
    try:
        message = json.loads(message)
      # print(message)
        if message["type"] == 1:
            if "ID" not in message or type(message["ID"]) != int:
                return json.loads('{"type": 0}')
        if message["type"] == 2:
            if "IP" not in message or len(message["IP"].split(".")) != 4:
                return json.loads('{"type": 0}')
        elif message["type"] == 3:
            if "body" not in message:
                return json.loads('{"type": 0}')
        return message
    except Exception as e:
        return json.loads('{"type": 0}')

# Function to get online users. It shows IPs that are not empty.
def get_users():
    users_lock.acquire()
    response = [(name, users[name]) for name in users]
    users_lock.release()
    return response

# Function to get IP address of a user.
def get_user(name):
    users_lock.acquire()
    response = users[name]
    users_lock.release()
    return response

# Checks if a user with specified name exists.
def check_user(name):
    users_lock.acquire()
    response = name in users
    users_lock.release()
    return response

# Adds a user to specified IP address in the user array
def add_user(ip, name):
    users_lock.acquire()
    if name not in users:
        print_green("{} is online".format(name))
    reverse = {users[name]:name for name in users}
    if ip in reverse:
        del users[reverse[ip]]
    users[name] = ip

    users_lock.release()

# Removes user from IP address, used when netcat can't connnect to an IP address
def remove_user(name):
    users_lock.acquire()
    del users[name]
    users_lock.release()


def response_to_discovery(ip):
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, PORT))
            s.sendall('{{"type": 2, "name": "{}", "IP": "{}"}}'.format(myName, myIP).encode())
    except Exception as e:
        print(e)    
        
def send_approval(taker, ID):
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((get_user(taker), PORT))
                approvepacket = {}
                approvepacket["ID"] = ID
                approvepacket["type"] = 8
                approvepacket["name"] = myName
                s.sendall(json.dumps(approvepacket).encode())
                print("send approval sent.")

    except Exception as e:
        print(e)        

def handle_connection(conn):
    with conn:
        data = conn.recv(10240)#.decode("utf-8")
        message = data.decode("utf-8")
    message = validate_and_parse_json(message)
    #print("handle coonection" , message)
    if message["type"] == 1:# Someone wants to discover you, send a discovery response 
        #print("User with name: ", message["name"], " and IP: ", message["IP"], "sent a discover message.")
        _thread.start_new_thread(response_to_discovery, (message["IP"], ))
        add_user(message["IP"], message["name"])
   
    elif message["type"] == 2: # There is a discovery response, save the user.
        #print("We discovered the user with name: ", message["name"], " and IP: ", message["IP"])
        add_user(message["IP"], message["name"])
    
    elif message["type"] == 3: # There is a message, log the message
        #print_cyan("\033[F "+message["name"] + ": " + message["body"] + "\n " + "\033[A ")
        print_cyan(message["name"] + ": " + message["body"])
   
    elif message["type"] == 9:
        print_cyan(message["name"] + ": " + message["item_name"] + " " + message["description"])
        lost_items[message["ID"]] = message
   
    elif message["type"] == 8:
        #print("approve taken")
        #result_message = input("Do you approve to take this item?")
        #while result_message == "yes" or result_message == "no":
        #result_message = input("Do you approve to take this item?")
        #result = True  
        #del lost_items[message["ID"]] 
        #print("lost item deleted")
        awaiting_approvals[message["ID"]] = message
       # _thread.start_new_thread(result_approval , (message["name"] , message["ID"] ,result ))
    
    elif message["type"] == 7 :
        if message["result"] == "yes" :
            print_cyan(message["ID"] + " is taken by " + message["name"])
            #found_items[message["ID"]] = lost_items[message["ID"]]
            #broadcast_found_item(lost_items[message["ID"]] , message["name"])
            if message["ID"] in lost_items:
                del lost_items[message["ID"]]
            #print(lost_items)
        elif message["result"] == "no" : 
            print_cyan(message["ID"] + " is not taken by " + message["name"] + ". Please check the user or ID. ")
            


def listen():
    try:
        while True:
            conn, addr = s.accept()
            _thread.start_new_thread(handle_connection, (conn,))

    except Exception as e:
        print(e)
        #print("Server crashed. Restarting server.")
        #_thread.start_new_thread(listen, ())

def listen_for_discovery():
    try: 
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udps:
                udps.bind(('', UDPPORT))
                #udps.setblocking(0)
                message, address = udps.recvfrom(10240)
                message = validate_and_parse_json(message)

                if message["type"] == 1:# Someone wants to discover you, send a discovery response 
                    #print("User with name: ", message["name"], " and IP: ", message["IP"], "sent a discover message.")
                    if message["ID"] in bursts: continue
                    bursts.add(message["ID"])
                    _thread.start_new_thread(response_to_discovery, (message["IP"], ))
                    add_user(message["IP"], message["name"])
                if message["type"] == 9:
                  # print("lost taken.")
                   lost_items[message["ID"]] = message
                  # print(message["ID"] , " sent by " , message["name"])
                if message["type"] == 11:
                    if  message["item"]["ID"] not in lost_items and message["item"]["ID"] not in found_items :
                        lost_items[message["item"]["ID"]] = message["item"]
                        find_items = {}
                        if len(notify_items) > 0 :
                            queryitem = {}
                            queryitem[message["item"]["ID"]] = message["item"]
                            find_items = search.searchItemName(notify_items["item_name"], queryitem ,find_items)

                            find_items = search.searchDescription(notify_items["description"],find_items)

                            find_items = search.searchLocation(notify_items["place"],find_items)
                            if len(find_items) > 0 :
                                print("An item found!")
                                print_lost_item(message["item"])
                        
                       # print(" lost item info ")
                if message["type"] == 12 :
                    if  message["item"]["ID"]  in lost_items:
                       del lost_items[message ["item"]["ID"] ]
                    if  message["item"]["ID"] not in found_items:
                        found_items[message["item"]["ID"]] = message["item"]
                      # print("found item deleted.")
                if message["type"] == 15:       
                    if  message["item"]["ID"] not in found_items:
                        found_items[message["item"]["ID"]] = message["item"]
                    if  message["item"]["ID"] in lost_items:
                        del lost_items[message["item"]["ID"]]
                    if message["item"] ["ID"] in awaiting_approvals.keys() :
                        del awaiting_approvals[message["item"] ["ID"]]
                     #   print(" found item info ")
    except Exception as e:
        print("33", e)

    finally:
        print_yellow("Closing the udp socket.")
        udps.close()
        



 
def discover():
    try: 
        ts = int(time.time())
        for i in range(10):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udps:
                udps.bind(('', 0))
                udps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
                udps.sendto('{{"type": 1, "name": "{}", "IP": "{}", "ID": {}}}'.format(myName, myIP, ts).encode(),('<broadcast>',UDPPORT))
        print_yellow("Discovery is done.")
    except Exception as e:
        print(e)

    finally:
        udps.close()

def synchronize():
     try: 
         ts = int(time.time())
         while True:
             end = int(time.time())
             if end - ts > 30:
                 for i in range(10):
                     ts = int(time.time())
                     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udps:
                         udps.bind(('', 0))
                         udps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
                         for item in lost_items:
                             lost_message = {}
                             lost_message["type"] = 11
                             lost_message["item"] = lost_items[item]
                             udps.sendto(json.dumps(lost_message).encode(),('<broadcast>',UDPPORT))
                # print("synchronize message sent")
     except Exception as e:
         print(e)

     finally:
         udps.close()
   
def synchronize_found_items():
     try: 
         ts = int(time.time())
         while True:
             end = int(time.time())
             if end - ts > 32:
                 for i in range(10):
                     ts = int(time.time())
                     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udps:
                         udps.bind(('', 0))
                         udps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
                         for item in found_items:
                             found_message = {}
                             found_message["type"] = 15
                             found_message["item"] = found_items[item]
                             udps.sendto(json.dumps(found_message).encode(),('<broadcast>',UDPPORT))
                # print("synchronize found message sent")
     except Exception as e:
         print(e)

     finally:
         udps.close()         
 
def broadcast_found_item(item ,name): 
         try: 
             ts = int(time.time())
             for i in range(10):
                 with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udps:
                     udps.bind(('', 0))
                     udps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
                     found_message = {}
                     found_message["type"] = 12
                     found_message["item"] = item
                     found_message["takername"] = name
                     udps.sendto(json.dumps(found_message).encode(),('<broadcast>',UDPPORT))
                     #print("found items sent")    
         except Exception as e:
             print(e)

         finally:
             udps.close()
def print_lost_item(item):
    
    print("Name:" , item["item_name"]) 
    print("Description:" , item["description"])
    print("Found at:" , item["place"])     
    print("Found date:" , item["date"])
    print("Now at:" , item["name"])
    print("ID of the item:" , item["ID"])
    print()
def print_found_item(item):
    print("Name:" , item["item_name"]) 
    print("Description:" , item["description"])
    print("Found at:" , item["place"])     
    print("Found date:" , item["date"])
    print("Taken by" , item["takername"])
    print("ID of the item:" , item["ID"])
    print()
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    myIP = s.getsockname()[0]
    splittedIP = ".".join(myIP.split(".")[:-1])


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((myIP, PORT))
    s.listen()


    _thread.start_new_thread(listen, ())
    myName = input("My name: ")
    _thread.start_new_thread(listen_for_discovery, ())
    _thread.start_new_thread(discover, ())
    _thread.start_new_thread(synchronize, ())
    _thread.start_new_thread(synchronize_found_items, ())


    while True:
        
        commandhelper = input("What do you want to do?  \nsee_onlines -> 0\nlost_items -> 1\napproval_message -> 2\nlost_item_broadcast -> 3\nfound_items -> 4\nexit -> 5\n")
        while commandhelper not in ["0" , "1" , "2" ,"3", "4" , "5" ]:
            commandhelper = input("What do you want to do?  \nsee_onlines -> 0\nlost_items -> 1\napproval_message -> 2\lost_item_broadcast -> 3\nfound_items -> 4\nexit -> 5\n")

        commands = ["see_onlines" , "lost_items" , "approval_message" , "lost_item_broadcast" , "found_items" , "exit"]
        command = commands[int (commandhelper)]        
        
        if command == "lost_item_broadcast":
            
            found_date = input("When it was found? (dd/mm/yyyy)")
            founder_name = input("Who found it? (name surname)")
            found_place = input("Where it was found?")
            lost_item_name = input("Name/type of lost item.")
            description = input("Brief description of lost item.")
            
            lost_packet = {}
            lost_packet["date"] = found_date
            lost_packet["foundername"] = founder_name
            lost_packet["place"] = found_place
            lost_packet["item_name"] = lost_item_name
            lost_packet["description"] = description
            lost_packet["name"] = myName 
            start = int(time.time())
            hashstring = lost_packet["item_name"] + str(start)
            hashbytes = hashstring.encode()
            hash_object = hashlib.sha256(hashbytes)
            ID = hash_object.hexdigest()[:16]
            lost_packet["ID"] = ID
            lost_packet["type"] = 9
            lost_items[lost_packet["ID"]] = lost_packet
            
            #_thread.start_new_thread(broadcast_lost_item , (found_date , founder_name, found_place, lost_item_name, description, ID))
      
        if command == "approval_message":
            taker = input("Who will take the item?")
            while taker not in users:
                taker = input("Please give an online user")                
            ID = input("ID of the lost item.")
            while ID not in lost_items  :
                ID = input("Wrong ID. Please write a correct ID.")
            _thread.start_new_thread(send_approval , (taker , ID))
            
        if command == "found_items":
            #print(found_items)
            for item in found_items:
               print_found_item(found_items[item])
            
        if command == "lost_items":
            for item in lost_items:
                print_lost_item(lost_items[item])
            
        
        elif command == "see_onlines":
            print_green("\n".join(u for u, _ in get_users()))
        elif command == "exit":
            break 

        
except Exception as e:
    print(e)

finally:
    print_yellow("Closing the socket.")
    s.close()

