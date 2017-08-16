#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)
import re
import threading
from xml.etree.ElementTree import fromstring
import sys

BUFFER_RECIVED = 1024


class recived_data(): # prijimani dat ze serveru

    def __init__(self,soc,log):
        self.recived_data_text = []
        self.recived_data_parse = []
        self.run = True
        self.soc = soc
        self.lock = threading.Lock()
        self.lock1 = threading.Event()
        self.log = log

    def search_answer(self, search_text): # vyhledani zpravy od serveru
        for y in range(0,6):
            self.lock.acquire() # zajisteni vylucneho pristupu
            x = self.get_by_id(search_text) # vyhledavani podle ID
            if x != False:
                self.lock.release()
                return x
            x = self.get_parse_text(search_text) # vyhledavani podle tagu
            if x != False:
                self.lock.release()
                return x
            x = self.get_text(search_text) #vyhledavani podle shody
            if x != False:
                self.lock.release()
                return x
            self.lock.release()
            self.lock1.wait(10) # ceka 10 sekund pokud driv nedojde zprava
        self.log.write_to_error("communications error\n")
        raise ValueError

    def get_text(self,search_text): # vyhledava zpravu, ve zpravach nezpracovanych xml parserem
        for x in self.recived_data_text:
            if re.search(search_text, x):
                self.recived_data_text.remove(x)
                return x
        return False

    def get_parse_text(self,search_text): # vyhledava ve zpravach zpracovanych xml parserem podle tagu
        for x in self.recived_data_parse:
            if re.search(search_text, x.tag):
                self.recived_data_parse.remove(x)
                return x
        return False

    def get_by_id(self,search_text): # vyhledava ve zpravach zpracovanych xml parserem podle atributu id
        for x in self.recived_data_parse:
            if 'id' in x.attrib:
                if x.attrib['id'] == search_text:
                    self.recived_data_parse.remove(x)
                    return x
        return False

    def read_message(self): # vyhledava ve zpravach uzivatelske zpravy
        while True:
            msg = self.get_parse_text('message')

            if msg:
                if ('from' in msg.attrib) and (msg.find('body') != None):
                    sys.stdout.write("\nFROM: "+msg.attrib['from']+"\n\t MESSAGE: "+msg.find('body').text+"\n")
            self.lock1.wait() # ceka dokud neprijde zprava od serveru

    def clear(self): # smaze vsechny prijate zpravy
         self.lock.acquire()
         self.recived_data_text = []
         self.recived_data_parse = []
         self.lock.release()

    def start_recived_data(self): # vytvori vlakno pro prijem zprav
        self.process1 = threading.Thread(target=self.recived_data, args = ())
        self.process1.daemon = True
        self.process1.start()

    
    def stop_recived_data(self): # zastavi vlakno pro prijem zprav
        self.run = False
        self.clear()
        self.lock1.clear()

    def recived_data(self): #prijma data ze serveru
        try:
            while self.run:
                recived_data_text = self.soc.recv(BUFFER_RECIVED) # prijme zpravu ze severu
                while True:
                    if re.search('>\s*$',recived_data_text.decode('utf-8'),re.MULTILINE) != None or re.search('/>\s*$',recived_data_text.decode('utf-8'),re.MULTILINE) != None:
                        break
                    else:
                        recived_data_text += self.soc.recv(BUFFER_RECIVED)
                msg = recived_data_text.decode('utf-8')
                self.lock.acquire() # vylucny pristup
                self.set_text(msg)
                self.log.write_to_log(msg) # zapis do log.txt
                self.lock.release()
                self.lock1.set() # uvolni zamky
                self.lock1.clear()
        except:
          return False;

    def set_text(self,msg): # zpracuje a ulozi prijate zpravy ze serveru
        try:
            self.recived_data_parse.append(fromstring(msg)) # zpracovani pomoci xml parseru
        except:
            self.recived_data_text.append(msg)