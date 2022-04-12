import copy
import math
import sys
from math import fabs, floor
from tkinter import Tk, Button, Label, Entry, Canvas, messagebox, Menu, Frame, SUNKEN, colorchooser
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from colorutils import Color

WIDTH = 1000
HEIGHT = 600
RADIUS = 3

EPS = 1e-8

IS_FIRST_DOT = True
dots_for_line = []

dots = []
last_activity = []

#c = Color(hex='#000000')
cb = Color(hex='#6b3e07')

TASK = '''Реализовать различные алгоритмы построения одиночных отрезков. \n
Отрезок задается координатой начала, \nкоординатой конца и цветом.\n
Сравнить визуальные характеристики отрезков, \nпостроенных разными алгоритмами,
с помощью построения \nпучка отрезков, с заданным шагом.\n
Сравнение со стандартным алгоритмом.\n
Задаются начальные и конечные координаты;\n
рисуется отрезок разными методами.\n
Отрисовка отрезка другим цветом и методом \n
поверх первого, для проверки совпадения.\n
Предоставить пользователю возможность \n
выбора двух цветов– цвета фона и цвета рисования. \n
Алгоритмы выбирать из выпадающего списка.\n
- ЦДА\n
- Брезенхем действительные числа\n
- Брезенхем целые числа\n
- Брезенхем с устранением ступенчатости\n
- ВУ\n
Построение гистограмм по количеству ступенек \nв зависимости от угла наклона.'''

def exit_prog():
    sys.exit()

def del_all_dots():
    dots.clear()
    last_activity.append(copy.deepcopy(dots))
    canvas.delete("all")

def last_event(event, last_arr, last_center):
    global dots_list, canvas
    global last_activity, last_center_place, CENTER
    last_activity = copy.deepcopy(dots_list)
    last_center_place = copy.deepcopy(CENTER)

    if last_arr:
        canvas.delete("all")
        dots_list.clear()
        dots_list = copy.deepcopy(last_arr)
        draw_picture_by_dots(dots_list)
    else:
        canvas.delete("all")
        dots_list.clear()


