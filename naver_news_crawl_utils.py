import requests
from bs4 import BeautifulSoup
import bs4.element

# Function Description : BeautifulSoup Object 생성
def get_soup_obj(url):
    # 상위 뉴스 HTML Crowling
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')

    return soup

# Function Description : URL의 상위 3개 News_Info Get
def get_top3_news_info(sec, _url):
    # 임시 이미지
    default_img = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=naver#"

    #해당 분야 상위 뉴스 HTML 가져오기
    soup = get_soup_obj(_url)

    #해당 분야 상위 뉴스 3개 가져오기
    news_list3 = []
    lis3 = soup.find('ul', class_='type06_headline').find_all("li", limit=3)
    for li in lis3:
        #title : 뉴스 제목, news_url : 뉴스 URL, image_url : 이미지 URL
        news_info = {
            "title" : li.img.attrs.get('alt') if li.img else li.a.text.replace("\n", "").replace("\t","").replace("\r","") , 
            "date" : li.find(class_="date").text,
            "news_url" : li.a.attrs.get('href'),
            "image_url" :  li.img.attrs.get('src') if li.img else default_img,
            "news_contents" : ""
        }
        news_list3.append(news_info)
        #print(news_info)

    return news_list3 

# Function Description : News 본문 Get
def get_news_contents(_url):
    soup = get_soup_obj(_url)
    body = soup.find('div', class_="_article_body_contents")

    news_contents = ''
    for content in body:
        if type(content) is bs4.element.NavigableString and len(content) > 50:
            # content.strip() : whitepace 제거 (참고 : https://www.tutorialspoint.com/python3/string_strip.htm)
            # 뉴스 요약을 위하여 '.' 마침표 뒤에 한칸을 띄워 문장을 구분하도록 함
            news_contents += content.strip() + ' '

    return news_contents

# Function Description : 정치, 경제, 사회 분야 상위 3개 뉴스 크롤링
def get_naver_news_top3():
    # 뉴스 결과를 담아낼 dictionary
    news_dic = dict()

    # Sections : 정치, 경제, 사회
    sections = ["pol", "eco", "soc"]
    # section_url : URL
    section_urls = [
        # 정치 섹션을 눌렀을때, url 주소
        "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=100",
        # 경제 섹션을 눌렀을때, url 주소
        "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=101",
        # 사회 섹션을 눌렀을때, url 주소
        "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=102",
    ]

    for sec, url in zip(sections, section_urls):
        # 뉴스의 기본 정보 load
        news_info = get_top3_news_info(sec, url)
        for news in news_info:
            # 뉴스 본문 Load
            news_url = news['news_url']
            news_contents = get_news_contents(news_url)

            #뉴스 정보를 저장하는 dictionary를 구성
            news['news_contents'] = news_contents
        
        news_dic[sec] = news_info

    return news_dic