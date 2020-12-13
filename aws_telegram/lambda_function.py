import json
import urllib3

def lambda_handler(event, context):
    # TODO implement
    chatuserid = str(event['message']['from']['id'])
    
    req = urllib3.PoolManager().request('GET','https://api.telegram.org/bot1480309823:AAHWQ_dGDK9-DRBejMKTO5JnC6KEna9A1KQ/sendMessage?chat_id='+chatuserid+'&text='+chatuserid)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
