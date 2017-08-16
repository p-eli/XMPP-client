#!/usr/bin/python3
#Autor: Jakub Pelikan (xpelik14)
import hashlib
import base64
import re
import send_data
import sys


class log_user(): # prihlaseni uzivatele, odesilani zpavy, zobrazovani a pridavani kontaktu do listu kontaktu

    def __init__(self,data,soc,recived,log):
        self.soc = soc
        self.set_username(data)
        self.log = log
        self.recived = recived
        self.message = send_data.send_data(self.soc,self.log)

    def set_username(self,data): # parsovani uzivatelskeho jmena a hesla
        if re.search('^[^:]+:[^:]+$',data):
            self.username = re.sub(':.*','',data)
            self.password = re.sub('[^:]*:','',data)
        else:
            self.log.write_to_error("bad parametr value, please check username and password \n")
            raise ValueError

    def login(self): # prihlaseni
        auth = self.recived.search_answer('mechanism')
        if "DIGEST-MD5" in auth: # autorizace pomoci DIGEST-MD5
            self.message.send_data(self.mp5())
        elif "PLAIN" in auth:   #autorizace pomoci PLAIN
            self.message.send_data(self.plain())

        if re.search('failure', self.recived.search_answer('succes|failure').tag) != None : #overeni ze se povedlo prihlasit
                self.log.write_to_error("login failed, please check username and password \n")
                raise ValueError
        self.message.send_data('<iq type="set" id="login"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"></bind></iq>')
        self.recived.search_answer('login')
        self.message.send_data('<presence><c xmlns="http://jabber.org/protocol/caps"/></presence>')
        self.recived.search_answer('presence')

    def log_out(self): #odhlaseni
        self.message.send_data('<presence xmlns="jabber:client" id="log_out" type="unavailable"><status>Logged out</status></presence>')
        if self.recived.search_answer('log_out').find('status').text != 'Logged out':
            self.log.write_to_error("log-out failed \n")
            raise ValueError

    def plain(self): # autorizace pomoci PLAIN
        log_data = "%s%s%s%s" % ("\x00",self.username,"\x00",self.password)
        log_data = log_data.encode('utf-8')
        log_encoded = base64.b64encode(log_data).decode('utf-8')
        msg = "<auth xmlns='urn:ietf:params:xml:ns:xmpp-sasl'mechanism='PLAIN'>"+log_encoded+"</auth>"
        return(msg)

    def message_decode(self,message): #dekodovani zpravy
        decoded = base64.b64decode(message)
        decoded = decoded.decode('utf-8')
        parsed = decoded.split(r',')
        return(parsed)

    def mp5(self): # autorizace pomoci DIGEST-MD5
        self.message.send_data('<auth xmlns="urn:ietf:params:xml:ns:xmpp-sasl"  mechanism="DIGEST-MD5"/>')
        mes = self.message_decode(self.recived.search_answer('challenge').text)
        if len(mes) == 5:
            realm = re.sub('realm="([^"]*)"','\\1',mes[0])
            nonce = re.sub('nonce="([^"]*)"','\\1',mes[1])
            qop = re.sub('qop="([^"]*)"','\\1',mes[2])
        else:
            self.log.write_to_error("error decoded md5 \n")
            raise ValueError
        cnonce = self.username + nonce
        digest_uri="xmpp/"+realm
        nc="00000001"

        X = "%s:%s:%s" % (self.username,realm,self.password)
        X = X.encode("ISO-8859-1")
        Y = hashlib.md5(X).digest()
        A1 = Y + str.encode(":") +str.encode(nonce)+ str.encode(":") +str.encode(cnonce)
        A2 = "AUTHENTICATE:"+digest_uri
        HA1 = hashlib.md5(A1).hexdigest()
        HA2 = hashlib.md5(A2.encode('utf-8')).hexdigest()
        KD = HA1+":"+nonce+":"+nc+":"+cnonce+":"+qop+":"+HA2
        Z = hashlib.md5(KD.encode('utf-8')).hexdigest()
        msg="username=\""+self.username+"\",realm=\""+realm+"\",nonce=\""+nonce+"\",cnonce=\""+cnonce+"\",nc=00000001,qop=auth,digest-uri=\""+digest_uri+"\",response="+Z+",charset=utf-8";
        encoded = base64.b64encode(msg.encode('utf-8'))
        msg = "<response xmlns=\"urn:ietf:params:xml:ns:xmpp-sasl\">"+encoded.decode('utf-8')+"</response>"
        return msg

    def show_contactlist(self,recived): # zobrazeni listu kontaktu
        self.message.send_data('<iq from="'+self.username+'" type="get" id="show_contactlist"><query xmlns="jabber:iq:roster"/></iq>')
        contact_list = self.recived.search_answer('show_contactlist')
        sys.stdout.write("\nContact list :\n")
        for child in contact_list:
            for child1 in child:
                if 'name' in child1.attrib:
                    sys.stdout.write('\t Name: '+child1.attrib['name']+'\n')


    def add_user(self,user_id,recived): # pridani uzivatele
        group = "General"
        self.message.send_data("<iq from='"+self.username+"' type='set' id='add_user'><query xmlns='jabber:iq:roster'><item jid='"+user_id+"' name='"+user_id+"'><group>"+group+"</group></item></query></iq>")
        self.recived.search_answer('add_user')

    def send_message(self,text,to): # odeslani zpavy
        self.message.send_data("<message to='"+to+"' from='"+self.username+"' type='chat' xml:lang='en'><body>"+text+"</body></message>")