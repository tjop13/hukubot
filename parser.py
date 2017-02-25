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
        if tag == 'a'.encode('utf-8') and len(attrs) > 0 and parameter_flag==2:
          tupple_content = attrs[0]
          print tupple_content
          parameters.append(tupple_content[1])
          parameter_flag=0
        if tag == 'div' and len(attrs) > 0 and parameter_flag==1:
          tupple_content = attrs[0]
          if 'image'.encode('utf-8') == tupple_content[1]:
            parameter_flag = 2
        if tag == 'li' and len(attrs) > 0:
          tupple_content = attrs[0]
          if 'like_mark' == tupple_content[1]:
            parameter_flag = 1
#    def handle_data(self, data): # 要素内用を扱うためのメソッド
       
#    def handle_endtag(self, tag):

def GetParameter(num):
    driver = webdriver.PhantomJS()

    driver.get("http://wear.jp/women-coordinate/?pageno="+num)
    source = driver.page_source
    driver.close()

    return source

if __name__ == "__main__":
    for i in range(1,334):
        print "No."+str(i)
        parser = Parser()        # パーサオブジェクトの生成
        parser.feed(GetParameter(str(i))) # パーサにHTMLを入力する
        parser.close()
        time.sleep(5)

    print parameters

    result = ""
    for data in parameters:
        result += data + '\n'

    f = open('code.txt', 'w')
    f.write(result)
    f.close()

    print "fin"
