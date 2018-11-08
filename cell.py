# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 19:45:21 2018, modified on Tue Aug  28 2018

@author: jiangsh16

function: cell input card
"""

import rm
import mr
import change

class cell:
    def __init__(self):
        self.name = 'CELL'
        self.id = 0
        self.surf_bool_definition = []
        self.mat = -1
        self.vol = 1.0
        self.tmp = 293.6
        self.void = 0
        self.fill = 0
        self.inner = 0

    def readRMC(self, s_line):
        ##print(s_line)
        l_line = s_line.split(' ')
        l_line = rm.format_line(l_line)
        l_line.pop(0)
        self.id = l_line.pop(0)
        i = l_line.count('MAT')
        if i != 0:
            j = l_line.index('MAT')
            self.mat = int(l_line[j + 1])
            del l_line[j:j + 2]
        i = l_line.count('VOL')
        if i != 0:
            j = l_line.index('VOL')
            self.vol = float(l_line[j + 1])
            del l_line[j:j + 2]
        i = l_line.count('TMP')
        if i != 0:
            j = l_line.index('TMP')
            self.tmp = float(l_line[j + 1])
            del l_line[j:j + 2]
        i = l_line.count('VOID')
        if i != 0:
            j = l_line.index('VOID')
            self.void = int(l_line[j + 1])
            del l_line[j:j + 2]
        i = l_line.count('INNER')
        if i != 0:
            j = l_line.index('INNER')
            self.inner = l_line[j + 1]
            del l_line[j:j + 2]
        i = l_line.count('FILL')
        if i != 0:
            j = l_line.index('FILL')
            self.fill = int(l_line[j + 1])
            del l_line[j:]
        self.surf_bool_definition = l_line

    def writeRMC(self):
        s = 'CELL ' + str(self.id) + ' '
        l_bool = [str(i) for i in self.surf_bool_definition]
        s = s + ' '.join(l_bool)
        if self.mat != -1:
            s = s + ' MAT=' + str(self.mat[0])
        if self.void == '1':
            s = s + ' VOID=1'
        if self.fill != 0:
            s = s + ' FILL=' + str(self.fill)
        s = s + '\n'
        return s


    def readMCNP(self,u,l_line):
        self.id = l_line[0]
        self.mat = l_line[1:3]
        if l_line.count('U') != 0:
            j = l_line.index('U')
        elif l_line.count('FILL') != 0:
            j = l_line.index('FILL')
            self.fill = l_line[j+1]
        else:
            j = l_line.index('IMP')
        if u == 0 and l_line[1] == '0':
            l_surf_bool_definition = l_line[2:j]
        else:
            l_surf_bool_definition = l_line[3:j]
        self.surf_bool_definition = mr.change_bool(l_surf_bool_definition)
        j = l_line.index('IMP')
        self.void = str(1 - int(l_line[j+3]))

    def writeMCNP1(self, number, l_blocklist):
        s = ''
        s = s + str(self.id)
        if self.mat == -1 or self.mat== 0:
            s = s + ' 0 '
        else:
            s = s + ' ' + str(self.mat)
            s_density = rm.find_density(self.mat, l_blocklist)
            s = s + ' ' + str(s_density) + ' '
        l_bool = self.surf_bool_definition[:]
        l_bool = change.change_surf_bool_RM(l_bool)
        s = s + ''.join(l_bool)
        
        if self.fill != 0:
            s = s + ' FILL=' + str(self.fill)
        imp = 1 - self.void
        s = s + ' imp:n=' + str(imp)
        s = s + '\n'

        return s

    def writeMCNP(self, number, l_blocklist):
        s = ''
        s = s + str(self.id)
        s = s + ' ' + str(self.mat)
        s_density = rm.find_density(self.mat, l_blocklist)
        s = s + ' ' + str(s_density) + ' '
        l_bool = self.surf_bool_definition[:]
        l_bool = change.change_surf_bool_RM(l_bool)
        s = s + ''.join(l_bool)
        
        s = s + ' u=' + str(number)
        imp = 1 - self.void
        s = s + ' imp:n=' + str(imp)
        s = s + '\n'

        return s
