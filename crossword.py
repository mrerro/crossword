# -*- coding: utf-8 -*-


_dictionary_words = []
_dictionary_words_len = []
_coord_empty_cells = []
_empty_words_len = []


def read_words():
    words = open("ruwords.txt", "r").readlines()
    for word in words:
        _dictionary_words_len.append(len(word.rstrip()))
        _dictionary_words.append(word.rstrip())


def read_geometry():
    lines = open("geometry.txt", "r").readlines()
    i = 0
    for line in lines:
        j = 0
        l = 0
        word_is_formed = False
        for cell in line:
            if cell == '@':
                word_is_formed = True
                _coord_empty_cells.append((i, j))
                l += 1
            elif cell == '#':
                if word_is_formed:
                    word_is_formed = False
                    if l > 1:
                        _empty_words_len.append(l)
                    elif l == 1:
                        _coord_empty_cells.pop()
                l = 0
            j += 1
        if word_is_formed:
            word_is_formed = False
            if l > 1:
                _empty_words_len.append(l)
            elif l == 1:
                _coord_empty_cells.pop()
        i += 1


read_geometry()
print(_coord_empty_cells)
print(_empty_words_len)
