#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)
import re
import send_data

class new_user(): # registrace noveho uzivatele
    def __init__(self,log):
        self.log = log

    def set_username(self,data): #parsovani uzivatelskeho jmeno
        if re.search('^[^:]+:[^:]+$',data):
            return re.sub(':.*','',data)
        else:
            self.log.write_to_error("bad value, please check username and password \n")
            raise ValueError
             
    def set_password(self,data): # parsovani hesla
        if re.search('^[^:]+:[^:]+$',data):
            return re.sub('[^:]*:','',data)
        else:
            self.log.write_to_error("bad value, please check username and password \n")
            raise ValueError

    def register_new_user(self,soc,recived,data): # zaslani pozadavku na sever
        message = send_data.send_data(soc,self.log)
        message.send_data("<iq type='get' id='register'><query xmlns='jabber:iq:register'/></iq>")
        recived.search_answer('register')
        message.send_data("<iq type='set' id='register_new_user'><query xmlns='jabber:iq:register'><username>"+self.set_username(data)+"</username><password>"+self.set_password(data)+"</password></query></iq>")
        if recived.search_answer('register_new_user').attrib['type'] == "error":
            self.log.write_to_error("register new user error, please try other username\n")
            raise ValueError
