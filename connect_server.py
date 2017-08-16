#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)
import socket
import re
import send_data

class connect_server(): # pripojeni k serveru
    server = None
    port = None

    def __init__(self,log):
        self.log = log
        self.soc = None

    def set_name_port(self,name_port): # parsovani jmena portu serveru
        if re.search('^[^:]+:\d+$',name_port):
            self.server = re.sub(':.*','',name_port)
            self.port = int(re.sub('[^:]*:','',name_port))
        else:
            self.log.write_to_error("parameter --server error, bad value\n")
            raise ValueError

    def get_socket(self): #vraci socket
        return self.soc  

    def get_server_name(self): # vraci jmeno serveru
        return self.server

    def create_socket(self): # vytvari soket
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #vytvoreni schranky
        try:
            self.soc.settimeout(10)
            self.soc.connect((self.server, self.port)) # pripojeni k serveru
            self.soc.settimeout(None)
        except:
            self.log.write_to_error("create socket error\n")
            raise ValueError from None

    def close_socket(self): # uzavreni socketu
        try:
            self.soc.settimeout(2)
            self.soc.close()
        except:
            self.log.write_to_error("close socket error\n")
            raise ValueError from None

    def willcome(self,recived): #nastaveni streamu
        message = send_data.send_data(self.soc,self.log)
        message.send_data('<stream:stream xmlns:stream="http://etherx.jabber.org/streams" version="1.0" xmlns="jabber:client" to="'+self.server+'" xml:lang="en" xmlns:xml="http://www.w3.org/XML/1998/namespace">')