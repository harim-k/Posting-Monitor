import requests
import json
import os
import datetime
from time import sleep

from kakao_send_msg import read_data
# 현재 사용자에게 REST API가 포함된 링크를 보내고, 거기서 사용자는 메시지 수신알림을 accept한상태
# 그 과정에서 data의 code를 추출할 수 있다. client_id는 develops.kakao에서 받아온 REST API ID
#client_id = '7412c5bbc84770efd9fb12162c229f9f'#project 2
client_id = '85ebef3a67f11e7f490a4fe518acd72b' # new

local = True
port = '10080'
def getLocal():
    return local
def getClientId():
    return client_id
def getPort():
    return port


def saveToken(get_txt):
    if local:
        ip = "localhost"
    else:
        ip = requests.get("https://api.ipify.org").text
        with open("ip.txt","w") as fp:
            fp.write(ip)
    code = extractCode(get_txt)
    #print('Creating token requests have been received.')
    #print('Code\n'+code)
    url = "https://kauth.kakao.com/oauth/token"
    data = {"grant_type": "authorization_code",

            #"client_id": "7412c5bbc84770efd9fb12162c229f9f",
            "client_id": client_id,
            "redirect_uri": "http://"+ip+":"+port, "code": code}
    # 이러한 정보를 담은 data를 아래 url로 request를 보내면, user token을 받아올 수 있다.
    # user token 은 제한 시간이 있는 것으로 추정되며, user token을 이용하여 message를 발행할 수 있다.
    # 다음과정은 kakao_send_msg.py에서 실행
    response = requests.post(url, data=data)
    uid =-1
    tokens = response.json()
    nickName2, uid = getInfo(response.text)

    #print('Token info\n'+str(tokens))
    if 'error' not in tokens.keys():
        #kakao2(tokens['access_token'])
        #time1 = str(datetime.datetime.now()).split('.')[0].replace(' ','_').replace('-','').replace(':','')
        if not os.path.isdir('./tokens'):
            os.mkdir('tokens')
        #name =  "./tokens/"+ time1[2:]+'.json'
        name =  "./tokens/"+ getTimeName()
        #print()
        with open(name,"w") as fp:
            json.dump(tokens,fp)
    res = '토큰이 생성됨\n이 이름을 kakao_send_msg.py의 sendMsg함수의 첫번째 인자로 넣고, 두번째 인자에 메시지 넣고 sendMsg함수실행\n'+name[2+7:]
    print(res)
    return name[2+7:]
def getTimeName():
    time1 = str(datetime.datetime.now()).split('.')[0].replace(' ', '_').replace('-', '').replace(':', '')
    name = time1[2:]+'.json'
    return name
def getDate(time_name):
    time_str = time_name.replace('.json','').replace('_','')
    year = int('20'+time_str[:2])
    month = int(time_str[2:4])
    day = int(time_str[4:6])
    hour = int(time_str[6:8])
    seconds = int(time_str[8:10])
    mili = int(time_str[10:])
    date = datetime.datetime(year,month,day,hour,seconds,mili)
    return date
def hour6over(time_name):
    old = getDate(time_name)
    new = getDate(getTimeName())
    #print((new-old).seconds)
    return (new-old).seconds > 21590
def extractToken(txt):
    data = txt
    aim = 'access_token:\": '
    init = data.find(aim) + len(aim)+2 # 모르겠다 2는
    end = data[init:].find(',')
    res = data[init:init + end].replace("\"", '').replace(',', '')
    #print(res)
    return res
def getInfo(text):
    access_token = extractToken(text)
    #print('hi2')
    #access_token=(read_data(tokenName))
    headers = {"Authorization": "Bearer " + access_token}
    response =requests.get("https://kapi.kakao.com/v2/user/me", headers = headers )
    #print('hi')
    #print(response.text)
    if 'kakao_account' in response.json().keys():
        res = response.json()['kakao_account']['profile']['nickname']
        res2 = response.json()['id']
    else:
        res ='err'
    return res, res2

def extractCode(get_txt):
    flag=0
    init =-1
    get_txt = str(get_txt)
    #print(get_txt)
    for idx, c in enumerate(get_txt):
        if c=='?' and idx+85+5<len(get_txt[idx:]) and get_txt[idx:idx+6] == '?code=':
            init = idx+6
            flag+=1
            break
    if init==-1:
        #print('extract_err_1')
        exit(0)
    for idx, c in enumerate(get_txt[init:]):
        if c==' ':
            end = idx+init
            flag+=1
            break
    if flag!=2:
        print('extract_err_2')
        exit(0)
    res = get_txt[init:end + 1]
    return res

def refrigerator(): # 21599초(6시간)마다 만료, (21599-600)(5시간 50분)마다 갱신
    #mutex.acquire()
    data ={}
    if not os.path.isdir('tokens'):
        os.mkdir('tokens')
    file_list = os.listdir('tokens')
    file_list.sort()
    if len(file_list) >0:
        for idx, f in enumerate(file_list):
            if hour6over(f):
                os.remove(f)
                continue
            data['client_id'] = client_id
            data['refresh_token'] = read_data(f,True)
            data['grant_type'] = 'refresh_token'
            response = requests.post("https://kauth.kakao.com/oauth/token", data=data)
            txt = response.text
            new = extractToken(txt)
            with open('./tokens/'+f,"r") as fp:
                old_file = fp.read()
                old = extractToken(old_file)
                old_file = old_file.replace(old,new)
                #print(old_file)
            with open('./tokens/'+f,"w") as fp:
                fp.write(old_file)
            #print(os.listdir())
            os.chdir('./tokens')
            #print(os.listdir())
            os.rename(f,getTimeName())
            os.chdir('../')
            #print(os.listdir())
            # print(response)
            # print(str(idx)+": "+str(f) +" "+txt)

    #mutex.release()
#'{"access_token":"BCbuRtz-0eCK-h7agdCGfBd03CO0rfp3i9aA0wo9dNsAAAF2VnrFcQ",
# "token_type":"bearer","expires_in":21599}'
