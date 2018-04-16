# -*- coding: utf-8 -*-

_dictionary_words = []
_dictionary_words_len = []
_dictionarys = []
_words_on_geometry = []
_geometry_matrix = []
_answers = []
_cargo = []


class Word(object):

    def __init__(self, length, coordinates_cells, word_orientation, status):
        self.length = length
        self.coordinates_cells = coordinates_cells
        self.word_orientation = word_orientation  # V - вертикально / H - горизонтально
        self.status = status
        self.intersections = 0
        self.name = 0
        self.children = []


class Dictionary(object):

    def __init__(self, rank, words, lengths):
        self.rank = rank
        self.words = words
        self.lengths = lengths


def read_words(words_on_geometry):
    dictionary_words_len = []
    dictionary_words = []
    words = open("ruwords.txt", "r").readlines()
    for word in words:
        dictionary_words_len.append(len(word.rstrip()))
        dictionary_words.append(word.rstrip())

    lengths = []
    for word in words_on_geometry:
        if lengths.count(word.length) == 0:
            lengths.append(word.length)

    dictionarys = []
    temp_dictionary_words_len = []
    temp_dictionary_words = []
    for length in lengths:
        for len_index in range(len(dictionary_words_len)):
            if length == dictionary_words_len[len_index]:
                temp_dictionary_words_len.append(dictionary_words_len[len_index])
                temp_dictionary_words.append(dictionary_words[len_index])
        dictionarys.append(Dictionary(length, temp_dictionary_words, temp_dictionary_words_len))
    return dictionarys


def create_geometry_matrix():
    lines = open("geometry.txt", "r").readlines()
    for line in lines:
        line = line.rstrip()
        # j = 0
        temp_line = []
        for cell in line:
            temp_line.append(cell)
            # j += 1
        # if j == len(lines):
        _geometry_matrix.append(temp_line)
        # else:
        # print("Не квадратичная геометрия")
        # return False
    return True


def search_empty_cells():
    def check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, word_orientation):
        # print word_is_formed, word_length, word_orientation
        if word_is_formed:
            if word_length > 1:
                _words_on_geometry.append(Word(word_length, coord_empty_cells, word_orientation, False))
            elif word_length == 1:
                coord_empty_cells.pop()

    for i in range(len(_geometry_matrix)):  # горизонтальный проход
        word_length = 0
        word_is_formed = False
        coord_empty_cells = []
        for j in range(len(_geometry_matrix[0])):
            if _geometry_matrix[i][j] == '@':
                word_is_formed = True
                coord_empty_cells.append((i, j))
                word_length += 1
            elif _geometry_matrix[i][j] == '#':
                check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, 'H')
                coord_empty_cells = []
                word_is_formed = False
                word_length = 0
        check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, 'H')

    for j in range(len(_geometry_matrix[0])):  # вертикальный проход
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
                coord_empty_cells = []
                word_is_formed = False
                word_length = 0
        check_for_the_end_empty_cells(word_is_formed, word_length, coord_empty_cells, 'V')


def sort_words(words):
    def count_intersections_or_children(words, key):
        for i in range(len(words)):  # подсчитываем количество пересекающихся ячеек в слове ???
            for j in range(len(words)):
                if i != j:
                    if key == 'c' and len(words[j].children) == 0:
                        for cell in words[i].coordinates_cells:
                            if words[j].coordinates_cells.count(cell) > 0:
                                words[i].children.append(words[j].name)
                    elif key == 'i' and words[i].intersections == 0:
                        for cell in words[i].coordinates_cells:
                            if words[j].coordinates_cells.count(cell) > 0:
                                words[i].intersections += 1

    def set_names(words):
        for name in range(len(words)):
            words[name].name = name

    def sort_by_children(words):
        sort_index = [0]
        for i in range(len(words)):
            sort_by_children_recurs(sort_index, words, i)
        sort_array = []
        # print sort_index
        for index in sort_index:
            sort_array.append(words[index])
        return sort_array

    def sort_by_children_recurs(sort_index, words, i):
        if i < range(len(words)):
            # print words[i].name,words[i].children
            if len(words[i].children) > 0:
                for child in words[i].children:
                    if sort_index.count(child) == 0:
                        sort_index.append(child)
                        if sort_by_children_recurs(sort_index, words, child) == 1:
                            return 1
                    else:
                        if sort_index.count(i) == 0:
                            sort_index.append(i)
                            return 1
            else:
                if sort_index.count(i) == 0:
                    sort_index.append(i)
                    return 1
        return 0

    words = radix_sort(words, 'l')  # сортируем по убыванию длины
    count_intersections_or_children(words, 'i')
    words = radix_sort(words, 'i')  # сортируем по убыванию пересечений
    set_names(words)
    count_intersections_or_children(words, 'c')
    # print_words_geometry(words)
    return sort_by_children(words)


