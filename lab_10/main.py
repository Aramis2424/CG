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
from tkinter import Tk, Button, Label, Entry, END,\
    Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar, PhotoImage
from tkinter import messagebox
import time
from itertools import combinations
from numpy import arange

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

TASK = 'Алгоритм Плавающий горизонт'
# Define
X_DOT = 0
Y_DOT = 1
Z_DOT = 2

FROM = 0
TO = 1
STEP = 2

FROM_SPIN_BOX = -1000.0
TO_SPIN_BOX = 1000.0
STEP_SPIN_BOX = 0.1

DEFAULT_SCALE = 45
DEFAULT_ANGLE = 30

# Для вращения
trans_matrix = []

def del_all_dots():
    global canvas
    canvas.delete("all")
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
def parse_funcs(func_num):
    func = lambda x, z: sin(x) * cos(z)

    if (func_num == 0):
        func = lambda x, z: sin(x)**2 + cos(z)**2
    elif (func_num == 1):
        func = lambda x, z: 2*sin(x) * sin(z)
    elif (func_num == 2):
        func = lambda x, z: sin(x) - cos(z)
    elif (func_num == 3):
        func = lambda x, z: cos(x) * cos(z)
    return func

def get_fill_check_color(collor_fill):
    return (int(collor_fill[1:3], 16), int(collor_fill[3:5], 16),\
            int(collor_fill[5:7], 16))

def read_limits():
    global line_x1, line_y1, line_z1,\
           line_x2, line_y2, line_z2
    try:
        x_from = float(line_x1.get())
        x_to = float(line_y1.get())
        x_step = float(line_z1.get())

        x_limits = [x_from, x_to, x_step]

        z_from = float(line_x2.get())
        z_to = float(line_y2.get())
        z_step = float(line_z2.get())

        z_limits = [z_from, z_to, z_step]

        return x_limits, z_limits
    except:
        return -5, 5

