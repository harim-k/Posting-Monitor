from tele_sendmsg import tele_sendmsg, tele_register_v2_auto
from kakao_token_server import run_token_server
from kakao_send_msg import sendMsg


def init_user(messenger_type, user_id):
    if messenger_type == 'kakaotalk':
        user = init_kakaotalk()
    else:
        user = init_telegram(user_id)
    
    return user


def send_message(messenger_type, user, msg):
    if messenger_type == 'kakaotalk':
        send_message_kakaotalk(user, msg)
    else:
        send_message_telegram(user, msg)


def init_kakaotalk():
    tokenName = run_token_server()

    return tokenName


def init_telegram(user_id):
    chat_id = tele_register_v2_auto(user_id)

    return chat_id


def send_message_kakaotalk(tokenName, msg):
    sendMsg(tokenName,msg)


def send_message_telegram(chat_id, msg):
    tele_sendmsg(chat_id, msg)


