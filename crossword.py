# -*- coding: utf-8 -*-
from tkinter import filedialog
from tkinter import *

_dictionaries = {}
_words_on_geometry = []
_geometry_matrix = []
_answers = []
_cargo = []
_number_of_answers = 1
_check = False

_file_geometry_name = "geometry.txt"
_file_dictionary_name = "ruwords.txt"


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

    def __init__(self, words, rank):
        self.words = words
        self.rank = rank


def read_words(words_on_geometry):
    dictionary_words_len = []
    dictionary_words = []
    words = open(_file_dictionary_name, "r").readlines()
    for word in words:
        dictionary_words_len.append(len(word.rstrip()))
        dictionary_words.append(word.rstrip())

    lengths = []
    for word in words_on_geometry:
        if lengths.count(word.length) == 0:
            lengths.append(word.length)

    dictionaries = {}
    for length in lengths:
        temp_dictionary_words = []
        for len_index in range(len(dictionary_words_len)):
            if length == dictionary_words_len[len_index]:
                temp_dictionary_words.append(dictionary_words[len_index])
        dictionaries[length] = Dictionary(temp_dictionary_words, length)
    return dictionaries


def create_geometry_matrix():
    lines = open(_file_geometry_name, "r").readlines()
    for line in lines:
        line = line.rstrip()
        temp_line = []
        for cell in line:
            temp_line.append(cell)
        _geometry_matrix.append(temp_line)
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
        if i < len(words):
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


def zapolnenie(dictionaries, words_on_geometry, n):
    global _cargo, _answers
    # print(_cargo)
    if n == len(words_on_geometry):
        if _answers.count(_cargo) == 0:
            _answers.append(list(_cargo))
            if len(_answers) == _number_of_answers:
                return 1

    if n < len(words_on_geometry):
        for i in range(len(dictionaries[words_on_geometry[n].length].words)):
            if intersection_check(dictionaries[words_on_geometry[n].length].words[i].strip(),
                                  words_on_geometry[n].coordinates_cells):
                words_on_geometry[n].status = True
                add_to_cargo(dictionaries[words_on_geometry[n].length].words[i].strip(),
                             words_on_geometry[n].coordinates_cells)
                temp_dictionary = dictionaries.copy()
                temp_dictionary[words_on_geometry[n].length] = Dictionary(
                    list(dictionaries[words_on_geometry[n].length].words), words_on_geometry[n].length)
                temp_dictionary[words_on_geometry[n].length].words.pop(i)
                if zapolnenie(temp_dictionary, words_on_geometry, n + 1) == 1:
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
        # if _cargo.count([coordinates_cells[i], letters[i]]) == 0:
        _cargo.append([coordinates_cells[i], letters[i]])


def dell_from_cargo(coordinates_cells):
    global _cargo
    # for i in range(len(cargo)):
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


def print_result(cargo):
    for item in cargo:
        _geometry_matrix[item[0][0]][item[0][1]] = item[1]

    for i in range(len(_geometry_matrix)):
        for j in range(len(_geometry_matrix[0])):
            print(_geometry_matrix[i][j]),
        print
    print


def print_result_spisok():
    index = int(message.get())
    for i in range(index):
        if i < len(_answers):
            h = []
            v = []
            for item in _words_on_geometry:
                word = ''
                for cell in item.coordinates_cells:
                    key = 0
                    for cargo_item in _answers[i]:
                        if cargo_item[0] == cell and key == 0:
                            word += cargo_item[1]
                            key += 1
                if item.word_orientation == 'V':
                    v.append(word)
                elif item.word_orientation == 'H':
                    h.append(word)

            s_h = "По горизонтали: {} \n".format(h)
            s_v = "По вертикали: {} \n".format(v)
            textbox.insert(INSERT, "\n {} - решение \n".format(index))
            textbox.insert(INSERT, s_h)
            textbox.insert(INSERT, s_v)


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


def start():
    global _answers, _geometry_matrix, _words_on_geometry, _number_of_answers, _dictionaries, _check

    if not _check:
        _dictionaries = {}
        _words_on_geometry = []
        _geometry_matrix = []
        _answers = []

        _number_of_answers = int(message.get())
        textbox.delete('1.0', 'end')
        textbox.insert('1.0', 'start')
        if create_geometry_matrix():
            _check = True
            search_empty_cells()
            _words_on_geometry = sort_words(_words_on_geometry)
            _dictionaries = read_words(_words_on_geometry)
            zapolnenie(_dictionaries, _words_on_geometry, 0)
            write_result()
            message.set(len(_answers))
            textbox.delete('1.0', 'end')
            textbox.insert('1.0', 'finish')
        _check = False


def window_quit():
    global root
    root.destroy()


def load_geometry():
    global _file_geometry_name
    fn = filedialog.Open(root, filetypes=[('*.txt files', '.txt')]).show()
    if fn == '':
        return
    _file_geometry_name = fn
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', open(fn, 'rt').read().replace('#', '  #'))


def save_geometry():
    fn = filedialog.SaveAs(root, filetypes=[('*.txt files', '.txt')]).show()
    if fn == '':
        return
    if not fn.endswith(".txt"):
        fn += ".txt"
    open(fn, 'wt').write(textbox.get('1.0', 'end-1c').replace(' ', ''))


def load_dictionary():
    global _file_dictionary_name
    fn = filedialog.Open(root, filetypes=[('*.txt files', '.txt')]).show()
    if fn == '':
        return
    _file_dictionary_name = fn


root = Tk()
root.title("Crossword filler")

panelFrame = Frame(root, height=60, bg='gray')
textFrame = Frame(root, height=340, width=600)

panelFrame.pack(side='top', fill='x')
textFrame.pack(side='bottom', fill='both', expand=1)

textbox = Text(textFrame, font='Arial 14', wrap='word')
scrollbar = Scrollbar(textFrame)

scrollbar['command'] = textbox.yview
textbox['yscrollcommand'] = scrollbar.set

textbox.pack(side='left', fill='both', expand=1)
scrollbar.pack(side='right', fill='y')

message = StringVar()
numberEntry = Entry(panelFrame, textvariable=message)
message.set(1)

loadBtn = Button(panelFrame, text='Загрузить геометрию', command=load_geometry)
saveBtn = Button(panelFrame, text='Сохранить геометрию', command=save_geometry)
quitBtn = Button(panelFrame, text='Выход', command=window_quit)
loadwordBtn = Button(panelFrame, text='Загрузить словарик', command=load_dictionary)
startBtn = Button(panelFrame, text='Запуск', command=start)
showBtn = Button(panelFrame, text='Показать решения', command=print_result_spisok)
#
# startBtn.bind("<Button-1>", start(message.get()))
# quitBtn.bind("<Button-1>", Quit)

loadBtn.place(x=10, y=10, width=130, height=40)
saveBtn.place(x=145, y=10, width=130, height=40)
loadwordBtn.place(x=280, y=10, width=125, height=40)
numberEntry.place(x=410, y=10, width=40, height=39)
startBtn.place(x=460, y=10, width=80, height=40)
showBtn.place(x=550, y=10, width=125, height=40)
quitBtn.place(x=680, y=10, width=50, height=40)

root.mainloop()
