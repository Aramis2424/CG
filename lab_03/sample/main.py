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

EPS = 1e-9

RESULT = False

dots = []
last_activity = []

c = Color(hex='#FFFFFF')
cb = Color(hex='#000000')


scale_k = 1

TASK = '''Реализация и исследование алгоритмов построения отрезков\n
————————————————————————————
Реализовать различные алгоритмы построения одиночных \nотрезко. Отрезок задается координатой начала, \nкоординатой конца и цветом.\n
Сравнить визуальные характеристики отрезков, \nпостроенных разными алгоритмами, с помощью построения \nпучка отрезков, с заданным шагом.\n
Сравнение со стандартным алгоритмом. \nЗадаются начальные и конечные координаты;\nрисуется отрезок разными методами.\n
Отрисовка отрезка другим цветом и методом \nповерх первого, для проверки совпадения. \n
Предоставить пользователю возможность выбора двух цветов \n– цвета фона и цвета рисования. \n
Алгоритмы выбирать из выпадающего списка.\n
- ЦДА\n
- Брезенхем действительные числа\n
- Брезенхем целые числа\n
- Брезенхем с устранением ступенчатости\n
- ВУ\n
Построение гистограмм по количеству ступенек \nв зависимости от угла наклона.'''


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder=None):
        super().__init__(master, font='-size 16')

        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_color = 'grey'
            self.default_fg_color = self['fg']

            self.bind("<FocusIn>", self.focus_in)
            self.bind("<FocusOut>", self.focus_out)

            self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()


def previous_state(event):
    global dots
    dots.clear()
    if len(last_activity) > 0:
        dots = last_activity.pop()

    draw(dots)


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


def color_koef_wu(color, k):
    return color + (k, k, k)


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


def clear_canvas():
    dots.clear()
    last_activity.append(copy.deepcopy(dots))
    main_canvas.delete("all")


def onChooseColor():
    global c
    rgb, hx = colorchooser.askcolor()
    c = Color(hex=hx)
    color_frame.config(bg=hx)


def onChooseColorBg():
    global cb
    rgbbg, hxbg = colorchooser.askcolor()
    cb = Color(hex=hxbg)
    color_frame_bg.config(bg=hxbg)
    main_canvas.config(bg=hxbg)


def draw(dots, k=1):
    main_canvas.delete("all")
    for line in dots:
        for dot in line:
            main_canvas.create_line(dot[0], dot[1], dot[0] + 1, dot[1], fill=dot[2])


