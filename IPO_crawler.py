# -*- coding: utf-8 -*-
"""
1. 회사명에서 DART 기업코드(8자리 숫자) 추출하기
2. KIND에서 설립일자 추출하기
3. DART 웹주소에서 정정신고 및 보고서 본문 웹주소 추출하기
4. DART 보고서 JSON 확인해서 투자설명서 본문 url 추출하기
5. DART 보고서 JSON 확인해서 증권발행실적보고서 본문 url 추출하기
6. DART 웹주소에서 증권신고서 최종접수일 추출하기
7. DART 웹주소에서 증권신고서 초기접수일 추출하기
8. DART 증권발행실적보고서 url에서 발행전후 지분율 추출하기
9. DART 증권신고서 url에서 재무제표 url 추출하기
10. 추출한 재무제표 url에서 재무제표 데이터 뽑아내기


11. 투자설명서 url에서 분포 데이터 뽑아내기 ( 참고: \xeb\xb6\x84\xed\x8f\xac  (분포) )
12. 투자설명서 url에서 기관투자자 신청수량 데이터 뽑아내기 ( 참고: \xeb\xb6\x84\xed\x8f\xac  (분포) )

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
    


#tagSplit: strSplit 텍스트를 기준으로 split: 
#           soup --> str변환 --> split 사용 --> soup변환
def tagSplit(tag,strSplit):
    return strlstToSoup(str(tag).split(strSplit))    

#strlstToSoup: string이 들어간 list를 bsoup로 변환하는 메소드
def strlstToSoup(lst):
    idx = 0    
    for item in lst:
        lst[idx]=bs4.BeautifulSoup(item)
        idx = idx + 1
    return lst    




#%% 실제 코드 -  투자설명서 url에서 기관투자자 신청수량 데이터 뽑아내기
#url 리스트

urls_list = txt_to_list('DART_tooja_jungjung_urls.txt')
names_list = txt_to_list('corp_DART_names.txt')
index_list = txt_to_list('corp_DART_indices.txt')

#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)


##test하는 부분. for문 돌릴때 주석처리.
#url = urls_list[idx]



#writeline변수(한 줄당 쓸 내용) 설정


time.sleep(0.05)

for url in urls_list:
    if len(url) > 0:    
        nav_tmp = code_to_html('',str(url),'')
        boonpo_idx = unicode(nav_tmp).find('\xeb\xb6\x84\xed\x8f\xac') #분포 인덱스 찾기
        if boonpo_idx > 0:
            if len(unicode(nav_tmp)) > boonpo_idx + 10000:
                html_content = bs(unicode(nav_tmp)[boonpo_idx-5000:boonpo_idx])
                if len(html_content.find_all('table')) > 0:
                    boonpo_tables = [ html_content.find_all('table')[-1]]
                    for boonpo_table in boonpo_tables:
                        rows = boonpo_table.find_all("th") + boonpo_table.find_all("tr")
            
                        for tr in rows:
                            if tr.find_all('td') != [] and tr.find_all('td')[0].contents != []:
                                rowtitle = tr.find_all('td')[0].contents[0]
                                tmp=""
                                for td in tr.find_all('td'):
                                    #각 cell 별 element                        
                                    tmp = tmp + unicode(td.contents[0]) + '\t'
                                #print tmp
                                writeline = names_list[idx] + '\t' + url + '\t' + tmp
                                #print writeline                    
                                lines.append(writeline)
                    lines.append("***********\t*****************\t****************\t***************\t**************\t**************")                            
    
    print "("+str(idx+1)+"/"+str(totalLen)+") recorded.." #로그 역할
    
    idx = idx + 1
            
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_out_shinchung_rate_tables.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()






#%% 실제 코드 -  투자설명서 url에서 분포 데이터 뽑아내기
#url 리스트

urls_list = txt_to_list('DART_tooja_jungjung_urls.txt')
names_list = txt_to_list('corp_DART_names.txt')
index_list = txt_to_list('corp_DART_indices.txt')

#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)


##test하는 부분. for문 돌릴때 주석처리.
#url = urls_list[idx]



#writeline변수(한 줄당 쓸 내용) 설정


time.sleep(0.05)

for url in urls_list:
    if len(url) > 0:    
        nav_tmp = code_to_html('',str(url),'')
        boonpo_idx = unicode(nav_tmp).find('\xeb\xb6\x84\xed\x8f\xac') #분포 인덱스 찾기
        if boonpo_idx > 0:
            if len(unicode(nav_tmp)) > boonpo_idx + 10000:
                html_content = bs(unicode(nav_tmp)[boonpo_idx:boonpo_idx+10000])
                if len(html_content.find_all('table')) > 1:
                    boonpo_tables = [ html_content.find_all('table')[0] , html_content.find_all('table')[1] ]
                    for boonpo_table in boonpo_tables:
                        rows = boonpo_table.find_all("th") + boonpo_table.find_all("tr")
            
                        for tr in rows:
                            if tr.find_all('td') != [] and tr.find_all('td')[0].contents != []:
                                rowtitle = tr.find_all('td')[0].contents[0]
                                tmp=""
                                for td in tr.find_all('td'):
                                    #각 cell 별 element                        
                                    tmp = tmp + unicode(td.contents[0]) + '\t'
                                #print tmp
                                writeline = names_list[idx] + '\t' + url + '\t' + tmp
                                #print writeline                    
                                lines.append(writeline)
                    lines.append("***********\t*****************\t****************\t***************\t**************\t**************")                            
    
    print "("+str(idx+1)+"/"+str(totalLen)+") recorded.." #로그 역할
    
    idx = idx + 1
            
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_out_boonpo_tables.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()








#%% 실제 코드 -  DART 증권발행실적보고서 청약률 추출하기
#url 리스트

urls_list = txt_to_list('corp_DART_jaemu2_urls.txt')
names_list = txt_to_list('corp_DART_names_2.txt')
index_list = txt_to_list('corp_DART_indices_2.txt')

#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)


##test하는 부분. for문 돌릴때 주석처리.
#url = urls_list[idx]



#writeline변수(한 줄당 쓸 내용) 설정


time.sleep(0.02)

for url in urls_list:
    if len(url) > 0:    
        nav_tmp = code_to_html('',str(url),'')
        rows = nav_tmp.find_all("tr")
        for tr in rows:
            if tr.find_all('td') != [] and tr.find_all('td')[0].contents != []:
                rowtitle = tr.find_all('td')[0].contents[0]
                #print unicode(rowtitle)
                if rowtitle.find(u'총계') > 0 or rowtitle.find(u'총 계') > 0 or (rowtitle.find(u'매출액') > 0 and len(rowtitle) < 10) or rowtitle.find(u'영업이익') > 0 or rowtitle.find(u'당기순이익') > 0:
                    tmp = ""
                    for td in tr.find_all('td'):
                        #각 cell 별 element                        
                        tmp = tmp + str(td.contents[0]) + '\t'
                    #print tmp
                    writeline = names_list[idx] + '\t' + url + '\t' + tmp
                    #print writeline                    
                    lines.append(writeline)
                    
                            
    print "("+str(idx+1)+"/"+str(totalLen)+") recorded.." #로그 역할
    
    idx = idx + 1
            
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_out_chungyak_Ratio.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()








#%%% 실제 코드 - DART 보고서 JSON 확인해서 투자설명서 본문 url 추출하기

#makeDARTurl: reportId(리스트) 변수 받아서 투자보고서 url로 변환
def makeDARTurl(lst):
    link = "http://dart.fss.or.kr/report/viewer.do?rcpNo=" + lst[0].strip() + "&dcmNo=" + \
        lst[1].strip() + "&eleId=" + lst[2].strip() + "&offset=" + lst[3].strip() + "&length=" + lst[4].strip() + "&dtd=" + lst[5].strip()
    return link

#url 리스트
urls_list = txt_to_list('corp_DART_shingoseo.txt')
names_list = txt_to_list('corp_DART_names_2.txt')
index_list = txt_to_list('corp_DART_indices_2.txt')


#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)

##test하는 부분. for문 돌릴때 주석처리.
#url = urls_list[idx]

#url 별로 print할 line 생성해서 lines 리스트에 append
for url in urls_list:
    #writeline변수(한 줄당 쓸 내용) 설정
    writeline = names_list[idx] + '\t'
    
        
    #string 추출
    time.sleep(0.02)    
    nav_tmp = code_to_html('',str(url),'')
    str_tmp = str(nav_tmp).split("var cnt")[-1].split("var view")[0]
    
    reportItems = str_tmp.split("text:")
    reportItems = reportItems[1:]#1st element 제거
   
    #각 보고서별(웹사이트 열었을때 좌측 패널에 보이는 목록) 이름 및 url을 붙여넣기
    for reportItem in reportItems:

        reportName = reportItem.split("id:")[0].strip()
        if reportName.find(u'재무에 관한 사항') > 0:
            #print "@@@@@@@@@@@@@@@@"
            reportId = reportItem.split("viewDoc(")[1].split(");}")[0].replace("'","").split(",")
            reportURL = makeDARTurl(reportId)
            writeline = writeline + reportName + '\t' + reportURL + '\t'
            #print writeline
            #print "error!! in", str(nav_tmp.title.contents), str(reportName)
    #print writeline
    
    #writeline변수 모아서 리스트 만들기    
    lines.append(writeline)
    print "("+str(idx+1)+"/"+str(totalLen)+") recorded.." #로그 역할
    idx = idx + 1    
    

#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_jaemu_urls.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()






#%% 실제 코드 -  DART 증권발행실적보고서 청약률 추출하기
#url 리스트

urls_list = txt_to_list('corp_DART_chungyak_list.txt')
names_list = txt_to_list('corp_DART_names.txt')
index_list = txt_to_list('corp_DART_indices.txt')

#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)


##test하는 부분. for문 돌릴때 주석처리.
#url = urls_list[idx]



#writeline변수(한 줄당 쓸 내용) 설정
writeline = names_list[idx] + '\t'


time.sleep(0.02)

for url in urls_list:
    if len(url) > 0:    
        nav_tmp = code_to_html('',str(url),'')
        rows = nav_tmp.find_all("tr")

        for tr in rows:
            writeline = index_list[idx] + '\t' + names_list[idx] + '\t' + str(url) + '\t'
            if len(tr.find_all('td')) > 8:
                tmp_len = len(tr.find_all('td')[0].contents[0])
                if tmp_len > 1 and tmp_len < 6:
                    #각 row에 들어갈 내용 기록 - (회사명 + 표에 나오는 row 내용)
                    for td in tr.find_all('td'):
                        #print td.contents[0]
                        #type(td.contents[0])
                        #td.contents[0] 데이터 클린징 ( '\n'하고 <p> tag 없애기)
                        tmp = td.contents
                        if len(tmp) > 0:    
                            writeline = writeline + str(tmp[0]) + '\t'                
                        #writeline = writeline + str(td.contents[0]) + '\t'
                    #lines 리스트에 row 내용 기록
                    
                    lines.append(writeline)
        
        print "("+str(idx+1)+"/"+str(totalLen)+") recorded.." #로그 역할
    
    idx = idx + 1
            
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_out_chungyak_Ratio.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()


#%% 실제 코드 -  DART 증권발행실적보고서 url에서 발행전후 지분율 추출하기
#url 리스트

urls_list = txt_to_list('corp_DART_balhang_urls.txt')
names_list = txt_to_list('corp_DART_names.txt')
index_list = txt_to_list('corp_DART_indices.txt')

#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)


##test하는 부분
'''
urls_list = [urls_list[4]]
nav_tmp = code_to_html('',str(urls_list[0]),'')
'''

#writeline변수(한 줄당 쓸 내용) 설정
writeline = names_list[idx] + '\t'


time.sleep(0.02)

for url in urls_list:
    if len(url) > 0:    
        nav_tmp = code_to_html('',str(url),'')
        rows = nav_tmp.find_all("tr")
        
        for tr in rows:
            writeline = index_list[idx] + '\t' + names_list[idx] + '\t' + str(url) + '\t'
            if len(tr.find_all('td')) > 2:
                #각 row에 들어갈 내용 기록 - (회사명 + 표에 나오는 row 내용)
                for td in tr.find_all('td'):
                    #print td.contents[0]
                    #type(td.contents[0])
                    #td.contents[0] 데이터 클린징 ( '\n'하고 <p> tag 없애기)
                    soup = td.contents
                    tmp = ""
                    for s in soup:
                        if s != u'\n':
                            tmp = tmp + str(s)            
                    writeline = writeline + tmp + '\t'                
                    #writeline = writeline + str(td.contents[0]) + '\t'
                #lines 리스트에 row 내용 기록
                lines.append(writeline)
        
        print "("+str(idx)+"/"+str(totalLen)+") recorded.." #로그 역할
    
    idx = idx + 1
            
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_jibun_byundong_list.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()
    



#%% 실제 코드 - DART 웹주소에서 증권신고서 초기접수일 추출하기
#url 리스트

urls_list = txt_to_list('corp_DART_chogi_urls.txt')
names_list = txt_to_list('corp_DART_names.txt')

#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)

#url 별로 print할 line 생성해서 lines 리스트에 append
# /dsaf001/main.do?rcpNo=20070808000017 (main 텍스트 포함한 href 링크)
# 찾아서 가장 작은 날짜값을 텍스트로 추가
for url in urls_list:
    time.sleep(0.05)
    #writeline변수(한 줄당 쓸 내용) 설정
    writeline = names_list[idx] + '\t'
    
    date_num = 999999999    
    
    idx = idx + 1    
    
    nav_tmp = code_to_html('',str(url),'')
    url_tags = nav_tmp.find_all("a")
    for url_tag in url_tags:
        time.sleep(0.02)
        if str(url_tag.get('href')).find("main") > 0:
            tmp_num = int(url_tag.get('href').split("rcpNo=")[-1]) / 1000000
            if date_num > tmp_num:
                date_num = tmp_num
    writeline = writeline + str(date_num)
    print writeline
    

            
    #writeline변수 모아서 리스트 만들기
    lines.append(writeline)
    print "("+str(idx)+"/"+str(totalLen)+") recorded.." #로그 역할
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_start_dates_list.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()


#%% 실제 코드 - DART 웹주소에서 최종접수일 추출하기
#url 리스트
from collections import Counter

urls_list = txt_to_list('corp_DART_urls.txt')
names_list = txt_to_list('corp_DART_names.txt')

#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)

#url 별로 print할 line 생성해서 lines 리스트에 append
for url in urls_list:
    time.sleep(0.05)
    #writeline변수(한 줄당 쓸 내용) 설정
    writeline = names_list[idx] + '\t'
    
    idx = idx + 1    
    
    nav_tmp = code_to_html('',str(url),'')
    url_tags = nav_tmp.find_all(attrs={"class": "cen_txt"}) 

    #duplicate된 값 찾아서 그 값만 남김    
    findduplist = []    
    
    #url 안에 있는 class=cen_txt 조건 충족하는 tag들에 대해 돌리는 for문
    for url_tag in url_tags:
        if len(url_tag) > 0:
            if len(url_tag.contents[0].strip()) > 1:
                date = url_tag.contents[0].strip()                
                findduplist.append(date)                
    counts = Counter(findduplist)                
    duplicated_date = [value for value, count in counts.items() if count > 1]

    #writeline에 duplicated_date 값 추가    
    if len(duplicated_date) > 0:    
        writeline = writeline + duplicated_date[0] + '\t'      
            
    #writeline변수 모아서 리스트 만들기
    lines.append(writeline)
    print "("+str(idx)+"/"+str(totalLen)+") recorded.." #로그 역할
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_dates_list.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()

    
    





#%%% 실제 코드 - DART 보고서 JSON 확인해서 증권발행실적보고서 본문 url 추출하기

#makeDARTurl: reportId(리스트) 변수 받아서 투자보고서 url로 변환
def makeDARTurl(lst):
    link = "http://dart.fss.or.kr/report/viewer.do?rcpNo=" + lst[0].strip() + "&dcmNo=" + \
        lst[1].strip() + "&eleId=" + lst[2].strip() + "&offset=" + lst[3].strip() + "&length=" + lst[4].strip() + "&dtd=" + lst[5].strip()
    return link

#url 리스트
urls_list = txt_to_list('corp_DART_balhang.txt')
names_list = txt_to_list('corp_DART_names.txt')


#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)


#url 별로 print할 line 생성해서 lines 리스트에 append
for url in urls_list:
    if url != "":
        #writeline변수(한 줄당 쓸 내용) 설정
        writeline = names_list[idx] + '\t'
        
        idx = idx + 1    
            
        #string 추출
        nav_tmp = code_to_html('',str(url),'')
        str_tmp = str(nav_tmp).split("var cnt")[-1].split("var view")[0]
        
        reportItems = str_tmp.split("text:")
        reportItems = reportItems[1:]#1st element 제거
       
        #각 보고서별(웹사이트 열었을때 좌측 패널에 보이는 목록) 이름 및 url을 붙여넣기
        for reportItem in reportItems:
            time.sleep(0.02)
            reportName = reportItem.split("id:")[0].strip()
            reportId = reportItem.split("viewDoc(")[1].split(");}")[0].replace("'","").split(",")
            
            if len(reportId) == 6:
                reportURL = makeDARTurl(reportId)
                writeline = writeline + reportName + '\t' + reportURL + '\t'
                #print writeline
            else: 
                print "error!! in", str(nav_tmp.title.contents), str(reportName)
               
        #writeline변수 모아서 리스트 만들기    
        lines.append(writeline)
        print "("+str(idx)+"/"+str(totalLen)+") recorded.." #로그 역할
    
    else:
        idx = idx + 1    
        print "!!! not recorded(empty URL) !!!"

#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_balhang_urls.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()






#%% 테스트 코드 - DART 보고서 JSON 확인해서 증권발행실적보고서 본문 url 추출하기

lines =[]

#url 리스트
urls_list = txt_to_list('corp_DART_balhang_test.txt')

#url 하나만 추출
tmpurl=urls_list[0]

#string 추출
nav_tmp = code_to_html('',str(tmpurl),'')
str_tmp = str(nav_tmp).split("var cnt")[-1].split("var view")[0]

reportItems = str_tmp.split("text:")
reportItems = reportItems[1:]#1st element 제거

#보고서명 추출: 첫번째 [] 안의 숫자 변경하면 보고서명 바뀜
#reportName = reportItems[0].split("id:")[0].strip()
#보고서ID(viewDoc 안의 변수들 )
#reportId = reportItems[0].split("viewDoc(")[1].split(");}")[0].replace("'","").split(",")

#makeDARTurl: reportId(리스트) 변수 받아서 투자보고서 url로 변환
def makeDARTurl(lst):
    link = "http://dart.fss.or.kr/report/viewer.do?rcpNo=" + lst[0].strip() + "&dcmNo=" + \
        lst[1].strip() + "&eleId=" + lst[2].strip() + "&offset=" + lst[3].strip() + "&length=" + lst[4].strip() + "&dtd=" + lst[5].strip()
    return link


#writeline변수(한 줄당 쓸 내용) 설정
writeline = ""

#각 보고서별(웹사이트 열었을때 좌측 패널에 보이는 목록) 이름 및 url을 붙여넣기
for reportItem in reportItems:
    time.sleep(0.02)
    reportName = reportItem.split("id:")[0].strip()
    reportId = reportItem.split("viewDoc(")[1].split(");}")[0].replace("'","").split(",")
    
    if len(reportId) == 6:
        reportURL = makeDARTurl(reportId)
        writeline = writeline + reportName + '\t' + reportURL + '\t'
    else: 
        print "error!! in", str(nav_tmp.title.contents), str(reportName)
    print writeline
    


lines.append(writeline)
#writeline변수 모아서 리스트 만들기
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_tooja_urls_test.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()




#%%% 실제 코드 - DART 보고서 JSON 확인해서 투자설명서 본문 url 추출하기

#makeDARTurl: reportId(리스트) 변수 받아서 투자보고서 url로 변환
def makeDARTurl(lst):
    link = "http://dart.fss.or.kr/report/viewer.do?rcpNo=" + lst[0].strip() + "&dcmNo=" + \
        lst[1].strip() + "&eleId=" + lst[2].strip() + "&offset=" + lst[3].strip() + "&length=" + lst[4].strip() + "&dtd=" + lst[5].strip()
    return link

#url 리스트
urls_list = txt_to_list('corp_DART_tooja.txt')
names_list = txt_to_list('corp_DART_names.txt')


#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)


#url 별로 print할 line 생성해서 lines 리스트에 append
for url in urls_list:
    if url != "":
        #writeline변수(한 줄당 쓸 내용) 설정
        writeline = names_list[idx] + '\t'
        
        idx = idx + 1    
            
        #string 추출
        nav_tmp = code_to_html('',str(url),'')
        str_tmp = str(nav_tmp).split("var cnt")[-1].split("var view")[0]
        
        reportItems = str_tmp.split("text:")
        reportItems = reportItems[1:]#1st element 제거
       
        #각 보고서별(웹사이트 열었을때 좌측 패널에 보이는 목록) 이름 및 url을 붙여넣기
        for reportItem in reportItems:
            time.sleep(0.02)
            reportName = reportItem.split("id:")[0].strip()
            reportId = reportItem.split("viewDoc(")[1].split(");}")[0].replace("'","").split(",")
            
            if len(reportId) == 6:
                reportURL = makeDARTurl(reportId)
                writeline = writeline + reportName + '\t' + reportURL + '\t'
                #print writeline
            else: 
                print "error!! in", str(nav_tmp.title.contents), str(reportName)
               
        #writeline변수 모아서 리스트 만들기    
        lines.append(writeline)
        print "("+str(idx)+"/"+str(totalLen)+") recorded.." #로그 역할
    
    else:
        idx = idx + 1    
        print "!!! not recorded(empty URL) !!!"

#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_tooja_urls.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()









#%%% 실제 코드 - DART 보고서 JSON 확인해서 투자설명서 본문 url 추출하기

#makeDARTurl: reportId(리스트) 변수 받아서 투자보고서 url로 변환
def makeDARTurl(lst):
    link = "http://dart.fss.or.kr/report/viewer.do?rcpNo=" + lst[0].strip() + "&dcmNo=" + \
        lst[1].strip() + "&eleId=" + lst[2].strip() + "&offset=" + lst[3].strip() + "&length=" + lst[4].strip() + "&dtd=" + lst[5].strip()
    return link

#url 리스트
urls_list = txt_to_list('corp_DART_tooja.txt')
names_list = txt_to_list('corp_DART_names.txt')


#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)


#url 별로 print할 line 생성해서 lines 리스트에 append
for url in urls_list:
    #writeline변수(한 줄당 쓸 내용) 설정
    writeline = names_list[idx] + '\t'
    
    idx = idx + 1    
        
    #string 추출
    nav_tmp = code_to_html('',str(url),'')
    str_tmp = str(nav_tmp).split("var cnt")[-1].split("var view")[0]
    
    reportItems = str_tmp.split("text:")
    reportItems = reportItems[1:]#1st element 제거
   
    #각 보고서별(웹사이트 열었을때 좌측 패널에 보이는 목록) 이름 및 url을 붙여넣기
    for reportItem in reportItems:
        time.sleep(0.02)
        reportName = reportItem.split("id:")[0].strip()
        reportId = reportItem.split("viewDoc(")[1].split(");}")[0].replace("'","").split(",")
        
        if len(reportId) == 6:
            reportURL = makeDARTurl(reportId)
            writeline = writeline + reportName + '\t' + reportURL + '\t'
            #print writeline
        else: 
            print "error!! in", str(nav_tmp.title.contents), str(reportName)
    
    lines =[]
    
    #writeline변수 모아서 리스트 만들기    
    lines.append(writeline)
    print "("+str(idx)+"/"+str(totalLen)+") recorded.." #로그 역할
    

#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_tooja_urls.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()




#%% 테스트 코드 - DART 보고서 JSON 확인해서 투자설명서 본문 url 추출하기

#url 리스트
urls_list = txt_to_list('corp_DART_tooja_test.txt')

#url 하나만 추출
tmpurl=urls_list[0]

#string 추출
nav_tmp = code_to_html('',str(tmpurl),'')
str_tmp = str(nav_tmp).split("var cnt")[-1].split("var view")[0]

reportItems = str_tmp.split("text:")
reportItems = reportItems[1:]#1st element 제거

#보고서명 추출: 첫번째 [] 안의 숫자 변경하면 보고서명 바뀜
#reportName = reportItems[0].split("id:")[0].strip()
#보고서ID(viewDoc 안의 변수들 )
#reportId = reportItems[0].split("viewDoc(")[1].split(");}")[0].replace("'","").split(",")

#makeDARTurl: reportId(리스트) 변수 받아서 투자보고서 url로 변환
def makeDARTurl(lst):
    link = "http://dart.fss.or.kr/report/viewer.do?rcpNo=" + lst[0].strip() + "&dcmNo=" + \
        lst[1].strip() + "&eleId=" + lst[2].strip() + "&offset=" + lst[3].strip() + "&length=" + lst[4].strip() + "&dtd=" + lst[5].strip()
    return link


#writeline변수(한 줄당 쓸 내용) 설정
writeline = ""

#각 보고서별(웹사이트 열었을때 좌측 패널에 보이는 목록) 이름 및 url을 붙여넣기
for reportItem in reportItems:
    time.sleep(0.02)
    reportName = reportItem.split("id:")[0].strip()
    reportId = reportItem.split("viewDoc(")[1].split(");}")[0].replace("'","").split(",")
    
    if len(reportId) == 6:
        reportURL = makeDARTurl(reportId)
        writeline = writeline + reportName + '\t' + reportURL + '\t'
        #print writeline
    else: 
        print "error!! in", str(nav_tmp.title.contents), str(reportName)

lines =[]


lines.append(writeline)
#writeline변수 모아서 리스트 만들기
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_tooja_urls_test.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()






#%% 테스트 코드 - DART 웹주소에서 정정신고 및 보고서 본문 웹주소 추출하기
'''
#url 리스트
urls_list = txt_to_list('corp_DART_urls_test.txt')

lines =[]

#url 하나만 추출
tmpurl=urls_list[0]

nav_tmp = code_to_html('',str(tmpurl),'')
url_tags = nav_tmp.find_all(attrs={"class": "cen_txt"}) 


#writeline변수(한 줄당 쓸 내용) 설정
writeline = ""
for url_tag in url_tags:
    if url_tag != []:
        writeline = writeline + url_tag.contents[0].strip() + '\t'     


lines.append(writeline)
#writeline변수 모아서 리스트 만들기
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_bogoseo_list_test.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()
'''

#%% 실제 코드 - DART 웹주소에서 정정신고 및 보고서 본문 웹주소 추출하기
#url 리스트
urls_list = txt_to_list('corp_DART_urls.txt')
names_list = txt_to_list('corp_DART_names.txt')

#메모장에 입력할 리스트 initialize
lines = []
idx = 0
totalLen = len(urls_list)

#url 별로 print할 line 생성해서 lines 리스트에 append
for url in urls_list:
    #writeline변수(한 줄당 쓸 내용) 설정
    writeline = names_list[idx] + '\t'
    
    idx = idx + 1    
    
    nav_tmp = code_to_html('',str(url),'')
    url_tags = nav_tmp.find_all("a") # <a> tag element만 추출
    
    #formatting하는 부분: 
    #(보고서 이름 <tab> http://.... <tab>),  (보고서 이름 ,...) , ... 형식으로 formatting
    for url_tag in url_tags:
        time.sleep(0.1)
        if str(url_tag.get('href')).find("main") > 0:
            writeline = writeline + url_tag.get('title') + '\t' + "http://dart.fss.or.kr/" + url_tag.get('href') + '\t'
    
    #writeline변수 모아서 리스트 만들기
    lines.append(writeline)
    print "("+str(idx)+"/"+str(totalLen)+") recorded.." #로그 역할
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_bogoseo_list.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()

    
    
#%% 테스트 코드 - KIND URL에서 설립일자 추출하기

#url 리스트
urls_list = txt_to_list('corp_KIND_urls_test.txt')

#url 하나만 추출
tmpurl=urls_list[0]

nav_tmp = code_to_html('',str(tmpurl),'')
url_tags = nav_tmp.find_all("td")[:6] #맨 앞 6개 <td> tag element만 추출


#writeline변수(한 줄당 쓸 내용) 설정
writeline = ""

for url_tag in url_tags:
    if len(url_tag.contents) > 0:
        writeline = writeline + unicode(url_tag.contents[-1].strip()) + '\t'
        print writeline
lines =[]


lines.append(writeline)
#writeline변수 모아서 리스트 만들기
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_KIND_founddate_test.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()


#%% 실제 코드 - KIND URL에서 설립일자 추출하기


#url 리스트
urls_list = txt_to_list('corp_KIND_urls.txt')


#메모장에 입력할 리스트 initialize
lines = []

#url 리스트에 있는 각 element(KIND url)에서 각 줄에 적을 정보를 writeline에 저장
for url in urls_list:
    nav_tmp = code_to_html('',str(url),'')
    url_tags = nav_tmp.find_all("td")[:6] #맨 앞 6개 <td> tag element만 추출
    
    #writeline변수(한 줄당 쓸 내용) 설정
    writeline = ""
    
    for url_tag in url_tags:
        #writeline변수에 <td>태그 안의 내용 붙여넣기       
        if len(url_tag.contents) > 0:
            writeline = writeline + unicode(url_tag.contents[-1].strip()) + '\t'
    
    print writeline        

    #writeline변수 모아서 리스트 만들기    
    lines.append(writeline)

    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_KIND_founddate.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()




    
#%% 테스트 코드 - 회사명에서 DART 기업코드(8자리 숫자) 추출하기
'''
corp_list = txt_to_list('corp_names_test.txt')    
#print corp_name

#회사명 변수 추출
corp_name=corp_list[0]

#회사명 --> 회사코드(8자리숫자)로 전환하여 리스트 형태로 반환
# 그 과정에서 회사명과 회사코드를 합쳐서 프린트할 리스트(firm_code) 만듦
nav_tmp = code_to_html('http://dart.fss.or.kr/corp/searchCorp.ax?textCrpNm=',corp_name,'')
firm_tags = nav_tmp.find_all(attrs={"name": "hiddenCikCD1"})


#writeline변수(한 줄당 쓸 내용. 회사명, 회사코드1, 회사코드2, ...) 설정
writeline = corp_name + '\t'
#print writeline

for firm_tag in firm_tags:
     #writeline변수 회사코드 붙여넣기    
    writeline = writeline + unicode(firm_tag['value']) + '\t'

lines = []

lines.append(writeline)
#writeline변수 모아서 리스트 만들기
    
#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_codes_test.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()

'''

#%% 실제 코드 - 회사명에서 DART 기업코드(8자리 숫자) 추출하기


corp_list = txt_to_list('corp_names.txt')    
print corp_list

#메모장에 입력할 리스트 initialize
lines = []

for corp_name in corp_list:    
    #회사명 --> 회사코드(8자리숫자)로 전환하여 리스트 형태로 반환
    # 그 과정에서 회사명과 회사코드를 합쳐서 프린트할 리스트(firm_code) 만듦
    nav_tmp = code_to_html('http://dart.fss.or.kr/corp/searchCorp.ax?textCrpNm=',corp_name,'')
    firm_tags = nav_tmp.find_all(attrs={"name": "hiddenCikCD1"})
    
    #writeline변수(한 줄당 쓸 내용, 회사명, 회사코드1, 회사코드2, ...) 설정
    writeline = corp_name + '\t'
    #print writeline
    
    for firm_tag in firm_tags:
        #writeline변수 회사코드 붙여넣기    
        writeline = writeline + unicode(firm_tag['value']) + '\t'
    
    print writeline
    
    #writeline변수 모아서 리스트 만들기
    lines.append(writeline)


#반환한 리스트를 텍스트 파일에 입력    
f = open("corp_DART_codes.txt",'w')
for writeline in lines: 
    data = writeline +'\n'
    f.write(data) 
f.close()

