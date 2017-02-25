# -*- coding: utf-8 -*- 
 
import urllib2
import time

from HTMLParser import HTMLParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

 
parameter_flag = 0
parameters = []

class Parser(HTMLParser): # htmLParserを継承したクラスを定義する
    def __init__(self):
        HTMLParser.__init__(self)
 
    def handle_starttag(self, tag, attrs): # 開始タグを扱うためのメソッド
        global parameter_flag

        # 構成要素取得
        if tag == 'a' and parameter_flag == 4:
          parameter_flag = 5

        if tag == 'p' and len(attrs) > 0 and parameter_flag==3:
          tupple_content = attrs[0]
          if tupple_content[1] == 'brand':
            parameter_flag = 4
          if tupple_content[1] == 'txt':
            parameter_flag=4
          if tupple_content[1] == 'btn btn_search':
            parameter_flag = 1

        if tag == 'div' and len(attrs) > 0 and parameter_flag==2:
          tupple_content = attrs[0]
          if tupple_content[1] == 'main':
            parameter_flag = 3

        if tag == 'li' and len(attrs) > 0 and parameter_flag==1:
          parameter_flag = 2

        if tag == 'section' and len(attrs) > 1:
          tupple_content0 = attrs[0]
          tupple_content1 = attrs[1]
          if 'item' == tupple_content0[1] and 'content_bg' == tupple_content1[1]:
            parameter_flag = 1


        # 日付取得
        if tag == 'p' and len(attrs) > 0:
          tupple_content = attrs[0]
          if tupple_content[1] == 'update_date icon_font':
            parameter_flag = 15

       
        # 全身画像のurl取得
        if tag == 'img' and len(attrs) > 1 and parameter_flag == 25:
          tupple_content = attrs[1]
          print tupple_content[1]
          parameters.append(tupple_content[1].rstrip(' 2x'))
          parameter_flag = 0
          
        if tag == 'div' and len(attrs) > 0:
          tupple_content = attrs[0]
          if tupple_content[1] == 'coordinate_img':
            parameter_flag = 25
 
    def handle_data(self, data): # 要素内用を扱うためのメソッド
        global parameter_flag
        if parameter_flag == 5:
          print data   
          parameters.append(data)
          parameter_flag=3
        if parameter_flag == 15:
          print data   
          parameters.append(data)
          parameter_flag=0
       
    def handle_endtag(self, tag):
        global parameter_flag
        if tag == 'ul':
          parameter_flag=0
        if tag == 'p' and parameter_flag==4:
          parameter_flag=3

def GetParameter(num):
    driver = webdriver.PhantomJS()

    driver.get("http://wear.jp"+path)
    source = driver.page_source
    driver.close()

    return source

if __name__ == "__main__":
    f = open('code.txt', 'r')
    for path in f:
        print path
        parser = Parser()        # パーサオブジェクトの生成
        parser.feed(GetParameter(path)) # パーサにHTMLを入力する
        parser.close()
        time.sleep(1)
    f.close()

    print parameters

    result = ""
    for data in parameters:
        result += data + '\n'

    f = open('data.txt', 'w')
    f.write(result.encode('utf-8'))
    f.close()

    print "fin"