def drawLine(start, end, color, method):
    try:
        start[0] = float(start[0])
        end[0] = float(end[0])
        start[1] = float(start[1])
        end[1] = float(end[1])
        if method == 0:
            tmp = copy.deepcopy(list(bresenham_int_method(start, end, color)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(bresenham_float_method(start, end, color)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(cda_method(start, end, color)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(bresenham_smooth_method(start, end, color)[0]))
        if method == 4:
            tmp = copy.deepcopy(list(wu_method(start, end, color)[0]))
        dots.append(tmp)
        last_activity.append(copy.deepcopy(dots))
        draw(dots)
    except:
        messagebox.showerror("Ошибка", "Неверные данные")


def scale(xc, yc):
    for i in range(len(dots)):
        for j in range(len(dots[i])):
            dots[i][j][0] = scale_k * (dots[i][j][0] - xc) + xc
            dots[i][j][1] = scale_k * (dots[i][j][1] - yc) + yc

    draw(dots)


def scale_up(event):
    global scale_k
    scale_k *= 2
    scale(event.x, event.y)


def scale_down(event):
    global scale_k
    if scale_k > 1:
        scale_k /= 2
    scale(event.x, event.y)


def measure_by_steps(len_line):
    try:
        len_line = float(len_line)
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    if len_line <= 0:
        messagebox.showerror("Ошибка", "Длина линии должна быть выше нуля")
        return

    start = [main_canvas.winfo_width() // 2, main_canvas.winfo_height() // 2]

    angle = 0

    cda_steps = []
    wu_steps = []
    bresenham_int_steps = []
    bresenham_float_steps = []
    bresenham_smooth_steps = []

    start = [main_canvas.winfo_width() // 2, main_canvas.winfo_height() // 2]
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
    print(len(bresenham_float_steps))
    print(bresenham_float_steps)
    angles = [i for i in range(0, 90, 1)]
    print(len(angles))

    plt.subplots(figsize=(60, 40))

    plt.subplot(2, 3, 1)
    plt.bar(angles, bresenham_int_steps)
    plt.title("Брезенхейм (целочисленный)")

    plt.subplot(2, 3, 2)
    plt.bar(angles, bresenham_float_steps)
    plt.title("Брезенхейм (вещественный)")

    plt.subplot(2, 3, 3)
    plt.bar(angles, bresenham_smooth_steps)
    plt.title("Брезенхейм (сглаживание)")

    plt.subplot(2, 3, 4)
    plt.bar(angles, wu_steps)
    plt.title("У")

    plt.subplot(2, 3, 5)
    plt.bar(angles, cda_steps)
    plt.title("ЦДА")

    plt.show()


def drawSpectr(len_line, color, delta_angle, method):
    try:
        len_line = int(len_line)
        delta_angle = float(delta_angle)
        if len_line <= 0:
            messagebox.showerror("Ошибка", "Длина линии должна быть выше нуля")
            return

        if delta_angle <= 0:
            messagebox.showerror("Ошибка", "Угол должен быть больше нуля")
            return

        start = [main_canvas.winfo_width() // 2, main_canvas.winfo_height() // 2]
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


def exit_prog():
    sys.exit()


def special_add():
    dots.clear()
    dots.append(bresenham_int_method([0, 0], [50, 400], c)[0])
    dots.append(bresenham_float_method([10, 0], [60, 400], c)[0])
    dots.append(cda_method([20, 0], [70, 400], c)[0])
    dots.append(bresenham_smooth_method([30, 0], [80, 400], c)[0])
    dots.append(wu_method([40, 0], [90, 400], c)[0])

    dots.append(bresenham_int_method([100, 0], [500, 50], c)[0])
    dots.append(bresenham_float_method([100, 10], [500, 60], c)[0])
    dots.append(cda_method([100, 20], [500, 70], c)[0])
    dots.append(bresenham_smooth_method([100, 30], [500, 80], c)[0])
    dots.append(wu_method([100, 40], [500, 90], c)[0])

    draw(dots)
    last_activity.append(copy.deepcopy(dots))


if __name__ == '__main__':
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №3")
    root.minsize(WIDTH, HEIGHT)

    main_canvas = Canvas(root, bg="black")
    main_canvas.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

    menu_label = Label(text="Меню", bg='red')
    menu_label.place(relx=0, rely=0, relwidth=0.4, relheight=0.05)

    method_label = Label(text="Метод", bg="grey")
    method_label.place(relx=0, rely=0.05, relwidth=0.4, relheight=0.05)

    method_list = ("Брезенхем (целочисленный)", "Брезенхем (вещественный)",
                   "ЦДА", "Брезенхем (сглаживание)", "У")
    font_combo = ("Courier", 16, "bold")

    method_combo = ttk.Combobox(root, state='readonly', values=method_list, font=font_combo)
    method_combo.place(relx=0, rely=0.1, relwidth=0.4, relheight=0.1)

    method_combo.current(0)

    color_btn = Button(text="Выберите цвет линии", command=onChooseColor)
    color_btn.place(relx=0, rely=0.2, relwidth=0.2, relheight=0.05)

    color_frame = Frame(border=1, relief=SUNKEN, bg='white')
    color_frame.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.05)

    color_bg_btn = Button(text="Выберите цвет фона", command=onChooseColorBg)
    color_bg_btn.place(relx=0, rely=0.25, relwidth=0.2, relheight=0.05)

    color_frame_bg = Frame(border=1, relief=SUNKEN, bg='black')
    color_frame_bg.place(relx=0.2, rely=0.25, relwidth=0.2, relheight=0.05)

    menu_label_line = Label(text="Отрезок", bg='grey')
    menu_label_line.place(relx=0, rely=0.3, relwidth=0.4, relheight=0.05)

    line_x1 = EntryWithPlaceholder(root, 'X1')
    line_x1.place(relx=0, rely=0.35, relwidth=0.2, relheight=0.05)

    line_y1 = EntryWithPlaceholder(root, 'Y1')
    line_y1.place(relx=0.2, rely=0.35, relwidth=0.2, relheight=0.05)

    line_x2 = EntryWithPlaceholder(root, 'X2')
    line_x2.place(relx=0, rely=0.4, relwidth=0.2, relheight=0.05)

    line_y2 = EntryWithPlaceholder(root, 'Y2')
    line_y2.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.05)

    line_btn = Button(text="Построить линию",
                      command=lambda: drawLine([line_x1.get(), line_y1.get()], [line_x2.get(), line_y2.get()], c,
                                               method_combo.current()))
    line_btn.place(relx=0, rely=0.45, relwidth=0.4, relheight=0.1)

    menu_label_spectr = Label(text="Спектр", bg='grey')
    menu_label_spectr.place(relx=0, rely=0.55, relwidth=0.4, relheight=0.05)

    len_spectr = EntryWithPlaceholder(root, 'Длина отрезка')
    len_spectr.place(relx=0, rely=0.6, relwidth=0.2, relheight=0.05)

    angle_spectr = EntryWithPlaceholder(root, 'Угол')
    angle_spectr.place(relx=0.2, rely=0.6, relwidth=0.2, relheight=0.05)

    spectr_btn = Button(text="Построить спектр",
                        command=lambda: drawSpectr(len_spectr.get(), c, angle_spectr.get(), method_combo.current()))
    spectr_btn.place(relx=0, rely=0.65, relwidth=0.4, relheight=0.1)

    menu_label_other = Label(text="Другое", bg='grey')
    menu_label_other.place(relx=0, rely=0.75, relwidth=0.4, relheight=0.05)

    plt_1_btn = Button(text="Сравнить ступенчатость", command=lambda: measure_by_steps(len_spectr.get()))
    plt_1_btn.place(relx=0, rely=0.8, relwidth=0.4, relheight=0.1)

    clean_btn = Button(text="Очистить все", command=clear_canvas)
    clean_btn.place(relx=0, rely=0.9, relwidth=0.4, relheight=0.1)

    main_menu = Menu(root)
    root.config(menu=main_menu)
    main_menu.add_command(label="О программе", command=lambda: messagebox.showinfo("О программе", TASK))
    main_menu.add_command(label="Об авторе", command=lambda: messagebox.showinfo("Об авторе", "Шаронов А. ИУ7-44Б"))

    filemenu = Menu(main_menu, tearoff=0)

    filemenu.add_command(label="Построить с шагом", command=special_add)
    filemenu.add_command(label="Назад", command=lambda: previous_state(7))

    main_menu.add_cascade(label="Инструменты", menu=filemenu)

    main_menu.add_command(label="Выход", command=exit_prog)

    root.bind("<Key-a>", scale_up)
    root.bind("<Key-b>", scale_down)
    root.bind("<Control-z>", lambda e: previous_state(e))

    root.mainloop()
