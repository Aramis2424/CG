import copy
import math
import sys
from time import time, sleep
from tkinter import Tk, Button, Label, Entry, Canvas,\
    messagebox, Menu, Frame, SUNKEN, colorchooser
from tkinter import ttk
import matplotlib.pyplot as plt
from colorutils import Color
from math import sqrt, cos, sin, pi
from math import fabs, floor
from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar, PhotoImage
from tkinter import messagebox
import time
from itertools import combinations

WIDE = 1000
WIDTH = 1000
HEIGHT = 600
RADIUS = 3

EPS = 1e-8

RESULT = False
IS_END_FIG = False
IS_END_ROMB = False

IS_FIRST_DOT = True
x_first, y_first = 0, 0
center_dot = 0

IS_FIRST_DOT_CLIP = True
IS_FIRST_DOT_ROMB = True
x_first_clip, y_first_clip = 0, 0

x_first_fig, y_first_fig = 0, 0

center_dot_clip = 0
center_dot_fig = 0

X_MIN = 0
X_MAX = 1
Y_MIN = 2
Y_MAX = 3

X_DOT = 0
Y_DOT = 1


dots_for_cir = []

center_pix = (0, 0)

dots = []
last_activity = []

TASK = 'Алгоритм Сазерленда-Ходжмена'


def del_all_dots():
    global lines, clipper, IS_FIRST_DOT_CLIP, IS_END_FIG, figure,\
        IS_FIRST_DOT_ROMB, IS_END_ROMB

    IS_FIRST_DOT_CLIP = True
    IS_FIRST_DOT_ROMB = True

    IS_END_FIG = False
    IS_END_ROMB = False

    canvas.delete("all")

    lines = [[]]
    clipper = []
    figure = []


def add_line(x1, y1, x2, y2, color):
    global lines

    try:
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
    except:
        messagebox.showinfo("Ошибка", "Неверно введены координаты")
        return

    cur_line = len(lines) - 1
    line_color = parse_color(color)

    lines[cur_line].append([x1, y1])
    lines[cur_line].append([x2, y2])
    lines[cur_line].append(line_color)

    lines.append(list())

    canvas.create_line(x1, y1, x2, y2, fill = line_color)

def add_line_by_click(event, color):
    global lines, IS_FIRST_DOT, x_first, y_first, center_dot

    if IS_FIRST_DOT:
        x_first = int(event.x)
        y_first = int(event.y)
        IS_FIRST_DOT = False
        center_dot = canvas.create_oval(
                event.x - RADIUS, event.y - RADIUS,
                event.x + RADIUS, event.y + RADIUS,
                fill="#fff", outline="#001", width=1
            )
        return
    else:
        canvas.delete(center_dot)

    x1 = x_first
    y1 = y_first
    x2 = int(event.x)
    y2 = int(event.y)
    IS_FIRST_DOT = True

    cur_line = len(lines) - 1
    line_color = parse_color(color)

    lines[cur_line].append([x1, y1])
    lines[cur_line].append([x2, y2])
    lines[cur_line].append(line_color)

    lines.append(list())

    canvas.create_line(x1, y1, x2, y2, fill = line_color)


def add_clipper(x, y, color):
    global clipper, IS_FIRST_DOT_CLIP, x_first_clip,\
        y_first_clip, center_dot_clip, IS_END_FIG

    if IS_END_FIG:
        del_all_dots()

    if IS_FIRST_DOT_CLIP:
        x_first_clip = int(x)
        y_first_clip = int(y)
        clipper.append([x_first_clip, y_first_clip])
        IS_FIRST_DOT_CLIP = False
        center_dot_clip = canvas.create_oval(
                x_first_clip - RADIUS, y_first_clip - RADIUS,
                x_first_clip + RADIUS, y_first_clip + RADIUS,
                fill="#fff", outline="#001", width=1
            )
        return
    else:
        canvas.delete(center_dot_clip)

    x1 = x_first_clip
    y1 = y_first_clip
    x2 = int(x)
    y2 = int(y)
    #IS_FIRST_DOT_CLIP = True
    x_first_clip = x2
    y_first_clip = y2

    clipper_color = parse_color(color)

    clipper.append([x2, y2])
    canvas.create_line(x1, y1, x2, y2, fill = clipper_color)

