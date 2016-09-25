#!/usr/bin/env python

import os
import socket
import json
from multiprocessing.reduction import reduce_handle, rebuild_handle


def exchangecenterstaff(server_pipe_update, RELATION_TABLE, to_megaphone_list):

    # waitting for recv the message from pipe

    print('ExchangeCenterStaff is ok.')

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

            print type(client_socket)

            # user_list_one will like [name, socket, chat_now_friend, long_time_friend]

            chat_now_friend = []

            long_time_friend = []

            user_list_one = []

            user_list_one.append(server_recv[1])

            user_list_one.append(client_socket)

            user_list_one.append(chat_now_friend)

            user_list_one.append(long_time_friend)

            RELATION_TABLE.append(user_list_one)

        if server_recv[0] == 'MESSAGE':
            #               0        1            2
            # message like [command, want_to_say, self_name]
            # append it in to_megaphone_list

            name_say_list = []

            name_say_list.append(server_recv[2])

            name_say_list.append(server_recv[1])

            # to_megaphone_list like [self_name, want_to_say]

            to_megaphone_list.append(name_say_list)

        if server_recv[0] == 'REMOVE MY NAME':
            #
            # message like [command, name]
            # delete the item about the name in RELATION_TABLE
            # share list like [name, socket, chat_now_friend, long_time_friend]

            for x in RELATION_TABLE:

                if x[0] == server_recv[1]:

                    RELATION_TABLE.remove(x)

        if server_recv[0] == 'GET ALL THE ONLINE USERS':
            #
            # return the server online user name
            #                   0                           1
            # server_recv like ['GET ALL THE ONLINE USERS', process_id]
            # RELATION_TABLE like [name, socket, chat_now_friend, long_time_friend]

            all_user_list = []

            for aul in RELATION_TABLE:

                all_user_list.append(aul[0])

            aul_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

            aul_socket.connect('temp/sock/sk-%d.sock' % server_recv[1])

            all_user_json = json.dumps(all_user_list)

            # print(all_user_list)

            aul_socket.send(all_user_json)

            aul_socket.close()

            # print(all_user_json)

        if server_recv[0] == 'ADD FRIEND':
            #
            # send a invitation to friends
            #                           0             1          2            3
            # server_recv message like ['ADD FRIEND', self_name, friend_list, process_id]
            # RELATION_TABLE will like [name, socket, chat_now_friend, long_time_friend]

            for want_friends in server_recv[2]:
                # server_recv is friend_list

                for user_each in RELATION_TABLE:

                    if want_friends == user_each[0]:
                        # this is the friend you want to talk
                        # RELATION_TABLE will like [name, socket, chat_now_friend, long_time_friend]

                        every_socket = user_each[1]

                        print type(every_socket)

                        every_json = json.dumps(['%s want to add you as friends' % server_recv[1], '[yes/no]'])

                        every_socket.send(every_json)

                        every_ack = every_socket.recv(1024)

                        if every_ack == 'y' or 'yes' or 'Yes' or 'YES' or 'YEs' or 'YeS' or 'yEs' or 'yES':

                            add_friends_list(server_recv[1], want_friends, RELATION_TABLE)

                            add_friends_list(want_friends, server_recv[1], RELATION_TABLE)

                            yes_json = json.dumps(['', 'Add friend success'])

                            add_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

                            add_socket.connect('temp/sock/add-%d.sock' % server_recv[3])

                            add_socket.send(yes_json)

                            print 'yes_json', yes_json

                            add_socket.close()

                        else:

                            no_json = json.dumps(['', 'The request is rejected'])

                            add_socket.send(no_json)

                            add_socket.close()



def add_friends_list(source_name, target_name, RELATION_TABLE):

    # add target_name in source_name self chat_now_friend and long_time_friend

    for r in RELATION_TABLE:
        #                           0     1       2                3
        # RELATION_TABLE will like [name, socket, chat_now_friend, long_time_friend]

        if r[0] == source_name:

            # r[0] is the RELATION_TABLE name, find the source_name in RELATION_TABLE
            # add the target_name in chat_now_friend and long_time_friend

            r[2].append(target_name)

            r[3].append(target_name)



def megaphone(RELATION_TABLE, to_megaphone_list):

    # pass the message to chat_now_friend
    #                         1          2
    # to_megaphone_list like [self_name, want_to_say]

    print('Megaphone is ok.')

    while True:

        if len(to_megaphone_list):

            for each_message in to_megaphone_list:
                # each_message like [self_name, want_to_say]

                for all_user in RELATION_TABLE:
                    # all_user like [name, socket, chat_now_friend, long_time_friend]

                    if all_user[0] == each_message[0]:
                        # all_user[0] is user name
                        # each_message[0] is sender name
                        # search RELATION_TABLE to find the sender name

                        # cnf is the chat_now_friend list
                        cnf = all_user[2]

                        if len(cnf):
                            # if the chat_now_friend list have friend now

                            for now_friend in chat_now_friend:
                                # get each want to send message friend

                                for all_user_0 in RELATION_TABLE:
                                    # all_user_0 like [name, socket, chat_now_friend, long_time_friend]

                                    if now_friend == all_user_0[0]:

                                        now_friend_sock = all_user_0[1]

                                        now_friend_json = json.dumps(['From %s' % each_message[0], each_message[1]])

                                        now_friend_sock.sendall(now_friend_json)

                        else:

                            have_no_friend = each_message[0]
                            # return a message to sender him don not have friend yet

                            for all_user_1 in RELATION_TABLE:
                                # all_user_1 like [name, socket, chat_now_friend, long_time_friend]

                                if have_no_friend == all_user_1[0]:

                                    no_friend_sock = all_user_1[1]

                                    no_friend_json = json.dumps(['Error', 'Please add a friend first'])

                to_megaphone_list.remove(each_message)

