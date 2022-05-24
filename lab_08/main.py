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

IS_FIRST_DOT = True
x_first, y_first = 0, 0
center_dot = 0

IS_FIRST_DOT_CLIP = True
x_first_clip, y_first_clip = 0, 0
center_dot_clip = 0

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

TASK = 'Алгоритм Кируса-Бэка'


def del_all_dots():
    global lines, clipper, IS_FIRST_DOT_CLIP, IS_END_FIG
    IS_FIRST_DOT_CLIP = True
    IS_END_FIG = False

    canvas.delete("all")

    lines = [[]]
    clipper = []


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

def add_clipper_by_click(event, color):
    global clipper, IS_FIRST_DOT_CLIP, x_first_clip,\
        y_first_clip, center_dot_clip, IS_END_FIG

    if IS_END_FIG:
        del_all_dots()

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


def end_fig(event, color):
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


# Алгоритм
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



def extra_check(): # чтобы не было пересечений

    clipper_lines = []

    for i in range(len(clipper) - 1):
        clipper_lines.append([clipper[i], clipper[i + 1]]) # разбиваю отсекатель на линии

    combs_lines = list(combinations(clipper_lines, 2)) # все возможные комбинации сторон

    for i in range(len(combs_lines)):
        line1 = combs_lines[i][0]
        line2 = combs_lines[i][1]

        if (are_connected_sides(line1, line2)):
            #print("Connected")
            continue

        a1, b1, c1 = line_koefs(line1[0][X_DOT], line1[0][Y_DOT], line1[1][X_DOT], line1[1][Y_DOT])
        a2, b2, c2 = line_koefs(line2[0][X_DOT], line2[0][Y_DOT], line2[1][X_DOT], line2[1][Y_DOT])

        dot_intersec = solve_lines_intersection(a1, b1, c1, a2, b2, c2)

        if (is_dot_between(line1[0], line1[1], dot_intersec)) \
                and (is_dot_between(line2[0], line2[1], dot_intersec)):
            return True

    return False


def check_polygon():
    if (len(clipper) < 3):
        return False

    sign = 0

    if (vector_mul(get_vector(clipper[1], clipper[2]), get_vector(clipper[0], clipper[1])) > 0):
        sign = 1
    else:
        sign = -1

    for i in range(3, len(clipper)):
        if sign * vector_mul(get_vector(clipper[i - 1], clipper[i]), get_vector(clipper[i - 2], clipper[i - 1])) < 0:
            return False

    check = extra_check()

    #print("\n\nResult:", check, "\n\n")

    if (check):
        return False

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


def cyrus_beck_algorithm(line, count, color_res):
    dot1 = line[0]
    dot2 = line[1]

    d = [dot2[X_DOT] - dot1[X_DOT], dot2[Y_DOT] - dot1[Y_DOT]]

    t_bottom = 0
    t_top = 1

    for i in range(-2, count - 2):
        normal = get_normal(clipper[i], clipper[i + 1], clipper[i + 2])

        w = [dot1[X_DOT] - clipper[i][X_DOT], dot1[Y_DOT] - clipper[i][Y_DOT]]

        d_scalar = scalar_mul(d, normal)
        w_scalar = scalar_mul(w, normal)

        if (d_scalar == 0):
            if (w_scalar < 0):
                return
            else:
                continue

        t = -w_scalar / d_scalar

        if (d_scalar > 0):
            if (t <= 1):
                t_bottom = max(t_bottom, t)
            else:
                return
        elif (d_scalar < 0):
            if (t >= 0):
                t_top = min(t_top, t)
            else:
                return

        if (t_bottom > t_top):
            break


    dot1_res = [round(dot1[X_DOT] + d[X_DOT] * t_bottom), round(dot1[Y_DOT] + d[Y_DOT] * t_bottom)]
    dot2_res = [round(dot1[X_DOT] + d[X_DOT] * t_top), round(dot1[Y_DOT] + d[Y_DOT] * t_top)]

    res_color = parse_color(color_res)

    if (t_bottom <= t_top):
        canvas.create_line(dot1_res, dot2_res, fill = res_color)

def find_start_dot():
    y_max = clipper[0][Y_DOT]
    dot_index = 0

    for i in range(len(clipper)):
        if (clipper[i][Y_DOT] > y_max):
            y_max = clipper[i][Y_DOT]
            dot_index = i

    clipper.pop()

    for _ in range(dot_index):
        clipper.append(clipper.pop(0))

    clipper.append(clipper[0])

    if (clipper[-2][0] > clipper[1][0]):
        clipper.reverse()

