# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 21:06:25 2016

@author: Administrator
"""

# -*- coding: utf8 -*-
 
# 유니코드로 다루기 예제1
hoo = unicode('한글', 'utf-8')
print str(hoo.encode('utf-8'))
 
# 유니코드로 다루기 예제2
bar = '한글'.decode('utf-8')
print bar.encode('utf-8')
 
# 유니코드로 다루기 예제3
foo = u'한글'
print str(foo.encode('utf-8'))