# -*- coding: utf-8 -*-

_dictionary_words = []
_dictionary_words_len = []
_words_on_geometry = []
_geometry_matrix = []


class Word(object):

    def __init__(self, length, coordinates_cells, word_orientation):
        self.length = length
        self.coordinates_cells = coordinates_cells
        self.word_orientation = word_orientation  # V - вертикально / H - горизонтально


def read_words():
    words = open("ruwords.txt", "r").readlines()
    for word in words:
        _dictionary_words_len.append(len(word.rstrip()))
        _dictionary_words.append(word.rstrip())


def create_geometry_matrix():
    lines = open("geometry.txt", "r").readlines()
    for line in lines:
        line = line.rstrip()
        j = 0
        temp_line = []
        for cell in line:
            temp_line.append(cell)
            j += 1
        if j == len(lines):
            _geometry_matrix.append(temp_line)
        else:
            print("Не квадратичная геометрия")
            return False
    return True


def search_empty_cells():
    def check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, word_orientation):
        if word_is_formed:
            if word_length > 1:
                _words_on_geometry.append(Word(word_length, coord_empty_cells, word_orientation))
            elif word_length == 1:
                coord_empty_cells.pop()

    for i in range(len(_geometry_matrix)):  # горизонтальный проход
        word_length = 0
        word_is_formed = False
        coord_empty_cells = []
        for j in range(len(_geometry_matrix)):
            if _geometry_matrix[i][j] == '@':
                word_is_formed = True
                coord_empty_cells.append((i, j))
                word_length += 1
            elif _geometry_matrix[i][j] == '#':
                check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, 'H')
                coord_empty_cells[:]
                word_is_formed = False
                word_length = 0
        check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, 'H')

    for j in range(len(_geometry_matrix)):  # вертикальный проход
        word_length = 0
        word_is_formed = False
        coord_empty_cells = []
        for i in range(len(_geometry_matrix)):
            if _geometry_matrix[i][j] == '@':
                word_is_formed = True
                coord_empty_cells.append((i, j))
                word_length += 1
            elif _geometry_matrix[i][j] == '#':
                check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, 'V')
                coord_empty_cells[:]
                word_is_formed = False
                word_length = 0
        check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, 'V')


def radix_sort(array, base=10):
    def list_to_buckets(array, base, iteration):
        buckets = [[] for _ in range(base)]
        for number in array:
            # Isolate the base-digit from the number
            digit = (number.length // (base ** iteration)) % base
            # Drop the number into the correct bucket
            buckets[digit].append(number)
        return buckets

    def buckets_to_list(buckets):
        numbers = []
        for bucket in reversed(buckets):
            # append the numbers in a bucket
            # sequentially to the returned array
            for number in bucket:
                numbers.append(number)
        return numbers

    word_len = []
    for item in array:
        word_len.append(item.length)
    maxval = max(word_len)

    it = 0
    # Iterate, sorting the array by each base-digit
    while base ** it <= maxval:
        array = buckets_to_list(list_to_buckets(array, base, it))
        it += 1

    return array


def zapolnenie(dictionary_words_len, dictionary_words, words_on_geometry, previous_index, n):
    global answer
    if n < len(words_on_geometry):
        # print(n,len(words_on_geometry))
        try:
            index = dictionary_words_len.index(words_on_geometry[n].length, previous_index)
        except ValueError:
            return 0
        # print(index)
        # print(dictionary_words[index])
        i = 0
        check = True
        if n > 0:
            for letter in dictionary_words[index]:
                if was_before(answer, words_on_geometry[n].coordinates_cells[i], letter):
                    check = False
                    break
                i += 1
        if check:
            i = 0
            for letter in dictionary_words[index]:
                answer.append([words_on_geometry[n].coordinates_cells[i], letter])
                i += 1
            dictionary_words_len.pop(index)
            dictionary_words.pop(index)
            # zapolnenie(dictionary_words_len, dictionary_words, words_on_geometry, 0, n + 1)
        else:
            zapolnenie(dictionary_words_len, dictionary_words, words_on_geometry, index + 1, n)
        return 1
    return 0


def was_before(cargo, coord, letter):
    for item in cargo:
        if item[0] == coord:
            if item[1] == letter:
                return True
            else:
                return False
    return True


read_words()
if create_geometry_matrix():
    search_empty_cells()

_words_on_geometry = radix_sort(_words_on_geometry)
# for word in _words_on_geometry:
# print(word.length, word.word_orientation)

answer = []
zapolnenie(_dictionary_words_len, _dictionary_words, _words_on_geometry, 0, 0)

for item in answer:
    #print item[1],
    #print item[0][0],
    #print item[0][1]
    _geometry_matrix[item[0][0]][item[0][1]] = item[1]

for i in range(len(_geometry_matrix)):
    for j in range(len(_geometry_matrix)):
        print (_geometry_matrix[i][j]),
    print
