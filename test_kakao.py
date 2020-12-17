from kakao_token_server import run_token_server
from kakao_send_msg import sendMsg
#tokens 폴더안의 이름을 tokenName에 넣어준다.
#tokenName = '201217_110431.json'
tokenName = ''
msg = 'Hello, world!'

if tokenName == '':
    tokenName = run_token_server()
sendMsg(tokenName,msg)
