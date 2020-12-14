import urllib3
import webbrowser
import telegram
import time

'''def tele_register_v1():
    webbrowser.open_new('https://t.me/skkunotify_bot')'''

# tele_register_v1 함수는 봇이 웹훅 설정이 된 경우 
# 로컬 웹 서버에 사용자가 텔레그램 메시지를 받기 위해
# 설정한 chat_id 가 없을 경우 호출하고, 텔레그램 상에서 직접 수동으로
# chat_id를 받을 수 있도록 합니다. 
# 이후 로컬 웹 서버에 chat_id 항목이 들어가 있는 경우, 해당 유저에게 봇이 
# 메시지를 보낼 수 있으므로 tele_sendmsg 함수를 호출합니다.

# cid에는 chat_id를 넣어주고, msg엔 보낼 메시지를 담습니다.
def tele_sendmsg(cid, msg):
    urllib3.PoolManager().request(\
    'GET','https://api.telegram.org/'+\
        'bot1480309823:AAHWQ_dGDK9-DRBejMKTO5JnC6KEna9A1KQ/sendMessage?chat_id='\
            +cid+'&text='+msg)
    # 직접 웹에 리퀘스트를 넣어서 바로 봇을 이용한 메시지를 보냄

# tele_register_v2_auto 함수는 패러미터로 user_id를 반드시 받아야함.
# 텔레그램 특성상 username은 중복되지 않음.
# 자동화를 위해 웹훅을 희생하고 사용자의 chat_id가 리턴되도록 했음

def tele_register_v2_auto(user_id):
    if user_id == '':
        return 'Get_chatid_Failed'
        # user_id가 공란이면 챗아이디를 받아올 수 없음. 
    tele_bot = telegram.Bot(token = '1480309823:AAHWQ_dGDK9-DRBejMKTO5JnC6KEna9A1KQ')
    # 토큰을 이용해 봇을 선언
    update = tele_bot.getUpdates()
    # 업데이트를 받아 그동안의 메시지 정보를 모은다.
    starttime = time.time()
    # 봇에 사용자가 메시지를 우선 날려야 chat_id를 받을 수 있는데, 
    # 1분 이상 봇에 메시지를 주지 않을 경우 취소하도록 하기 위해 시간을 체크.
    last_update_id = update[-1].update_id
    # for 문이 너무 많은 메시지 정보를 확인하지 않도록 오프셋 설정을 위해 마지막 update_id를 확인
    webbrowser.open_new('https://t.me/skkunotify_bot')
    # 웹브라우저로 링크를 연다.
    while time.time() - starttime < 60:
        # 60초동안
        update = tele_bot.getUpdates(offset=last_update_id)
        # 마지막 update_id 이후의 업데이트만을 받아온다.
        for u in update:
            if u.message.chat.username == user_id.lower():
                return str(u.message.chat_id)
            # 메시지 정보에 username이 패러미터의 user_id와 동일한 경우,
            # chat_id를 string으로 리턴한다.(원래는 integer이나 tele_sendmsg에 활용하기 위함.)
        last_update_id = update[-1].update_id
        # 마지막 update_id를 갱신한다.
        time.sleep(1)
        # 1초동안 가만히 있는다.

    return 'Get_chatid_Failed'
    # 60초동안 해당 user_id에 매칭되는 username이 없다면, chat_id를 찾을 수 없으므로
    # 'Get_chatid_Failed'를 리턴한다.