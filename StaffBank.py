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
import threading
from multiprocessing.reduction import reduce_handle, rebuild_handle

def staff(q_to_bank, q_back_bank, q_to_staff):
    
    SOCKETBANK = []
    
    BACK_BANK = []
    
    while True:
        
        if not q_to_staff.empty():
            
            data = q_to_staff.get()
            
            if data[0][0] == 'UPDATE CLIENT SOCKET':
                
                # message send to staff [[command], [name], [client_socket], [process_id]]
                
                # in order to prevent the /tmp file destroying the socket, so we rebuild the socket here once
                again_h = data[2][0]
                
                again_fd = rebuild_handle(again_h)
                
                again_socket = socket.fromfd(again_fd, socket.AF_INET, socket.SOCK_STREAM)
                
                again_list = []
                
                again_list.append(data[0])
                
                again_list.append(data[1])
                
                again_once = reduce_handle(again_socket.fileno())
                
                again_list.append([again_once])
                
                again_list.append(data[3])
                
                q_to_bank.put(again_list)
                
            if data[0][0] == 'GET ALL THE ONLINE USERS':
                
                q_to_bank.put(data)
                
            if data[0][0] == 'GET FRIEND':
                
                # message like [['GET FRIEND'], [process_id], [friend_list]]
                q_to_bank.put(data)
                
            if data[0][0] == 'REMOVE MY NAME':
                
                # message like [['REMOVE MY NAME'], [process_id]]
                
                q_to_bank.put(data)
                
        if not q_back_bank.empty():
            
            data_back_bank = q_back_bank.get()
            
            if len(data_back_bank):
                
                th = threading.Thread(target = socket_connected_threading, args = (data_back_bank,))
                
                th.setDaemon(True)
                
                th.start()


def socket_connected_threading(data_back_bank):
    
    if data_back_bank[0][0] == 'ALL':
        
        return_result_all = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        
        # back message [[ALL], [process_id], [name_list]]]
        all_list = data_back_bank[2]
        
        send_all_list = json.dumps(all_list)
        
        socket_id = data_back_bank[1][0]
        
        return_result_all.connect('temp/sock/socket_%d' % socket_id)
        
        return_result_all.sendall(send_all_list)
        
        return_result_all.close()
        
    if data_back_bank[0][0] == 'RETURN QUERY RESULT':
        
        return_result_friend = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        
        # back message [[RETURN QUERY RESULT], [process_id], [[name, socket], [name, socket], [...]]]
        return_query_id = data_back_bank[1][0]
        
        return_result_friend.connect('temp/sock/socket_%d' % return_query_id)
        
        data_socket = data_back_bank[2]
        
        name_socket_again = []
        
        for ii in data_socket:
            
            iih = ii[1]
            
            iifd = rebuild_handle(iih)
            
            iis = socket.fromfd(iifd, socket.AF_INET, socket.SOCK_STREAM)
            
            iih_again = reduce_handle(iis.fileno())
            
            temp_ns = []
            
            temp_ns.append(iih[0])
            
            temp_ns.append(iih_again)
            
            name_socket_again.append(temp_ns)
        
        new_data = []
        
        new_data.append(data_back_bank[0])
        
        new_data.append(data_back_bank[1])
        
        new_data.append(name_socket_again)
        
        data_back_json = json.dumps(new_data)
        
        return_result_friend.sendall(data_back_json)
        
        return_result_friend.close()
        
        print 'ok'
