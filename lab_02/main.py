import sys
from math import sqrt, pi, cos, sin, radians
import copy
from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, messagebox, Menu

WIDTH = 1000
HEIGHT = 600
X_CENTER = 350
Y_CENTER = 300
CENTER = [350, 300]
name_center = 0
RADIUS = 3

file_name = 'dots.txt'

EPS = 1e-8

RESULT = False

last_activity = []
last_center_place = []


TASK = "Нарисовать рисунок медведицы, затем его переместить, "+\
        "промасштабировать, повернуть."

def del_all_dots(dots_list):
    global last_activity
    last_activity = copy.deepcopy(dots_list)
    canvas.delete("all")
    dots_list.clear()

def read_dots(name):
    form = []
    figure = []
    file_dots = open(name, 'r')
    try:
        string = file_dots.readline()
        while string:
            if string == '\n':
                figure.append(form.copy())
                form.clear()
            else:
                string = list(map(float, string.split()))
                form.append(string)
            string = file_dots.readline()
    finally:
        file_dots.close()

    return figure

def reset_picture():
    global dots_list
    global last_activity, CENTER, X_CENTER, Y_CENTER
    last_activity = copy.deepcopy(dots_list)

    CENTER[0] = X_CENTER
    CENTER[1] = Y_CENTER

    del_all_dots(dots_list)
    dots_list = read_dots(file_name)
    draw_picture_by_dots(dots_list)

def draw_picture_by_dots(figure):
    global CENTER, name_center
    for form in figure:
        for dot in form:
            canvas.create_polygon(form, fill="#148012", outline="#fff",\
                                  width=3)
    #Центр экрана
    name_center = canvas.create_oval(CENTER[0] - RADIUS, CENTER[1] - RADIUS,\
                       CENTER[0] + RADIUS, CENTER[1] + RADIUS,
                       fill="red", outline="red", width=1)

def shift_picture(figure, dx, dy):
    global last_activity
    last_activity = copy.deepcopy(figure)
    try:
        dx = float(dx)
        dy = -float(dy)
    except:
        dx = 0
        dy = 0

    for form in figure:
        for dot in form:
            dot[0] += dx
            dot[1] += dy
    canvas.delete("all")
    draw_picture_by_dots(figure)


def rotate_picture(figure, angle, xc, yc):
    global CENTER
    global last_activity
    last_activity = copy.deepcopy(figure)
    try:
        xc = float(dx)
        yc = float(dy)
    except:
        xc = CENTER[0]
        yc = CENTER[1]

    try:
        angle = float(angle)
    except:
        angle = 0

    for form in figure:
        for dot in form:

            x1 = float(xc + (dot[0] - xc) * cos(radians(angle)) +\
                    (dot[1] - yc) * sin((radians(angle))))
            y1 = float(yc - (dot[0] - xc) * sin(radians(angle)) +\
                    (dot[1] - yc) * cos(radians(angle)))
            dot[0] = x1
            dot[1] = y1

    canvas.delete("all")
    draw_picture_by_dots(figure)


def scale_picture(figure, kx, ky, xm, ym):
    global CENTER
    global last_activity
    last_activity = copy.deepcopy(figure)
    try:
        xm = float(dx)
        ym = float(dy)
    except:
        xm = CENTER[0]
        ym = CENTER[1]

    try:
        kx = float(kx)
        ky = float(ky)
    except:
        kx = 1
        ky = 1

    for form in figure:
        for dot in form:

            x1 = float(kx*dot[0] + (1 - kx) * xm)
            y1 = float(ky*dot[1] + (1 - ky) * ym)
            dot[0] = x1
            dot[1] = y1

    canvas.delete("all")
    draw_picture_by_dots(figure)


def draw_center(x, y):
    global CENTER, canvas, name_center, last_center_place
    last_center_place = copy.deepcopy(CENTER)

    canvas.delete(name_center)
    try:
        x = float(x)
        y = float(y)
    except:
        x = CENTER[0]
        y = CENTER[1]

    CENTER[0] = x
    CENTER[1] = y

    name_center = canvas.create_oval(CENTER[0] - RADIUS, CENTER[1] - RADIUS,\
                       CENTER[0] + RADIUS, CENTER[1] + RADIUS,
                       fill="red", outline="red", width=1)


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



