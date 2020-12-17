
from posting_monitor2 import monitor_posting
from messenger import init_user



# saramin(사람인) 검색
url1 = 'http://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&loc_mcd=101000&cat_cd=101'  # 
# youtube 채널
url2 = 'https://www.youtube.com/channel/UCiKp-s_U7RVSGvft-SpIDgw/videos?view_as=subscriber'
# 카카오 채용 공고
url3 = 'https://careers.kakao.com/jobs'
# 에브리타임
url4 = 'https://everytime.kr/370444'
# 성균관대학교 소프트웨어학과 공지사항
url5 = 'https://cs.skku.edu/news/recent/list'
# 디씨인사이드 롤게시판 문제점 : 게시글이 밀려서 page가 바뀌면 url도 바뀜 
url6 = 'https://gall.dcinside.com/board/lists/?id=leagueoflegends4'
# 서울주택도시공사 주택임대 공지사항
url7 = 'https://www.i-sh.co.kr/main/lay2/program/S1T294C297/www/brd/m_247/list.do?multi_itm_seq=2'


urls = [url2]

user_id = 'harim_k'
messenger_type = 'telegram'
keywords = ['']
user = init_user(messenger_type, user_id)

monitor_posting(messenger_type, user, urls, keywords)