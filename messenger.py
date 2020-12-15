from tele_sendmsg import tele_sendmsg, tele_register_v2_auto


# def init_kakaotalk():

def init_user(user_id):
    user = init_telegram(user_id)
    
    return user


def init_telegram(user_id):
    chat_id = tele_register_v2_auto(user_id)

    return chat_id


def send_message_telegram(chat_id, msg):
    tele_sendmsg(chat_id, msg)


def send_message(user, msg):
    send_message_telegram(user, msg)
# def send_message_kakaotalk(chat_id, msg):
#     tele_sendmsg(chat_id, msg)