def del_clipper(color_clipper):
    global clipper, IS_FIRST_DOT_CLIP, IS_END_FIG,\
        IS_FIRST_DOT_FIG, IS_END_ROMB, figure
    IS_FIRST_DOT_CLIP = True
    IS_END_FIG = False
    #IS_FIRST_DOT_FIG = True
    #IS_END_ROMB = False

    canvas.delete("all")
    clipper = []
    #figure = []



    color_clipper = parse_color(color_clipper)
    for i in range(len(figure)-1):
        x1 = figure[i][0]
        y1 = figure[i][1]

        x2 = figure[i+1][0]
        y2 = figure[i+1][1]

        canvas.create_line(x1, y1, x2, y2, fill = color_clipper)

def del_fig(color_fig):
    global clipper, IS_FIRST_DOT_CLIP, IS_END_FIG,\
        IS_FIRST_DOT_ROMB, IS_END_ROMB, figure
    #IS_FIRST_DOT_CLIP = True
    #IS_END_FIG = False
    IS_FIRST_DOT_ROMB = True
    IS_END_ROMB = False

    canvas.delete("all")
    #clipper = []
    figure = []

    color_fig = parse_color(color_fig)
    for i in range(len(clipper)-1):
        x1 = clipper[i][0]
        y1 = clipper[i][1]

        x2 = clipper[i+1][0]
        y2 = clipper[i+1][1]

        canvas.create_line(x1, y1, x2, y2, fill = color_fig)


def add_clipper_by_click(event, color, dop_color):
    global clipper, IS_FIRST_DOT_CLIP, x_first_clip,\
        y_first_clip, center_dot_clip, IS_END_FIG

    if IS_END_FIG:
        #del_all_dots()
        del_clipper(dop_color)

    if IS_FIRST_DOT_CLIP:
        x_first_clip = int(event.x)
        y_first_clip = int(event.y)
        clipper.append([x_first_clip, y_first_clip])
        IS_FIRST_DOT_CLIP = False
        center_dot_clip = canvas.create_oval(
                event.x - RADIUS, event.y - RADIUS,
                event.x + RADIUS, event.y + RADIUS,
                fill="#fff", outline="#001", width=1
            )
        return
    else:
        canvas.delete(center_dot_clip)

    x1 = x_first_clip
    y1 = y_first_clip
    x2 = int(event.x)
    y2 = int(event.y)
    #IS_FIRST_DOT_CLIP = True
    x_first_clip = x2
    y_first_clip = y2

    clipper_color = parse_color(color)

    clipper.append([x2, y2])
    canvas.create_line(x1, y1, x2, y2, fill = clipper_color)


def end_clipper(event, color):
    global clipper, IS_END_FIG, x_first_clip, y_first_clip, center_dot_clip

    if IS_END_FIG:
        messagebox.showerror("Ошибка", "Фигура уже замкнута")
        return

    cur_dot = len(clipper)

    if (cur_dot < 3):
        messagebox.showerror("Ошибка", "Недостаточно ребер")

    add_clipper(clipper[0][0], clipper[0][1], color)
    IS_END_FIG = True


def draw_sides():

    for side in lines:
        if (len(side) != 0):
            x1 = side[0][0]
            y1 = side[0][1]

            x2 = side[1][0]
            y2 = side[1][1]

            color_line = side[2]


            canvas.create_line(x1, y1, x2, y2, fill = color_line)


