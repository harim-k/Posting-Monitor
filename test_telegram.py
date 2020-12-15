from messenger import init_telegram, send_message_telegram

user_id = 'harim_k'
msg = 'hello'


chat_id = init_telegram(user_id) 
send_message_telegram(chat_id, msg)
