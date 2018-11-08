# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 15:27:39 2018

功能：判断是否为符合的字符

@author: dell
"""

def judge1(x,a):
    if x == a:
        return True
    else:
        return False
    
def judge2(x,a,b):
    if x == a:
        return True
    elif x == b:
        return True
    else:
        return False
    
def judge3(x,a,b,c):
    if x ==a:
        return True
    elif x ==b:
        return True
    elif x ==c:
        return True
    else:
        return False
    
def judge4(x,a,b,c,d):
    if x ==a:
        return True
    elif x ==b:
        return True
    elif x ==c:
        return True
    elif x==d:
        return True
    else:
        return False
    
def judge5(x,a,b,c,d,e):
    if x ==a:
        return True
    elif x ==b:
        return True
    elif x ==c:
        return True
    elif x==d:
        return True
    elif x ==e:
        return True
    else:
        return False
    
def isnumber(s_num):   #判断某个字符串是否是数字（含负数情况）
    l_num = list(s_num)
    i_leng = len(l_num)
    p = 0
    while p < i_leng:
        if judge4(l_num[p],'-','.',')','('):
            del l_num[p]
            p = p - 1
            i_leng -= 1
        p = p + 1
    s_num = ''.join(l_num)
    return s_num.isdigit()