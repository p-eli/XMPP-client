#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)
from threading import Lock
import sys

class log_file():
    def __init__(self):
        self.lock = Lock()
        self.log = None
        self.error = None

    def open_file(self): # otevreni souboru log.txt a error_log.txt
        try:
            self.log = open('log.txt','w')
            self.error = open('error_log.txt','w')
        except:
            raise ValueError from None

    def write_to_log(self,data): # zapsani do log.txt
        try:
            self.lock.acquire()
            self.log.write(data)
            self.lock.release()
        except:
            raise ValueError from None

    def write_to_error(self,data): # zapsani chyb do error_log.txt
        sys.stderr.write(data)
        try:
            self.error.write(data)
        except:
            raise ValueError from None

    def close_file(self): # uzavreni log souboru
        self.log.close()
        self.error.close()
