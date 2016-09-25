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
                "a + <Friend Name> - Add <Friend Name> in you friend list\n"
                "c + <Friend Name> - Chat with <Friend Name>\n"
                "q - Quit menu\n"
                "Q - Quit Chat")

    while True:

        reads, writes, errors = select.select(ONE_LIST, [], [])

        for sock in reads:

            data = sock.recv(4096)

            print data

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

                        ec_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

                        ec_socket.bind('temp/sock/sk-%d.sock' % process_id)

                        ec_socket.listen(MAX_LISTEN)

                        cons, _ = ec_socket.accept()

                        online_user_json = cons.recv(4096)

                        ec_socket.close()

                        cons.close()

                        online_user = json.loads(online_user_json)

                        s_once = ''

                        num_key = 1

                        for i in online_user:

                            s_once = s_once + '%d - %s\n' % (num_key, i)

                            num_key += 1

                        string_1 = "Add friend like 'a + Jack, Piter'\nq - quit"

                        user_json = json.dumps(['Friends list', s_once + string_1])

                        sock.sendall(user_json)

                        friends_key = sock.recv(4096)

                        print friends_key

                        if friends_key == 'q':
                            # quit the Menu

                            qqq_json = json.dumps('', 'Quiting...')

                            sock.sendall(qqq_json)

                            baby = False

                        elif friends_key == '##':
                            # Chat Menu again

                            t_json = json.dumps(['', 'Please quit the menu first, now quiting friends list...'])

                            sock.sendall(t_json)

                        elif friends_key[0:3] == 'a +':
                            # get the friend's socket friends_key like 'Jack, Piter'

                            print 'This is a +'

                            friends_list_old = friends_key[4:].split(',')

                            friends_list_new = []

                            for st in friends_list_old:

                                st.lstrip()

                                st.rstrip()

                                friends_list_new.append(st)

                            print 'friends_list_new', friends_list_new

                            get_list = ['ADD FRIEND']

                            get_list.append(name)

                            get_list.append(friends_list_new)

                            get_list.append(process_id)

                            # message like ['ADD FRIEND', self_name, friend_list, process_id]
                            pipe.send(get_list)

                            ec_add_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

                            ec_add_socket.bind('temp/sock/add-%d.sock' % process_id)

                            ec_add_socket.listen(MAX_LISTEN)

                            gfs, _ = ec_add_socket.accept()

                            query_json = gfs.recv(4096)

                            print 'query_json', query_json

                            ec_add_socket.close()

                            gfs.close()

                            sock.send(query_json)

                    elif user_choice == 'q':

                        qq_json = json.dumps(['', 'Quiting...'])

                        sock.sendall(qq_json)

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