def main():
    global dots_list, dots_listbox, canvas
    dots_list = []

    dots_list = read_dots(file_name)

    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №2")
    root.minsize(WIDTH, HEIGHT)
    root["bg"] = "#6b5a45"

    #Центр масштабирования и поворота
    label_zoom_center = Label(root, text="Центр повората и масштабирования:",
                              bg='#6b7a0a')
    label_zoom_center.place(relx=0, rely=0, relwidth=0.3, relheight=0.04)

    x_label_zoom_center = Label(root, text="X:", bg='#6b7a0a')
    x_label_zoom_center.place(relx=0., rely=0.05, relwidth=0.02, relheight=0.06)
    x_zoom_center = Entry(root, bg='#6b7a0a')
    x_zoom_center.place(relx=0.03, rely=0.05, relwidth=0.04, relheight=0.06)

    y_label_zoom_center = Label(root, text="Y:", bg='#6b7a0a')
    y_label_zoom_center.place(relx=0.1, rely=0.05, relwidth=0.02, relheight=0.06)
    y_zoom_center = Entry(root, bg='#6b7a0a')
    y_zoom_center.place(relx=0.13, rely=0.05, relwidth=0.04, relheight=0.06)

    center_btn = Button(text="Поставить", width=9, height=2, bg='#6b7a0a',
                    activebackground='#6b7a0a',
                    command=lambda:
                    draw_center(x_zoom_center.get(), y_zoom_center.get()))
    center_btn.place(relx=0.18, rely=0.05, relwidth=0.1, relheight=0.06)

    #Перемещение
    label_shift = Label(root, text="Перемещение:",
                              bg='#6b7a0a')
    label_shift.place(relx=0, rely=0.16, relwidth=0.3, relheight=0.04)

    x_label_shift = Label(root, text="dX:", bg='#6b7a0a')
    x_label_shift.place(relx=0.05, rely=0.21, relwidth=0.02, relheight=0.06)
    x_shift = Entry(root, bg='#6b7a0a')
    x_shift.place(relx=0.08, rely=0.21, relwidth=0.04, relheight=0.06)

    y_label_shift = Label(root, text="dY:", bg='#6b7a0a')
    y_label_shift.place(relx=0.15, rely=0.21, relwidth=0.02, relheight=0.06)
    y_shift = Entry(root, bg='#6b7a0a')
    y_shift.place(relx=0.18, rely=0.21, relwidth=0.04, relheight=0.06)

    shift_btn = Button(text="Переместить", width=9, height=2, bg='#6b7a0a',
                    activebackground='#6b7a0a',
                    command=lambda:
                    shift_picture(dots_list, x_shift.get(), y_shift.get()))
    shift_btn.place(relx=0, rely=0.28, relwidth=0.3, relheight=0.08)

    #Поворот
    label_rotation = Label(root, text="Поворот:",
                              bg='#6b7a0a')
    label_rotation.place(relx=0, rely=0.4, relwidth=0.3, relheight=0.04)

    angle_label_rotation = Label(root, text="Угол°:", bg='#6b7a0a')
    angle_label_rotation.place(relx=0.1, rely=0.45, relwidth=0.05, relheight=0.06)
    angle_rotation = Entry(root, bg='#6b7a0a')
    angle_rotation.place(relx=0.16, rely=0.45, relwidth=0.04, relheight=0.06)

    rotation_btn = Button(text="Повернуть", width=9, height=2, bg='#6b7a0a',
                    activebackground='#6b7a0a', command=lambda:
                    rotate_picture(dots_list, angle_rotation.get(),\
                    x_zoom_center.get(), y_zoom_center.get()))
    rotation_btn.place(relx=0, rely=0.52, relwidth=0.3, relheight=0.08)

    #Масштабирование
    label_scale = Label(root, text="Масштабирование:",
                              bg='#6b7a0a')
    label_scale.place(relx=0, rely=0.65, relwidth=0.3, relheight=0.04)

    x_label_scale = Label(root, text="kX:", bg='#6b7a0a')
    x_label_scale.place(relx=0.05, rely=0.7, relwidth=0.02, relheight=0.06)
    x_scale = Entry(root, bg='#6b7a0a')
    x_scale.place(relx=0.08, rely=0.7, relwidth=0.04, relheight=0.06)

    y_label_scale = Label(root, text="kY:", bg='#6b7a0a')
    y_label_scale.place(relx=0.15, rely=0.7, relwidth=0.02, relheight=0.06)
    y_scale = Entry(root, bg='#6b7a0a')
    y_scale.place(relx=0.18, rely=0.7, relwidth=0.04, relheight=0.06)

    scale_btn = Button(text="Масштабировать", width=9, height=2, bg='#6b7a0a',
                    activebackground='#6b7a0a', command=lambda:
                    scale_picture(dots_list, x_scale.get(), y_scale.get(),\
                    x_zoom_center.get(), y_zoom_center.get()))
    scale_btn.place(relx=0, rely=0.77, relwidth=0.3, relheight=0.08)

    #List_box
    dots_listbox = Listbox(font = ("Times", 14))
    dots_listbox.bind("<<ListboxSelect>>",
          lambda e, a=dots_listbox, b=dots_list: listbox_select_event(e, a, b))

    #Сброс
    reset_btn = Button(text="Сбросить", width=9, height=2, bg='#6b7a0a',
                    activebackground='#6b7a0a', command = lambda:
                    reset_picture())

    reset_btn.place(relx=0, rely=0.91, relwidth=0.3, relheight=0.08)

    #Canvas
    canvas = Canvas(root, bg="#148012",
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
                        del_all_dots(dots_list))

    #Команды
    root.bind("<Control-z>", lambda e:\
                last_event(e, last_activity, last_center_place))

    draw_picture_by_dots(dots_list)

##    #Центр экрана
##    canvas.create_oval(CENTER[0] - RADIUS, CENTER[1] - RADIUS,\
##                       CENTER[0] + RADIUS, CENTER[1] + RADIUS,
##                       fill="red", outline="red", width=1)

    root.mainloop()

if __name__ == "__main__":
    main()
