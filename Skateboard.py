#!/usr/bin/env python

import os
import socket
import select
import json
from multiprocessing.reduction import rebuild_handle

def smooth(s_to_client, q_to_staff, name, process_id, staff_socket):
    
    MAX_LISTEN = 3
    
    ONE_LIST = []
    
    ONE_LIST.append(s_to_client)
    
    FriendCircle = []
    
    ChatMenu = ("f - Find friend in this server\n"
                "q - Quit menu\n"
                "Q - Quit Chat")
    
    Skateboard_say = ("This is Customer Service Mr.Skateboard\n"
                      "You could use the ## to enter the <Chat Menu>\n"
                      "You ars talking with a Server Machine."
                      "Please search a friend")
    
    while True:
    
        reads, writes, errors = select.select(ONE_LIST, [], [])
        
        for sock in reads:
            
            data = sock.recv(4096)
            
            if data:
                
                if data != '##':
                    
                    sock.sendall(Skateboard_say)
                    
                    for s in FriendCircle:
                        
                        s.sendall(data)
                
                elif data == '##':
                    
                    sock.sendall(ChatMenu)
                    
                    #print 'sock'
                    
                    user_choice = sock.recv(4096)
                    
                    if user_choice == 'f':
                        
                        find_list = [['GET ALL THE ONLINE USERS']]
                        
                        find_list.append([process_id])
                        
                        # message like [['GET ALL THE ONLINE USERS'], [process_id]]
                        q_to_staff.put(find_list)
                        
                        staff_socket.listen(MAX_LISTEN)
                        
                        cons, addr = staff_socket.accept()
                        
                        online_user_json = cons.recv(4096)
                        
                        online_user = json.loads(online_user_json)
                        
                        s_once = ''
                        
                        db_key = 1
                        
                        for i in online_user:
                            
                            s_once = s_once + '%d - %s\n' % (db_key, i[0])
                            
                            db_key += 1
                            
                        string_1 = "Enter your friends name\nEtc 'Jack,Piter'\nq - quit"
                        
                        sock.sendall(s_once + string_1)
                        
                        friends_key = sock.recv(4096)
                        
                        if friends_key == 'q':
                            
                            # quit the Menu
                            sock.sendall("Quiting...")
                            
                            baby = False
                            
                        else:
                            
                            # get the friend's socket friends_key like 'Jack, Piter'
                            friends_list = friends_key.split(',')
                            
                            get_list = [['GET FRIEND']]
                            
                            get_list.append([process_id])
                            
                            get_list.append(friends_list)
                            
                            # message like [['GET FRIEND'], [process_id], friend_list]
                            q_to_staff.put(get_list)
                            
                            staff_socket.listen(MAX_LISTEN)
                            
                            gfs, gfr = staff_socket.accept()
                            
                            query_json = gfs.recv(4096)
                            
                            query_result = json.loads(query_json)
                            
                            # deal with the origin data
                            
                            print len(query_result)
                            
                            # data like [[RETURN QUERY RESULT], [process_id], [[name, socket], [name, socket], [...]]]
                            name_socket_list = query_result[2]
                            
                            # name_socket_list like [[name, socket], [name, socket], [...]]
                            for s in name_socket_list:
                                
                                print s[0]
                                
                                fd = rebuild_handle(s[1])
                                
                                fd_socket = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
                                
                                FriendCircle.append(fd_socket)
                                
                            sock.sendall("Ok, add successful")
                                
                        break
                        
                    elif user_choice == 'q':
                        
                        sock.sendall('Quiting...')
                        
                        break
                        
                    elif user_choice == 'Q':
                        
                        scok.sendall('Thank you using')
                        
                        search_db = sqlite3.connect('temp/server.db')
                        
                        search_cursor = search_db.cursor()
                        
                        search_cursor.execute("delete from online where name =" + name)
                        
                        search_db.commit()
                        
                        search_cursor.close()
                        
                        search_db.close()
                        
                        os._exit()
                        
            else:
                
                sock.sendall('No data')
