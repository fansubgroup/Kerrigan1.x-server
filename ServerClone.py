#!/usr/bin/env python

from multiprocessing import Process, Queue
from multiprocessing.reduction import reduce_handle, rebuild_handle
import os
import socket
import time

import Skateboard

def server(s_to_client, q_to_staff, PASSWD, addrnew, process_id):
    
    data = s_to_client.recv(4096)
    
    SERVERINFO = '@Author: East Evil\nDefault Message From Server\nAnd You Can Change This Information By Youself'
    
    staff_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    staff_socket.bind('temp/sock/socket_%d' % process_id)
    
    if data:
        
        #print data
        
        s_to_client.sendall("%s\nPlease enter passwd:" % SERVERINFO)
        
        data_0 = s_to_client.recv(4096)
        
        if data_0 == PASSWD:
            
            s_to_client.sendall('Permit access to login the server...\nInput a name for show you friends')
            
            name_once = s_to_client.recv(4096)
            
            # message to staff [0][0] is command
            message_to_staff = [['UPDATE CLIENT SOCKET']]
            
            # message to staff [1][0] is socket owner name
            name_list = []
            
            name_list.append(name_once)
            
            message_to_staff.append(name_list)
            
            # message to staff [2][0] is socket
            sock_list = []
            
            s_to_client_reduction = reduce_handle(s_to_client.fileno())
            
            sock_list.append(s_to_client_reduction)
            
            message_to_staff.append(sock_list)
            
            # messaget to staff [3][0] is socket to recveive result from staff
            result_list = []
            
            result_list.append(process_id)
            
            #                          0          1       2                3
            # message send to staff [[command], [name], [client_socket], [process_id]]
            message_to_staff.append(result_list)
            
            # put into queue
            q_to_staff.put(message_to_staff)
            
            s_to_client.sendall('Ok, server get you name [%s]\nEnter the chat room...' % name_once)
            
            Skateboard.smooth(s_to_client, q_to_staff, name_once, process_id, staff_socket)
            
        else:
            
            print 'Error password'
            
            t_0 = time.localtime()
            
            now_time_0 = "%d-%d-%d-%d:%d:%d" % (t_0.tm_year, t_0.tm_mon, t_0.tm_mday, t_0.tm_hour, t_0.tm_min, t_0.tm_sec)
            
            log_file.writelines("ip:%s, port:%s failed to login at %s\n" % (addrnew[0], addrnew[1], now_time_0))
            
            s_to_client.sendall("Have no permission to enter the server")
            
            self.CONNECTION_LIST.remove(s_to_client)
            
            s_to_client.close()
            
