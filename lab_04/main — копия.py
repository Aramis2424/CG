import copy
import math
import sys
import time
from tkinter import Tk, Button, Label, Entry, Canvas, messagebox, Menu, Frame, SUNKEN, colorchooser
from tkinter import ttk
import matplotlib.pyplot as plt
from colorutils import Color
from math import sqrt, cos, sin, pi

WIDTH = 1000
HEIGHT = 600

EPS = 1e-9

RESULT = False

dots = []
last_activity = []

c = Color(hex='#FFFFFF')
cb = Color(hex='#000000')

TASK = '''Реализовать построение окружности (эллипса) методами: \n
- Канонического уравнения\n
- Параметрического уравнения\n
- Алгоритма Брезенхема\n
- Алгоритма средней точки\n
Построить спектр окружностей и эллипсов.\n
Замер эффективности по времени.'''


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


#################################################################
def canon_method_cir(dot_center, radius, color):
    c_dots = []
    x_c = dot_center[0]
    y_c = dot_center[1]
    color = color.hex

    end = round(radius / math.sqrt(2))

    r2 = radius ** 2
    x = 0
    while x <= end:
        y = round(math.sqrt(r2 - x * x))

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


def canon_method_ell(dot_center, a, b, color):
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


#################################################################
#################################################################
def param_method_cir(dot_center, radius, color):
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


def param_method_ell(dot_center, a, b, color):
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


#################################################################
#################################################################
def bresenham_method_cir(dot_center, radius, color):
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


def bresenham_method_ell(dot_center, a, b, color):
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


#################################################################
#################################################################
def mid_dot_method_cir(dot_center, radius, color):
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


def mid_dot_method_ell(dot_center, a, b, color):
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


#################################################################


def previous_state(event):
    global dots
    dots.clear()
    last_activity.pop()
    if len(last_activity) > 0:
        dots = copy.deepcopy(last_activity[-1])
    draw()


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


def draw():
    main_canvas.delete("all")
    for line in dots:
        for dot in line:
            main_canvas.create_line(dot[0], dot[1], dot[0] + 1, dot[1], fill=dot[2])


def exit_prog():
    sys.exit()


