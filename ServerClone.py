#!/usr/bin/env python

from multiprocessing import Process, Queue
from multiprocessing.reduction import reduce_handle, rebuild_handle
import os
import socket
import time
import threading
import json

import Skateboard

def server(s_to_client, PASSWD, addrnew, process_id, client_pipe):

    print('ServerClone is ok.')

    data = s_to_client.recv(4096)

    SERVERINFO = '@Author: East Evil\nDefault Message From Server\nAnd You Can Change This Information By Youself'

    if data:

        #print data

        fuck_json_0 = json.dumps(['', "%s\nPlease enter passwd:" % SERVERINFO])

        s_to_client.sendall(fuck_json_0)

        data_0 = s_to_client.recv(4096)

        if data_0 == PASSWD:

            fuck_json_x = json.dumps(['', 'Permit access to login the server...\nInput a name for show you friends'])

            s_to_client.sendall(fuck_json_x)

            name_once = s_to_client.recv(4096)

            # message to staff [0] is command
            message_to_ec = ['UPDATE CLIENT SOCKET']

            # message to staff [1] is socket owner name
            message_to_ec.append(name_once)

            # message to staff [2] is socket
            s_to_client_reduction = reduce_handle(s_to_client.fileno())

            message_to_ec.append(s_to_client_reduction)

            # messaget to staff [3] is socket to recveive result from staff
            message_to_ec.append(process_id)

            #                        0        1     2              3
            # message send to ec [command, name, client_socket, process_id]
            # put into pipe
            client_pipe.send(message_to_ec)

            fuck_json = json.dumps(['Server Room', 'Ok, server get you name [%s]\nEnter the chat room...' % name_once])

            s_to_client.sendall(fuck_json)

            Skateboard.smooth(s_to_client, client_pipe, name_once, process_id)

        else:

            print 'Error password'

            log_file = open('temp/log-server.log')

            t_0 = time.localtime()

            now_time_0 = "%d-%d-%d-%d:%d:%d" % (t_0.tm_year, t_0.tm_mon, t_0.tm_mday, t_0.tm_hour, t_0.tm_min, t_0.tm_sec)

            log_file.writelines("ip:%s, port:%s failed to login at %s\n" % (addrnew[0], addrnew[1], now_time_0))

            log_file.close()

            err_json = json.dumps(['Error Password', 'Have no permission to enter the server'])

            s_to_client.sendall(err_json)

            self.CONNECTION_LIST.remove(s_to_client)

            s_to_client.close()
