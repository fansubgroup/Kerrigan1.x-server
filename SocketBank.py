#!/usr/bin/env python

import socket
from multiprocessing.reduction import reduce_handle, rebuild_handle

def boss(q_to_bank, q_back_bank):
    
    # SOCKETBANK [[[name], [client_socket], [process_id]], [...]]
    SOCKETBANK = []
    
    while True:
        
        if not q_to_bank.empty():
            
            data = q_to_bank.get()
            
            if data[0][0] == 'UPDATE CLIENT SOCKET':
                
                # message send to staff [[command], [name], [client_socket], [process_id]]
                new_socket_list = []
                
                new_socket_list.append(data[1])
                
                new_socket_fd = rebuild_handle(data[2][0])
                
                new_socket = socket.fromfd(new_socket_fd, socket.AF_INET, socket.SOCK_STREAM)
                
                new_socket_list.append([new_socket])
                
                new_socket_list.append(data[3])
                
                # [[name], [client_socket], [process_id]]
                SOCKETBANK.append(new_socket_list)
                
            elif data[0][0] == 'GET ALL THE ONLINE USERS':
                # message like [['GET ALL THE ONLINE USERS'], [process_id]]
                
                back_all = []
                
                back_all.append(['ALL'])
                
                back_all.append(data[1])
                
                name_list = []
                
                for lines in SOCKETBANK:
                    
                    name_list.append(lines[0])
                    
                back_all.append(name_list)
                
                # back message [[ALL], [process_id], [name_list]]
                q_back_bank.put(back_all)
                
            elif data[0][0] == 'GET FRIEND':
                
                # message like [['GET FRIEND'], [process_id], friend_list]
                friends_name_list = data[2]
                    
                want_list = [['RETURN QUERY RESULT']]
                
                #append the [process_id] in list
                want_list.append(data[1])
                
                name_and_socket_list = []
                
                # SOCKETBANK [[[name], [client_socket], [process_id]], [...]]
                for friends_name in friends_name_list:
                    
                    for lines_name in SOCKETBANK:
                        
                        if friends_name == lines_name[0][0]:
                            
                            temp_list = []
                            
                            temp_list.append(lines_name[0][0])
                            
                            hh = reduce_handle(lines_name[1][0].fileno())
                            
                            temp_list.append(hh)
                            
                            name_and_socket_list.append(temp_list)
                            
                want_list.append(name_and_socket_list)
                
                # back message [[RETURN QUERY RESULT], [process_id], [[name, socket], [name, socket], [...]]]
                q_back_bank.put(want_list)
                
            elif data[0][0] == 'REMOVE MY NAME':
                
                # message like [['REMOVE MY NAME', [process_id]]
                # SOCKETBANK [[[name], [client_socket], [process_id]], [...]]
                for lines_remove in SOCKETBANK:
                    
                    # lines_remove like [[name], [client_socket], [process_id]]
                    if lines_remove[2][0] == data[1][0]:
                        
                        SOCKETBANK.remove(lines_remove)
