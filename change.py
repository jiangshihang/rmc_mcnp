# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 15:42:50 2018

本脚本包含所有的含有转换的函数

@author: dell
"""
import judge

#把RMC里的曲面布尔定义转化成MCNP里的曲面布尔定义
def change_surf_bool_RM(l_bool_0):
    l_bool_1 = []
    i = 0
    while i < len(l_bool_0):
        if judge.judge2(l_bool_0[i],'(',')')==False:
            l_bool_1.append(l_bool_0[i])
        else:
            if judge.judge1(l_bool_0[i],'('):
                j = i
                k = 1
                while(k!=0):
                    j = j + 1
                    if judge.judge1(l_bool_0[j],'('):
                        k = k + 1;
                    if judge.judge1(l_bool_0[j],')'):
                        k = k - 1;
                        #while循环结束后，j应表示之前的'('对应的')'
                l_bool_new = l_bool_0[i+1:j]
                l_bool_new = change_surf_bool_RM(l_bool_new) #递归
                l_bool_new.insert(0,'(')
                l_bool_new.append(')')
                s_bool_new = ''.join(l_bool_new)
                l_bool_1.append(s_bool_new)
                i = j
        i = i + 1
    #将括号内的内容作为一个整体，下面将针对&和：插入括号
    m = 0
    count = 0
    len2 = (len(l_bool_1))
    while(m<len2-1):
        if judge.judge2(l_bool_1[m],':','&'):
            if judge.judge1(l_bool_1[m],':'):
                n = m
                p = 0
                count=count+1
                if count == 1:
                    #找到第一个:前需要插入左括号的地方
                    m0 = m - 1
                    while l_bool_1 != ' ' and m0 > 0:
                        m0 = m0 - 1
                while judge.judge1(l_bool_1[n],'&')== False:
                    #找到需要插入右括号的位置，找不到则p=1
                    n = n + 1
                    if n > len(l_bool_1)-1:
                        p = 1
                        break
                if p == 0:
                    l_bool_1.insert(n,')')
                    l_bool_1.insert(m0,'(')
                    len2 = len2 + 2
                    m = m + 1
        m = m + 1
    for i in range(len(l_bool_1)):
            if l_bool_1[i] == '&':
                l_bool_1[i] = ' '    
    
    return l_bool_1
    
        