def rotate_matrix(matrix):
    global trans_matrix

    res_matrix = [[0 for i in range(4)] for j in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                res_matrix[i][j] += trans_matrix[i][k] * matrix[k][j]

    trans_matrix = res_matrix

def spin_x(angel, func, color):
    try:
        angle = float(angel) / 180 * pi
    except:
        messagebox.showerror("Ошибка", "Угол - число")
        return

    if (len(trans_matrix) == 0):
        messagebox.showerror("Ошибка", "График не задан")
        return

    rotating_matrix = [[1, 0, 0, 0],
                     [0, cos(angle), sin(angle), 0],
                     [0, -sin(angle), cos(angle), 0],
                     [0, 0, 0, 1]   ]

    rotate_matrix(rotating_matrix)

    build_graph(func, color)

def spin_y(angel, func, color):
    try:
        angle = float(angel) / 180 * pi
    except:
        messagebox.showerror("Ошибка", "Угол - число")
        return

    if (len(trans_matrix) == 0):
        messagebox.showerror("Ошибка", "График не задан")
        return

    rotating_matrix = [[cos(angle), 0, -sin(angle), 0],
                     [0, 1, 0, 0],
                     [sin(angle), 0, cos(angle), 0],
                     [0, 0, 0, 1]   ]

    rotate_matrix(rotating_matrix)

    build_graph(func, color)

def spin_z(angel, func, color):
    try:
        angle = float(angel) / 180 * pi
    except:
        messagebox.showerror("Ошибка", "Угол - число")
        return

    if (len(trans_matrix) == 0):
        messagebox.showerror("Ошибка", "График не задан")
        return

    rotating_matrix = [[cos(angle), sin(angle), 0, 0],
                     [-sin(angle), cos(angle), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]   ]

    rotate_matrix(rotating_matrix)

    build_graph(func, color)

def scale_graph(scale, func, color):
    try:
        scale_param = float(scale)
    except:
        messagebox.showerror("Ошибка",\
            "Коэффициент масштабирования должен быть числом")
        return

    if (len(trans_matrix) == 0):
        messagebox.showerror("Ошибка", "График не задан")
        return

    build_graph(func, color, scale_param = scale_param)

def trans_dot(dot, scale_param):
    dot.append(1)

    #print(dot)

    res_dot = [0, 0, 0, 0]

    for i in range(4):
        for j in range(4):
            res_dot[i] += dot[j] * trans_matrix[j][i]

    #print(res_dot)

    for i in range(3):
        res_dot[i] *= scale_param

    res_dot[0] += WIDE // 2
    res_dot[1] += HEIGHT // 2

    return res_dot[:3]

def is_visible(dot):
    return (0 <= dot[X_DOT] <= WIDE) and \
            (0 <= dot[Y_DOT] <= HEIGHT)

def draw_pixel(x, y, color):
    color = parse_color(color)

    canvas.create_line(x, y, x + 1, y + 1, fill = color)

def draw_dot(x, y, high_horizon, low_horizon, color):
    if (not is_visible([x, y])):
        return False

    #print(x, y)

    if (y > high_horizon[x]):
        high_horizon[x] = y
        draw_pixel(x, y, color)
    elif (y < low_horizon[x]):
        low_horizon[x] = y
        draw_pixel(x, y, color)

    return True

def draw_horizon_part(dot1, dot2, high_horizon, low_horizon, color):
    if (dot1[X_DOT] > dot2[X_DOT]):
        dot1, dot2 = dot2, dot1

    #print(dot1, dot2)

    dx = dot2[X_DOT] - dot1[X_DOT]
    dy = dot2[Y_DOT] - dot1[Y_DOT]

    if (dx > dy):
        l = dx
    else:
        l = dy

    dx /= l
    dy /= l

    x = dot1[X_DOT]
    y = dot1[Y_DOT]

    for _ in range(int(l) + 1):
        if (not draw_dot(round(x), y, high_horizon, low_horizon, color)):
            return

        x += dx
        y += dy

def draw_horizon(function, high_horizon, low_horizon, limits, z,\
                scale_param, color):
    f = lambda x: function(x, z)

    prev = None

    for x in arange(limits[FROM], limits[TO] + limits[STEP], limits[STEP]):
        cur = trans_dot([x, f(x), z], scale_param)

        if (prev):
            draw_horizon_part(prev, cur, high_horizon, low_horizon, color)

        prev = cur

def draw_horizon_limits(f, x_limits, z_limits, scale_param, color):
    color = parse_color(color)

    for z in arange(z_limits[FROM], z_limits[TO] + z_limits[STEP],
                                                            z_limits[STEP]):
        dot1 = trans_dot([x_limits[FROM], f(x_limits[FROM], z), z], scale_param)
        dot2 = trans_dot([x_limits[FROM], f(x_limits[FROM],
            z + x_limits[STEP]), z + x_limits[STEP]], scale_param)

        canvas.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT],
            dot2[Y_DOT], fill = color)

        dot1 = trans_dot([x_limits[TO], f(x_limits[TO], z), z], scale_param)
        dot2 = trans_dot([x_limits[TO], f(x_limits[TO], z + x_limits[STEP]),
            z + x_limits[STEP]], scale_param)

        canvas.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT],
            dot2[Y_DOT], fill = color)

def set_trans_matrix():
    global trans_matrix

    trans_matrix.clear()

    for i in range(4):
        tmp_arr = []

        for j in range(4):
            tmp_arr.append(int(i == j))

        trans_matrix.append(tmp_arr)
def build_graph(func, color, new_graph = False, scale_param = DEFAULT_SCALE):
    del_all_dots()

    if (new_graph):
        set_trans_matrix()

    f = parse_funcs(func)

    x_limits, z_limits = read_limits()

    #print(x_limits, z_limits)

    high_horizon = [0 for i in range(WIDE + 1)]
    low_horizon = [HEIGHT for i in range(WIDE + 1)]

    #  Горизонт
    for z in arange(z_limits[FROM],
        z_limits[TO] + z_limits[STEP], z_limits[STEP]):
        draw_horizon(f, high_horizon, low_horizon,\
            x_limits, z, scale_param, color)

    # Границы горизонта
    draw_horizon_limits(f, x_limits, z_limits, scale_param, color)