def cut_area(color_clipper, color_res):
    global IS_END_FIG, clipper
    if not IS_END_FIG:
        messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
        return

    if (len(clipper) < 3):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if (not check_polygon()):
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    clipper_color = parse_color(color_clipper)
    canvas.create_polygon(clipper, outline = clipper_color, fill = "#148012")

    find_start_dot()

    dot = clipper.pop()

    for line in lines:
        if (line):
            cyrus_beck_algorithm(line, len(clipper), color_res)

    clipper.append(dot)

def add_paral_line_clipper(event):
    #print("Pressed: Space", event.x, event.y)

    dif_x = abs(event.x - clipper[len(clipper) - 1][X_DOT])
    dif_y = abs(event.y - clipper[len(clipper) - 1][Y_DOT])

    if (dif_x > dif_y):
        add_dot(event.x, clipper[len(clipper) - 1][Y_DOT])
    else:
        add_dot(clipper[len(clipper) - 1][X_DOT], event.y)


def add_paral_line_line(event):
    #print("Pressed: Control_L", event.x, event.y)

    cur_line = len(lines) - 1

    if (len(lines[cur_line]) > 0):
        dif_x = abs(event.x - lines[cur_line][0][X_DOT])
        dif_y = abs(event.y - lines[cur_line][0][Y_DOT])

        if (dif_x > dif_y):
            add_line(event.x, lines[cur_line][0][Y_DOT])
        else:
            add_line(lines[cur_line][0][X_DOT], event.y)


def main():
    global lines, clipper, canvas

    lines = [[]]
    clipper = []
    x_draw = 0
    y_draw = 0

    y_groups = dict()
    y_max = 0
    y_min = 1000
    active_edges = []

    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №8")
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
    label_shift = Label(root, text="Координаты концов отрезка:", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.4, relwidth=0.3, relheight=0.04)
    #Координаты отрезка
    label_x1 = Label(root, text="Xн:", anchor='c',
                              bg='#6b7a0a')
    label_x1.place(relx=0, rely=0.445, relwidth=0.04, relheight=0.06)
    line_x1 = Entry(root, bg='#6b7a0a')
    line_x1.place(relx=0.043, rely=0.445, relwidth=0.04, relheight=0.06)

    label_y1 = Label(root, text="Yн:", anchor='c',
                              bg='#6b7a0a')
    label_y1.place(relx=0.1, rely=0.445, relwidth=0.04, relheight=0.06)
    line_y1 = Entry(root, bg='#6b7a0a')
    line_y1.place(relx=0.143, rely=0.445, relwidth=0.04, relheight=0.06)

    label_x2 = Label(root, text="Xк:", anchor='c',
                              bg='#6b7a0a')
    label_x2.place(relx=0, rely=0.514, relwidth=0.04, relheight=0.06)
    line_x2 = Entry(root, bg='#6b7a0a')
    line_x2.place(relx=0.043, rely=0.514, relwidth=0.04, relheight=0.06)

    label_y2 = Label(root, text="Yк:", anchor='c',
                              bg='#6b7a0a')
    label_y2.place(relx=0.1, rely=0.514, relwidth=0.04, relheight=0.06)
    line_y2 = Entry(root, bg='#6b7a0a')
    line_y2.place(relx=0.143, rely=0.514, relwidth=0.04, relheight=0.06)

    add_dot_btn = Button(text="Добавить отрезок",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: add_line(line_x1.get(),
                                    line_y1.get(),
                                    line_x2.get(),
                                    line_y2.get(),
                                    color_line_combo.current())
                   )
    add_dot_btn.place(relx=0, rely=0.585, relwidth=0.3, relheight=0.05)

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
                                    color_clipper_combo.current())
                   )
    draw_clipper_btn.place(relx=0, rely=0.78, relwidth=0.3, relheight=0.05)

    end_clipper_btn = Button(text="Замкнуть отсекатель",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: add_clipper(line_xrt.get(),
                                    line_yrt.get(),
                                    line_xlb.get(),
                                    line_ylb.get(),
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
    canvas.bind("<Button-1>", lambda event: add_line_by_click(event,
        color_line_combo.current()))
    canvas.bind("<Button-2>", lambda event: end_fig(event,
                                           color_clipper_combo.current())
                                           )
    canvas.bind("<Button-3>", lambda event: add_clipper_by_click(event,
                                    color_clipper_combo.current()))
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




