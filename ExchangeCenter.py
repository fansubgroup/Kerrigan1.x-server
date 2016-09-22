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

            # user_list_one will like [name, socket, friends_list]

            friends_list = []

            user_list_one = []

            user_list_one.append(server_recv[1])

            user_list_one.append(client_socket)

            user_list_one.append(friends_list)

            user_list.append(user_list_one)

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

            # print(all_user_list)

            aul_socket.send(all_user_json)

            # print(all_user_json)

        if server_recv[0] == 'ADD FRIEND':
            #
            # send a invitation to friends
            # server_recv message like ['ADD FRIEND', name, friend_list]
            # user_list will like [name, socket, friends_list]

            for want_name in server_recv[2]:

                for user_each in user_list:

                    if want_name == user_each[0]:

                        every_socket = want_name[1]

                        every_json = json.dumps(['%s want to add you as friends[yes/no]' % server_recv[1], ''])

                        every_socket.send(every_json)

                        every_ack = every_socket.recv(1024)

                        if every_ack == 'y' or 'yes' or 'Yes' or 'YES' or 'YEs' or 'YeS' or 'yEs' or 'yES':

                            add_friends_list(server_recv[1], want_name, user_list)

                            add_friends_list(want_name, server_recv[1], user_list)



def add_friends_list(source_name, target_name, user_list):

    # add target_name in source_name friends_list

    for uu in user_list:
        # user_list will like [name, socket, friends_list]
        if uu[0] == source_name:

            uu[2].append(target_name)



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

                            send_message(fl, each_one[0], each_one[1], user_list)

                        else:

                            send_message([each_one[0]], 'server', 'You not have friends yet, add a friends with ## first', user_list)

                to_megaphone_list.remove(each_one)



def send_message(friends_list, name, want_to_say, user_list):

    # send the message to allow friends

    all_friends = []

    for f in friends_list:

        for a in user_list:
            # like [name, socket, friends_list]

            if a[0] == f:

                all_friends.append(a[1])

            elif a[0] == name:

                self_socket = a[1]

    if len(all_friends):

        for s in all_friends:

            jj_json = json.dumps(['From %s' % name, want_to_say])

            s.sendall(jj_json)

    self_json = json.dumps(['Check', 'Message arrived'])

    self_socket.sendall(self_json)
