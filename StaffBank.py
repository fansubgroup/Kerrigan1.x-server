#!/usr/bin/env python

# NOTE: The Command List
#
# <UPDATE CLIENT SOCKET>
# Meaning: Put client socket into a bank in order to query backup
#
# <GET ALL THE ONLINE USERS>
# Meaning: Returns a list of all online users
#
# <GET FRIENDS>
# Meaning: Returns a list of the friends you want to talk with

import socket
import json

def staff(q_to_bank, q_back_bank, q_to_staff):
    
    SOCKETBANK = []
    
    BACK_BANK = []
    
    return_result_all = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    return_result_friend = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    while True:
        
        if not q_to_staff.empty():
            
            data = q_to_staff.get()
            
            if data[0][0] == 'UPDATE CLIENT SOCKET':
                
                # message send to staff [[command], [name], [client_socket], [process_id]]
                update_to_bank = []
                
                command_to_bank = ['UPDATE']
                
                update_to_bank.append(command_to_bank)
                
                update_to_bank.append(data[1])
                
                update_to_bank.append(data[2])
                
                update_to_bank.append(data[3])
                
                q_to_bank.put(update_to_bank)
                
            if data[0][0] == 'GET ALL THE ONLINE USERS':
                
                q_to_bank.put(data)
                
            if data[0][0] == 'GET FRIEND':
                
                # message like [['GET FRIEND'], [process_id], [friend_list]]
                q_to_bank.put(data)
                
                
        if not q_back_bank.empty():
            
            data_back_bank = q_back_bank.get()
            
            if data_back_bank[0][0] == 'ALL':
                
                # back message [[ALL], [process_id], [name_list]]]
                all_list = data_back_bank[2]
                
                send_all_list = json.dumps(all_list)
                
                socket_id = data_back_bank[1][0]
                
                return_result_all.connect('temp/sock/socket_%d' % socket_id)
                
                return_result_all.sendall(send_all_list)
                
            if data_back_bank[0][0] == 'RETURN QUERY RESULT':
                
                # back message [[RETURN QUERY RESULT], [process_id], [name], [socket]]
                return_query_id = data_back_bank[1][0]
                
                return_friend_list = []
                
                return_friend_list.append(data_back_bank[2])
                
                return_friend_list.append(data_back_bank[3])
                
                return_result_friend.connect('temp/sock/socket_%d' % return_query_id)
                
                return_result-friend.sendall()
                
                print 'ok'
