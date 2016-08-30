#!/usr/bin/env python

import os
import socket
import select

def smooth(s_to_client, q_send, q_recv, name):
    
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
                    
                    user_choice = sock.recv(4096)
                    
                    if user_choice == 'f':
                        
                        find_string = 'GET ALL THE ONLINE USERS'
                        
                        find_list = []
                        
                        find_list.append(find_string)
                        
                        #for compatibility with other lists with data, here we are still using a binary array
                        send_1 = []
                        
                        send_1.append(find_list)
                        
                        q_send.put(send_1)
                        
                        online_user = q_recv.get()
                        
                        baby = True
                        
                        while baby:
                        
                            s_once = ''
                            
                            db_key = 1
                            
                            for i in online_user:
                                
                                s_once = s_once + '%d - %s\n' % (db_key, i[0])
                                
                                db_key += 1
                                
                            string_1 = "Find your friends in this list\nTo distinguish multiple friends with ',' etc '1,2,3'\nq - quit"
                            
                            sock.sendall(s_once + string_1)
                            
                            friends_key = sock.recv(4096)
                            
                            if friends_key == 'q':
                                
                                sock.sendall("Quiting...")
                                
                                baby = False
                                
                            else:
                                
                                friends_list = friends_key.split(',')
                                
                                get_friends_command = 'GET FRIEND'
                                
                                get_list = []
                                
                                get_list.append(get_friends_command)
                                
                                friend_send_list = []
                                
                                friend_send_list.append(get_list)
                                
                                friend_send_list.append(friends_list)
                                
                                #put the friend list in queue
                                q_send.put(friend_send_list)
                                
                                friend_sock = q_recv.get()
                                
                                for s in friend_sock:
                                    
                                    FriendCircle.append(s)
                                    
                                sock.sendall("Ok, add successful")
                                
                        break
                        
                    elif user_choice == 'q':
                        
                        sock.sendall('Quiting...')
                        
                        break
                        
                    elif user_choice == 'Q':
                        
                        scok.sendall('Thank you useing')
                        
                        search_db = sqlite3.connect('temp/server.db')
                        
                        search_cursor = search_db.cursor()
                        
                        search_cursor.execute("delete from online where name =" + name)
                        
                        search_db.commit()
                        
                        search_cursor.close()
                        
                        search_db.close()
                        
                        os._exit()