def main():
    global line_x1, line_y1, line_z1,\
           line_x2, line_y2, line_z2, canvas

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
    root.title("Лабораторная работа №10")
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

    func_list = ("y = sin^2(x) + cos^2(z)",
                 "y = 2*sin(x) * sin(z)",
                 "y = sin(x) - cos(x)",
                 "y = cos(x) * cos(z)")

    # Выбор цвета результата
    label_color = Label(text="Цвет результата:", bg="#6b7a0a", anchor='w')
    label_color.place(relx=0, rely=0.16, relwidth=0.3, relheight=0.04)

    color_res_combo = ttk.Combobox(root, state='readonly', values=color_list,
                    font=font_combo)
    color_res_combo.place(relx=0, rely=0.2, relwidth=0.3, relheight=0.06)
    color_res_combo.current(0)

    # Выбор функции
    label_color = Label(text="Функция:", bg="#6b7a0a", anchor='w')
    label_color.place(relx=0, rely=0.05, relwidth=0.3, relheight=0.04)

    func_combo = ttk.Combobox(root, state='readonly', values=func_list,
                    font=font_combo)
    func_combo.place(relx=0, rely=0.09, relwidth=0.3, relheight=0.06)
    func_combo.current(0)

    # Ввод отрезка
    label_shift = Label(root, text="Пределы (ось X):", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.3, relwidth=0.3, relheight=0.04)
    #Координаты отрезка
    label_x1 = Label(root, text="Нач:", anchor='c',
                              bg='#6b7a0a')
    label_x1.place(relx=0, rely=0.345, relwidth=0.04, relheight=0.06)
    line_x1 = Entry(root, bg='#6b7a0a')
    line_x1.insert(0, "-5")
    line_x1.place(relx=0.043, rely=0.345, relwidth=0.04, relheight=0.06)

    label_y1 = Label(root, text="Кон:", anchor='c',
                              bg='#6b7a0a')
    label_y1.place(relx=0.1, rely=0.345, relwidth=0.04, relheight=0.06)
    line_y1 = Entry(root, bg='#6b7a0a')
    line_y1.insert(0, "5")
    line_y1.place(relx=0.143, rely=0.345, relwidth=0.04, relheight=0.06)

    label_z1 = Label(root, text="Шаг:", anchor='c',
                              bg='#6b7a0a')
    label_z1.place(relx=0.2, rely=0.345, relwidth=0.04, relheight=0.06)
    line_z1 = Entry(root, bg='#6b7a0a')
    line_z1.insert(0, "0.2")
    line_z1.place(relx=0.243, rely=0.345, relwidth=0.04, relheight=0.06)

    label_shift = Label(root, text="Пределы (ось Z):", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.414, relwidth=0.3, relheight=0.04)
    label_x2 = Label(root, text="Нач:", anchor='c',
                              bg='#6b7a0a')
    label_x2.place(relx=0, rely=0.464, relwidth=0.04, relheight=0.06)
    line_x2 = Entry(root, bg='#6b7a0a')
    line_x2.insert(0, "-5")
    line_x2.place(relx=0.043, rely=0.464, relwidth=0.04, relheight=0.06)

    label_y2 = Label(root, text="Кон:", anchor='c',
                              bg='#6b7a0a')
    label_y2.place(relx=0.1, rely=0.464, relwidth=0.04, relheight=0.06)
    line_y2 = Entry(root, bg='#6b7a0a')
    line_y2.insert(0, "5")
    line_y2.place(relx=0.143, rely=0.464, relwidth=0.04, relheight=0.06)

    label_z2 = Label(root, text="Шаг:", anchor='c',
                              bg='#6b7a0a')
    label_z2.place(relx=0.2, rely=0.464, relwidth=0.04, relheight=0.06)
    line_z2 = Entry(root, bg='#6b7a0a')
    line_z2.insert(0, "0.2")
    line_z2.place(relx=0.243, rely=0.464, relwidth=0.04, relheight=0.06)


    label_scale = Label(root, text="Масштабирование:", anchor='w',
                              bg='#6b7a0a')
    label_scale.place(relx=0, rely=0.56, relwidth=0.3, relheight=0.04)
    label_xrt = Label(root, text="k:", anchor='c',
                              bg='#6b7a0a')
    label_xrt.place(relx=0, rely=0.61, relwidth=0.04, relheight=0.06)
    line_k = Entry(root, bg='#6b7a0a')
    line_k.insert(0, '100')
    line_k.place(relx=0.043, rely=0.61, relwidth=0.04, relheight=0.06)
    draw_clipper_btn = Button(text="Масштабировать",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: scale_graph(line_k.get(), func_combo.current(),
                                              color_res_combo.current())
                   )
    draw_clipper_btn.place(relx=0.1, rely=0.61, relwidth=0.12, relheight=0.06)


    # Ввод отсекателя
    label_pix = Label(root, text="Вращение:", anchor='w',
                              bg='#6b7a0a')
    label_pix.place(relx=0, rely=0.715, relwidth=0.3, relheight=0.04)
    # Координаты отсекателя
    label_xrt = Label(root, text="X:", anchor='c',
                              bg='#6b7a0a')
    label_xrt.place(relx=0, rely=0.77, relwidth=0.04, relheight=0.06)
    line_xrt = Entry(root, bg='#6b7a0a')
    line_xrt.insert(0, "45")
    line_xrt.place(relx=0.043, rely=0.77, relwidth=0.04, relheight=0.06)
    x_btn = Button(text="Вращать",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: spin_x(line_xrt.get(), func_combo.current(),
                                              color_res_combo.current())
                   )
    x_btn.place(relx=0, rely=0.84, relwidth=0.08, relheight=0.05)

    label_yrt = Label(root, text="Y:", anchor='c',
                              bg='#6b7a0a')
    label_yrt.place(relx=0.1, rely=0.77, relwidth=0.04, relheight=0.06)
    line_yrt = Entry(root, bg='#6b7a0a')
    line_yrt.insert(0, "45")
    line_yrt.place(relx=0.143, rely=0.77, relwidth=0.04, relheight=0.06)
    y_btn = Button(text="Вращать",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: spin_y(line_yrt.get(), func_combo.current(),
                                              color_res_combo.current())
                   )
    y_btn.place(relx=0.1, rely=0.84, relwidth=0.08, relheight=0.05)

    label_yrt = Label(root, text="Z:", anchor='c',
                              bg='#6b7a0a')
    label_yrt.place(relx=0.2, rely=0.77, relwidth=0.04, relheight=0.06)
    line_zrt = Entry(root, bg='#6b7a0a')
    line_zrt.insert(0, "45")
    line_zrt.place(relx=0.243, rely=0.77, relwidth=0.04, relheight=0.06)
    z_btn = Button(text="Вращать",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: spin_z(line_zrt.get(), func_combo.current(),
                                              color_res_combo.current())
                   )
    z_btn.place(relx=0.2, rely=0.84, relwidth=0.08, relheight=0.05)

    # Отсечь
    cutoff_btn = Button(text="Изобразить",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: build_graph(func_combo.current(),
                                              color_res_combo.current(),
                                              new_graph = True)
                   )
    cutoff_btn.place(relx=0, rely=0.92, relwidth=0.3, relheight=0.05)

    #Canvas
    canvas = Canvas(root, bg="#148012", #148012
                        highlightthickness=4, highlightbackground="#6b3e07")
    canvas.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

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