def radix_sort(array, key, base=10, ):
    def list_to_buckets(array, base, iteration, key):
        buckets = [[] for _ in range(base)]
        for number in array:
            # Isolate the base-digit from the number
            if key == 'l':
                digit = (number.length // (base ** iteration)) % base
            elif key == 'i':
                digit = (number.intersections // (base ** iteration)) % base
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
        if key == 'l':
            word_len.append(item.length)
        elif key == 'i':
            word_len.append(item.intersections)

    maxval = max(word_len)

    it = 0
    # Iterate, sorting the array by each base-digit
    while base ** it <= maxval:
        array = buckets_to_list(list_to_buckets(array, base, it, key))
        it += 1
    return array


def zapolnenie(dictionary_words_len, dictionary_words, words_on_geometry, n):
    global _cargo, _answers
    if n == len(words_on_geometry):
        if _answers.count(_cargo) == 0:
            _answers.append(list(_cargo))

    if n < len(words_on_geometry):
        for i in range(len(dictionary_words_len)):
            if dictionary_words_len[i] == words_on_geometry[n].length:
                if intersection_check(dictionary_words[i].strip(), words_on_geometry[n].coordinates_cells):
                    words_on_geometry[n].status = True
                    add_to_cargo(dictionary_words[i].strip(), words_on_geometry[n].coordinates_cells)
                    temp_dictionary_words_len = list(dictionary_words_len)
                    temp_dictionary_words = list(dictionary_words)
                    temp_dictionary_words_len.pop(i)
                    temp_dictionary_words.pop(i)
                    if zapolnenie(temp_dictionary_words_len, temp_dictionary_words, words_on_geometry, n + 1) == 1:
                        return 1
                    words_on_geometry[n].status = False
                    dell_from_cargo(words_on_geometry[n].coordinates_cells)
    return 0


def check_all_words_filled(words_on_geometry):  # можно использовать для поиска одного пкрвого решения
    i = 0
    for word in words_on_geometry:
        if word.status:
            i += 1
    if i == len(words_on_geometry):
        return True
    return False


def add_to_cargo(letters, coordinates_cells):
    global _cargo
    for i in range(len(letters)):
        _cargo.append([coordinates_cells[i], letters[i]])


def dell_from_cargo(coordinates_cells):
    global _cargo
    for item in coordinates_cells:
        _cargo.pop()


def intersection_check(letters, coordinates_cells):
    global _cargo
    check = []
    if len(_cargo) > 0:
        for item in _cargo:
            for c in range(len(coordinates_cells)):
                if item[0] == coordinates_cells[c]:
                    if item[1] == letters[c]:
                        check.append(True)
                    else:
                        check.append(False)
        if check.count(False) == 0:
            return True
        else:
            return False
    else:
        return True


def print_words_geometry(array):
    for word in array:
        print("name", word.name, "dlina", word.length, "peresech", word.intersections, "child", word.children,
              word.word_orientation, "coord", word.coordinates_cells)
    print "------------"


def print_result():
    for item in _cargo:
        _geometry_matrix[item[0][0]][item[0][1]] = item[1]

    for i in range(len(_geometry_matrix)):
        for j in range(len(_geometry_matrix[0])):
            print (_geometry_matrix[i][j]),
        print
    print


def write_result():
    file = open("answer.txt", "w")
    for cargo in _answers:
        for item in cargo:
            _geometry_matrix[item[0][0]][item[0][1]] = item[1]

        for i in range(len(_geometry_matrix)):
            for j in range(len(_geometry_matrix[0])):
                file.write(_geometry_matrix[i][j] + ' ')
            file.write('\n')
        file.write('\n')


if create_geometry_matrix():
    search_empty_cells()
    # print_words_geometry(_words_on_geometry)
    # print(len(_words_on_geometry))
    _words_on_geometry = sort_words(_words_on_geometry)
    print_words_geometry(_words_on_geometry)
    # print(len(_words_on_geometry))
    _dictionarys = read_words(_words_on_geometry)
    # print(len(_dictionary_words_len))

    print_result()
    for i in range(len(_dictionary_words_len)):
        _cargo = []
        zapolnenie(_dictionary_words_len, _dictionary_words, _words_on_geometry, 0)
    print len(_answers)
    write_result()
