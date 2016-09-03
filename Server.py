#!/usr/bin/env python

import socket
import os
import sys
import select
import time
import shutil
from multiprocessing import Process, Queue

import ServerClone
import SocketBank
import StaffBank

class ServerLoop:
    
    def __init__(self, host_ip, port, passwd):
        
        self.HOST_IP = host_ip
        
        self.PORT = port
        
        self.MAXLISTEN = 10
        
        self.PASSWD = passwd
        
        self.PROCESS_ID = 1
        
        
        
    def remove_sock_temp(self):
        
        if os.path.isdir('temp/sock'):
            
            shutil.rmtree('temp/sock')
            
        os.mkdir('temp/sock')
        
        
        
    def super_server(self):
        
        self.remove_sock_temp()
        
        q_to_staff = Queue()
        
        q_to_bank = Queue()
        
        q_back_bank = Queue()
        
        CONNECTION_LIST = []
        
        server_socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_socks.bind((self.HOST_IP, self.PORT))
        
        server_socks.listen(self.MAXLISTEN)
        
        # create a process for saving socket named socket bank
        bank = Process(target = SocketBank.boss, args = (q_to_bank, q_back_bank))
        
        bank.daemon = True
        
        bank.start()
        
        # create a process for deal with command from Skateboard
        bank_staff = Process(target = StaffBank.staff, args = (q_to_bank, q_back_bank, q_to_staff))
        
        bank_staff.daemon = True
        
        bank_staff.start()
        
        print "Server start at %s:%d..." % (self.HOST_IP, self.PORT)
        
        CONNECTION_LIST.append(server_socks)
        
        log_file = open('temp/Log-server.log', 'a')
        
        while True:
            
            # get the list sockets which are ready to be read through select
            reads, writes, errors = select.select(CONNECTION_LIST, [], [])
            
            for s in reads:
                
                # new connection
                if s == server_socks:
                    
                    socknew, addrnew = server_socks.accept()
                    
                    CONNECTION_LIST.append(socknew)
                    
                    t = time.localtime()
                    
                    now_time = "%d-%d-%d-%d:%d:%d"  % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
                    
                    log_file.writelines("ip:%s, port:%s want to connected at %s\n" % (addrnew[0], addrnew[1], now_time))
                    
                else:
                    
                    transfer_trouble = Process(target = ServerClone.server, args = (s, q_to_staff, self.PASSWD, addrnew, self.PROCESS_ID))
                    
                    transfer_trouble.daemon = True
                    
                    transfer_trouble.start()
                    
                    CONNECTION_LIST.remove(s)
                    
                    self.PROCESS_ID += 1


def main():
    
    chat_init = ServerLoop('127.0.0.1', 8001, '11')
    chat_init.super_server()
    
if __name__ == "__main__":
    
    main()
