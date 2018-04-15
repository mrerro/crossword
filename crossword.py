# -*- coding: utf-8 -*-

_dictionary_words = []
_dictionary_words_len = []
_words_on_geometry = []
_geometry_matrix = []
cargo = []


class Word(object):

    def __init__(self, length, coordinates_cells, word_orientation, status):
        self.length = length
        self.coordinates_cells = coordinates_cells
        self.word_orientation = word_orientation  # V - вертикально / H - горизонтально
        self.status = status


def read_words():
    dictionary_words_len = []
    dictionary_words = []
    words = open("ruwords.txt", "r").readlines()
    for word in words:
        dictionary_words_len.append(len(word.rstrip()))
        dictionary_words.append(word.rstrip())

    temp_dictionary_words_len = []
    temp_dictionary_words = []
    for word in _words_on_geometry:
        for len_index in range(len(dictionary_words_len)):
            if word.length == dictionary_words_len[len_index]:
                temp_dictionary_words_len.append(dictionary_words_len[len_index])
                temp_dictionary_words.append(dictionary_words[len_index])

    return temp_dictionary_words_len, temp_dictionary_words


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
                _words_on_geometry.append(Word(word_length, coord_empty_cells, word_orientation, False))
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


def zapolnenie(dictionary_words_len, dictionary_words, words_on_geometry, n):
    global cargo
    print(n)
    if check2(words_on_geometry):
        return 1
    if n < len(words_on_geometry):
        for i in range(len(dictionary_words_len)):
            if dictionary_words_len[i] == words_on_geometry[n].length:
                if check(dictionary_words[i].strip(), words_on_geometry[n].coordinates_cells):
                    words_on_geometry[n].status = True
                    add(dictionary_words[i].strip(), words_on_geometry[n].coordinates_cells)
                    if zapolnenie(dictionary_words_len, dictionary_words, words_on_geometry, n + 1) == 1:
                        return 1
        dell(words_on_geometry[n].coordinates_cells)
    return 0

    # def alg(cargo, dictionary_words_len, dictionary_words, words_on_geometry, n):


def check2(words_on_geometry):
    i = 0
    for word in words_on_geometry:
        if word.status:
            i += 1
    if i == len(words_on_geometry):
        return True
    return False


def add(letters, coordinates_cells):
    global cargo
    for i in range(len(letters)):
        cargo.append([coordinates_cells[i], letters[i]])


def dell(coordinates_cells):
    global cargo
    for item in coordinates_cells:
        cargo.pop()


def check(letters, coordinates_cells):
    global cargo
    check = []
    if len(cargo) > 0:
        for item in cargo:
            if coordinates_cells.count(item[0]) != 0:
                if item[1] == letters[coordinates_cells.index(item[0])]:
                    check.append(True)
                else:
                    check.append(False)
        if len(check) == check.count(True):
            return True
        else:
            return False
    else:
        return True


if create_geometry_matrix():
    search_empty_cells()
_words_on_geometry = radix_sort(_words_on_geometry)
_dictionary_words_len, _dictionary_words = read_words()

for word in _words_on_geometry:
    print(word.length, word.word_orientation)

print zapolnenie(_dictionary_words_len, _dictionary_words, _words_on_geometry, 0)

print(cargo)
for item in cargo:
    _geometry_matrix[item[0][0]][item[0][1]] = item[1]

for i in range(len(_geometry_matrix)):
    for j in range(len(_geometry_matrix)):
        print (_geometry_matrix[i][j]),
    print
