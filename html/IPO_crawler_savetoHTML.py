# -*- coding: utf-8 -*-
"""

DART 투자설명서 - [본   문] 의 html내용만 파일로 저장

Created on Tue Apr 05 20:54:41 2016

@author: KDH
"""

#%% 클래스 및 메소드 호출

import re
import requests as rs
import bs4
import time
#import xlsxwriter


# sys.setdefaultencoding() does not exist, here!
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


#LINK(헤더+코드+풋터) 를 html로 파싱하는 메소드
def code_to_html(header, code, footer):
    url=header+code+footer
    response = rs.get(url)
    #html_content = response.text.encode('utf-8')
    #nav = bs4.BeautifulSoup(html_content, from_encoding="utf-8")
    html_content = response.text.encode(response.encoding)
    nav = bs4.BeautifulSoup(html_content)
    return nav




#txt_to_list: txt파일을 \n 기준으로 나누어 list로 변환
def txt_to_list(filename):
    lst=[]
    
    tmpfile = open(filename,'r')
    for line in tmpfile.readlines():
        #print str(unicode(line))
        lst.append(unicode(line))
    tmpfile.close()
    
    lst = map(lambda s: s.strip(), lst) #/n 제거
    
    return lst
    

#bs(text): str을 soup로 변경
def bs(text):
    return bs4.BeautifulSoup(text)
    
        
    
    
#%% 실제 코드 - DART 투자설명서 - [본   문] 의 html내용만 파일로 저장
#url 리스트
urls_list = txt_to_list('corp_DART_bonmoon.txt')
names_list = txt_to_list('corp_DART_names.txt')
index_list = txt_to_list('corp_DART_indices.txt')

idx = 0
totalLen = len(urls_list)

#url = urls_list[0]
for url in urls_list:
    #delay 200ms
    time.sleep(0.33)
    if len(url) > 0:
        #htmldoc 문서 생성해서 filename.html 파일에 저장        
        htmldoc = rs.get(url)
        filename = unicode(index_list[idx]).strip()+"_"+names_list[idx]+"_"+unicode("투자설명서")+".html"
    
        with open(filename, "w") as f:
          f.write(htmldoc.content)

    idx = idx + 1
#nav_tmp = code_to_html('',str(url),'')

'''
for url in urls_list:
'''    