def step_diagram(len_line):
    try:
        len_line = float(len_line)
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    if len_line <= 0:
        messagebox.showerror("Ошибка", "Длина линии должна быть выше нуля")
        return

    angle = 0

    cda_steps = []
    wu_steps = []
    bresenham_int_steps = []
    bresenham_float_steps = []
    bresenham_smooth_steps = []

    start = [canvas.winfo_width() // 2, canvas.winfo_height() // 2]
    angle = 0
    delta_angle = 1
    color = Color((0, 0, 0))

    while angle < math.pi / 2:
        end = [start[0] + len_line * math.cos(angle), start[1] + len_line * math.sin(angle)]
        bresenham_int_steps.append(bresenham_int_method(start, end, color)[1])
        bresenham_float_steps.append(bresenham_float_method(start, end, color)[1])
        cda_steps.append(cda_method(start, end, color)[1])
        bresenham_smooth_steps.append(bresenham_smooth_method(start, end, color)[1])
        wu_steps.append(wu_method(start, end, color)[1])
        angle += delta_angle * math.pi / 180
    #print(len(bresenham_float_steps))
    #print(bresenham_float_steps)
    angles = [i for i in range(0, 90, 1)]
    #print(len(angles))

    fig, ax = plt.subplots(figsize=(60, 40))

    ax = plt.subplot(2, 3, 1)
    ax.set_xlabel('Угол')
    ax.set_ylabel('Кол-во ступенек')
    plt.bar(angles, bresenham_int_steps)
    plt.title("Брезенхейм (целочисленный)")

    ax = plt.subplot(2, 3, 2)
    ax.set_xlabel('Угол')
    ax.set_ylabel('Кол-во ступенек')
    plt.bar(angles, bresenham_float_steps)
    plt.title("Брезенхейм (вещественный)")

    ax = plt.subplot(2, 3, 3)
    ax.set_xlabel('Угол')
    ax.set_ylabel('Кол-во ступенек')
    plt.bar(angles, bresenham_smooth_steps)
    plt.title("Брезенхейм (сглаживание)")

    ax = plt.subplot(2, 3, 4)
    ax.set_xlabel('Угол')
    ax.set_ylabel('Кол-во ступенек')
    plt.bar(angles, wu_steps)
    plt.title("Ву")

    ax = plt.subplot(2, 3, 5)
    ax.set_xlabel('Угол')
    ax.set_ylabel('Кол-во ступенек')
    plt.bar(angles, cda_steps)
    plt.title("ЦДА")

    plt.show()

def cda_method(start_point, end_point, color):
    x1 = start_point[0]
    y1 = start_point[1]
    x2 = end_point[0]
    y2 = end_point[1]

    if fabs(x2 - x1) < EPS and fabs(y2 - y1) < EPS:
        return [[[x1, y1, color.hex]]]

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        l = abs(dx)
    else:
        l = abs(dy)

    dx /= l
    dy /= l
    x = round(x1)
    y = round(y1)
    dd = [[x, y, color.hex]]
    i = 1
    steps = 0

    while i < l + 1:
        x += dx
        y += dy
        dot = [round(x), round(y), color.hex]
        dd.append(dot)

        if not ((round(x + dx) == round(x) and
                 round(y + dy) != round(y)) or
                (round(x + dx) != round(x) and
                 round(y + dy) == round(y))):
            steps += 1

        i += 1
    return dd, steps

def bresenham_float_method(start_point, end_point, color):
    x1 = start_point[0]
    y1 = start_point[1]
    x2 = end_point[0]
    y2 = end_point[1]

    if fabs(x2 - x1) < EPS and fabs(y2 - y1) < EPS:
        return [[[x1, y1, color.hex]]]

    x = x1
    y = y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    s1 = (x2 - x1) / fabs(x2 - x1) if fabs(x2 - x1) > EPS else 0
    s2 = (y2 - y1) / fabs(y2 - y1) if fabs(y2 - y1) > EPS else 0

    if dy > dx:
        dx, dy = dy, dx
        swaped = 1
    else:
        swaped = 0

    m = dy / dx
    e = m - 1 / 2
    i = 1
    dd = []
    steps = 0

    while i < dx + 1:
        dot = [x, y, color.hex]
        dd.append(dot)

        x_buf = x
        y_buf = y

        if e >= 0:
            if swaped:
                x = x + s1
            else:
                y = y + s2
            e = e - 1

        if swaped:
            y = y + s2
        else:
            x = x + s1

        e = e + m

        if not ((x_buf == x and y_buf != y) or
                (x_buf != x and y_buf == y)):
            steps += 1

        i += 1

    return dd, steps


def bresenham_int_method(start_point, end_point, color):
    x1 = start_point[0]
    y1 = start_point[1]
    x2 = end_point[0]
    y2 = end_point[1]

    if fabs(x2 - x1) < EPS and fabs(y2 - y1) < EPS:
        return [[[x1, y1, color.hex]]]

    x = x1
    y = y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    s1 = (x2 - x1) / fabs(x2 - x1) if fabs(x2 - x1) > EPS else 0
    s2 = (y2 - y1) / fabs(y2 - y1) if fabs(y2 - y1) > EPS else 0

    if dy > dx:
        dx, dy = dy, dx
        swaped = 1
    else:
        swaped = 0

    e = 2 * dy - dx
    i = 1
    dots = []
    steps = 0

    while i < dx + 1:
        dot = [x, y, color.hex]
        dots.append(dot)

        x_buf = x
        y_buf = y

        if e >= 0:
            if swaped:
                x = x + s1
            else:
                y = y + s2

            e = e - 2 * dx

        if swaped:
            y = y + s2
        else:
            x = x + s1

        e = e + 2 * dy

        if (x_buf != x) and (y_buf != y):
            steps += 1

        i += 1

    return dots, steps

def color_koef(color, k):
    global cb
    cc = list(color.rgb)
    ccb = list(cb.rgb)

    kk = k / 255
    kkk = 1 - kk

    if cc[0] - ccb[0] < 0:
        c1 = cc[0] + kk * fabs(cc[0] - ccb[0])
    else:
        c1 = ccb[0] + kkk * fabs(cc[0] - ccb[0])

    if cc[1] - ccb[1] < 0:
        c2 = cc[1] + kk * fabs(cc[1] - ccb[1])
    else:
        c2 = ccb[0] + kkk * fabs(cc[1] - ccb[1])

    if cc[2] - ccb[2] < 0:
        c3 = cc[2] + kk * fabs(cc[2] - ccb[2])
    else:
        c3 = ccb[2] + kkk * fabs(cc[2] - ccb[2])

    kk = k / 255

    cl = Color((int(c1), int(c2), int(c3)))
    return cl
def bresenham_smooth_method(start_point, end_point, color):
    x1 = start_point[0]
    y1 = start_point[1]
    x2 = end_point[0]
    y2 = end_point[1]

    if fabs(x2 - x1) < EPS and fabs(y2 - y1) < EPS:
        return [[[x1, y1, color.hex]]]


    x = x1
    y = y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    s1 = (x2 - x1) / fabs(x2 - x1) if fabs(x2 - x1) > EPS else 0
    s2 = (y2 - y1) / fabs(y2 - y1) if fabs(y2 - y1) > EPS else 0

    if dy > dx:
        dx, dy = dy, dx
        swaped = 1
    else:
        swaped = 0

    k = 255
    m = dy / dx * k
    e = k / 2
    w = k - m
    dots = [[x, y, color_koef(color, round(e)).hex]]
    i = 1
    steps = 0

    while i < dx + 1:
        x_buf = x
        y_buf = y

        if e < w:
            if swaped:
                y += s2
            else:
                x += s1
            e += m
        else:
            y += s2
            x += s1
            e -= w

        dot = [x, y, color_koef(color, round(e)).hex]

        dots.append(dot)

        if not ((x_buf == x and y_buf != y) or
                (x_buf != x and y_buf == y)):
            steps += 1

        i += 1

    return dots, steps

def color_koef_wu(color, k):
    return color + (k, k, k)
def wu_method(start_point, end_point, color):
    x1 = start_point[0]
    y1 = start_point[1]
    x2 = end_point[0]
    y2 = end_point[1]

    if fabs(x2 - x1) < EPS and fabs(y2 - y1) < EPS:
        return [[[x1, y1, color.hex]]]

    if fabs(y2 - y1) > fabs(x2 - x1):
        swaped = 1
    else:
        swaped = 0

    if swaped == 1:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x2, x1 = x1, x2
        y2, y1 = y1, y2

    dots = []
    if swaped:
        dots.append([y1, x1, color_koef_wu(color, 1).hex])
    else:
        dots.append([x1, y1, color_koef_wu(color, 1).hex])

    steps = 0
    dx = x2 - x1
    dy = y2 - y1

    m = 0
    if fabs(dy) > EPS:
        m = dy / dx

    y = y1 + m
    x = x1 + 1
    while x <= x2:
        k = y - int(y)
        k *= 255
        if swaped == 1:
            dots.append([int(y), x, color_koef_wu(color, 255 - k).hex])
            dots.append([int(y) + 1, x, color_koef_wu(color, k).hex])
        else:
            dots.append([x, int(y), color_koef_wu(color, 255 - k).hex])
            dots.append([x, int(y) + 1, color_koef_wu(color, k).hex])

        if int(y) != int(y + m):
            steps += 1

        y += m
        x += 1

    return dots, steps

def drawSpectr(len_line, color, delta_angle, method):
    try:
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

        len_line = int(len_line)
        delta_angle = float(delta_angle)
        if len_line <= 0:
            messagebox.showerror("Ошибка", "Длина линии должна быть выше нуля")
            return

        if delta_angle <= 0:
            messagebox.showerror("Ошибка", "Угол должен быть больше нуля")
            retu
        start = [canvas.winfo_width() // 2, canvas.winfo_height() // 2]
        angle = 0
        while angle < 2 * math.pi:
            end = [start[0] + len_line * math.cos(angle), start[1] + len_line * math.sin(angle)]
            if method == 0:
                tmp = bresenham_int_method(start, end, color)[0]
            if method == 1:
                tmp = bresenham_float_method(start, end, color)[0]
            if method == 2:
                tmp = cda_method(start, end, color)[0]
            if method == 3:
                tmp = bresenham_smooth_method(start, end, color)[0]
            if method == 4:
                tmp = wu_method(start, end, color)[0]
            dots.append(tmp)
            # last_activity.append(copy.deepcopy(dots))
            angle += delta_angle * math.pi / 180

        draw(dots)
    except:
        messagebox.showerror("Ошибка", "Неверные данные")

def draw(dots, k=1):
    canvas.delete("all")
    for line in dots:
        for dot in line:
            canvas.create_line(dot[0], dot[1], dot[0] + 1, dot[1], fill=dot[2])

def drawLine(start, end, color, method):
    try:
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
        start[0] = float(start[0])
        end[0] = float(end[0])
        start[1] = float(start[1])
        end[1] = float(end[1])
        if method == 0:
            tmp = copy.deepcopy(list(cda_method(start, end, color)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(bresenham_float_method(start, end, color)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(bresenham_int_method(start, end, color)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(bresenham_smooth_method(start, end, color)[0]))
        if method == 4:
            tmp = copy.deepcopy(list(wu_method(start, end, color)[0]))
        dots.append(tmp)
        #last_activity.append(copy.deepcopy(dots))
        draw(dots)
    except:
        messagebox.showerror("Ошибка", "Неверные данные")

def add_dot_event(event, color, method):
    global IS_FIRST_DOT, dots_for_line
    if IS_FIRST_DOT:
        IS_FIRST_DOT = False
        dots_for_line.append([event.x, event.y])
    else:
        IS_FIRST_DOT = True
        dots_for_line.append([event.x, event.y])
        drawLine(dots_for_line[0], dots_for_line[1], color, method)
        dots_for_line.clear()

def main():
    global canvas

    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №3")
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
    label_method.place(relx=0, rely=0.07, relwidth=0.3, relheight=0.04)

    method_list = ("ЦДА", "Брезенхем (вещественный)",
                   "Брезенхем (целочисленный)",
                   "Брезенхем (сглаживание)", "Ву")
    font_combo = ("Times", 12)

    method_combo = ttk.Combobox(root, state='readonly', values=method_list,
                    font=font_combo)
    method_combo.place(relx=0, rely=0.11, relwidth=0.3, relheight=0.06)
    method_combo.current(0)

    #Задание отрезка
    label_shift = Label(root, text="Отрезок:", anchor='w',
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.23, relwidth=0.3, relheight=0.04)

    #Цвет
    color_list = ("Черный", "Белый", "Красный",
                   "Синий", "Зеленый")
    label_color = Label(root, text="Цвет:", anchor='w',
                              bg='#6b7a0a')
    label_color.place(relx=0, rely=0.275, relwidth=0.1, relheight=0.06)
    color_combo = ttk.Combobox(root, state='readonly', values=color_list,
                    font=font_combo)
    color_combo.place(relx=0.1, rely=0.275, relwidth=0.2, relheight=0.06)
    color_combo.current(0)

    #Координаты отрезка
    label_x1 = Label(root, text="X1:", anchor='c',
                              bg='#6b7a0a')
    label_x1.place(relx=0, rely=0.35, relwidth=0.04, relheight=0.06)
    line_x1 = Entry(root, bg='#6b7a0a')
    line_x1.place(relx=0.045, rely=0.35, relwidth=0.04, relheight=0.06)

    label_y1 = Label(root, text="Y1:", anchor='c',
                              bg='#6b7a0a')
    label_y1.place(relx=0.15, rely=0.35, relwidth=0.04, relheight=0.06)
    line_y1 = Entry(root, bg='#6b7a0a')
    line_y1.place(relx=0.195, rely=0.35, relwidth=0.04, relheight=0.06)

    label_x2 = Label(root, text="X2:", anchor='c',
                              bg='#6b7a0a')
    label_x2.place(relx=0, rely=0.415, relwidth=0.04, relheight=0.06)
    line_x2 = Entry(root, bg='#6b7a0a')
    line_x2.place(relx=0.045, rely=0.415, relwidth=0.04, relheight=0.06)

    label_y2 = Label(root, text="Y2:", anchor='c',
                              bg='#6b7a0a')
    label_y2.place(relx=0.15, rely=0.415, relwidth=0.04, relheight=0.06)
    line_y2 = Entry(root, bg='#6b7a0a')
    line_y2.place(relx=0.195, rely=0.415, relwidth=0.04, relheight=0.06)

    line_btn = Button(text="Построить отрезок",
                  bg='#6b7a0a',
                  activebackground='#6b7a0a',
                  command=lambda: drawLine([line_x1.get(), line_y1.get()],
                  [line_x2.get(), line_y2.get()], color_combo.current(),
                   method_combo.current()))
    line_btn.place(relx=0, rely=0.485, relwidth=0.3, relheight=0.08)

    #Спектр
    menu_label_spectr = Label(text="Спектр:", anchor='w', bg='#6b7a0a')
    menu_label_spectr.place(relx=0, rely=0.6, relwidth=0.3, relheight=0.05)

    label_len = Label(root, text="Длина:", anchor='c',
                              bg='#6b7a0a')
    label_len.place(relx=0, rely=0.655, relwidth=0.15, relheight=0.06)
    len_spectr = Entry(root, bg='#6b7a0a')
    len_spectr.place(relx=0.155, rely=0.655, relwidth=0.14, relheight=0.06)

    label_angle = Label(root, text="Угол:", anchor='c',
                             bg='#6b7a0a')
    label_angle.place(relx=0, rely=0.722, relwidth=0.15, relheight=0.06)
    angle_spectr = Entry(root, bg='#6b7a0a')
    angle_spectr.place(relx=0.155, rely=0.722, relwidth=0.14, relheight=0.06)

    spectr_btn = Button(text="Построить спектр",
                      bg='#6b7a0a',
                      activebackground='#6b7a0a',
                      command=lambda: drawSpectr(len_spectr.get(),
                      color_combo.current(), angle_spectr.get(),
                      method_combo.current()))
    spectr_btn.place(relx=0, rely=0.79, relwidth=0.3, relheight=0.08)

    #Диаграмма
    plt_1_btn = Button(text="Диаграмма ступенчатости", bg='#6b7a0a',
                    activebackground='#6b7a0a',
                    command=lambda: step_diagram(len_spectr.get()))

    plt_1_btn.place(relx=0, rely=0.91, relwidth=0.3, relheight=0.08)


    #Canvas
    canvas = Canvas(root, bg="#148012",
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
    #menu.add_command(label="Построить с шагом")#, command=special_add)
    menu.add_command(label="Выход", command=root.destroy)

    #Команды
    root.bind("<Control-z>", lambda e:\
                last_event(e, last_activity, last_center_place))

    root.mainloop()

if __name__ == "__main__":
    main()






