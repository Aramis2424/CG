import copy
import math
import sys
import time
from tkinter import Tk, Button, Label, Entry, Canvas,\
    messagebox, Menu, Frame, SUNKEN, colorchooser
from tkinter import ttk
import matplotlib.pyplot as plt
from colorutils import Color
from math import sqrt, cos, sin, pi

WIDTH = 1000
HEIGHT = 600
RADIUS = 3

EPS = 1e-8

IS_FIRST_DOT = True
dots_for_line = []

dots = []
last_activity = []

TASK = '''Реализовать алгоритмы построения окружности и эллипса методами: \n
- Канонического уравнения\n
- Параметрического уравнения\n
- Алгоритма Брезенхема\n
- Алгоритма средней точки\n
Построить спектр окружностей и эллипсов.\n
Замерить время работы алгоритмов.'''


def del_all_dots():
    canvas.delete("all")

##import tkinter as tk
##from math import cos, sin, radians
##
##root = tk.Tk()
##canvas = tk.Canvas(root, width=400, height=400)
##
##x_offset = 200
##y_offset = 200
##radius = 100
##
##coords = [ (radius * cos(radians(angle)), radius * sin(radians(angle))) for angle in range(360)]
##
### Замыкаем круг путём добавления первой координаты в конец списка.
### Иначе будет разрыв между последней и первой точкой.
##coords.append(coords[0])
##for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
##    canvas.create_line(x_offset + x1, y_offset + y1, x_offset + x2, y_offset + y2, width=3)
#Окружности
def cir_lib_method(center, radius, color):
    x_c = center[0]
    y_c = center[1]
    color = color.hex

    canvas.create_oval(
                    x_c - radius, y_c - radius,
                    x_c + radius, y_c + radius,
                    fill="#148012", outline=color, width=1
                    )


def cir_canon_method(center, radius, color):
    c_dots = []
    x_c = center[0]
    y_c = center[1]
    color = color.hex

    end = round(radius / sqrt(2))

    r2 = radius ** 2
    x = 0
    while x <= end:
        y = round(sqrt(r2 - x ** 2))

        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        c_dots.append([x_c + y, y_c + x, color])
        c_dots.append([x_c - y, y_c + x, color])
        c_dots.append([x_c + y, y_c - x, color])
        c_dots.append([x_c - y, y_c - x, color])

        x += 1
    return c_dots, 0


def cir_param_method(dot_center, radius, color):
    x_c = dot_center[0]
    y_c = dot_center[1]
    c_dots = []
    color = color.hex
    step = 1 / radius

    alpha = 0

    while alpha < pi / 4 + step:
        x = round(radius * cos(alpha))
        y = round(radius * sin(alpha))

        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        c_dots.append([x_c + y, y_c + x, color])
        c_dots.append([x_c - y, y_c + x, color])
        c_dots.append([x_c + y, y_c - x, color])
        c_dots.append([x_c - y, y_c - x, color])

        alpha += step
    return c_dots, 0


def cir_bresenham_method(dot_center, radius, color):
    x_c = round(dot_center[0])
    y_c = round(dot_center[1])
    c_dots = []
    color = color.hex
    x = 0
    y = radius
    tmp_pxl = 1
    delta_i = 2 * (1 - radius)

    err = 0

    while x <= y:
        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        c_dots.append([x_c + y, y_c + x, color])
        c_dots.append([x_c - y, y_c + x, color])
        c_dots.append([x_c + y, y_c - x, color])
        c_dots.append([x_c - y, y_c - x, color])

        if delta_i <= 0:
            err = 2 * delta_i + 2 * y - 1

            if err < 0:
                x = x + 1
                delta_i = delta_i + 2 * x + 3
            else:
                x = x + 1
                y = y - 1
                delta_i = delta_i + 2 * x - 2 * y + 6
        elif delta_i > 0:
            err = 2 * delta_i - 2 * x - 1

            if err < 0:
                x = x + 1
                y = y - 1
                delta_i = delta_i + 2 * x - 2 * y + 6
            else:
                y = y - 1
                delta_i = delta_i - 2 * y + 1
    return c_dots, 0


