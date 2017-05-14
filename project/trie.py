import sys
import time
from collections import deque
import csv
import pandas as pd
import xlrd
from collections import defaultdict
from Lib import linecache
from e import *


class Node:
    def __init__(self, character, parent):
        self.character = character
        if self.character is not None:
            self.character = self.character.lower()
        self.parent = parent
        self.children = dict()
        self.terminus = False

    def add(self, child_node):
        self.children[child_node.character] = child_node


class Trie:

    def __init__(self):
        self._root = Node(None, None)

    def insert(self, word):
        if word:
            current_node = self._root
            for i, character in enumerate(self._normalize_word(word)):
                if character in current_node.children:
                    current_node = current_node.children[character]
                else:
                    child_node = Node(character, current_node)
                    current_node.add(child_node)
                    current_node = child_node
            current_node.terminus = True

    def __contains__(self, item):
        current_node = self._root
        contained = True
        for symbol in self._normalize_word(item):
            if symbol in current_node.children:
                current_node = current_node.children[symbol]
            else:
                contained = False
                break
        return contained and current_node.terminus

    def _normalize_word(self, word):
        return word.strip().lower()

    def _get_all_words(self, prefix, node, word_list):
        if node.character:
            prefix.append(node.character)
        for child in node.children.values():
            self._get_all_words(prefix, child, word_list)
        if node.terminus:
            word_list.append("".join([i[0] for i in prefix]))
        if len(prefix) > 0:
            prefix.pop()

    def get_possible_words(self, prefix):
        current_node = self._root
        found_prefix = True
        word_list = []
        prefix_deque = deque()
        for symbol in prefix.strip().lower():
            if symbol in current_node.children:
                current_node = current_node.children[symbol]
            else:
                found_prefix = False
                break
        if found_prefix:
            self._get_all_words(prefix_deque, current_node, word_list)
            
        word_list = list(map(lambda word: prefix[:len(prefix)-1] + word, word_list))

        return word_list

    def get_all_words(self):
        word_list = []
        self._get_all_words(deque(), self._root, word_list)
        return word_list

if __name__ == '__main__':
    t=Trie()

    file = open("read.txt", "r")
    count=0
    flag=0
    weight=0

    
    for line in file:
        count=count+1
        t.insert(line)

    file.close()
    print(" enter the seed url")
    url_initial=input()

    file=open("IMPORTANTLINKS.txt","w")
    file.write(url_initial + '\n')
    file.close()

    a=-1
    while(1) :
        #
        a=a+1
        start=time.time()
        #s=linecache(read the a line)
        s=linecache.getline("IMPORTANTLINKS.txt",(a+1))
        scrap(s,a)
        linecache.clearcache()
        path = 't.xlsx'
        workbook = xlrd.open_workbook(path)
        ring=str(a)
        #f=open('currenturl.txt','r')
        #sheet_name=f.read()
        #f.close()
        worksheet= workbook.sheet_by_name(ring)
        i=worksheet.nrows
        j=worksheet.ncols
        i=i-1
        j=j-1
        for I in range(0,i):
            flag=0
            count=0
            weight=0
            for J in range(0,j):
                word=worksheet.cell_value(I,J)
                word=word.replace(',',' ')
                count=0
                if(J==0 or J==2):
                    for m in word.split(" "):
                        b=t.__contains__(m)
                        if b==True:
                            count=count+1;

                    weight=weight+(count*20)



                if(J==1):
                    link_associated=worksheet.cell_value(I,J)
                    continue

                if(J==3 or J==4):
                    for m in word.split(" "):


                        b=t.__contains__(m)
                        if b==True:

                            count=count+1;

                    weight=weight+(count*3)

            if(weight>10):
                print(link_associated)
                file = open("IMPORTANTLINKS.txt", "a+")
                file.write(link_associated)
                file.write("\n")
                file.close()
            


        print(time.time()-start)
        #input()
