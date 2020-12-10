# 3 https://kauth.kakao.com/oauth/authorize?client_id=5cf279ec1ec559b2809d43df80623fad&response_type=code&redirect_uri=https://localhost.com
# 3 vkF923J8UG9uL_zjYpFUZtNvpuC6VaDGwEXI6-Fw-hRr_j3Ush6sDgAk2WjF_NK8IoVg5AorDKYAAAF2RquyNg
import requests
import json
# 현재 사용자에게 REST API가 포함된 링크를 보내고, 거기서 사용자는 메시지 수신알림을 accept한상태
# 그 과정에서 data의 code를 추출할 수 있다. client_id는 develops.kakao에서 받아온 REST API ID
url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": "7412c5bbc84770efd9fb12162c229f9f",
    "redirect_uri": "https://localhost.com",
    "code": "HjmIb7MIQX4LvE6G9tT9PUdF-LEFig0GFERhzC_NYV1qp8XWGBKx3PBt-LXXhkmyt_0Xawo9dVsAAAF2RsmUzQ"

}
# 이러한 정보를 담은 data를 아래 url로 request를 보내면, user token을 받아올 수 있다.
# user token 은 제한 시간이 있는 것으로 추정되며, user token을 이용하여 message를 발행할 수 있다.
# 다음과정은 kakao2.py로
response = requests.post(url, data=data)

tokens = response.json()

print(tokens)
with open("kakao_token.json","w") as fp:
    json.dump(tokens,fp)