# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 14:47:46 2018

@author: jiangsh16

function: change rmc format to mcnp format
"""

import surface
import universe
import cell
import material
#import criticality
#import plot
import format

def read_RMC(s_inp):
    l_blockstring = s_inp.split('\n\n')
    l_blocklist = [getblocklist(s) for s in l_blockstring]
    return l_blocklist

def change_list(l_blocklist):
    #function: change the order of keys in the list, for the next step to write
    l_i = []
    l_j = []
    l_k = []
    for l_key in l_blocklist:
        if l_key[0] == 'MATERIAL':
            i = l_blocklist.index(l_key)
            l_i = l_key
        if l_key[0] == 'SURFACE':
            j = l_blocklist.index(l_key)
            l_j = l_key
        if l_key[0] == 'CRITICALITY':
            k = l_blocklist.index(l_key)
            l_k = l_key

    l_blocklist[i] = l_k
    l_blocklist[j] = l_j
    l_blocklist[k] = l_i
    return l_blocklist

def write_MCNP(l_blocklist):
    s_out = 'MCNP\n'
    for l_key in l_blocklist:
        c_block = l_key[2]
        if c_block != -1:
            s_out = s_out + c_block.writeMCNP(l_key, l_blocklist)
        else:
            s_out = s_out + '\nNOT CONVERTED BLOCK: ' + l_key[0] + '\n'
#    s_out = format.short_line(s_out)
    return s_out


def getblocklist(s_block):
    l_blockkey = ['', 0,0]  # [name,number,content]
    l_blockkey[0] = getblockname(s_block)
    l_blockkey[1] = getblocknumber(s_block)
    l_blockkey[2] = getblockkey(l_blockkey[0], s_block)
    return l_blockkey


def getblockname(s_block):
    l_block_word = s_block.split(' ')
    l_block_word1 = l_block_word[0].split('\n')
    return l_block_word1[0]


def getblocknumber(s_block):
    l_block_word = s_block.split('\n')
    l_block_word1 = l_block_word[0].split(' ')
    if len(l_block_word1) == 1:
        return -1
    s_block_number = l_block_word1[1]
    if s_block_number.isdigit():
        return int(s_block_number)
    else:
        return -1


def getblockkey(s_keyname, s_block):
    if s_keyname == 'SURFACE':
        c_surface = surface.surface()
        c_surface.readRMC(s_block)
        return c_surface
    if s_keyname == 'UNIVERSE':
        c_universe = universe.universe()
        c_universe.readRMC(s_block)
        return c_universe
    if s_keyname == 'MATERIAL':
        c_material = material.material()
        c_material.readRMC(s_block)
        return c_material
#    if s_keyname == 'CRITICALITY':
#        c_criticality = criticality.criticality()
#        c_criticality.readRMC(s_block)
#        return c_criticality
#    if s_keyname == 'PLOT':
#        c_plot = plot.plot()
#        c_plot.readRMC(s_block)
#        return c_plot
    else:
        return -1

def format_line(l_word):
    n = l_word.count('')
    for i in range(n):
        l_word.remove('')        #移除列表中可能产生的空字符
    n = l_word.count('=')
    for i in range(n):
        l_word.remove('=')
    return l_word

def find_density(number, l_blocklist):
    # function: find the density of one material in blocklist
    l_material = []
    number = str(number)
    for l_block in l_blocklist:
        if l_block[0] == 'MATERIAL':
            l_material = l_block
            break
    c_material0 = l_material[2]
    l_material_line = c_material0.element
    for c_mat_or_sab in l_material_line:
        if c_mat_or_sab.id == number and c_mat_or_sab.name == 'mat':
            return c_mat_or_sab.density

def find_surface(id,l_pitch,l_blocklist):
    id = int(id)
    l_surf_bool = []
    x1 = -l_pitch[0]/2
    x2 = l_pitch[0]/2
    y1 = -l_pitch[1]/2
    y2 = l_pitch[1]/2
    l_surface = []
    for l_block in l_blocklist:
        if l_block[0] == 'SURFACE':
            l_surface = l_block
            break
    c_surface = l_surface[2]
    l_surf = c_surface.element
    for c_surf in l_surf:
        if c_surf.type == 'PX' and c_surf.params[0] == x1:
            l_surf_bool.append(str(c_surf.id))
    for c_surf in l_surf:
        if c_surf.type == 'PX' and c_surf.params[0] == x2:
            l_surf_bool.append('-'+str(c_surf.id))
    for c_surf in l_surf:
        if c_surf.type == 'PY' and c_surf.params[0] == y1:
            l_surf_bool.append(str(c_surf.id))
    for c_surf in l_surf:
        if c_surf.type == 'PY' and c_surf.params[0] == y2:
            l_surf_bool.append('-'+str(c_surf.id))
    if l_pitch[2] == 1:
        for l_block in l_blocklist:
            if l_block[0] == 'UNIVERSE' and l_block[1] == 0:
                l_cell = l_block[2]
                break
        for c_cell in l_cell.cells:
            if int(c_cell.fill) == id:
                l_surf_cell = c_cell.surf_bool_definition
                if len(l_surf_cell) > 7:
                    l_surf_bool.append(l_surf_cell[8])
                    l_surf_bool.append(l_surf_cell[10])

    return l_surf_bool