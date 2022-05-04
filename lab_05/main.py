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

WIDTH = 1000
HEIGHT = 600
RADIUS = 3

EPS = 1e-8

RESULT = False
IS_END_FIG = False

IS_FIRST_DOT = True
dots_for_cir = []
center_dot = 0

dots = []
last_activity = []

TASK = 'Алгоритм с упорядоченным списком ребер'


def del_all_dots():
    global edges, active_edges, y_groups, y_max, y_min, canvas, RESULT
    RESULT = False
    edges = [[]]
    active_edges = []
    y_groups = dict()
    y_max = 0
    y_min = 1000
    canvas.delete("all")


def draw_line(dots):
    for line in dots:
        for dot in line:
            canvas.create_line(dot[0], dot[1], dot[0] + 1, dot[1], fill=dot[2])


def bresenham_int(x_start, y_start, x_end, y_end, color):
    dx = x_end - x_start
    dy = y_end - y_start

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    e = 2*dy - dx
    y = 0

    dots = []

    for x in range(dx + 1):
        dots.append([[x_start + x*xx + y*yx, y_start + x*xy + y*yy, color]])
        if e >= 0:
            y += 1
            e -= 2*dx
        e += 2*dy

    return dots

def add_dot(event, color):
    global edges, canvas, IS_FIRST_DOT, center_dot, RESULT

    if RESULT:
        messagebox.showerror("Ошибка", "Фигура уже закрашена")
        return

    if IS_FIRST_DOT:
        IS_FIRST_DOT = False
        center_dot = canvas.create_oval(
                event.x - RADIUS, event.y - RADIUS,
                event.x + RADIUS, event.y + RADIUS,
                fill="#001", outline="#001", width=1
            )
    else:
        canvas.delete(center_dot)

    if color == 0:
        color = "#000000"
    if color == 1:
        color = "#ffffff"
    if color == 2:
        color = "#ff0000"
    if color == 3:
        color = "#0000ff"
    if color == 4:
        color = "#148012"

    edges[-1].extend([[event.x, event.y, color]])
    if len( edges[-1]) > 1:
        line = bresenham_int(
            edges[-1][-2][0],
            edges[-1][-2][1],
            edges[-1][-1][0],
            edges[-1][-1][1],
            color
        )
        draw_line(line)
        update_y_group(
            edges[-1][-2][0],
            edges[-1][-2][1],
            edges[-1][-1][0],
            edges[-1][-1][1]
        )


def add_dot_by_btn(x1, y1, color):
    global edges, canvas, IS_FIRST_DOT, center_dot, RESULT

    if RESULT:
        messagebox.showerror("Ошибка", "Фигура уже закрашена")
        return

    try:
        x = int(x1)
        y = int(y1)
    except:
        messagebox.showerror("Ошибка", "Неверные координаты")
        return

    if IS_FIRST_DOT:
        IS_FIRST_DOT = False
        center_dot = canvas.create_oval(
                x - RADIUS, y - RADIUS,
                x + RADIUS, y + RADIUS,
                fill="#001", outline="#001", width=1
            )
    else:
        canvas.delete(center_dot)

    if color == 0:
        color = "#000000"
    if color == 1:
        color = "#ffffff"
    if color == 2:
        color = "#ff0000"
    if color == 3:
        color = "#0000ff"
    if color == 4:
        color = "#148012"

    edges[-1].extend([[x, y, color]])
    if len( edges[-1]) > 1:
        line = bresenham_int(
            edges[-1][-2][0],
            edges[-1][-2][1],
            edges[-1][-1][0],
            edges[-1][-1][1],
            color
        )
        draw_line(line)
        update_y_group(
            edges[-1][-2][0],
            edges[-1][-2][1],
            edges[-1][-1][0],
            edges[-1][-1][1]
        )


def end_fig(event, color):
    global edges, canvas, IS_FIRST_DOT, center_dot, IS_END_FIG

    IS_END_FIG = True

    if color == 0:
        color = "#000000"
    if color == 1:
        color = "#ffffff"
    if color == 2:
        color = "#ff0000"
    if color == 3:
        color = "#0000ff"
    if color == 4:
        color = "#148012"

    if len(edges[-1]) > 2:
        IS_FIRST_DOT = True
        line = bresenham_int(
            edges[-1][0][0],
            edges[-1][0][1],
            edges[-1][-1][0],
            edges[-1][-1][1],
            color
        )
        draw_line(line)
        update_y_group(
            edges[-1][0][0],
            edges[-1][0][1],
            edges[-1][-1][0],
            edges[-1][-1][1]
        )
        edges.append([])
    else:
        messagebox.showerror("Ошибка", "Недостаточно ребер")


def update_y_group(x_start, y_start, x_end, y_end):
    global edges, y_groups, y_max, y_min
    if y_start > y_end:
       x_end, x_start = x_start, x_end
       y_end, y_start = y_start, y_end

    if y_end >  y_max:
        y_max = y_end

    if y_start <  y_min:
        y_min = y_start

    y_proj = y_end - y_start if y_end - y_start else 1
    x_step = -(x_end - x_start) / y_proj
    if y_proj != 1:
        if y_end not in  y_groups:
            y_groups[y_end] = [[x_end, x_step, y_proj]]
        else:
            y_groups[y_end].extend([[x_end, x_step, y_proj]])


def check_active_edges(active_edges):
    i = 0
    while i < len(active_edges):
        active_edges[i][0] += active_edges[i][1]
        active_edges[i][2] -= 1
        if active_edges[i][2] < 1:
            active_edges.pop(i)
        else:
            i += 1


