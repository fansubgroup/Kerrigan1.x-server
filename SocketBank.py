#!/usr/bin/env python

from multiprocessing import Queue
from multiprocessing.reduction import reduce_handle, rebuild_handle

def boss(q):
    
    # SOCKETBANK [[[command], [name], [client_socket], [unique_queue_client_send], [unique_queue_client_recv]], [...]]
    SOCKETBANK = []
    
    QUEUE_LIST = []
    
    while True:
        
        if not q.empty():
            
            data = q.get()
            
            if data[0][0] == 'PUT CLONE SERVER SOCKET':
                
                SOCKETBANK.append(data)
                
        for sb in SOCKETBANK:
            
            if not uq_client_send.empty():
                
                unique_data = uq_client_send.get()
                
                if unique_data[0][0] == 'GET ALL THE ONLINE USERS':
                    
                    name_list = []
                    
                    uq_client_send = sb[3][0]
                    
                    uq_client_recv = sb[4][0]
                    
                    for i in SOCKETBANK:
                        
                        name = i[1][0]
                        
                        name_list.append(name)
                    
                    uq_client_recv.put(name_list)
                    
                if unique_data[0][0] == 'GET FRIEND':
                    
                    socket_list = []
                    
                    friends_list = unique_data[1]
                    
                    for num in friends_list:
                        
                        array_friend = SOCKETBANK[num]
                        
                        f_socket = array_friend[2][0]
                        
                        socket_list.append(f_socket)
                        
                    uq_client_recv.put(socket_list)