def parse_color(color):
    if color == 0:
        color = "#ffffff"
    if color == 1:
        color = "#000000"
    if color == 2:
        color = "#ff0000"
    if color == 3:
        color = "#0000ff"
    if color == 4:
        color = "#148012"

    return color



######################################################################################
def add_fig(x, y, color, dop_color):
    global figure, IS_FIRST_DOT_ROMB, x_first_fig,\
        y_first_fig, center_dot_fig, IS_END_ROMB

    if IS_END_ROMB:
        del_all_dots()
        del_fig(dop_color)

    if IS_FIRST_DOT_ROMB:
        x_first_fig = int(x)
        y_first_fig = int(y)
        figure.append([x_first_fig, y_first_fig])
        IS_FIRST_DOT_ROMB = False
        center_dot_fig = canvas.create_oval(
                x_first_fig - RADIUS, y_first_fig - RADIUS,
                x_first_fig + RADIUS, y_first_fig + RADIUS,
                fill="#fff", outline="#001", width=1
            )
        return
    else:
        canvas.delete(center_dot_fig)

    x1 = x_first_fig
    y1 = y_first_fig
    x2 = int(x)
    y2 = int(y)
    #IS_FIRST_DOT_ROMB = True
    x_first_fig = x2
    y_first_fig = y2

    clipper_color = parse_color(color)

    figure.append([x2, y2])
    canvas.create_line(x1, y1, x2, y2, fill = clipper_color)


def add_fig_by_click(event, color, dop_color):
    global figure, IS_FIRST_DOT_ROMB, x_first_fig,\
        y_first_fig, center_dot_fig, IS_END_ROMB

    if IS_END_ROMB:
        #del_all_dots()
        del_fig(dop_color)

    if IS_FIRST_DOT_ROMB:
        x_first_fig = int(event.x)
        y_first_fig = int(event.y)
        figure.append([x_first_fig, y_first_fig])
        IS_FIRST_DOT_ROMB = False
        center_dot_fig = canvas.create_oval(
                event.x - RADIUS, event.y - RADIUS,
                event.x + RADIUS, event.y + RADIUS,
                fill="#fff", outline="#001", width=1
            )
        return
    else:
        canvas.delete(center_dot_fig)

    x1 = x_first_fig
    y1 = y_first_fig
    x2 = int(event.x)
    y2 = int(event.y)
    #IS_FIRST_DOT_ROMB = True
    x_first_fig = x2
    y_first_fig = y2

    clipper_color = parse_color(color)

    figure.append([x2, y2])
    canvas.create_line(x1, y1, x2, y2, fill = clipper_color)


def end_fig(event, color):
    global figure, IS_END_ROMB

    if IS_END_ROMB:
        messagebox.showerror("Ошибка", "Фигура уже замкнута")
        return

    cur_dot = len(figure)

    if (cur_dot < 3):
        messagebox.showerror("Ошибка", "Недостаточно ребер")

    add_fig(figure[0][0], figure[0][1], color, 3)
    IS_END_ROMB = True
######################################################################################


#---------------------------------------------------------------------------------------



# Algorithm

def get_vector(dot1, dot2):
    return [dot2[X_DOT] - dot1[X_DOT], dot2[Y_DOT] - dot1[Y_DOT]]


def vector_mul(vec1, vec2):
    return (vec1[0] * vec2[1] - vec1[1] * vec2[0])


def scalar_mul(vec1, vec2):
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1])


