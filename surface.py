# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 19:26:09 2018

@author: jiangsh16

function: surface input card
"""

import rm
import mr

class surface:
    def __init__(self):
        self.element = []

    def readRMC(self, s_block):
        l_line = s_block.split('\n')
        for i in range(1, len(l_line)):
            c_surf = surf()
            c_surf.readRMC(l_line[i])
            self.element.append(c_surf)

    def writeMCNP(self, l_key, l_blocklist):
        s = '\n'
        for c in self.element:
            s = s + c.writeMCNP()
        return s

    def readMCNP(self,s_surface):
        l_surf = s_surface.split('\n')
        for s_line in l_surf:
            c_surf = surf()
            c_surf.readMCNP(s_line)
            self.element.append(c_surf)

    def writeRMC(self):
        s = 'SURFACE\n'
        for c in self.element:
            s = s + c.writeRMC()
        return s


class surf:
    def __init__(self):
        self.name = ''
        self.id = 0
        self.type = 'PX'
        self.params = []
        self.bc = 0

    def readRMC(self, s_line):
        l_line = s_line.split(' ')
        l_line = rm.format_line(l_line)
        self.id = int(l_line[1])
        self.type = l_line[2]
        if s_line.find('BC') == -1:
            l_params = l_line[3:]
        else:
            i = l_line.index('BC')
            self.bc = l_line[i + 1]
            l_params = l_line[3:i]
        self.params = [float(s) for s in l_params]

    def readMCNP(self,s_line):
        l_line = s_line.split(' ')
        l_line = rm.format_line(l_line)
        self.id = int(l_line[0])
        self.type = l_line[1]
        if s_line.find('BC') == -1:
            l_params = l_line[2:]
        else:
            i = l_line.index('BC')
            self.bc = l_line[i + 1]
            l_params = l_line[2:i]
        self.params = [float(s) for s in l_params]

    def writeRMC(self):
        l_params = [str(s) for s in self.params]
        s1 = 'SURF '+ str(self.id) + ' ' + self.type + ' ' + ' '.join(l_params) + '\n'
        return s1

    def writeMCNP(self):
        l_params = [str(s) for s in self.params]
        s1 = str(self.id) + ' ' + self.type + ' ' + ' '.join(l_params) + '\n'
        return s1
