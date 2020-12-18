#-*- coding: utf-8 -*-
from socket import *
import os.path
import threading
from pathlib import Path
import webbrowser
from selenium import webdriver
from kakao_token import *

local = getLocal()
client_id = getClientId()
port = getPort()

def main():
    run_token_server()

def recieve(connectionSock, addr, serverSock):
    sum_content = b''
    while 1:
        content = connectionSock.recv(4096)
        sum_content += content
        if b'\r\n\r\n' in sum_content:
            break
    strA = saveToken(sum_content)
    #print(strA)
    make200(strA)
    data = sum_content.decode('utf-8').split()
    data2 = sum_content.decode('utf-8')
    snd_pkt = make_pkt(data, data2)
    connectionSock.send(snd_pkt)
    undo200(strA)
    # print('connection thread is end. :' +str(addr[0])+':'+str(addr[1]))
    connectionSock.close()
    #mutex.release()
    return strA
def run_token_server():
    refrigerator()
    if not os.path.isdir('tokens'):
        os.mkdir('tokens')
    file_list = os.listdir('tokens')
    file_list.sort()
    #print(hour6over(file_list[0]))
    #print(file_list)
    if len(file_list)>0 :
        return file_list[0]
    serverSock = socket()
    serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSock.bind(('', int(port)))
    serverSock.listen(1000)
    #driver = webdriver.Chrome('./chromedriver')
    link = setLink()
    #driver.get(link)
    webbrowser.open_new(link)
    print('Share this login link (Port forwarding is needed)\n' + link)
    print('Server has started.')
    # refresher = threading.Thread(target = refrigerator, args=( ))
    # refresher.start() # 토큰 refresh
    try:
        connectionSock, addr = serverSock.accept()
        tokenName = recieve(connectionSock, addr, serverSock)
    except OSError as e:
        print(e)
        # break
    serverSock.close()
    print('Program ended.')
    return tokenName

def make200(strA):
    #print(strA)
    #print('hi')
    if strA =='':
        return
    fileName = '200.html'
    with open(fileName,"r",encoding='UTF8') as fp:
        data =  fp.read().replace('<p></p>','<p>'+str(strA)+'</p>')
    with open(fileName,"w",encoding='UTF8') as fp:
        fp.write(data)
def undo200(strA):
    if strA=='':
        return
    fileName = '200.html'
    with open(fileName,"r",encoding='UTF8') as fp:
        data =  fp.read()
    data=data.replace(str(strA),'')
    with open(fileName,"w",encoding='UTF8') as fp:
        fp.write(data)
def isFile(strA):
    my_file = Path(strA)  # Path는 string을 return하는것 아님.window에서만 사용하능함.
    if my_file.is_file():
        return True
    else:
        return False
def make_pkt(data, data2):
    res_type = '200 OK'
    version = "HTTP/1.1"
    try:
        filename= '200.html'
        f1 = open(filename, "rb")
        file_data = b''
        while 1:
            content = f1.read(1024)
            if not content:
                break
            file_data += content
        f1.close()
    except OSError as e:
        print(e)
        res_type = '404 Not found'
        filename = '404.html'
    #print(filename)
    mod_time = os.path.getmtime(filename)
    mod_time = datetime.datetime.fromtimestamp(mod_time)
    server_name = "Network_assignment2_server"
    cur_time = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST')
    mod_time = mod_time.strftime('%a, %d %b %Y %H:%M:%S KST')
    data = '{0} {6}\r\n'
    data += 'Date: {1}\r\nServer: {2}\r\nLast-Modified: {3}\r\n'
    data += 'Accept-Ranges: bytes\r\nContent-Length: {4}\r\n'
    # data += 'Keep-Alive: timeout=10, max=100\r\nConnection: Keep-Alive\r\n'
    data += 'Content-type:{5}\r\n'
    #data += set_cookie(data2)
    data += '\r\n'
    data = data.format(version, cur_time, server_name, mod_time, str(len(file_data)), MIME(filename), res_type)
    #print(data)
    data = data.encode('utf-8')
    data += file_data
    return data
def MIME(filename): #노의미
    dictA=dict()
    dictA['aac']='audio/aac'
    dictA['avi']='video/x-msvideo'
    dictA['bin']='application/octet-stream'
    dictA['css']='text/css'
    dictA['csv']='text/csv'
    dictA['doc']='application/msword'
    dictA['gif']='image/gif'
    dictA['htm']='text/html; charset=ISO-8859-1'
    dictA['html']='text/html; charset=ISO-8859-1'
    dictA['ico']='image/x-icon'
    dictA['jpeg']='image/jpeg'
    dictA['jpg']='image/jpeg'
    dictA['json']='application/json'
    dictA['mpeg']='video/mpeg'
    dictA['png']='image/png'
    result= dictA.get(filename.split('.')[1])
    if result is None:
        result = 'application/octet-stream'
    return result
def setLink():
    if local:
        ip = "localhost"
        link = "https://kauth.kakao.com/oauth/authorize?client_id="
        link += client_id + "&response_type=code&redirect_uri=http://"
        link += ip + ":"+ port
        return link
    #if isFile('short_url.txt'):
     #   with open('short_url.txt',"r") as fp:
    #        link = fp.read()
    else:
        ip = requests.get("https://api.ipify.org").text
        link = "https://kauth.kakao.com/oauth/authorize?client_id="
        link += client_id + "&response_type=code&redirect_uri=http://"
        link += ip + ":" + port
        #link = shortUrl(link)
        #with open('short_url.txt',"w") as fp:
        #    fp.write(link)
    return link

if __name__ == "__main__":
    main()