import sys
from math import sqrt, pi
from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, messagebox, Menu

WIDTH = 1000
HEIGHT = 600
CENTER = (350, 300)
RADIUS = 3

file_name = 'dots.txt'

EPS = 1e-8

RESULT = False

last_activity = []


TASK = "Нарисовать рисунок медведицы, затем его переместить, "+\
        "промасштабировать, повернуть."

def scale(dots_list, k):
    global RESULT
    RESULT = False
    for i in range(len(dots_list)):
        dots_list[i][0] = k * dots_list[i][0]
        dots_list[i][1] = k * dots_list[i][1]

    draw(dots_list)

def scale_up(event):
    scale(dots_list, 1.2)

def scale_down(event):
    scale(dots_list, 0.9)

def scale_com(event):
    if event.delta == -120:
        scale_down(event)
    elif event.delta == 120:
        scale_up(event)


def draw(dots_list, special_dot=None):
    canvas.delete("all")
    for item in dots_list:
        if item != special_dot:
            canvas.create_oval(
                item[0] - RADIUS, item[1] - RADIUS, item[0] + RADIUS, item[1] + RADIUS,
                fill="#fff", outline="#fff", width=1
            )
        else:
            canvas.create_oval(
                item[0] - RADIUS, item[1] - RADIUS, item[0] + RADIUS, item[1] + RADIUS,
                fill="red", outline="red", width=1
            )


def del_all_dots(dots_list):
    canvas.delete("all")
    if len(dots_list) != 0:
        deleted_dots = []
        for i in range(len(dots_list)):
            deleted_dots.append(dots_list[i].copy())
        dots_list.clear()
        last_activity.append(("DEL_ALL", deleted_dots))

def previous_state_event(event, dots_list):
    global RESULT
    if not RESULT:
        if len(last_activity) > 0:
            act = last_activity.pop()

            if act[0] == 'DEL':
                add_dot(dots_listbox, dots_list, act[2][0], act[2][1], act[1], 1)
                dot_str = "(%-3.1f, %-3.1f)" % (act[2][0], act[2][1])
                if len(dots_list) == 0 or act[1] >= len(dots_list):
                    dots_list.append(act[2])
                    dots_listbox.insert(END, dot_str)
                else:
                    dots_list.insert(act[1], act[2])
                    dots_listbox.insert(act[1], dot_str)
            elif act[0] == 'DEL_ALL':
                for i in range(len(act[1])):
                    dots_list.append(act[1][i])
                for i in range(len(dots_list)):
                    dot_str = "(%-3.1f, %-3.1f)" % (dots_list[i][0], dots_list[i][1])
                    dots_listbox.insert(END, dot_str)
            elif act[0] == 'CHANGE':
                dots_list.pop(act[1])
                dots_listbox.delete(act[1])
                dots_list.insert(act[1], act[2])
                dot_str = "(%-3.1f, %-3.1f)" % (act[2][0], act[2][1])
                dots_listbox.insert(act[1], dot_str)
            else:
                print("ERRORxx")
            draw(dots_list, None)

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
    del_all_dots(dots_list)
    dots_list = read_dots(file_name)
    draw_picture_by_dots(dots_list)

def draw_picture_by_dots(figure):
    for form in figure:
        for dot in form:
            canvas.create_polygon(form, fill="#148012", outline="#fff",\
                                  width=3)

def shift_picture(figure, dx, dy):
    try:
        dx = int(dx)
        dy = -int(dy)
    except:
        dx = 0
        dy = 0

    #print(figure)
    for form in figure:
        for dot in form:
            dot[0] += dx
            dot[1] += dy
    canvas.delete("all")
    draw_picture_by_dots(figure)

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
    x_label_zoom_center.place(relx=0.05, rely=0.05, relwidth=0.02, relheight=0.06)
    x_zoom_center = Entry(root, bg='#6b7a0a')
    x_zoom_center.place(relx=0.08, rely=0.05, relwidth=0.04, relheight=0.06)

    y_label_zoom_center = Label(root, text="Y:", bg='#6b7a0a')
    y_label_zoom_center.place(relx=0.15, rely=0.05, relwidth=0.02, relheight=0.06)
    y_zoom_center = Entry(root, bg='#6b7a0a')
    y_zoom_center.place(relx=0.18, rely=0.05, relwidth=0.04, relheight=0.06)

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
                    activebackground='#6b7a0a')
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
                    activebackground='#6b7a0a')
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
    root.bind("<Control-z>", lambda e: previous_state_event(e, dots_list))
    root.bind("<Control-MouseWheel>", scale_com)
    root.bind("<Control-Up>", scale_up)
    root.bind("<Control-Down>", scale_down)

    draw_picture_by_dots(dots_list)

    #Центр экрана
    canvas.create_oval(CENTER[0] - RADIUS, CENTER[1] - RADIUS,\
                       CENTER[0] + RADIUS, CENTER[1] + RADIUS,
                       fill="red", outline="red", width=1)

    root.mainloop()

if __name__ == "__main__":
    main()