def drawCircle(dot_center, radius, color, method):
    try:
        t1 = float(dot_center[0])
        t2 = float(dot_center[1])
        t3 = float(radius)
        if method == 0:
            tmp = copy.deepcopy(list(canon_method_cir([t1, t2], t3, color)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(param_method_cir([t1, t2], t3, color)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(bresenham_method_cir([t1, t2], t3, color)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(mid_dot_method_cir([t1, t2], t3, color)[0]))
        dots.append(tmp)
        last_activity.append(copy.deepcopy(dots))
        draw()
    except:
        messagebox.showerror("Ошибка", "Неверные данные")


def drawEll(dot_center, a, b, color, method):
    try:
        t1 = float(dot_center[0])
        t2 = float(dot_center[1])
        t3 = float(a)
        t4 = float(b)
        if method == 0:
            tmp = copy.deepcopy(list(canon_method_ell([t1, t2], t3, t4, color)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(param_method_ell([t1, t2], t3, t4, color)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(bresenham_method_ell([t1, t2], t3, t4, color)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(mid_dot_method_ell([t1, t2], t3, t4, color)[0]))
        dots.append(tmp)
        last_activity.append(copy.deepcopy(dots))
        draw()
    except:
        messagebox.showerror("Ошибка", "Неверные данные")


def drawSpectrEll(step, count, a, b, method):
    try:
        step = float(step)
        count = float(count)
        a = float(a)
        b = float(b)
    except:
        messagebox.showerror("Ошибка", "Неверно введены данные")
        return

    if step <= 0 or count <= 0 or a <= 0 or b <= 0:
        messagebox.showerror("Ошибка", "Неверно введены данные")
        return

    dot_center = [main_canvas.winfo_width() // 2, main_canvas.winfo_height() // 2]
    kk = b / a

    index = 0

    while index < count:
        if method == 0:
            tmp = copy.deepcopy(list(canon_method_ell(dot_center, a, b, c)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(param_method_ell(dot_center, a, b, c)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(bresenham_method_ell(dot_center, a, b, c)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(mid_dot_method_ell(dot_center, a, b, c)[0]))
        dots.append(tmp)
        a += step
        b = a * kk
        index += 1

    last_activity.append(copy.deepcopy(dots))
    draw()


def drawSpectrСircle(step, count, start, end, method):
    cc = 0
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

    if flag == 1:
        step = int((end - start) / count)
    elif flag == 2:
        count = int((end - start) / step)
    elif flag == 3:
        start = float(end - step * count)
    elif flag == 4:
        end = float(start + step * count)

    radius = start

    dot_center = [main_canvas.winfo_width() // 2, main_canvas.winfo_height() // 2]

    index = 0

    while index < count:
        if method == 0:
            tmp = copy.deepcopy(list(canon_method_cir(dot_center, radius, c)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(param_method_cir(dot_center, radius, c)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(bresenham_method_cir(dot_center, radius, c)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(mid_dot_method_cir(dot_center, radius, c)[0]))
        dots.append(tmp)
        radius += step
        index += 1
    last_activity.append(copy.deepcopy(dots))
    draw()


def add_dot_event(event, method, color):
    global flag, ddot, drad
    if flag == 0:
        flag = 1
        ddot = [event.x, event.y]
    elif flag == 1:
        flag = 0
        drad = sqrt((ddot[0] - event.x) ** 2 + (ddot[1] - event.y) ** 2)
        if method == 0:
            tmp = copy.deepcopy(list(canon_method_cir(ddot, drad, c)[0]))
        if method == 1:
            tmp = copy.deepcopy(list(param_method_cir(ddot, drad, c)[0]))
        if method == 2:
            tmp = copy.deepcopy(list(bresenham_method_cir(ddot, drad, c)[0]))
        if method == 3:
            tmp = copy.deepcopy(list(mid_dot_method_cir(ddot, drad, c)[0]))
        dots.append(tmp)
        last_activity.append(copy.deepcopy(dots))
        draw()


def measure_by_time():
    dot_center = [main_canvas.winfo_width() // 2, main_canvas.winfo_height() // 2]

    ddt = 200
    var = 50
    res_time = [0] * 8
    for i in range(8):
        res_time[i] = [0] * 10
    count_ = 0
    for i in range(10, 20):
        t1 = time.time()
        for k in range(10):
            canon_method_cir(dot_center, ddt * i, c)
        t2 = time.time()
        res_time[0][count_] = ((t2 - t1) / 10)

        t1 = time.time()
        for k in range(10):
            param_method_cir(dot_center, ddt * i, c)
        t2 = time.time()
        res_time[1][count_] = ((t2 - t1) / 10)

        t1 = time.time()
        for k in range(10):
            bresenham_method_cir(dot_center, ddt * i, c)
        t2 = time.time()
        res_time[2][count_] = ((t2 - t1) / 10)

        t1 = time.time()
        for k in range(10):
            mid_dot_method_cir(dot_center, ddt * i, c)
        t2 = time.time()
        res_time[3][count_] = ((t2 - t1) / 10)

        ###############

        t1 = time.time()
        for k in range(10):
            canon_method_ell(dot_center, ddt * i, ddt * 2 * i, c)
        t2 = time.time()
        res_time[4][count_] = ((t2 - t1) / 10)

        t1 = time.time()
        for k in range(10):
            param_method_ell(dot_center, ddt * i, ddt * 2 * i, c)
        t2 = time.time()
        res_time[5][count_] = ((t2 - t1) / 10)

        t1 = time.time()
        for k in range(10):
            bresenham_method_ell(dot_center, ddt * i, ddt * 2 * i, c)
        t2 = time.time()
        res_time[6][count_] = ((t2 - t1) / 10)

        t1 = time.time()
        for k in range(10):
            mid_dot_method_ell(dot_center, ddt * i, ddt * 2 * i, c)
        t2 = time.time()
        res_time[7][count_] = ((t2 - t1) / 10)

        count_ += 1

    rad_arr = list(i * ddt for i in range(10, 20))
    plt.subplot(1, 2, 1)
    plt.title("Эффективность алгоритмов (окружность)")
    plt.plot(rad_arr, res_time[0], label="Каноническое\nуравнеие")
    plt.plot(rad_arr, res_time[1], label="Параметрическое\nуравнение")
    plt.plot(rad_arr, res_time[2], label="Брезенхем")
    plt.plot(rad_arr, res_time[3], label="Алгоритм\nсредней точки")
    plt.xticks(list(i * ddt for i in range(10, 20)))
    plt.ylabel("Время")
    plt.xlabel("Радиус")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title("Эффективность алгоритмов (эллипс)")
    plt.plot(rad_arr, res_time[4], label="Каноническое\nуравнеие\n(Эллипс)")
    plt.plot(rad_arr, res_time[5], label="Параметрическое\nуравнение\n(Эллипс)")
    plt.plot(rad_arr, res_time[6], label="Брезенхем\n(Эллипс)")
    plt.plot(rad_arr, res_time[7], label="Алгоритм\nсредней точки\n(Эллипс)")


    plt.show()




if __name__ == '__main__':
    root = Tk()
    flag = 0
    ddot = [0, 0]
    drad = 0
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №4")
    root.minsize(WIDTH, HEIGHT)

    main_canvas = Canvas(root, bg="black")
    main_canvas.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

    menu_label = Label(text="Меню", bg='red')
    menu_label.place(relx=0, rely=0, relwidth=0.4, relheight=0.05)

    method_label = Label(text="Метод", bg="grey")
    method_label.place(relx=0, rely=0.05, relwidth=0.4, relheight=0.05)

    method_list = ("Каноническое уравнение",
                   "Параметрическое уравнение",
                   "Алгоритма Брезенхема ",
                   "Алгоритма средней точки")
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

    menu_label_circle = Label(text="Окружность", bg='grey')
    menu_label_circle.place(relx=0, rely=0.3, relwidth=0.4, relheight=0.05)

    circle_x = EntryWithPlaceholder(root, 'X')
    circle_x.place(relx=0, rely=0.35, relwidth=0.13, relheight=0.05)

    circle_y = EntryWithPlaceholder(root, 'Y')
    circle_y.place(relx=0.13, rely=0.35, relwidth=0.13, relheight=0.05)

    circle_r = EntryWithPlaceholder(root, 'R')
    circle_r.place(relx=0.26, rely=0.35, relwidth=0.14, relheight=0.05)

    circle_btn = Button(text="Построить окружность",
                        command=lambda: drawCircle([circle_x.get(), circle_y.get()], circle_r.get(), c,
                                                   method_combo.current()))
    circle_btn.place(relx=0, rely=0.40, relwidth=0.4, relheight=0.05)

    menu_label_ell = Label(text="Эллипс", bg='grey')
    menu_label_ell.place(relx=0, rely=0.45, relwidth=0.4, relheight=0.05)

    ell_x = EntryWithPlaceholder(root, 'X')
    ell_x.place(relx=0, rely=0.5, relwidth=0.1, relheight=0.05)

    ell_y = EntryWithPlaceholder(root, 'Y')
    ell_y.place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.05)

    ell_a = EntryWithPlaceholder(root, 'A')
    ell_a.place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.05)

    ell_b = EntryWithPlaceholder(root, 'B')
    ell_b.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.05)

    ell_btn = Button(text="Построить эллипс",
                     command=lambda: drawEll([ell_x.get(), ell_y.get()], ell_a.get(), ell_b.get(), c,
                                             method_combo.current()))
    ell_btn.place(relx=0, rely=0.55, relwidth=0.4, relheight=0.05)

    menu_label_sp_circle = Label(text="Спектр", bg='grey')
    menu_label_sp_circle.place(relx=0, rely=0.6, relwidth=0.4, relheight=0.05)

    sp_circle_step = EntryWithPlaceholder(root, 'Шаг')
    sp_circle_step.place(relx=0, rely=0.65, relwidth=0.1, relheight=0.05)

    sp_circle_count = EntryWithPlaceholder(root, 'Кол-во')
    sp_circle_count.place(relx=0.1, rely=0.65, relwidth=0.1, relheight=0.05)

    sp_circle_start = EntryWithPlaceholder(root, 'R(нач)')
    sp_circle_start.place(relx=0.2, rely=0.65, relwidth=0.1, relheight=0.05)

    sp_circle_end = EntryWithPlaceholder(root, 'R(кон)')
    sp_circle_end.place(relx=0.3, rely=0.65, relwidth=0.1, relheight=0.05)

    sp_circle_btn = Button(text="Построить спектр окружности",
                           command=lambda: drawSpectrСircle(sp_circle_step.get(), sp_circle_count.get(),
                                                            sp_circle_start.get(), sp_circle_end.get(),
                                                            method_combo.current()))
    sp_circle_btn.place(relx=0, rely=0.7, relwidth=0.4, relheight=0.05)

    sp_ell_step = EntryWithPlaceholder(root, 'Шаг(А)')
    sp_ell_step.place(relx=0, rely=0.75, relwidth=0.1, relheight=0.05)

    sp_ell_count = EntryWithPlaceholder(root, 'Кол-во')
    sp_ell_count.place(relx=0.1, rely=0.75, relwidth=0.1, relheight=0.05)

    sp_ell_start = EntryWithPlaceholder(root, 'A(нач)')
    sp_ell_start.place(relx=0.2, rely=0.75, relwidth=0.1, relheight=0.05)

    sp_ell_end = EntryWithPlaceholder(root, 'B(нач)')
    sp_ell_end.place(relx=0.3, rely=0.75, relwidth=0.1, relheight=0.05)

    sp_ell_btn = Button(text="Построить спектр эллипса",
                        command=lambda: drawSpectrEll(sp_ell_step.get(), sp_ell_count.get(),
                                                      sp_ell_start.get(), sp_ell_end.get(),
                                                      method_combo.current()))
    sp_ell_btn.place(relx=0, rely=0.8, relwidth=0.4, relheight=0.05)

    menu_label_other = Label(text="Другое", bg='grey')
    menu_label_other.place(relx=0, rely=0.85, relwidth=0.4, relheight=0.05)

    plt_1_btn = Button(text="Сравнить эффективность", command=lambda: measure_by_time())
    plt_1_btn.place(relx=0, rely=0.9, relwidth=0.4, relheight=0.05)

    clean_btn = Button(text="Очистить все", command=clear_canvas)
    clean_btn.place(relx=0, rely=0.95, relwidth=0.4, relheight=0.05)

    main_menu = Menu(root)
    root.config(menu=main_menu)
    main_menu.add_command(label="О программе", command=lambda: messagebox.showinfo("О программе", TASK))
    main_menu.add_command(label="Об авторе", command=lambda: messagebox.showinfo("Об авторе", "Шаронов А. ИУ7-44Б"))

    filemenu = Menu(main_menu, tearoff=0)

    filemenu.add_command(label="Назад", command=lambda: previous_state(7))

    main_menu.add_cascade(label="Инструменты", menu=filemenu)

    main_menu.add_command(label="Выход", command=exit_prog)

    main_canvas.bind("<Button-1>", lambda e, a=method_combo.current(), b=c: add_dot_event(e, a, b))
    root.bind("<Control-z>", lambda e: previous_state(e))
    root.mainloop()
