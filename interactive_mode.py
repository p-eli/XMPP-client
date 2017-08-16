#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)
import sys

class interactive_mode(): # interaktivni mod

    def __init__(self,init):
        self.parametrs = None
        self.init = init

    def run(self): # spusti interaktivni mod
        while True:
            if not self.init.is_init_user():
                if not self.reg_or_log():
                    break
            if not self.send_recived_message():
                break

    def reg_or_log(self): # registrace nebo prihlaseni uzivatele
        while True:
            msg = input("\nfor log user set 'log-user'\n for register new user set 'register-user' \n for exit set 'exit' \n Please enter command:  ")
            if msg == 'log-user':
                if self.log_user():
                    return True
            elif msg == 'register-user':
                self.register_new_user()
            elif msg == 'exit':
                return False
            else:
                sys.stdout.write("\nbad parametr, please try again or 'exit' for exit\n")

    def set_sever_name(self): # nastaveni serveru
        if not self.init.is_init_server():
            server  = input("Please enter server: ")
            port  = input("Please enter port: ")
            self.init.init_server_data(server+":"+port)
    
    def register_new_user(self): # registrace noveho uzivatele
        self.set_sever_name()
        user  = input("Please enter new username: ")
        password = input("Please enter new password: ")
        if self.init.init_register_user([user+":"+password]):
            sys.stdout.write("registracion new user succes\n")


    def log_user(self): # prihlaseni uzivatele
        self.set_sever_name()
        user  = input("Please enter username: ")
        password = input("Please enter password: ")
        try:
            self.init.init_log_user(user+":"+password)
            sys.stdout.write("user login succes\n")
            return True
        except ValueError:
            return False

    def send_recived_message(self): #interaktivni rezim po prihlaseni
        self.init.init_recived()
        while True:
            input_command  = input("Set command: ")
            if input_command == 'show-contactlist': # zobrazeni contact listu
                self.init.init_show_contactlist()
            elif input_command == 'add-user': # pridani uzivatele
                try:
                    self.init.init_add_user([input("Set JID: ")])
                    sys.stdout.write("user add\n")
                except ValueError:
                    None
            elif input_command == 'send-message': # odeslani zpravy
                to = [input("To: ")]
                message = [input("Message text: ")]
                if self.init.init_send_message(message,to):
                    sys.stdout.write("message send\n")
            elif input_command == 'log-out': # odhlaseni uzivatele
                if self.init.init_log_out():
                    sys.stdout.write("user logout\n")
                    return True
                else:
                    return False
            elif input_command == 'exit': # ukonceni aplikace
                self.init.init_log_out()
                return False
            elif input_command == 'help': # zorazeni napovedy
                sys.stdout.write("for show contact list set 'show-contactlist'\n for add contact set 'add-user' \n for send message set 'send-message' \n for log-out set 'log-out' \n for exit set 'exit' \n Please enter command:  ")
            else:
                sys.stdout.write("bad parametr, please try again or 'help' for help or 'exit' for exit")