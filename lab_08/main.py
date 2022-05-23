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

TASK = 'Алгоритм Сазерленда - Коэна'


def del_all_dots():
    global lines, rect

    canvas.delete("all")

    lines = [[]]
    rect = [-1, -1, -1, -1]


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


def add_clipper(x1, y1, x2, y2, color):
    global rect

    try:
        x_min = int(x1)
        y_max = int(y1)
        x_max = int(x2)
        y_min = int(y2)
    except:
        messagebox.showinfo("Ошибка", "Неверно введены координаты")
        return

    cutter_color = parse_color(color)

    canvas.delete("all")
    canvas.create_rectangle(x_min, y_max, x_max, y_min, outline = cutter_color)

    rect = [x_min, x_max, y_min, y_max]

    draw_sides()

def add_clipper_by_click(event, color):
    global rect, IS_FIRST_DOT_CLIP, x_first_clip, y_first_clip, center_dot_clip

    if IS_FIRST_DOT_CLIP:
        x_first_clip = int(event.x)
        y_first_clip = int(event.y)
        IS_FIRST_DOT_CLIP = False
        center_dot_clip = canvas.create_oval(
                event.x - RADIUS, event.y - RADIUS,
                event.x + RADIUS, event.y + RADIUS,
                fill="#fff", outline="#001", width=1
            )
        return
    else:
        canvas.delete(center_dot_clip)

    x_min = x_first_clip
    y_min = y_first_clip
    x_max = int(event.x)
    y_max = int(event.y)
    IS_FIRST_DOT_CLIP = True

    cutter_color = parse_color(color)

    canvas.delete("all")
    canvas.create_rectangle(x_min, y_max, x_max, y_min, outline = cutter_color)

    rect = [x_min, x_max, y_min, y_max]

    draw_sides()

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



def main():
    global lines, rect, canvas

    lines = [[]]
    rect = []
    x_draw = 0
    y_draw = 0

    y_groups = dict()
    y_max = 0
    y_min = 1000
    active_edges = []

    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №7")
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
                                    line_xlb.get(),
                                    line_ylb.get(),
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
                  command=lambda: cut_area(color_res_combo.current(),
                                           color_clipper_combo.current())
                   )
    cutoff_btn.place(relx=0, rely=0.93, relwidth=0.3, relheight=0.05)

    #Canvas
    canvas = Canvas(root, bg="#148012", #148012
                        highlightthickness=4, highlightbackground="#6b3e07")
    canvas.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
    canvas.bind("<Button-1>", lambda event: add_line_by_click(event,
        color_line_combo.current()))
    canvas.bind("<Button-2>", lambda event: cut_area(color_res_combo.current(),
                                           color_clipper_combo.current())
                                           )
    canvas.bind("<Button-3>", lambda event: add_clipper_by_click(event,
                                    color_clipper_combo.current()))
    root.bind("<space>",
                lambda event: fill(event, type_combo.current(),
                                    color_combo.current(),
                                    label_time_2))

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
