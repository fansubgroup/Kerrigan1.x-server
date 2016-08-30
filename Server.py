#!/usr/bin/env python

import socket
import os
import sys
import select
import time
from multiprocessing import Process, Queue

import ServerClone
import SocketBank

class ServerLoop:
    
    def __init__(self, host_ip, port, passwd):
        
        self.HOST_IP = host_ip
        
        self.PORT = port
        
        self.MAXLISTEN = 10
        
        self.PASSWD = passwd
        
        
        
    def super_server(self):
        
        q = Queue()
        
        CONNECTION_LIST = []
        
        server_socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_socks.bind((self.HOST_IP, self.PORT))
        
        server_socks.listen(self.MAXLISTEN)
        
        bank = Process(target = SocketBank.boss, args = (q,))
        
        bank.daemon = True
        
        bank.start()
        
        print "Server start at %s:%d..." % (self.HOST_IP, self.PORT)
        
        CONNECTION_LIST.append(server_socks)
        
        log_file = open('temp/Log-server.log', 'a')
        
        while True:
            
            #Get the list sockets which are ready to be read through select
            reads, writes, errors = select.select(CONNECTION_LIST, [], [])
            
            for s in reads:
                
                #New connection
                if s == server_socks:
                    
                    socknew, addrnew = server_socks.accept()
                    
                    CONNECTION_LIST.append(socknew)
                    
                    t = time.localtime()
                    
                    now_time = "%d-%d-%d-%d:%d:%d"  % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
                    
                    log_file.writelines("ip:%s, port:%s want to connected at %s\n" % (addrnew[0], addrnew[1], now_time))
                    
                else:
                    
                    transfer_trouble = Process(target = ServerClone.server, args = (s, q, self.PASSWD, addrnew))
                    
                    transfer_trouble.daemon = True
                    
                    transfer_trouble.start()
                    
                    CONNECTION_LIST.remove(s)


def main():
    
    chat_init = ServerLoop('127.0.0.1', 8001, '11')
    chat_init.super_server()
    
if __name__ == "__main__":
    
    main()
