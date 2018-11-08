# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 19:47:56 2018

@author: jiangsh16

function: mateial input card
"""

import rm
import mr

class material:
    def __init__(self):
        self.element = []

    def readRMC(self, s_block):
        l_line = s_block.split('\n')
        for i in range(1, len(l_line)):
            if l_line[i][0] == 'M':
                c_mat = mat()
                c_mat.readRMC(l_line[i])
                self.element.append(c_mat)
            if l_line[i][0] == 'S':
                c_sab = sab()
                c_sab.readRMC(l_line[i])
                self.element.append(c_sab)

    def writeRMC(self):
        s = 'MATERIAL\n'
        for c in self.element:
            s = s + c.writeRMC()
        return s

    def readMCNP(self,s_material,l_blocklist):
        l_mat = s_material.split('\n')
        i = len(l_mat)
        if l_mat[i-1] == '':
            l_mat.pop()
        for s_mat in l_mat:
            if s_mat[1] == 'T':
                c_mat = sab()
                c_mat.readMCNP(s_mat)
            else:
                c_mat = mat()
                c_mat.readMCNP(s_mat,l_blocklist)
            self.element.append(c_mat)

    def writeMCNP(self,l_key, l_blocklist):
        s = ''
        for c in self.element:
            s = s + c.writeMCNP()
        return s


class mat:
    def __init__(self):
        self.name = 'mat'
        self.id = 0
        self.density = 0
        self.zaid = []

    def readRMC(self, s_line):
        l_line = s_line.split(' ')
        l_line = rm.format_line(l_line)
        self.id = l_line[1]
        self.density = l_line[2]
        l_zaid = l_line[3:]
        z = int(len(l_zaid)/2)
        self.zaid = []
        for i in range(z):
            self.zaid.append(l_zaid[2*i]+' '+l_zaid[2*i+1])
        if self.density == '0':
            self.density = calculate(self.zaid)

    def readMCNP(self,s_mat,l_blocklist):
        self.id = s_mat[1]
        l_line = s_mat.split(' ')
        self.zaid = l_line[1:]
        self.density = mr.finddensity1(self.id,l_blocklist)

    def writeRMC(self):
        s1 = 'MAT ' + str(self.id)+ ' ' + str(self.density) + '\n    '
        s1 = s1 + ' '.join(self.zaid) + '\n'
        return s1

    def writeMCNP(self):
        s = ''
        s = s + 'm' + str(self.id) + ' '
        s = s + '&\n '.join(self.zaid)
        s = s + '\n'
        return s


class sab:
    def __init__(self):
        self.name = 'sab'
        self.id = 0
        self.zaid = []

    def readRMC(self, s_line):
        l_line = s_line.split(' ')
        l_line = rm.format_line(l_line)
        self.id = l_line[1]
        self.zaid = l_line[2:]

    def readMCNP(self,s_mat):
        self.id = s_mat[2]
        l_line = s_mat.split(' ')
        self.zaid = l_line[1:]

    def writeRMC(self):
        s = 'SAB '
        s = s + str(self.id) + ' '
        s = s + ' '.join(self.zaid)
        s = s + '\n'
        return s

    def writeMCNP(self):
        s = ''
        s = s + 'mt' + str(self.id) + ' '
        s = s + ' '.join(self.zaid)
        s = s + '\n'
        return s

#当density输入为0的时候，自动计算density
def calculate(l_zaid):
    i_total = 0
    for s_zaid in l_zaid:
        l_0 = s_zaid.split(' ')
        s_1 = l_0[1]
        if s_1.find('E') == -1:
            i_1 = float(s_1)
        else:
            l_2 = s_1.split('E')
            i_0 = float(l_2[0])
            i_r = int(l_2[1])
            i_1 = i_0 * (10**i_r)
        i_total = i_total + i_1
    return i_total