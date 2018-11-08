# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 21:20:18 2018

@author: jiangsh16
"""

import rm
import mr
import format

print("欢迎使用RMC-MCNP输入卡互转程序")
print("1：RMC转MCNP,2：MCNP转RMC")
str = input("请输入转换模式：")
name = input("请输入待转换文件名：")
name2 = input("请输入生成的文件名：")

if str == "1":
    s2 = format.format_RMC(open(name, 'r').read())
    l1 = rm.read_RMC(s2)
    l1 = rm.change_list(l1)
    ss2 = rm.write_MCNP(l1)
    f_ss2 = open(name2, 'w')
    f_ss2.write(ss2)
    f_ss2.close()
    
if str == "2":
    s1 = format.format_MCNP(open(name, 'r').read())
    l2 = mr.read_MCNP(s1)
    l2 = mr.change_list2(l2)
    ss1 = mr.write_RMC(l2)
    f_ss1 = open(name2, 'w')
    f_ss1.write(ss1)
    f_ss1.close()