import urllib.request as request
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager


def getMovieTitleUrl(url):
    req = request.Request(url, headers={  # 模仿使用者去抓取避免被拒絕存取
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
    })
    with request.urlopen(req) as response:  # 連上網站去讀取資料 存在data內
        data = response.read().decode('utf-8')

    root = bs4.BeautifulSoup(data, "html.parser")  # 透過bs4去解析網站原始碼

    titles = root.find_all("div", class_="td")  # 要看網站的原始碼 找到標題的位置
    for title in titles:
        if title.a != None:
            Link = (title.a["href"])  # 找到該標題的網址
            getMovieCommentUrl(Link)  # 進入該貼文去抓取資料


def getMovieCommentUrl(url):
    req = request.Request(url, headers={  # 模仿使用者去抓取避免被拒絕存取
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
    })
    with request.urlopen(req) as response:  # 連上網站去讀取資料 存在data內
        data = response.read().decode('utf-8')

    root = bs4.BeautifulSoup(data, "html.parser")  # 透過bs4去解析網站原始碼

    titles = root.find_all("div", class_="btn_plus_more usercom_more gabtn")  # 要看網站的原始碼 找到標題的位置
    for title in titles:
        if title.a != None:
            for i in range(1, 11):  # 限定抓取十頁
                Link = (title.a["href"]) + "?sort=update_ts&order=desc&page=" + str(i)  # 找到該標題的網址加上頁數
                getMovieCommentandDownload(Link)  # 進入評論區抓取評論


def getMovieCommentandDownload(url):
    req = request.Request(url, headers={  # 模仿使用者去抓取避免被拒絕存取
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36",
        "Content-type": "https://movies.yahoo.com.tw/ajax/thumb_review"
    })
    with request.urlopen(req) as response:  # 連上網站去讀取資料 存在data內
        data = response.read().decode('utf-8')

    root = bs4.BeautifulSoup(data, "html.parser")

    PATH = './chromedriver'  # 設定selenium的路徑
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    scores = driver.find_elements_by_xpath('//*[@id="form_good1"]/input[2]')  # 找到分數所在的xpath

    comment_list = []
    score_list = []

    for score in scores:
        score_list.append(score.get_attribute('value'))  # 把每筆的評分都存下來

    namehtml = root.find('h1', class_="inform_title")  # 抓到電影名稱
    name = namehtml.text.split("\n")  # 電影名稱有中英文 用\n區隔

    reply_all = root.find_all('div', class_="usercom_inner _c")  # 看網站的原始碼 找到內文的位置

    for reply in reply_all:
        if reply.text != None:  # 避免抓到被刪除的評論
            tx = reply.find_all('span')  # 只抓取留言的部分
            comment_list.append(tx[2].text)
    for i in range(len(comment_list)):
        print(name[0] + " " + comment_list[i] + " " + score_list[i])
        # with open("movie_comments_data.txt", "a", encoding="utf-8") as file:  # 讀進檔案內 "a"為不複寫模式
        # file.write(name[0]+" "+comment_list[i]+" "+score_list[i]+"\n")

    # print("下載完成")


url = "https://movies.yahoo.com.tw/chart.html"
getMovieTitleUrl(url)