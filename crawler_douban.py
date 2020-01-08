from bs4 import BeautifulSoup
from selenium import webdriver
import csv


def get_content(url, content):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path="D:/wangyang/其他软件/chromedriver.exe")  # 打开谷歌浏览器，这里使用的无头浏览器，也可以把第一个参数删去，同时删除前三行代码

    driver.maximize_window()  # 最大化窗口

    driver.get(url)  # 打开网页

    # 构造BeautifulSoup类
    bs = BeautifulSoup(driver.page_source, "html.parser")
    body = bs.body
    # print(body)
    if content == []:
        content_title = []  # 存储第一行标题
        data = body.find("div", {"id": "content"}).find("h1")
        content_title.append(str(data.get_text()))
        content.append(content_title)
        content_subtitle = ["电影名", "导演/主演/时间/国家/类型", "评语"]  # 每一列的标题
        content.append(content_subtitle)
    # 爬取电影
    data = body.find("ol", {"class": "grid_view"})
    Li = data.find_all("li")
    for li in Li:
        every_content = []  # 存储每一个电影的信息
        title = li.find("div", {"class": "hd"}).find(
            "span", {"class": "title"}).get_text()#爬取电影的名字
        every_content.append(str(title))
        director = li.find("div", {"class": "bd"}).find("p").get_text()#爬取电影的导演等信息
        every_content.append(str(director))
        comment = li.find("div", {"class": "bd"}).find(
            "p", {"class": "quote"}).find("span").get_text()#爬取电影的相关评论
        every_content.append(str(comment))
        content.append(every_content)
    driver.find_element_by_class_name("next").click()#点击下一页
    url = driver.current_url#获取当前页面的url
    driver.quit()#关闭网页
    return url, content, body


url = "https://movie.douban.com/top250"
content = []
url, content, body = get_content(url, content)
while True:
    # 判断是否到达最后一页
    if body.find("span", {"class": "next"}).find("a") == None:
        break
    else:
        url, content, body = get_content(url, content)
#写入文件
file_name = "D:\\wangyang\\练习的python程序\\网络爬虫\\爬取豆瓣网前250名的电影信息.csv"
with open(file_name, "a", errors="ignore", newline="") as f:
    f_csv = csv.writer(f)
    f_csv.writerows(content)
