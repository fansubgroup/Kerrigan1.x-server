#!/usr/bin/env python

import socket
from multiprocessing.reduction import reduce_handle, rebuild_handle


def exchangecenterstaff(server_pipe_update, share_list, to_tegaphone_list):

    # waitting for recv the message from pipe

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

        share_list.append(share_list_one)

    if server_recv[0] == 'MESSAGE':
        #               0        1
        # message like [command, want_to_say, name]

        name_say_list = []

        name_say_list.append(server_recv[2])

        name_say_list.append(server_recv[1])

        to_megaphone_list.append(name_say_list)



def megaphone(share_list, to_megaphone_list):

    # pass the message between the client

    while True:

        if len(to_megaphone_list):

            for each_one in to_megaphone_list:
                # each_one like [name, want_to_say]

                for all_user in share_list:
                    # like [name, socket, friends_list]

                    if all_user[0] == each_one[0]:

                        fl = all_user[2]

                        if len(fl):

                            send_message(fl, each_one[0], each_one[1])

                        else:

                            else_message = [[each_one[0]], 'server', 'You not have friends yet, add a friends with ## first']

                            send_message(else_message)



def send_message(friends_list, name, string):

    # send the message to allow friends

    all_friends = []

    for f in friends_list:

        for a in share_list:
            # like [name, socket, friends_list]

            if a[0] == f:

                all_friends.append(a[1])

    for s in all_friends:

        s.sendall(['From %s' % name, string])
