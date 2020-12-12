import os
import sys
import urllib.request
def shortUrl(link):
    client_id = "p99AAR1FgP8Y3erF9HN9" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "c3N1up4WkC" # 개발자센터에서 발급받은 Client Secret 값
    #encText = urllib.parse.quote("https://developers.naver.com/docs/utils/shortenurl")
    encText = urllib.parse.quote(link)
    data = "url=" + encText
    url = "https://openapi.naver.com/v1/util/shorturl"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_body = response_body.decode('utf-8')
        #print(type(response_body))
        aim  ="\"url\":\""
        init = response_body.find(aim) +len(aim)
        response_body=response_body[init:]
        end = response_body.find("\",")
        response_body = response_body[:end]
        #print(response_body)
        return response_body
    else:
        print("Error Code:" + rescode)
        return 'fail'
#shortUrl('https://kauth.kakao.com/oauth/authorize?client_id='+
#         '7412c5bbc84770efd9fb12162c229f9f&response_type=code&redirect_uri=http://14.33.48.113:10080')