def line_koefs(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1*y2 - x2*y1

    return a, b, c


def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1*b2 - a2*b1
    opr1 = (-c1)*b2 - b1*(-c2)
    opr2 = a1*(-c2) - (-c1)*a2

    if (opr == 0):
        return -5, -5 # прямые параллельны

    x = opr1 / opr
    y = opr2 / opr

    return x, y


def is_coord_between(left_coord, right_coord, dot_coord):
    return (min(left_coord, right_coord) <= dot_coord) \
            and (max(left_coord, right_coord) >= dot_coord)


def is_dot_between(dot_left, dot_right, dot_intersec):
    return is_coord_between(dot_left[X_DOT], dot_right[X_DOT], dot_intersec[X_DOT]) \
            and is_coord_between(dot_left[Y_DOT], dot_right[Y_DOT], dot_intersec[Y_DOT])


def are_connected_sides(line1, line2):

    if ((line1[0][X_DOT] == line2[0][X_DOT]) and (line1[0][Y_DOT] == line2[0][Y_DOT])) \
            or ((line1[1][X_DOT] == line2[1][X_DOT]) and (line1[1][Y_DOT] == line2[1][Y_DOT])) \
            or ((line1[0][X_DOT] == line2[1][X_DOT]) and (line1[0][Y_DOT] == line2[1][Y_DOT])) \
            or ((line1[1][X_DOT] == line2[0][X_DOT]) and (line1[1][Y_DOT] == line2[0][Y_DOT])):
        return True

    return False


def extra_check(object): # чтобы не было пересечений

    lines = []

    for i in range(len(object) - 1):
        lines.append([object[i], object[i + 1]]) # разбиваю многоугольник на линии

    combs_lines = list(combinations(lines, 2)) # все возможные комбинации сторон

    for i in range(len(combs_lines)):
        line1 = combs_lines[i][0]
        line2 = combs_lines[i][1]

        if (are_connected_sides(line1, line2)):
            continue

        a1, b1, c1 = line_koefs(line1[0][X_DOT], line1[0][Y_DOT], line1[1][X_DOT], line1[1][Y_DOT])
        a2, b2, c2 = line_koefs(line2[0][X_DOT], line2[0][Y_DOT], line2[1][X_DOT], line2[1][Y_DOT])

        dot_intersec = solve_lines_intersection(a1, b1, c1, a2, b2, c2)

        if (is_dot_between(line1[0], line1[1], dot_intersec)) \
                and (is_dot_between(line2[0], line2[1], dot_intersec)):
            return True

    return False


def check_polygon(): # через проход по всем точкам, поворот которых должен быть все время в одну сторону
    if (len(clipper) < 3):
        return False

    sign = 0

    if (vector_mul(get_vector(clipper[1], clipper[2]),\
            get_vector(clipper[0], clipper[1])) > 0):
        sign = 1
    else:
        sign = -1

    for i in range(3, len(clipper)):
        if sign * vector_mul(get_vector(clipper[i - 1], clipper[i]),\
                    get_vector(clipper[i - 2], clipper[i - 1])) < 0:
            return False

    check = extra_check(clipper)

    if (check):
        return False

    if (sign < 0):
        clipper.reverse()

    return True


def get_normal(dot1, dot2, pos):
    f_vect = get_vector(dot1, dot2)
    pos_vect = get_vector(dot2, pos)

    if (f_vect[1]):
        normal = [1, -f_vect[0] / f_vect[1]]
    else:
        normal = [0, 1]

    if (scalar_mul(pos_vect, normal) < 0):
        normal[0] = -normal[0]
        normal[1] = -normal[1]

    return normal


def is_visible(dot, f_dot, s_dot):
    vec1 = get_vector(f_dot, s_dot)
    vec2 = get_vector(f_dot, dot)

    if (vector_mul(vec1, vec2) <= 0):
        return True
    else:
        return False


def get_lines_parametric_intersec(line1, line2, normal):
    d = get_vector(line1[0], line1[1])
    w = get_vector(line2[0], line1[0])

    d_scalar = scalar_mul(d, normal)
    w_scalar = scalar_mul(w, normal)

    t = -w_scalar / d_scalar

    dot_intersec = [line1[0][X_DOT] + d[0] * t, line1[0][Y_DOT] + d[1] * t]

    return dot_intersec


def sutherland_hodgman_algorythm(cutter_line, position, prev_result):
    cur_result = []

    dot1 = cutter_line[0]
    dot2 = cutter_line[1]

    normal = get_normal(dot1, dot2, position)

    prev_vision = is_visible(prev_result[-2], dot1, dot2)

    for cur_dot_index in range(-1, len(prev_result)):
        cur_vision = is_visible(prev_result[cur_dot_index], dot1, dot2)

        if (prev_vision):
            if (cur_vision):
                cur_result.append(prev_result[cur_dot_index])
            else:
                figure_line = [prev_result[cur_dot_index - 1], prev_result[cur_dot_index]]

                cur_result.append(get_lines_parametric_intersec(figure_line, cutter_line, normal))
        else:
            if (cur_vision):
                figure_line = [prev_result[cur_dot_index - 1], prev_result[cur_dot_index]]

                cur_result.append(get_lines_parametric_intersec(figure_line, cutter_line, normal))

                cur_result.append(prev_result[cur_dot_index])

        prev_vision = cur_vision

    return cur_result




def cut_area(color_clipper, color_res):
    global IS_END_FIG, clipper, figure, IS_END_ROMB
    if not IS_END_FIG:
        messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
        return

    if not IS_END_ROMB:
        messagebox.showinfo("Ошибка", "Отекаемый многоугольник не замкнут")
        return

    if (extra_check(figure)):
        messagebox.showinfo("Ошибка", "Отекаемое должно быть многоугольником")
        return

    if (len(clipper) < 3):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if (not check_polygon()):
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    result = copy.deepcopy(figure)

    for cur_dot_ind in range(-1, len(clipper) - 1):
        line = [clipper[cur_dot_ind], clipper[cur_dot_ind + 1]]

        position_dot = clipper[cur_dot_ind + 1]

        result = sutherland_hodgman_algorythm(line, position_dot, result)

        if (len(result) <= 2):
            return

    color_clipper = parse_color(color_clipper)
    canvas.create_polygon(clipper, fill = "#148012", outline=color_clipper)
    for i in range(len(clipper)-2):
        x1 = clipper[i][0]
        y1 = clipper[i][1]

        x2 = clipper[i+1][0]
        y2 = clipper[i+1][1]

        canvas.create_line(x1, y1, x2, y2, fill = color_clipper)
    canvas.create_polygon(clipper, fill = "#148012", outline=color_clipper)


    draw_result_figure(result, color_res)



def draw_result_figure(figure_dots, color_res):
    fixed_figure = remove_odd_sides(figure_dots)

    res_color = parse_color(color_res)

    for line in fixed_figure:
        canvas.create_line(line[0], line[1], fill = res_color)


# Odd sides
def make_unique(sides):

    for side in sides:
        side.sort()

    return list(filter(lambda x: (sides.count(x) % 2) == 1, sides))


def is_dot_in_side(dot, side):
    if abs(vector_mul(get_vector(dot, side[0]), get_vector(side[1], side[0]))) <= 1e-6:
        if (side[0] < dot < side[1] or side[1] < dot < side[0]):
            return True
    return False


def get_sides(side, rest_dots):
    dots_list = [side[0], side[1]]

    for dot in rest_dots:
        if is_dot_in_side(dot, side):
            dots_list.append(dot)

    dots_list.sort()

    sections_list = list()

    for i in range(len(dots_list) - 1):
        sections_list.append([dots_list[i], dots_list[i + 1]])

    return sections_list


def remove_odd_sides(figure_dots):
    all_sides = list()
    rest_dots = figure_dots[2:]

    for i in range(len(figure_dots)):
        cur_side = [figure_dots[i], figure_dots[(i + 1) % len(figure_dots)]]

        all_sides.extend(get_sides(cur_side, rest_dots))

        rest_dots.pop(0)
        rest_dots.append(figure_dots[i])

    return make_unique(all_sides)

#---------------------------------------------------------------------------------------


def main():
    global lines, clipper, canvas, figure

    lines = [[]]
    clipper = []
    figure = []

    x_draw = 0
    y_draw = 0

    y_groups = dict()
    y_max = 0
    y_min = 1000
    active_edges = []

    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №9")
    root.minsize(WIDTH, HEIGHT)
    root["bg"] = "#6b5a45"

    #label меню
    label_menu = Label(root, text="Меню",
                              bg='#6b7a0a')
    label_menu.place(relx=0, rely=0, relwidth=0.3, relheight=0.04)

    # Установка combox`a
    combostyle = ttk.Style() #стиль для Combox`a
    combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#6b7a0a',
                                       'fieldbackground': '#6b7a0a',
                                       'background': '#6b7a0a'
                                       }}}
                           )
    combostyle.theme_use('combostyle')

    color_list = ("Белый", "Черный", "Красный",
                   "Синий", "Зеленый")
    font_combo = ("Times", 12)

    # Выбор цвета отсекателя
    label_color = Label(text="Цвет отсекателя:", bg="#6b7a0a", anchor='w')
    label_color.place(relx=0, rely=0.06, relwidth=0.3, relheight=0.04)

    color_clipper_combo = ttk.Combobox(root, state='readonly',
                    values=color_list,
                    font=font_combo)
    color_clipper_combo.place(relx=0, rely=0.1, relwidth=0.3, relheight=0.06)
    color_clipper_combo.current(0)

    # Выбор цвета отрезка
    label_color = Label(text="Цвет отрезка:", bg="#6b7a0a", anchor='w')
    label_color.place(relx=0, rely=0.17, relwidth=0.3, relheight=0.04)

    color_line_combo = ttk.Combobox(root, state='readonly', values=color_list,
                    font=font_combo)
    color_line_combo.place(relx=0, rely=0.21, relwidth=0.3, relheight=0.06)
    color_line_combo.current(1)

    # Выбор цвета результата
    label_color = Label(text="Цвет результата:", bg="#6b7a0a", anchor='w')
    label_color.place(relx=0, rely=0.28, relwidth=0.3, relheight=0.04)

    color_res_combo = ttk.Combobox(root, state='readonly', values=color_list,
                    font=font_combo)
    color_res_combo.place(relx=0, rely=0.32, relwidth=0.3, relheight=0.06)
    color_res_combo.current(2)

    # Ввод отрезка
    label_shift = Label(root, text="Координаты вершины многоугольника:", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.4, relwidth=0.3, relheight=0.04)
    #Координаты отрезка
    label_x1 = Label(root, text="X:", anchor='c',
                              bg='#6b7a0a')
    label_x1.place(relx=0, rely=0.445, relwidth=0.04, relheight=0.06)
    line_x1 = Entry(root, bg='#6b7a0a')
    line_x1.place(relx=0.043, rely=0.445, relwidth=0.04, relheight=0.06)

    label_y1 = Label(root, text="Y:", anchor='c',
                              bg='#6b7a0a')
    label_y1.place(relx=0.1, rely=0.445, relwidth=0.04, relheight=0.06)
    line_y1 = Entry(root, bg='#6b7a0a')
    line_y1.place(relx=0.143, rely=0.445, relwidth=0.04, relheight=0.06)

