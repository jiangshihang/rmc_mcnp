# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 14:48:38 2018

@author: jiangsh16

function: change the format of rmc and mcnp input files before convertion
"""

import judge

def format_RMC(s_inp):
    '''
    function:
    1.replace all '\t' with blank;
    2.delete all '\r';
    3.delete all comments;
    4.add blanks around '=',':','&','(',')','!';
    5.delete redundant returns;
    6.change '!' into '#';
    7.delete blanks;
    8.delete more than three consecutive returns;
    '''
    
    s_inp = s_inp.upper()

    l_inp = list(s_inp)

    l_inp.append('\n')

    # replace all '\t' with blank
    for index in range(len(l_inp)):
        if l_inp[index] == '\t':
            l_inp[index] = ' '

    # delete all '\r'
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '\r':
            del l_inp[index]
            n_del = 1
            n_len_inp -= 1
        index = index - n_del + 1
        n_del = 0

    # add blanks around equals '='
    index = 0
    n_insert = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '=':
            l_inp.insert(index + 1, ' ')
            l_inp.insert(index, ' ')
            n_insert = n_insert + 2
            n_len_inp = n_len_inp + 2
        index = index + n_insert + 1
        n_insert = 0

    # delete comments
    # delete a comment line
    index = 1
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '/' and l_inp[index - 1] == '\n':
            del l_inp[index - 1]
            n_len_inp -= 1
        index += 1
    # delete comment at end of a line
    n_slash_count = 0
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '/' and n_slash_count != 2:
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
            n_slash_count = n_slash_count + 1
        if n_slash_count == 2 and l_inp[index] != '\n':
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
        if n_slash_count == 2 and l_inp[index] == '\n':
            n_slash_count = 0
        index = index - n_del + 1
        n_del = 0


    # delete redundant returns
    # delete returns with a blank following
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 1:
        if l_inp[index] == '\n' and l_inp[index + 1] == ' ':
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
        index = index - n_del + 1
        n_del = 0


    # delete returns at file beginning and ending
    # delete returns at file beginning
    while l_inp[0] == '\n':
        del l_inp[0]
    # delete all returns at file ending
    index = len(l_inp) - 1
    while l_inp[index] == '\n':
        del l_inp[index]
        index = index - 1
    # add a return at file ending
    l_inp.append('\n')

    # add ' ' around ':' and '&' and '()'and'!'
    index = 0
    n_insert = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if judge.judge5(l_inp[index],':','&','(',')','!'):
            l_inp.insert(index + 1, ' ')
            l_inp.insert(index, ' ')
            n_insert = n_insert + 2
            n_len_inp = n_len_inp + 2
        index = index + n_insert + 1
        n_insert = 0
    
    # change '!' into '#'
    index = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 1:
        if l_inp[index] == '!':
            l_inp[index] = '#'
        index = index + 1


    # delete blanks
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 1:
        if l_inp[index] == ' ' and (l_inp[index + 1] == ' ' or l_inp[index + 1] == '\n'):
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
        index = index - n_del + 1
        n_del = 0
    
    # delete more than three consecutive returns
    index = 2
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '\n' and l_inp[index - 1] == '\n' and l_inp[index - 2] == '\n':
            del l_inp[index]
            n_del += 1
            n_len_inp -= 1
        index = index - n_del + 1
        n_del = 0
        
    return ''.join(l_inp)

def format_MCNP(s_inp):
    """
    function:
    1.delete all comments;
    2.delete the first line;
    3.join the splited lines together;
    4.add ' ' around '=',':','#','(',')';
    5.change '#' into '!';
    6.delete returns;
    7.delete blanks;
    """
    s_inp = s_inp.upper()

    l_inp = list(s_inp)

    l_inp.append('\n')

    # delete all comments
    index = 1
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == 'C' and l_inp[index - 1] == '\n':
            index2 = l_inp[index:].index('\n')
            del l_inp[index:(index + index2 + 1)]
            index = index - 1
            n_len_inp = len(l_inp)
        index += 1

    n_slash_count = 0
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '$' :
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
            n_slash_count = n_slash_count + 1
        if n_slash_count == 1 and l_inp[index] != '\n':
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
        if n_slash_count == 1 and l_inp[index] == '\n':
            n_slash_count = 0
        index = index - n_del + 1
        n_del = 0

    # delete the first line
    while 1:
        if l_inp[0] != '\n':
            del l_inp[0]
        else:
            del l_inp[0]
            break

    # join the splited lines together
    # when there is & at the end of a line,delete it and add the next line
    index = 0
    j = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 1:
        if l_inp[index] == '&':
            del l_inp[index]
            j = 0
            while l_inp[index] == ' ' or l_inp[index] == '\n':
                j = j + 1
                del l_inp[index]
                l_inp.insert(index,' ')
        n_len_inp = n_len_inp - j
        index = index + 1
        
    # when a line begin after 5 or more blanks, add it to the line before it.
    index = 0
    j = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 6:
        if l_inp[index] == '\n':
            while l_inp[index+1]==' ':
                del l_inp[index+1]
                n_len_inp = n_len_inp - 1
                j = j + 1
            if j >= 5 and l_inp[index+1]!='\n':
                del l_inp[index]
                n_len_inp = n_len_inp - 1
        j = 0
        index = index + 1
            

    # add ' ' around '=' and ':'
    index = 0
    index = 0
    n_insert = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if judge.judge5(l_inp[index],':','=','(',')','#'):
            l_inp.insert(index + 1, ' ')
            l_inp.insert(index, ' ')
            n_insert = n_insert + 2
            n_len_inp = n_len_inp + 2
        index = index + n_insert + 1
        n_insert = 0

    
    # change '#' into '！'
    index = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 1:
        if l_inp[index] == '!':
            l_inp[index] = '#'
        index = index + 1
    
    # delete redundant returns
    # delete blanks at the beginning of a line
    index = 0
    j = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '\n':
            j = 0
            if l_inp[index + 1] == ' ':
                del l_inp[index + 1]
                j = j + 1
            if j != 0:
                del l_inp[index]
        n_len_inp = n_len_inp - j
        index = index + 1


    # delete returns at file beginning and ending
    # delete returns at file beginning
    while l_inp[0] == '\n':
        del l_inp[0]
    # delete all returns at file ending
    index = len(l_inp) - 1
    while l_inp[index] == '\n':
        del l_inp[index]
        index = index - 1
    # add a return at file ending
    l_inp.append('\n')

    # delete more than two ' 's
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 1:
        if l_inp[index] == ' ' and l_inp[index + 1] == ' ':
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
        index = index - n_del + 1
        n_del = 0

    return ''.join(l_inp)
    