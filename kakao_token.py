# 3 https://kauth.kakao.com/oauth/authorize?client_id=5cf279ec1ec559b2809d43df80623fad&response_type=code&redirect_uri=https://localhost.com
# 3 vkF923J8UG9uL_zjYpFUZtNvpuC6VaDGwEXI6-Fw-hRr_j3Ush6sDgAk2WjF_NK8IoVg5AorDKYAAAF2RquyNg
import requests
import json
# 현재 사용자에게 REST API가 포함된 링크를 보내고, 거기서 사용자는 메시지 수신알림을 accept한상태
# 그 과정에서 data의 code를 추출할 수 있다. client_id는 develops.kakao에서 받아온 REST API ID
import os
#from kakao2 import kakao2
import datetime

ip = requests.get("https://api.ipify.org").text
def saveToken(get_txt):
    code = extractCode(get_txt)
    print('Code: '+code)
    url = "https://kauth.kakao.com/oauth/token"
    data = {"grant_type": "authorization_code",
            "client_id": "7412c5bbc84770efd9fb12162c229f9f",
            "redirect_uri": "http://"+ip+":10080", "code": code}
    # 이러한 정보를 담은 data를 아래 url로 request를 보내면, user token을 받아올 수 있다.
    # user token 은 제한 시간이 있는 것으로 추정되며, user token을 이용하여 message를 발행할 수 있다.
    # 다음과정은 kakao2.py로
    response = requests.post(url, data=data)

    tokens = response.json()

    print('Token info\n'+str(tokens))
    if 'error' not in tokens.keys():
        #kakao2(tokens['access_token'])
        time1 = str(datetime.datetime.now()).split('.')[0].replace(' ','_').replace('-','').replace(':','')
        if not os.path.isdir('./tokens'):
            os.mkdir('tokens')
        name =  "./tokens/kakao_token_"+time1+'.json'
        with open(name,"w") as fp:
            json.dump(tokens,fp)

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