def cir_mid_dot_method(dot_center, radius, color):
    x_c = dot_center[0]
    y_c = dot_center[1]
    c_dots = []
    color = color.hex
    x = 0
    y = radius

    delta = 1 - radius

    while x <= y:
        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        c_dots.append([x_c + y, y_c + x, color])
        c_dots.append([x_c - y, y_c + x, color])
        c_dots.append([x_c + y, y_c - x, color])
        c_dots.append([x_c - y, y_c - x, color])

        x += 1

        if delta < 0:
            delta = delta + 2 * x + 1
        else:
            y -= 1
            delta = delta + 2 * (x - y) + 1
    return c_dots, 0


#Эллипсы


def draw_cir(center, radius, color, method):
    global last_activity, dots
    if color == 0:
        color = Color(hex='#000000')
    if color == 1:
        color = Color(hex='#ffffff')
    if color == 2:
        color = Color(hex='#ff0000')
    if color == 3:
        color = Color(hex='#0000ff')
    if color == 4:
        color = Color(hex='#148012')
    try:
        t1 = float(center[0])
        t2 = float(center[1])
        t3 = float(radius)
        if method == 0:
            tmp = copy.deepcopy(list(cir_canon_method([t1, t2], t3, color)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(cir_param_method([t1, t2], t3, color)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(cir_bresenham_method([t1, t2], t3, color)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(cir_mid_dot_method([t1, t2], t3, color)[0]))
        if method == 4:
            cir_lib_method([t1, t2], t3, color)
            return
        dots.append(tmp)
        last_activity.append(copy.deepcopy(dots))
        draw()
    except:
        messagebox.showerror("Ошибка", "Неверные данные")

def draw():
    global last_activity, dots
    canvas.delete("all")
    for line in dots:
        for dot in line:
            canvas.create_line(dot[0], dot[1],
                    dot[0] + 1, dot[1], fill=dot[2])


def main():
    global canvas

    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №4")
    root.minsize(WIDTH, HEIGHT)
    root["bg"] = "#6b5a45"

    #label меню
    label_menu = Label(root, text="Меню",
                              bg='#6b7a0a')
    label_menu.place(relx=0, rely=0, relwidth=0.3, relheight=0.04)

    #Выбор метода; Установка combox`a
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

    label_method = Label(text="Метод:", bg="#6b7a0a", anchor='w')
    label_method.place(relx=0, rely=0.06, relwidth=0.3, relheight=0.04)

    method_list = ("Каноническое уравнение", "Параметрическое уравнение",
                   "Алгоритм Брезенхема",
                   "Алгоритм средней точки", "Библиотечноая функция")
    font_combo = ("Times", 12)

    method_combo = ttk.Combobox(root, state='readonly', values=method_list,
                    font=font_combo)
    method_combo.place(relx=0, rely=0.1, relwidth=0.3, relheight=0.06)
    method_combo.current(0)

    #Цвет
    color_list = ("Черный", "Белый", "Красный",
                   "Синий", "Зеленый")
    label_color = Label(root, text="Цвет:", anchor='w',
                              bg='#6b7a0a')
    label_color.place(relx=0, rely=0.162, relwidth=0.1, relheight=0.06)
    color_combo = ttk.Combobox(root, state='readonly', values=color_list,
                    font=font_combo)
    color_combo.place(relx=0.1, rely=0.162, relwidth=0.2, relheight=0.06)
    color_combo.current(0)

    #Задание окружности
    label_shift = Label(root, text="Окружность:", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.245, relwidth=0.3, relheight=0.04)
    #Координаты окружности
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

    label_rc = Label(root, text="R:", anchor='c',
                              bg='#6b7a0a')
    label_rc.place(relx=0.2, rely=0.29, relwidth=0.04, relheight=0.06)
    line_rc = Entry(root, bg='#6b7a0a')
    line_rc.place(relx=0.243, rely=0.29, relwidth=0.04, relheight=0.06)

    cir_btn = Button(text="Построить окружность",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: draw_cir([line_x1.get(),\
                                            line_y1.get()],\
                                            line_rc.get(),\
                                            color_combo.current(),\
                                            method_combo.current())
                   )
    cir_btn.place(relx=0, rely=0.36, relwidth=0.3, relheight=0.05)

    #Задание эллипса
    label_shift = Label(root, text="Эллипс:", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.44, relwidth=0.4, relheight=0.04)
    #Координаты эллипса
    label_x2 = Label(root, text="X:", anchor='c',
                              bg='#6b7a0a')
    label_x2.place(relx=0, rely=0.485, relwidth=0.03, relheight=0.06)
    line_x2 = Entry(root, bg='#6b7a0a')
    line_x2.place(relx=0.033, rely=0.485, relwidth=0.03, relheight=0.06)

    label_y2 = Label(root, text="Y:", anchor='c',
                              bg='#6b7a0a')
    label_y2.place(relx=0.075, rely=0.485, relwidth=0.03, relheight=0.06)
    line_y2 = Entry(root, bg='#6b7a0a')
    line_y2.place(relx=0.108, rely=0.485, relwidth=0.03, relheight=0.06)

    label_ra = Label(root, text="Ra:", anchor='c',
                              bg='#6b7a0a')
    label_ra.place(relx=0.155, rely=0.485, relwidth=0.03, relheight=0.06)
    line_ra = Entry(root, bg='#6b7a0a')
    line_ra.place(relx=0.188, rely=0.485, relwidth=0.03, relheight=0.06)

    label_rb = Label(root, text="Rb:", anchor='c',
                              bg='#6b7a0a')
    label_rb.place(relx=0.231, rely=0.485, relwidth=0.03, relheight=0.06)
    line_rb = Entry(root, bg='#6b7a0a')
    line_rb.place(relx=0.264, rely=0.485, relwidth=0.03, relheight=0.06)

    ell_btn = Button(text="Построить эллипс",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a')#,
                  #command=lambda: drawLine([line_x1.get(), line_y1.get()],
                  #[line_x2.get(), line_y2.get()], color_combo.current(),
                  #method_combo.current()))
    ell_btn.place(relx=0, rely=0.555, relwidth=0.3, relheight=0.05)

    #Спектр окружности
    label_shift = Label(root, text="Спектр окружности:", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.64, relwidth=0.4, relheight=0.04)
    #Данные спектра
    label_xspec_c = Label(root, text="Шаг:", anchor='c',
                              bg='#6b7a0a')
    label_xspec_c.place(relx=0, rely=0.685, relwidth=0.03, relheight=0.06)
    line_xspec_c = Entry(root, bg='#6b7a0a')
    line_xspec_c.place(relx=0.033, rely=0.685, relwidth=0.03, relheight=0.06)

    label_yspec_c = Label(root, text="N:", anchor='c',
                              bg='#6b7a0a')
    label_yspec_c.place(relx=0.075, rely=0.685, relwidth=0.03, relheight=0.06)
    line_yspec_c = Entry(root, bg='#6b7a0a')
    line_yspec_c.place(relx=0.108, rely=0.685, relwidth=0.03, relheight=0.06)

    label_rspec_cb = Label(root, text="Нач:", anchor='c',
                              bg='#6b7a0a')
    label_rspec_cb.place(relx=0.155, rely=0.685, relwidth=0.03, relheight=0.06)
    line_rspec_cb = Entry(root, bg='#6b7a0a')
    line_rspec_cb.place(relx=0.188, rely=0.685, relwidth=0.03, relheight=0.06)

    label_rspec_cf = Label(root, text="Кон:", anchor='c',
                              bg='#6b7a0a')
    label_rspec_cf.place(relx=0.231, rely=0.685, relwidth=0.03, relheight=0.06)
    line_rspec_cf = Entry(root, bg='#6b7a0a')
    line_rspec_cf.place(relx=0.264, rely=0.685, relwidth=0.03, relheight=0.06)

    spec_c_btn = Button(text="Построить спектр окружности",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a')#,
                  #command=lambda: drawLine([line_x1.get(), line_y1.get()],
                  #[line_x2.get(), line_y2.get()], color_combo.current(),
                  #method_combo.current()))
    spec_c_btn.place(relx=0, rely=0.755, relwidth=0.3, relheight=0.05)

    #Спектр эллипса
    label_shift = Label(root, text="Спектр эллипса:", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.835, relwidth=0.4, relheight=0.04)
    #Данные спектра
    label_xspec_e = Label(root, text="Шаг:", anchor='c',
                              bg='#6b7a0a')
    label_xspec_e.place(relx=0, rely=0.88, relwidth=0.03, relheight=0.06)
    line_xspec_e = Entry(root, bg='#6b7a0a')
    line_xspec_e.place(relx=0.033, rely=0.88, relwidth=0.03, relheight=0.06)

    label_yspec_e = Label(root, text="N:", anchor='c',
                              bg='#6b7a0a')
    label_yspec_e.place(relx=0.075, rely=0.88, relwidth=0.03, relheight=0.06)
    line_yspec_e = Entry(root, bg='#6b7a0a')
    line_yspec_e.place(relx=0.108, rely=0.88, relwidth=0.03, relheight=0.06)

    label_rspec_eb = Label(root, text="A_н:", anchor='c',
                              bg='#6b7a0a')
    label_rspec_eb.place(relx=0.155, rely=0.88, relwidth=0.03, relheight=0.06)
    line_rspec_eb = Entry(root, bg='#6b7a0a')
    line_rspec_eb.place(relx=0.188, rely=0.88, relwidth=0.03, relheight=0.06)

    label_rspec_ef = Label(root, text="B_н:", anchor='c',
                              bg='#6b7a0a')
    label_rspec_ef.place(relx=0.231, rely=0.88, relwidth=0.03, relheight=0.06)
    line_rspec_ef = Entry(root, bg='#6b7a0a')
    line_rspec_ef.place(relx=0.264, rely=0.88, relwidth=0.03, relheight=0.06)

    spec_e_btn = Button(text="Построить спектр эллипса",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a')#,
                  #command=lambda: drawLine([line_x1.get(), line_y1.get()],
                  #[line_x2.get(), line_y2.get()], color_combo.current(),
                  #method_combo.current()))
    spec_e_btn.place(relx=0, rely=0.945, relwidth=0.3, relheight=0.05)

    #Canvas
    canvas = Canvas(root, bg="#148012", #148012
                        highlightthickness=4, highlightbackground="#6b3e07")
    canvas.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
    canvas.bind("<Button-1>", lambda e: add_dot_event(e, color_combo.current(),
                method_combo.current()))

    #Меню
    menu = Menu(root)
    root.config(menu=menu)
    menu.add_command(label="Задание", command=lambda:\
                        messagebox.showinfo("Задание", TASK))
    menu.add_command(label="Автор",command=lambda:\
                        messagebox.showinfo("Автор", "Симонович Р.Д. ИУ7-44Б"))
    menu.add_command(label="Очистить холст", command=lambda:\
                        del_all_dots())
    #Диаграмма
    menu.add_command(label="Диаграмма", command=lambda:\
                        time_diagram(len_spectr.get()))
    menu.add_command(label="Выход", command=root.destroy)

    #Команды
    #root.bind("<Control-z>", lambda e: last_event(e))

    root.mainloop()

if __name__ == "__main__":
    main()