##    label_x2 = Label(root, text="Xк:", anchor='c',
##                              bg='#6b7a0a')
##    label_x2.place(relx=0, rely=0.514, relwidth=0.04, relheight=0.06)
##    line_x2 = Entry(root, bg='#6b7a0a')
##    line_x2.place(relx=0.043, rely=0.514, relwidth=0.04, relheight=0.06)
##
##    label_y2 = Label(root, text="Yк:", anchor='c',
##                              bg='#6b7a0a')
##    label_y2.place(relx=0.1, rely=0.514, relwidth=0.04, relheight=0.06)
##    line_y2 = Entry(root, bg='#6b7a0a')
##    line_y2.place(relx=0.143, rely=0.514, relwidth=0.04, relheight=0.06)

    end_figure_btn = Button(text="Замкнуть многоугольник",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: end_fig(1,
                                           color_line_combo.current())
                   )
    end_figure_btn.place(relx=0, rely=0.514, relwidth=0.3, relheight=0.05)

    add_dot_btn = Button(text="Добавить вершину",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: add_line(line_x1.get(),
                                    line_y1.get(),
                                    line_x2.get(),
                                    line_y2.get(),
                                    color_line_combo.current())
                   )
    add_dot_btn.place(relx=0, rely=0.57, relwidth=0.3, relheight=0.05)

    # Ввод отсекателя
    label_pix = Label(root, text="Координаты вершины отсекателя:", anchor='w',
                              bg='#6b7a0a')
    label_pix.place(relx=0, rely=0.655, relwidth=0.3, relheight=0.04)
    # Координаты отсекателя
    label_xrt = Label(root, text="X:", anchor='c',
                              bg='#6b7a0a')
    label_xrt.place(relx=0, rely=0.71, relwidth=0.04, relheight=0.06)
    line_xrt = Entry(root, bg='#6b7a0a')
    line_xrt.place(relx=0.043, rely=0.71, relwidth=0.04, relheight=0.06)

    label_yrt = Label(root, text="Y:", anchor='c',
                              bg='#6b7a0a')
    label_yrt.place(relx=0.1, rely=0.71, relwidth=0.04, relheight=0.06)
    line_yrt = Entry(root, bg='#6b7a0a')
    line_yrt.place(relx=0.143, rely=0.71, relwidth=0.04, relheight=0.06)

    draw_clipper_btn = Button(text="Добавить вершину отсекателя",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: add_clipper(line_xrt.get(),
                                    line_yrt.get(),
                                    color_clipper_combo.current(),
                                    color_line_combo.current())
                   )
    draw_clipper_btn.place(relx=0, rely=0.78, relwidth=0.3, relheight=0.05)

    end_clipper_btn = Button(text="Замкнуть отсекатель",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: end_clipper(1,
                                           color_clipper_combo.current())
                   )
    end_clipper_btn.place(relx=0, rely=0.84, relwidth=0.3, relheight=0.05)

    # Отсечь
    cutoff_btn = Button(text="Отсечь",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: cut_area(color_clipper_combo.current(),
                                            color_res_combo.current())
                   )
    cutoff_btn.place(relx=0, rely=0.93, relwidth=0.3, relheight=0.05)

    #Canvas
    canvas = Canvas(root, bg="#148012", #148012
                        highlightthickness=4, highlightbackground="#6b3e07")
    canvas.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
    canvas.bind("<Button-1>", lambda event: add_fig_by_click(event,
                                    color_line_combo.current(),
                                    color_clipper_combo.current()))
    canvas.bind("<Control-Button-1>", lambda event: end_fig(event,
                                           color_line_combo.current())
                                           )

    canvas.bind("<Control-Button-3>", lambda event: end_clipper(event,
                                           color_clipper_combo.current())
                                           )
    canvas.bind("<Button-3>", lambda event: add_clipper_by_click(event,
                                    color_clipper_combo.current(),
                                    color_line_combo.current()))
    root.bind("<space>",
                lambda event: cut_area(color_clipper_combo.current(),
                                            color_res_combo.current()))

    #Меню
    menu = Menu(root)
    root.config(menu=menu)
    menu.add_command(label="Задание", command=lambda:\
                        messagebox.showinfo("Задание", TASK))
    menu.add_command(label="Автор",command=lambda:\
                        messagebox.showinfo("Автор", "Симонович Р.Д. ИУ7-44Б"))
    menu.add_command(label="Очистить холст", command=lambda:\
                        del_all_dots())
    menu.add_command(label="Выход", command=root.destroy)

    #Команды
    #root.bind("<Control-z>", lambda e: last_event(e))


    root.mainloop()

if __name__ == "__main__":
    main()

