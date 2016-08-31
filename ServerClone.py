#!/usr/bin/env python

from multiprocessing import Process, Queue
from multiprocessing.reduction import reduce_handle, rebuild_handle

import Skateboard

def server(s_to_client, q_to_bank, PASSWD, addrnew):
    
    data = s_to_client.recv(4096)
    
    SERVERINFO = '@Author: East Evil\nDefault Message From Server\nAnd You Can Change This Information By Youself'
    
    if data:
        
        #print data
        
        s_to_client.sendall("%s\nPlease enter passwd:" % SERVERINFO)
        
        data_0 = s_to_client.recv(4096)
        
        if data_0 == PASSWD:
            
            s_to_client.sendall('Permit access to login the server...\nInput a name for show you friends')
            
            name_once = s_to_client.recv(4096)
            
            #message to bank [0][0] is command
            message_to_bank = [['PUT CLONE SERVER SOCKET']]
            
            #message to bank [1][0] is sock owner name
            name_list = []
            
            name_list.append(name_once)
            
            message_to_bank.append(name_list)
            
            #message to bank [2][0] is socket
            sock_list = []
            
            sock_list.append(s_to_client)
            
            message_to_bank.append(sock_list)
            
            #messaget to bank [3][0] and [4][0] is CloneServer process to SocketBank unique Queue
            unique_list_client_send = []
            
            unique_list_client_recv = []
            
            unique_q_client_send = Queue()
            
            unique_q_client_recv = Queue()
            
            unique_list_client_send.append(unique_q_client_send)
            
            unique_list_client_recv.append(unique_q_client_recv)
            
            message_to_bank.append(unique_list_client_send)
            
            message_to_bank.append(unique_list_client_recv)
            
            #put into queue
            try:
                
                q_to_bank.put(s_client)
                
            except:
                
                print 'error'
            
            s_to_client.sendall('Ok, server get you name [%s]\nEnter the chat room...' % name_once)
            
            Skateboard.smooth(s_to_client, unique_q_client_send, unique_q_client_recv, name_once)
            
        else:
            
            print 'Error password'
            
            t_0 = time.localtime()
            
            now_time_0 = "%d-%d-%d-%d:%d:%d" % (t_0.tm_year, t_0.tm_mon, t_0.tm_mday, t_0.tm_hour, t_0.tm_min, t_0.tm_sec)
            
            log_file.writelines("ip:%s, port:%s failed to login at %s\n" % (addrnew[0], addrnew[1], now_time_0))
            
            s_to_client.sendall("Have no permission to enter the server")
            
            self.CONNECTION_LIST.remove(s_to_client)
            
            s_to_client.close()
            
