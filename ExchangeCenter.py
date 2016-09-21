#!/usr/bin/env python

import os
import socket
import json
from multiprocessing.reduction import reduce_handle, rebuild_handle


def exchangecenterstaff(server_pipe_update, user_list, to_tegaphone_list):

    # waitting for recv the message from pipe

    Skateboard_say = ("This is Customer Service Mr.Skateboard\n"
                      "You could use the ## to enter the <Chat Menu>\n"
                      "You ars talking with a Server Machine."
                      "Please search a friend")

    while True:

        server_recv = server_pipe_update.recv()

        if server_recv[0] == 'UPDATE CLIENT SOCKET':
            #               0        1     2              3
            # message like [command, name, client_socket, process_id]

            client_socket_h = server_recv[2]

            socket_fd = rebuild_handle(client_socket_h)

            client_socket = socket.fromfd(socket_fd, socket.AF_INET, socket.SOCK_STREAM)

            # share_list_one will like [name, socket, friends_list]

            friends_list = []

            share_list_one = []

            share_list_one.append(server_recv[1])

            share_list_one.append(client_socket)

            share_list_one.append(friends_list)

            user_list.append(share_list_one)

        if server_recv[0] == 'MESSAGE':
            #               0        1            2
            # message like [command, want_to_say, self_name]
            # append it in to_tegaphone_list

            name_say_list = []

            name_say_list.append(server_recv[2])

            name_say_list.append(server_recv[1])

            # to_tegaphone_list like [self_name, want_to_say]

            to_tegaphone_list.append(name_say_list)

        if server_recv[0] == 'REMOVE MY NAME':
            #
            # message like [command, name]
            # delete the item about the name in user_list
            # share list like [name, socket, friends_list]

            for x in user_list:

                if x[0] == server_recv[1]:

                    user_list.remove(x)

        if server_recv[0] == 'GET ALL THE ONLINE USERS':
            #
            # return the server online user name
            #                   0                           1
            # server_recv like ['GET ALL THE ONLINE USERS', process_id]
            # user_list like [name, socket, friends_list]

            all_user_list = []

            for aul in user_list:

                all_user_list.append(aul[0])

            aul_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

            aul_socket.connect('temp/sock/sk-%d.sock' % server_recv[1])

            all_user_json = json.dumps(all_user_list)

            print(all_user_list)

            aul_socket.send(all_user_json)



def megaphone(user_list, to_megaphone_list):

    # pass the message between the client
    #                         1          2
    # to_tegaphone_list like [self_name, want_to_say]

    while True:

        if len(to_megaphone_list):

            for each_one in to_megaphone_list:
                # each_one like [name, want_to_say]

                for all_user in user_list:
                    # like [name, socket, friends_list]

                    if all_user[0] == each_one[0]:

                        fl = all_user[2]

                        if len(fl):

                            send_message(fl, each_one[0], each_one[1])

                        else:

                            else_message = [[each_one[0]], 'server', 'You not have friends yet, add a friends with ## first']

                            send_message(else_message)

                to_megaphone_list.remove(each_one)



def send_message(friends_list, name, want_to_say):

    # send the message to allow friends

    all_friends = []

    for f in friends_list:

        for a in user_list:
            # like [name, socket, friends_list]

            if a[0] == f:

                all_friends.append(a[1])

    if len(all_friends):

        for s in all_friends:

            s.sendall(['From %s' % name, want_to_say])
