# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 19:39:19 2018

@author: jiangsh16

function: universe input card
"""

import rm
import mr
import cell

class universe:
    def __init__(self):
        self.name = ''
        self.id = 0
        self.move = [0, 0, 0]
        self.rotate = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.lat = 0
        self.pitch = [0, 0, 0]
        self.scope = [0, 0, 0]
        self.sita = 60
        self.fill = []
        self.surf_bool = [1, 2, 3, 4, 5, 6]
        self.cells = []

    def readRMC(self, s_block):
        l_line = s_block.split('\n')
        if len(l_line) == 1:
            l_line = l_line[0].split(' ')
            l_line = rm.format_line(l_line)
            l_line.pop(0)
            self.id = l_line.pop(0)
            i = l_line.count('MOVE')
            if i != 0:
                j = l_line.index('MOVE')
                l_move = l_line[j + 1:j + 4]
                self.move = [float(s) for s in l_move]
                del l_line[j:j + 4]

            i = l_line.count('ROTATE')
            if i != 0:
                j = l_line.index('ROTATE')
                l_rotate = l_line[j + 1:j + 10]
                self.rotate = [float(s) for s in l_rotate]
                del l_line[j:j + 10]
            i = l_line.count('FILL')
            if i != 0:
                j = l_line.index('FILL')
                l_fill = l_line[j + 1:]
                self.fill = [int(s) for s in l_fill]
                del l_line[j:]
            i = l_line.count('LAT')
            if i != 0:
                j = l_line.index('LAT')
                self.lat = l_line[j + 1]
                j = l_line.index('PITCH')
                l_pitch = l_line[j + 1:j + 4]
                self.pitch = [float(s) for s in l_pitch]
                if self.lat == '1':
                    j = l_line.index('SCOPE')
                    l_scope = l_line[j + 1:j + 4]
                    self.scope = [int(s) for s in l_scope]
                elif self.lat == '2':
                    j = l_line.index('SCOPE')
                    self.scope = l_line[j + 1:j + 3]
                    l_scope = l_line[j + 1:j + 4]
                    self.scope = [int(s) for s in l_scope]
                    j = l_line.index('SITA')
                    self.sita = float(l_line[j + 1])
        else:
            l_line0 = l_line[0].split(' ')
            l_line0.pop()
            self.id = l_line0.pop(0)
            i = l_line.count('MOVE')
            if i != 0:
                j = l_line.index('MOVE')
                l_move = l_line[j + 1:j + 4]
                self.move = [float(s) for s in l_move]
                del l_line[j:j + 4]
            for i in range(1, len(l_line)):
                c_cell =cell. cell()
                c_cell.readRMC(l_line[i])
                self.cells.append(c_cell)


    def writeRMC(self):
        s = 'UNIVERSE ' + str(self.id)
        if self.move != [0, 0, 0] and self.move != []:
            l_move = [str(i) for i in self.move]
            s = s + ' MOVE=' + ' '.join(l_move)
        if self.cells == []:
            s = s + ' LAT=' + str(self.lat)
            l_pitch = [str(i) for i in self.pitch]
            s = s + ' PITCH=' + ' '.join(l_pitch)
            l_scope = [str(i) for i in self.scope]
            s = s + ' SCOPE=' + ' '.join(l_scope)
            s = s + ' FILL =\n '
            j_row = self.scope[0]
            for i in range(0, j_row):
                if i == 0:
                    s = s + ' ' + ' '.join(self.fill[i * j_row:i * j_row + j_row]) + '\n'
                else:
                    s = s + '  ' + ' '.join(self.fill[i * j_row:i * j_row + j_row]) + '\n'

        else:
            s = s + '\n'
            for c_cell in self.cells:
                s = s + c_cell.writeRMC()
        return s


    def readMCNP(self,u,l_line,l_blocklist):
        self.id = u
        i = l_line.count('LAT')     #默认不含LAT的UNIVERSE都是包含CELL子单元的
        if i == 0:
            c_cell = cell.cell()
            c_cell.readMCNP(u,l_line)
            self.cells.append(c_cell)
        else:
            l_line = rm.format_line(l_line)
            j = l_line.index('LAT')
            self.lat = l_line[j+1]
            if l_line.count('IMP:N') != 0:
                j = l_line.index('IMP:N')
                self.void = str(1 - int(l_line[j+1]))
            if l_line[1] == '0':
                i = 2
            else:
                i = 3
            j = i
            while l_line[j] != 'U':
                 j = j + 1
            self.surf_bool = l_line[i:j]
            j = l_line.index('FILL')
            self.scope[0] = mr.getscope(l_line[j+1:j+4])
            self.scope[1] = mr.getscope(l_line[j+4:j+7])
            self.scope[2] = mr.getscope(l_line[j+7:j+10])
            self.fill = l_line[j+10:]
            self.pitch = mr.getpitch(self.surf_bool,l_blocklist)

        self.move = mr.getmove(u,l_blocklist,self)


    def readMCNP_con(self,u,l_line):
        c_cell = cell.cell()
        c_cell.readMCNP(u,l_line)
        self.cells.append(c_cell)

    def writeMCNP(self, l_key, l_blocklist):
        s = ''
        if l_key[1] == 0:   #如果是universe0
            for c in self.cells:
                s = s + c.writeMCNP1(l_key[1], l_blocklist)

        else:
            if self.cells == []:    #如果是填充阵列
                s = s + str(self.id) + ' 1 -1.0 '
                l_surf_bool = rm.find_surface(self.id,self.pitch,l_blocklist)
                s = s + ' '.join(l_surf_bool)
                s = s + ' u=' + str(self.id)
                s = s + ' lat=' + str(self.lat)
                s = s + ' imp:n=1'
                s = s + ' fill='
                x1 = -(self.scope[0] - 1) / 2
                x2 = (self.scope[0] - 1) / 2
                y1 = -(self.scope[1] - 1) / 2
                y2 = (self.scope[1] - 1) / 2
                z1 = -(self.scope[2] - 1) / 2
                z2 = (self.scope[2] - 1) / 2
                s = s + str(x1) + ':' + str(x2) + ' '
                s = s + str(y1) + ':' + str(y2) + ' '
                s = s + str(z1) + ':' + str(z2) + '&\n'
                j_row = self.scope[0]
                l_fill = [str(i) for i in self.fill]
                for i in range(0, j_row):
                    if i < j_row - 1:
                        s = s + '  ' + ' '.join(l_fill[i * j_row:i * j_row + j_row]) + ' &\n'
                    else:
                        s = s + '  ' + ' '.join(l_fill[i * j_row:i * j_row + j_row]) + '\n'

            else:
                for c in self.cells:
                    s = s + c.writeMCNP(l_key[1], l_blocklist)
        return s