def add_active_edges(y_groups, active_edges, y):
    if y in y_groups:
        for edge in y_groups[y]:
            active_edges.append(edge)
    active_edges.sort(key=lambda edge: edge[0])


def draw_scanline(y, color):
    global active_edges, canvas
    print(active_edges)
    for i in range(0, len(active_edges), 2):
        canvas.create_line(int(active_edges[i][0]),
                            y,
                            round(active_edges[i+1][0]),
                            y,
                            fill=color
                           )


def fill(root, delay, color, label_time_2):
    global active_edges, y_groups, y_max, y_min, canvas, RESULT, IS_END_FIG
    print(y_groups)

    if not IS_END_FIG:
        messagebox.showerror("Ошибка", "Нет фигуры для закраски")
        return
    if RESULT:
        messagebox.showerror("Ошибка", "Фигура уже закрашена")
        return
    RESULT = True
    IS_END_FIG = False

    if color == 0:
        color = "#000000"
    if color == 1:
        color = "#ffffff"
    if color == 2:
        color = "#ff0000"
    if color == 3:
        color = "#0000ff"
    if color == 4:
        color = "#148012"

    start = time()

    y_end = y_max
    y_start = y_min
    while y_end > y_start:
        check_active_edges(active_edges)
        add_active_edges(y_groups, active_edges, y_end)
        if delay:
            sleep(0.02)
            canvas.update()
        draw_scanline(y_end, color)
        y_end -= 1

    end = time()

    prog_time = round((end - start), 10)

    label_time_2.config(text = str(prog_time))

def main():
    global edges, active_edges, y_groups, y_max, y_min, canvas

    edges = [[]]
    y_groups = dict()
    y_max = 0
    y_min = HEIGHT
    active_edges = []

    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №5")
    root.minsize(WIDTH, HEIGHT)
    root["bg"] = "#6b5a45"

    #label меню
    label_menu = Label(root, text="Меню",
                              bg='#6b7a0a')
    label_menu.place(relx=0, rely=0, relwidth=0.3, relheight=0.04)

    #Выбор цвета; Установка combox`a
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

    label_color = Label(text="Цвет закраски:", bg="#6b7a0a", anchor='w')
    label_color.place(relx=0, rely=0.06, relwidth=0.3, relheight=0.04)

    color_list = ("Черный", "Белый", "Красный",
                   "Синий", "Зеленый")
    font_combo = ("Times", 12)

    color_combo = ttk.Combobox(root, state='readonly', values=color_list,
                    font=font_combo)
    color_combo.place(relx=0, rely=0.1, relwidth=0.3, relheight=0.06)
    color_combo.current(0)

    # С задержкой / без задержки
    type_list = ("Без задержки", "С задержкой")

    label_type = Label(root, text="Тип закраски:", anchor='w',
                              bg='#6b7a0a')
    label_type.place(relx=0, rely=0.162, relwidth=0.1, relheight=0.06)
    type_combo = ttk.Combobox(root, state='readonly', values=type_list,
                    font=font_combo)
    type_combo.place(relx=0.1, rely=0.162, relwidth=0.2, relheight=0.06)
    type_combo.current(0)

    # Ввод точки
    label_shift = Label(root, text="Координаты точки:", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.245, relwidth=0.3, relheight=0.04)
    #Координаты точки
    label_x1 = Label(root, text="X:", anchor='c',
                              bg='#6b7a0a')
    label_x1.place(relx=0, rely=0.29, relwidth=0.04, relheight=0.06)
    line_x1 = Entry(root, bg='#6b7a0a')
    line_x1.place(relx=0.043, rely=0.29, relwidth=0.04, relheight=0.06)

    label_y1 = Label(root, text="Y:", anchor='c',
                              bg='#6b7a0a')
    label_y1.place(relx=0.1, rely=0.29, relwidth=0.04, relheight=0.06)
    line_y1 = Entry(root, bg='#6b7a0a')
    line_y1.place(relx=0.143, rely=0.29, relwidth=0.04, relheight=0.06)

    cir_btn = Button(text="Добавить точку",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: add_dot_by_btn(line_x1.get(),
                                    line_y1.get(),
                                    color_combo.current())
                   )
    cir_btn.place(relx=0, rely=0.36, relwidth=0.3, relheight=0.05)

    # Замкнуть фигуру
    end_btn = Button(text="Замкнуть фигуру",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: end_fig(0,
                  color_combo.current())
                    )
    end_btn.place(relx=0, rely=0.46, relwidth=0.3, relheight=0.05)

    # Закрасить
    fill_btn = Button(text="Закрасить",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: fill(root, type_combo.current(),
                                    color_combo.current(),
                                    label_time_2)
                   )
    fill_btn.place(relx=0, rely=0.56, relwidth=0.3, relheight=0.05)

    # Время
    label_time_1 = Label(root, text="Время (в секундах):", anchor='w',
                              bg='#6b7a0a')
    label_time_1.place(relx=0, rely=0.66, relwidth=0.4, relheight=0.04)

    label_time_2 = Label(root, text="0.0 ", anchor='w',
                              bg='#6b7a0a')
    label_time_2.place(relx=0, rely=0.7, relwidth=0.4, relheight=0.04)


    #Canvas
    canvas = Canvas(root, bg="#148012", #148012
                        highlightthickness=4, highlightbackground="#6b3e07")
    canvas.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
    canvas.bind("<Button-1>", lambda event: add_dot(event,
        color_combo.current()))
    canvas.bind("<Button-3>", lambda event: end_fig(event,
        color_combo.current()))
    canvas.bind("<Button-2>", lambda event: fill(root, type_combo.current(),
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
