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
dots_for_cir = []
center_dot = 0

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
    global dots
    dots.clear()
    canvas.delete("all")


#Окружности
def cir_lib_method(center, radius, color, is_test_time=False):
    x_c = center[0]
    y_c = center[1]
    color = color.hex

    if is_test_time:
        color = '#148012'
        canvas.create_oval(
                        x_c - radius, y_c - radius,
                        x_c + radius, y_c + radius,
                        fill="", outline=color, width=1
                        )
    else:
        canvas.create_oval(
                        x_c - radius, y_c - radius,
                        x_c + radius, y_c + radius,
                        fill="", outline=color, width=1
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


def draw_cir(center, radius, color, method):
    global last_activity, dots
    if color == 0:
        color = Color(hex='#000000')
    elif color == 1:
        color = Color(hex='#ffffff')
    elif color == 2:
        color = Color(hex='#ff0000')
    elif color == 3:
        color = Color(hex='#0000ff')
    elif color == 4:
        color = Color(hex='#148012')
    try:
        t1 = float(center[0])
        t2 = float(center[1])
        t3 = float(radius)
        if method == 0:
            tmp = copy.deepcopy(list(cir_canon_method([t1, t2], t3, color)[0]))
        elif method == 1:
            tmp = copy.deepcopy(list(cir_param_method([t1, t2], t3, color)[0]))
        elif method == 2:
            tmp = copy.deepcopy(list(cir_bresenham_method([t1, t2], t3, color)[0]))
        elif method == 3:
            tmp = copy.deepcopy(list(cir_mid_dot_method([t1, t2], t3, color)[0]))
        elif method == 4:
            cir_lib_method([t1, t2], t3, color)
            return
        dots.append(tmp)
        last_activity.append(copy.deepcopy(dots))
        draw()
    except:
        messagebox.showerror("Ошибка", "Неверные данные")


#Эллипсы
def ell_lib_method(center, b, a, color, is_test_time=False):
    x_c = center[0]
    y_c = center[1]
    color = color.hex

    if is_test_time:
        color = '#148012'
        canvas.create_oval(
                        x_c - b, y_c - a,
                        x_c + b, y_c + a,
                        fill="", outline=color, width=1
                        )
    else:
        canvas.create_oval(
                        x_c - b, y_c - a,
                        x_c + b, y_c + a,
                        fill="", outline=color, width=1
                        )


def ell_canon_method(dot_center, a, b, color):
    x_c = dot_center[0]
    y_c = dot_center[1]
    c_dots = []
    color = color.hex
    a2 = a * a
    b2 = b * b
    end = round(a / sqrt(1 + b2 / a2))

    x = 0

    while x <= end:
        y = round(sqrt(1 - x * x / a2) * b)

        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        x += 1

    end = round(b2 / sqrt(a2 + b2))

    y = 0

    while y <= end:
        x = round(sqrt(1 - y * y / b2) * a)

        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        y += 1
    return c_dots, 0


def ell_param_method(dot_center, a, b, color):
    x_c = dot_center[0]
    y_c = dot_center[1]
    c_dots = []
    color = color.hex
    if a > b:
        step = 1 / a
    else:
        step = 1 / b

    alpha = 0

    while alpha < pi / 2 + step:
        x = round(a * cos(alpha))
        y = round(b * sin(alpha))

        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        alpha += step
    return c_dots, 0


def ell_bresenham_method(dot_center, a, b, color):
    x_c = round(dot_center[0])
    y_c = round(dot_center[1])
    c_dots = []
    color = color.hex
    x = 0
    y = b

    a2 = a ** 2
    b2 = b ** 2

    delta = b2 - a2 * (2 * y + 1)
    tmp_pxl = 1
    err = 0

    while y >= 0:
        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        if delta <= 0:
            err = 2 * delta + (2 * y + 2) * a2

            if err < 0:
                x = x + 1
                delta = delta + (2 * x) * b2 + b2
            else:
                x = x + 1
                y = y - 1
                delta = delta + (2 * x) * b2 - (2 * y) * a2 + (a2 + b2)
        elif delta > 0:
            err = 2 * delta + (- 2 * x + 2) * b2

            if err < 0:
                x = x + 1
                y = y - 1
                delta = delta + (2 * x) * b2 - (2 * y) * a2 + (a2 + b2)
            else:
                y = y - 1
                delta = delta - (2 * y) * a2 + a2
    return c_dots, 0


def ell_mid_dot_method(dot_center, a, b, color):
    x_c = dot_center[0]
    y_c = dot_center[1]
    c_dots = []
    color = color.hex
    x = 0
    y = b
    a2 = a ** 2
    b2 = b ** 2
    end = round(a / sqrt(1 + b2 / a2))
    delta = b2 - round(a2 * (b - 1 / 2))
    while x <= end:
        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])
        if delta > 0:
            y -= 1
            delta = delta - a2 * y * 2
        x += 1
        delta = delta + b2 * (2 * x + 1)

    x = a
    y = 0
    end = round(b / sqrt(1 + a2 / b2))
    delta = a2 - round(b2 * (x - 1 / 2))
    while y <= end:
        c_dots.append([x_c + x, y_c + y, color])
        c_dots.append([x_c - x, y_c + y, color])
        c_dots.append([x_c + x, y_c - y, color])
        c_dots.append([x_c - x, y_c - y, color])

        if delta > 0:
            x -= 1
            delta = delta - b2 * x * 2

        y += 1

        delta = delta + a2 * (2 * y + 1)
    return c_dots, 0


