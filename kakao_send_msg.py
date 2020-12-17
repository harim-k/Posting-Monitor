import json
import requests
import os

link = "http://www.naver.com"
def read_data(name,refresh = False): #토큰 폴더의 내용을 읽어서 access token의 value를 추출한다
    name = 'tokens/'+name
    with open(name,"r") as fp:
        data = fp.read()
    if refresh:
        aim = 'refresh_token\": '
    else:
        aim = 'access_token\": '
    init = data.find(aim) + len(aim)
    end = data[init:].find(',')
    res = data[init:init + end].replace("\"", '').replace(',', '')
    #print(res)
    return res

# def makeMobile(link):
#     m_link = link.replace('www','m')
#     return m_link

def sendMsg(tokenName,msg):
    if tokenName == '':
        print('No tokenName : error')
        return
    #m_link = makeMobile(link)
    msg +='\n'+link
    access_token=(read_data(tokenName))
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    #access_token = "{'access_token': '_5PpTNVC_TOnAGypTBNSzGNHZTXOlgCwUCwFcQo9dZwAAAF2Rq6GQg','token_type': 'bearer', 'refresh_token': 'pxRUdPpZ3q2Y5RSL7da4CPGeKg_-3YyJL7iJTAo9dZwAAAF2Rq6GQA','expires_in': 21599, 'scope': 'account_email profile', 'refresh_token_expires_in': 5183999}"
    #access_token = '0uJoic99d5I5k10bWfOYAoZnqA0hWeOOz5TALgo9dJkAAAF2RsqL_g'
    #https://kauth.kakao.com/oauth/authorize?client_id=7412c5bbc84770efd9fb12162c229f9f&response_type=code&redirect_uri=https://localhost.com
    # 사용자 토큰을 기반으로 하여 카카오 api에 request를 보내면, 카카오 api에서 data를 바탕으로
    # 해당 카카오톡 유저에게 메시지를 발송한다.
    # scope error 발생시, 수신 알림을 적절하게 처리하지 못한것
    headers = {
        "Authorization": "Bearer " + access_token
    }


    data = {
        "template_object" : json.dumps({ "object_type" : "text",
                                         "text" : msg,
                                          "link" : {
                                                      "web_url" : link
                                                     #,"mobile_web_url" : m_link
                                                   },
                                         # "button_title": "변경된 웹 사이트 확인"
        })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다. :' + str(response.json()))
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

    url = 'https://kapi.kakao.com/v1/user/ids'
    response  = requests.get(url, data=data)
    #https://kapi.kakao.com/v1/user/ids?Authorization=a498a890d7f8e180b3c54c262ac9836d
def main():
    if not os.path.isdir('tokens'):
        os.mkdir('tokens')
    file_list = os.listdir('tokens')
    file_list.sort()
    if len(file_list) >0:
        for idx, f in enumerate(file_list):
            print(idx,end=': ')
            print(f)
        while True:
            num = int(input('Select number: '))
            msg = input('Message: ')
            #link = input('Link: ')
            tokenName= file_list[num]
            sendMsg(tokenName,msg)
    else:
        print('no tokens')

        #1212
        #유저식별, token refresh
        #웹페이지 만들기 사용자에게 input(page, 관심사)
        # 토큰이 만료되지 않고 없어질수도 있다?
if __name__ == "__main__":
    main()