#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)
import connect_server
import login_user
import new_user
import recived_data
import threading
from time import sleep
import re
import sys

class init_service(): # poskytuje univerzalni rozhrani

    def __init__(self,log):
        self.server = None
        self.user = None
        self.recived_dat = None
        self.log = log

    def is_init_server(self): # vraci jestli je server inicializovan
        if self.server == None:
            return False
        return True
    
    def is_init_user(self): # vraci jestli je prihlasen uzivatel
        if self.user == None:
            return False
        return True

    def init_server_data(self,server): #inicializuje data serveru, nastavi jmeno a port
        self.server = connect_server.connect_server(self.log)
        self.server.set_name_port(server)

    def init_server(self): #pripojeni k severu
        self.server.create_socket()
        self.recived_dat = recived_data.recived_data(self.server.get_socket(),self.log)
        self.recived_dat.start_recived_data()
        self.server.willcome(self.recived_dat)

    def init_close_sever(self): # uzavre socket
        self.recived_dat.stop_recived_data()
        self.server.close_socket()

    def init_register_user(self,register_user): # registrace uzivatele
        try:
            self.init_server()
        except:
            return False
        try:
            for x in register_user:
                self.user = new_user.new_user(self.log)
                self.user.register_new_user(self.server.get_socket(),self.recived_dat,x)
            return True
        except ValueError:
            return False
        finally:
            self.init_close_sever()
    def init_log_user(self,user): # prihlaseni uzivatele
        self.init_server()
        try:
            self.user = login_user.log_user(user,self.server.get_socket(),self.recived_dat,self.log)
            self.user.login()
        except ValueError:
            self.init_close_sever()
            self.user == None
            raise

    def init_show_contactlist(self): # zobrazeni listu kontaktu
        if self.user != None:
            try:
                self.user.show_contactlist(self.recived_dat)
                return True
            except ValueError:
                self.log.write_to_error('show contact list failed\n')
                return False
        else:
            self.log.write_to_error('show contact list failed,please login\n')
            return False

    def init_add_user(self,add_user): # pridani uzivatele do kontaktu listu
        if self.user != None:
            for x in add_user:
                self.user.add_user(x,self.recived_dat)
        else:
            self.log.write_to_error("add user failed, please login\n")
            raise ValueError

    def init_send_message(self,message,to): # odeslani zpavy
        if self.user != None:
            if len(message) == len(to):
                for x in range(len(message)):
                    try:

                        self.user.send_message(self.spec_char_sub(message[x]),to[x])
                    except ValueError:
                        self.log.write_to_error("send message failed\n")
                        return False
                return True
            else:
                self.log.write_to_error("send message failed, number of messages does not match the number of recipient \n")
                return False
        else:
            self.log.write_to_error("send message failed, please login \n")
            return False

    def spec_char_sub(self,mes): # nahrazovani specialnich znku ve zprave
        mes = re.sub('&','&amp;',mes)
        mes = re.sub('<','&lt;',mes)
        mes = re.sub('>','&gt;',mes)
        mes = re.sub('"','&quot;',mes)
        mes = re.sub("'",'&apos;',mes)
        return mes

    def init_wait(self,time): # inicializuje provedni parametru --wait
        if self.user != None:
            self.init_recived()
            sleep(int(time))
        else:
            self.log.write_to_error("wait failed, please login\n")
    
    def init_recived(self): # zahaji prijem zprav ze serveru
        process1 = threading.Thread(target=self.recived_dat.read_message, args = ())
        process1.daemon = True
        process1.start()

    def init_log_out(self): # odhlasi uzivatele
        try:
            self.user.log_out()
            self.recived_dat.stop_recived_data()
            self.recived_dat.clear()
            self.user = None
            self.init_close_sever()
            return True
        except ValueError:
            return False

    def init_help(self): # zobrazi napovedu
        sys.stdout.write("Umožňuje vytvořit nový uživatelský účet nebo se připojit k stávajícímu účtu. Po přihlášení je možno přijímat a odesílat zprávy, přidávat a zobrazovat kontakty v listu kontaktů. Prováděné činnosti je možno zadat pomocí parametrů při spuštění aplikace, v interaktivním módu, nebo kombinací zadání pomocí parametrů a interaktivním módem. Aplikace umožňuje redefinici některých parametrů. \n\n Seznam parametru: \n\t -s, --server server_name [:port] - jméno portu a číslo serveru \n\t -r, --register-user username:password - nové uživatelské jméno a heslo (možná redefinice parametru) \n\t -l, --log-user username:password} - uživatelské jméno a heslo pro přihlášení \n\t -c, --show-contactlist - zobrazí list kontaktů \n\t -a, --add-user JID - přidá uživatele do listu kontaktů (možná redefinice parametru) \n\t -m, --message message - text zasílané zprávy(možná redefinice parametru v závislosti na --user) \n\t -u, --user JID - příjemce zasílané zprávy (možná redefinice parametru v závislosti na --message) \n\t -w, --wait ss - počet sekund, jak dlouho se bude čekat na příchozí zprávy \n\t -i, --interactive - interaktivní mód \n\t -h, --help - vypíše nápovědu  \n")



