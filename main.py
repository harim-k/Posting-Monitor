
from posting_monitor import monitor_posting
from messenger import init_user


url1 = 'https://docs.google.com/document/d/1i9j_XGRqFNHX-nu3ehOQ3RgUpLCHNtctCXrXTNKMGVw/edit'
url2 = 'http://acebedmall.co.kr/front/search/categorySearch.do?searchYn=N&ctgNo=2'
url3 = 'https://blog.naver.com/harim9355'
url4 = 'https://everytime.kr/370444'
url5 = 'https://cs.skku.edu/news/recent/list'
url6 = 'https://gall.dcinside.com/board/lists/?id=leagueoflegends4'
url7 = 'https://www.i-sh.co.kr/main/lay2/program/S1T294C297/www/brd/m_247/list.do?multi_itm_seq=2'
url8 = 'https://careers.kakao.com/jobs'

urls = [url4]

user_id = 'harim_k'
messenger_type = 'kakaotalk'
keyword = '??'
user = init_user(messenger_type, user_id)

monitor_posting(messenger_type, user, urls, keyword)
