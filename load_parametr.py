#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)
import sys

class load_parametr(): # nacteni a zpracovani parametru

    def __init__(self,log):
        self.switchs = {'--server':None,'--register-user':[],'--log-user':None,'--show-contactlist':False,'--add-user':[],'--message':[],'--user':[],'--wait':None,'--interactive':False,'--help':False}
        self.possible_switchs = ['-s','--server','-r','--register-user','-l','--log-user','-c','--show-contactlist','-a','--add-user','-m','--message','-u','--user','-w','--wait','-i','--interactive','-h']
        self.log = log
        self.arguments = sys.argv
        self.argument_count = len(self.arguments)

    def get_parametr_count(self): # vraci pocet parametru
        return  self.argument_count

    def get_value(self, value): # vraci hodnotu argumentu
        return self.switchs[value]

    def parametr_procces(self): # zpracovani parametru
        x = 1
        while x < self.argument_count:
            if self.arguments[x] == '-s' or self.arguments[x] == '--server':
                x += 1
                self.parametr_none('--server',x)
            elif self.arguments[x] == '-r' or self.arguments[x] == '--register-user':
                x += 1
                self.parametr_arry('--register-user',x)
            elif self.arguments[x] == '-l' or self.arguments[x] == '--log-user':
                x += 1
                self.parametr_none('--log-user',x)
            elif self.arguments[x] == '-c' or self.arguments[x] == '--show-contactlist':
                self.parametr_bool('--show-contactlist')
            elif self.arguments[x] == '-a' or self.arguments[x] == '--add-user':
                x += 1
                self.parametr_arry('--add-user',x)
            elif self.arguments[x] == '-m' or self.arguments[x] == '--message':
                x += 1
                self.parametr_arry('--message',x)
            elif self.arguments[x] == '-u' or self.arguments[x] == '--user':
                x += 1
                self.parametr_arry('--user',x)
            elif self.arguments[x] == '-w' or self.arguments[x] == '--wait':
                x += 1
                self.parametr_none('--wait',x)
            elif self.arguments[x] == '-i' or self.arguments[x] == '--interactive':
                self.parametr_bool('--interactive')
            elif self.arguments[x] == '-h' or self.arguments[x] == '--help':
                self.parametr_bool('--help')
            else:
                self.log.write_to_error('unknown parametr\n')
                raise ValueError
            x += 1

    def parametr_bool(self,switch_value): # zpracovani paramatru ktere bud jsou nebo nejsou nastaveny
        if not self.switchs[switch_value] :
            self.switchs[switch_value] = True
        else:
            self.log.write_to_error('redefinicion parametr\n')

    def parametr_arry(self,switch_value,x): # zpracovani parametru, ktere muzou byt redefinovane
        if x < self.argument_count and not self.arguments[x] in self.possible_switchs:
            self.switchs[switch_value].append(self.arguments[x])
        else:
            self.log.write_to_error('bad parametr value\n')
            raise ValueError
    
    def parametr_none(self,switch_value,x): # zpracovani parametru ktere nemuzou byt redefinovane
        if self.switchs[switch_value] == None:
            if x < self.argument_count and not self.arguments[x] in self.possible_switchs:
                self.switchs[switch_value] = self.arguments[x]
            else:
                self.log.write_to_error('bad parametr value\n')
                raise ValueError
        else:
            self.log.write_to_error('redefinicion parametr\n')
            raise ValueError