def draw_ell(dot_center, a, b, color, method):
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
        t1 = float(dot_center[0])
        t2 = float(dot_center[1])
        t3 = float(a)
        t4 = float(b)
        if method == 0:
            tmp = copy.deepcopy(list(ell_canon_method([t1, t2], t3, t4, color)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(ell_param_method([t1, t2], t3, t4, color)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(ell_bresenham_method([t1, t2], t3, t4, color)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(mid_dot_method_ell([t1, t2], t3, t4, color)[0]))
        if method == 4:
            ell_lib_method([t1, t2], t3, t4, color)
            return
        dots.append(tmp)
        last_activity.append(copy.deepcopy(dots))
        draw()
    except:
        messagebox.showerror("Ошибка", "Неверные данные")


def draw():
    global last_activity, dots
    #canvas.delete("all")
    for line in dots:
        for dot in line:
            canvas.create_line(dot[0], dot[1],
                    dot[0] + 1, dot[1], fill=dot[2])


def draw_manual(event, color, method):
    global IS_FIRST_DOT, dots_for_cir, canvas, center_dot
    #center_dot = 0
    if IS_FIRST_DOT:
        IS_FIRST_DOT = False
        dots_for_cir.append([event.x, event.y])
        center_dot = canvas.create_oval(
                event.x - RADIUS, event.y - RADIUS,
                event.x + RADIUS, event.y + RADIUS,
                fill="#001", outline="#001", width=1
            )
    else:
        canvas.delete(center_dot)
        canvas.update()
        IS_FIRST_DOT = True
        x1 = dots_for_cir[0][0]
        y1 = dots_for_cir[0][1]
        x2 = float(event.x)
        y2 = float(event.y)
        radius = sqrt((x1-x2)**2 + (y1-y2)**2)
        draw_cir(dots_for_cir[0], radius, color, method)
        dots_for_cir.clear()


def spec_cir(step, count, start, end, color, method):
    global canvas
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

    cc = 0 # Проверка данных, три из следующих четырех параметров
    flag = 0
    try:
        step = float(step)
    except:
        cc += 1
        flag = 1
    try:
        count = float(count)
    except:
        cc += 1
        flag = 2
    try:
        start = float(start)
    except:
        cc += 1
        flag = 3
    try:
        end = float(end)
    except:
        cc += 1
        flag = 4

    if cc > 1:
        messagebox.showerror("Ошибка", "Неверно введены данные")
        return

    if flag == 1: # три из следующих четырех параметров
        step = int((end - start) / count)
    elif flag == 2:
        count = int((end - start) / step)
    elif flag == 3:
        start = float(end - step * count)
    else:
        end = float(start + step * count)

    radius = start

    dot_center = [canvas.winfo_width() // 2,\
                  canvas.winfo_height() // 2]

    index = 0

    while index < count:
        #draw_cir(dot_center, radius, color, method)
        if method == 0:
            tmp = copy.deepcopy(list(cir_canon_method(dot_center, radius, color)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(cir_param_method(dot_center, radius, color)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(cir_bresenham_method(dot_center, radius, color)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(cir_mid_dot_method(dot_center, radius, color)[0]))
        if method == 4:
            cir_lib_method(dot_center, radius, color)
            radius += step
            index += 1
            continue
        dots.append(tmp)
        radius += step
        index += 1
    last_activity.append(copy.deepcopy(dots))
    if method != 4:
        draw()


def spec_ell(step, count, a, b, color, method):
    try: #прием данныйх
        step = float(step)
        count = float(count)
        a = float(a)
        b = float(b)
    except:
        messagebox.showerror("Ошибка", "Неверно введены данные")
        return

    if step <= 0 or count <= 0 or a <= 0 or b <= 0: #проверка данных
        messagebox.showerror("Ошибка", "Неверно введены данные")
        return

    dot_center = [canvas.winfo_width() // 2,\
                   canvas.winfo_height() // 2] # Находим центр
    kk = b / a # коэф-нт прибавления по b

    index = 0

    while index < count:
        # Строим эллипс по методу
        draw_ell(dot_center, a, b, color, method)

        #Прибавление данных
        a += step
        b = a * kk
        index += 1

    last_activity.append(copy.deepcopy(dots))
    if method != 4:
        draw()

def time_diagram():
    dot_center = [canvas.winfo_width() // 2, canvas.winfo_height() // 2]
    color = Color(hex="#fff")

    ddt = 10
    var = 1000
    res_time = [0] * 10
    for i in range(10):
        res_time[i] = [0] * 10
    count_ = 0
    for i in range(10, 20):
        t1 = time.time()
        for k in range(var):
            cir_canon_method(dot_center, ddt * i, color)
        t2 = time.time()
        res_time[0][count_] = ((t2 - t1) / var)

        t1 = time.time()
        for k in range(var):
            cir_param_method(dot_center, ddt * i, color)
        t2 = time.time()
        res_time[1][count_] = ((t2 - t1) / var)

        t1 = time.time()
        for k in range(var):
            cir_bresenham_method(dot_center, ddt * i, color)
        t2 = time.time()
        res_time[2][count_] = ((t2 - t1) / var)

        t1 = time.time()
        for k in range(var):
            cir_mid_dot_method(dot_center, ddt * i, color)
        t2 = time.time()
        res_time[3][count_] = ((t2 - t1) / var)

        t1 = time.time()
        for k in range(var):
            cir_lib_method(dot_center, ddt * i, color, True)
        t2 = time.time()
        res_time[4][count_] = ((t2 - t1) / var)

        ###############

        t1 = time.time()
        for k in range(var):
            ell_canon_method(dot_center, ddt * i, ddt * 2 * i, color)
        t2 = time.time()
        res_time[5][count_] = ((t2 - t1) / var)

        t1 = time.time()
        for k in range(var):
            ell_param_method(dot_center, ddt * i, ddt * 2 * i, color)
        t2 = time.time()
        res_time[6][count_] = ((t2 - t1) / var)

        t1 = time.time()
        for k in range(var):
            ell_bresenham_method(dot_center, ddt * i, ddt * 2 * i, color)
        t2 = time.time()
        res_time[7][count_] = ((t2 - t1) / var)

        t1 = time.time()
        for k in range(var):
            ell_mid_dot_method(dot_center, ddt * i, ddt * 2 * i, color)
        t2 = time.time()
        res_time[8][count_] = ((t2 - t1) / var)

        t1 = time.time()
        for k in range(var):
            ell_lib_method(dot_center, ddt * i, ddt * 2 * i, color, True)
        t2 = time.time()
        res_time[9][count_] = ((t2 - t1) / var)

        count_ += 1

    rad_arr = list(i * ddt for i in range(10, 20))
    plt.subplot(1, 2, 1)
    plt.title("Эффективность алгоритмов (окружность)")
    plt.plot(rad_arr, res_time[0], label="Каноническое\nуравнеие")
    plt.plot(rad_arr, res_time[1], label="Параметрическое\nуравнение")
    plt.plot(rad_arr, res_time[2], label="Брезенхем")
    plt.plot(rad_arr, res_time[3], label="Алгоритм\nсредней точки")
    plt.plot(rad_arr, res_time[4], label="Библиотечный\nалгоритм")
    plt.xticks(list(i * ddt for i in range(10, 20)))
    plt.ylabel("Время")
    plt.xlabel("Радиус")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title("Эффективность алгоритмов (эллипс)")
    plt.plot(rad_arr, res_time[5], label="Каноническое\nуравнеие\n(Эллипс)")
    plt.plot(rad_arr, res_time[6], label="Параметрическое\nуравнение\n(Эллипс)")
    plt.plot(rad_arr, res_time[7], label="Брезенхем\n(Эллипс)")
    plt.plot(rad_arr, res_time[8], label="Алгоритм\nсредней точки\n(Эллипс)")
    plt.plot(rad_arr, res_time[9], label="Библиотечный\nалгоритм")
    plt.ylabel("Время")
    plt.xlabel("Радиус")
    #plt.legend()


    plt.show()


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
                  activebackground='#6b7a0a',
                  command=lambda: draw_ell([line_x2.get(), line_y2.get()],
                                  line_ra.get(), line_rb.get(),
                                  color_combo.current(),
                                  method_combo.current()))
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
                  activebackground='#6b7a0a',
                  command=lambda: spec_cir(line_xspec_c.get(),\
                                  line_yspec_c.get(),\
                                  line_rspec_cb.get(), line_rspec_cf.get(),
                                  color_combo.current(),
                                  method_combo.current()))
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
                  activebackground='#6b7a0a',
                  command=lambda: spec_ell(
                                  line_xspec_e.get(),\
                                  line_yspec_e.get(),\
                                  line_rspec_eb.get(), line_rspec_ef.get(),
                                  color_combo.current(),
                                  method_combo.current()))
    spec_e_btn.place(relx=0, rely=0.945, relwidth=0.3, relheight=0.05)

    #Canvas
    canvas = Canvas(root, bg="#148012", #148012
                        highlightthickness=4, highlightbackground="#6b3e07")
    canvas.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
    canvas.bind("<Button-1>", lambda e: draw_manual(e, color_combo.current(),
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
                        time_diagram())
    menu.add_command(label="Выход", command=root.destroy)

    #Команды
    #root.bind("<Control-z>", lambda e: last_event(e))

    root.mainloop()

if __name__ == "__main__":
    main()
