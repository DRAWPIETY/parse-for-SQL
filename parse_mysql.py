import ply.lex as lex
import ply.yacc as yacc
import re
from math import *

class node:
    def __init__(self, data):
        self._data = data
        self._children = []

    def getdata(self):
        return self._data

    def getchildren(self):
        return self._children

    def add(self, node):
        self._children.append(node)

    def print_node(self, prefix):
        print ('  ' * prefix, '+', self._data)
        for child in self._children:
            child.print_node(prefix + 1)


# TOKENS
tokens = ('SELECT', 'FROM', 'ORDER', 'BY', 'NAME', 'AVG', 'LP', 'RP',)
t_LP = r'\('
t_RP = r'\)'
literals = ['=', '+', '-', '*', '^', '>', '<']


# DEFINE OF TOKENS
def t_AVG(t):
    r'AVG'
    return t


def t_SELECT(t):
    r'SELECT'
    return t


def t_FROM(t):
    r'FROM'
    return t


def t_ORDER(t):
    r'ORDER'
    return t


def t_BY(t):
    r'BY'
    return t


def t_NAME(t):
    r'[A-Za-z]+|[a-zA-Z_][a-zA-Z0-9_]*|[A-Z]*\.[A-Z]$'
    return t


# IGNORED
t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# LEX ANALYSIS
lex.lex()


# PARSING
def p_query(t):
    '''query :  select '''
    t[0] = t[1]


def p_select_1(t):
    '''select :  SELECT list FROM table ORDER BY list '''
    t[0] = node('QUERY')
    t[0].add(node('[SELECT]'))
    t[0].add(t[2])
    t[0].add(node('[FROM]'))
    t[0].add(t[4])
    t[0].add(node('[ORDER BY]'))
    t[0].add(t[7])


def p_select_2(t):
    '''select :  SELECT AVG LP list RP FROM table'''
    t[0] = node('QUERY')
    t[0].add(node('[SELECT]'))
    t[0].add(node('[AVG]'))
    t[0].add(t[4])
    t[0].add(node('[FROM]'))
    t[0].add(t[7])


def p_table(t):
    '''table : NAME '''
    if len(t) == 2:
        t[0] = node('[TABLE]')
        t[0].add(node(t[1]))


def p_list(t):
    ''' list : '*'
             | NAME
            '''
    t[0] = node('[FIELD]')
    t[0].add(node(t[1]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()


def readFile(dress):
    try:
        openFile = open(dress, 'r')
    except:
        print('File open error')
    else:
        firstLine = openFile.readline()  # Jump across the first
        lis = []
        for line in openFile:
            lis.append(list(eval(line)))
        openFile.close()
        return lis


def element(lst):
    return lst[dic[orderName]]

def run_sql(command):
    parse = yacc.parse(command)
    son_List = parse.getchildren()

    listName = []
    tableName = []

    if len(son_List)==5:
        for m in son_List[2].getchildren():
            listName.append(m.getdata())
        for m in son_List[4].getchildren():
            tableName.append(m.getdata()+'.csv')
        lst = readFile(tableName[0])
        sum = 0
        for m in lst:
            for e in listName:
                sum +=m[dic[e]]
        print('average value is %d' % (sum/len(lst)))

    if len(son_List) == 6:
        global orderName
        for m in son_List[1].getchildren():
            listName.append(m.getdata())
        for m in son_List[3].getchildren():
            tableName.append(m.getdata()+'.csv')
        orderName = son_List[5].getchildren()[0].getdata()
        lst = readFile(tableName[0])
        lst.sort(key=element)
        if listName[0] == '*':
            for m in lst:
                print(m)
        else:
            for m in lst:
                for name in listName:
                    print(m[dic[name]])


if __name__ == '__main__':
    dic = {'sno': 0, 'chinese': 1, 'math': 2, 'english': 3, 'sum': 4,}

    sum = 'SELECT AVG (sum) FROM student'
    print('-------测试sum的平均值-------')
    run_sql(sum)

    math = 'SELECT AVG (math) FROM student'
    print('-------测试math的平均值-------')
    run_sql(math)

    s = 'SELECT * FROM student ORDER BY sum'
    print('-------输出按sum排序后的表-------')
    run_sql(s)

    ss = 'SELECT sno FROM student ORDER BY math'
    print('-------输出按math排序后的sno列-------')
    run_sql(ss)


