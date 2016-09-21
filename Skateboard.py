#!/usr/bin/env python

import os
import socket
import select
import json
from multiprocessing.reduction import rebuild_handle

def smooth(s_to_client, pipe, name, process_id):
    
    MAX_LISTEN = 1
    
    ONE_LIST = []
    
    ONE_LIST.append(s_to_client)
    
    ChatMenu = ("f - Find friend in this server\n"
                "c <somebody name> - Chat with <somebody name>\n"
                "q - Quit menu\n"
                "Q - Quit Chat")

    ec_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    ec_socket.bind('temp/sock/sk-%d.sock' % process_id)

    while True:
    
        reads, writes, errors = select.select(ONE_LIST, [], [])
        
        for sock in reads:
            
            data = sock.recv(4096)
            
            if len(data):
                
                if data != '##':
                    
                    send_to_ec_message = ['MESSAGE']

                    send_to_ec_message.append(data)

                    send_to_ec_message.append(name)

                    pipe.send(send_to_ec_message)

                elif data == '##':

                    fuck_json_1 = json.dumps(['Chat Menu', ChatMenu])

                    sock.sendall(fuck_json_1)

                    #print 'sock'

                    user_choice = sock.recv(4096)

                    if user_choice == 'f':

                        find_list = ['GET ALL THE ONLINE USERS']

                        find_list.append(process_id)

                        # message like ['GET ALL THE ONLINE USERS', process_id]
                        pipe.send(find_list)

                        ec_socket.listen(MAX_LISTEN)

                        cons, _ = ec_socket.accept()

                        online_user_json = cons.recv(4096)

                        online_user = json.loads(online_user_json)

                        s_once = ''

                        num_key = 1

                        for i in online_user:

                            s_once = s_once + '%d - %s\n' % (num_key, i[0])

                            num_key += 1

                        string_1 = "Enter your friends name\nLike 'Jack, Piter'\nq - quit"

                        user_json = json.dumps(['Friends list', s_once + string_1])

                        sock.sendall(user_json)

                        friends_key = sock.recv(4096)

                        if friends_key == 'q':
                            # quit the Menu

                            qqq_json = json.dumps('', 'Quiting...')

                            sock.sendall(qqq_json)

                            baby = False

                        elif friends_key == '##':
                            # Chat Menu again

                            t_json = json.dumps(['', 'Please quit the menu first, now quiting friends list...'])

                            sock.sendall(t_json)

                        else:

                            # get the friend's socket friends_key like 'Jack, Piter'
                            friends_list = friends_key.split(',')

                            get_list = ['GET FRIEND']

                            get_list.append(process_id)

                            get_list.append(friends_list)

                            # message like ['GET FRIEND', process_id, friend_list]
                            pipe.send(get_list)

                            ec_socket.listen(MAX_LISTEN)

                            gfs,  = ec_socket.accept()

                            query_json = gfs.recv(4096)

                            query_result = json.loads(query_json)

                            # deal with the origin data

                            print len(query_result)

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

                        qq_json = json.dumps(['', 'Quiting...'])

                        sock.sendall(qq_json)

                        break

                    elif user_choice == 'Q':

                        q_json = json.dumps(['Quiting'], 'Thank you for using')

                        sock.sendall(q_json)

                        Quit_list = ['REMOVE MY NAME']

                        Quit_list.append(name)

                        # Quit_list like ['REMOVE MY NAME', name]

                        pipe.send(Quit_list)

                        os._exit()

                    else:

                        escape_json = json.dumps(['', 'Enter q to escape the menu'])

                        sock.sendall(escape_json)
            else:

                fuck_error = json.dumps(['Error', 'No data'])

                sock.sendall(fuck_error)
