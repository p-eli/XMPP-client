#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)

class send_data(): # odesilani dat na server

    def __init__(self,soc,log):
        self.soc = soc
        self.log = log

    def send_data(self,data):
        try: # pokusi se odeslat data
            self.soc.send(bytes(data, 'UTF-8'))
            self.log.write_to_log(data)
        except: # data se nepodarilo odeslat
            self.log.write_to_error('data send error\n')
            raise ValueError from None
