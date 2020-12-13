from typing import Text
import telegram
import webbrowser

def tele_register():
    webbrowser.open_new('https://t.me/skkunotify_bot')

# tele_register 함수는 로컬 웹 서버에 사용자가 텔레그램 메시지를 받기 위해
# 설정한 chat_id 가 없을 경우 호출하고, 텔레그램 상에서 직접 수동으로
# chat_id를 받을 수 있도록 합니다.
# 이후 로컬 웹 서버에 chat_id 항목이 들어가 있는 경우, 해당 유저에게 봇이 
# 메시지를 보낼 수 있으므로 tele_sendmsg 함수를 호출합니다.

# cid에는 chat_id를 넣어주고, msg엔 보낼 메시지를 담습니다.
def tele_sendmsg(cid, msg):
    tele_token = '1480309823:AAHWQ_dGDK9-DRBejMKTO5JnC6KEna9A1KQ'
    tele_bot = telegram.Bot(token = tele_token)
    # 토큰으로 봇을 특정함

    tele_bot.sendMessage(chat_id = cid, text = msg)


