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

TASK = '''Реализовать построение окружности (эллипса) методами: \n
- Канонического уравнения\n
- Параметрического уравнения\n
- Алгоритма Брезенхема\n
- Алгоритма средней точки\n
Построить спектр окружностей и эллипсов.\n
Замер эффективности по времени.'''


def del_all_dots():
    canvas.delete("all")


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

##    #Выбор метода; Установка combox`a
##    combostyle = ttk.Style() #стиль для Combox`a
##    combostyle.theme_create('combostyle', parent='alt',
##                         settings = {'TCombobox':
##                                     {'configure':
##                                      {'selectbackground': '#6b7a0a',
##                                       'fieldbackground': '#6b7a0a',
##                                       'background': '#6b7a0a'
##                                       }}}
##                           )
##    combostyle.theme_use('combostyle')
##
##    label_method = Label(text="Метод:", bg="#6b7a0a", anchor='w')
##    label_method.place(relx=0, rely=0.07, relwidth=0.3, relheight=0.04)
##
##    method_list = ("ЦДА", "Брезенхем (вещественный)",
##                   "Брезенхем (целочисленный)",
##                   "Брезенхем (сглаживание)", "Ву")
##    font_combo = ("Times", 12)
##
##    method_combo = ttk.Combobox(root, state='readonly', values=method_list,
##                    font=font_combo)
##    method_combo.place(relx=0, rely=0.11, relwidth=0.3, relheight=0.06)
##    method_combo.current(0)
##
##    #Задание отрезка
##    label_shift = Label(root, text="Отрезок:", anchor='w',
##                              bg='#6b7a0a')
##    label_shift.place(relx=0, rely=0.23, relwidth=0.3, relheight=0.04)
##
##    #Цвет
##    color_list = ("Черный", "Белый", "Красный",
##                   "Синий", "Зеленый")
##    label_color = Label(root, text="Цвет:", anchor='w',
##                              bg='#6b7a0a')
##    label_color.place(relx=0, rely=0.275, relwidth=0.1, relheight=0.06)
##    color_combo = ttk.Combobox(root, state='readonly', values=color_list,
##                    font=font_combo)
##    color_combo.place(relx=0.1, rely=0.275, relwidth=0.2, relheight=0.06)
##    color_combo.current(0)
##
##    #Координаты отрезка
##    label_x1 = Label(root, text="X1:", anchor='c',
##                              bg='#6b7a0a')
##    label_x1.place(relx=0, rely=0.35, relwidth=0.04, relheight=0.06)
##    line_x1 = Entry(root, bg='#6b7a0a')
##    line_x1.place(relx=0.045, rely=0.35, relwidth=0.04, relheight=0.06)
##
##    label_y1 = Label(root, text="Y1:", anchor='c',
##                              bg='#6b7a0a')
##    label_y1.place(relx=0.15, rely=0.35, relwidth=0.04, relheight=0.06)
##    line_y1 = Entry(root, bg='#6b7a0a')
##    line_y1.place(relx=0.195, rely=0.35, relwidth=0.04, relheight=0.06)
##
##    label_x2 = Label(root, text="X2:", anchor='c',
##                              bg='#6b7a0a')
##    label_x2.place(relx=0, rely=0.415, relwidth=0.04, relheight=0.06)
##    line_x2 = Entry(root, bg='#6b7a0a')
##    line_x2.place(relx=0.045, rely=0.415, relwidth=0.04, relheight=0.06)
##
##    label_y2 = Label(root, text="Y2:", anchor='c',
##                              bg='#6b7a0a')
##    label_y2.place(relx=0.15, rely=0.415, relwidth=0.04, relheight=0.06)
##    line_y2 = Entry(root, bg='#6b7a0a')
##    line_y2.place(relx=0.195, rely=0.415, relwidth=0.04, relheight=0.06)
##
##    line_btn = Button(text="Построить отрезок",
##                  bg='#6b7a0a',
##                  activebackground='#6b7a0a',
##                  command=lambda: drawLine([line_x1.get(), line_y1.get()],
##                  [line_x2.get(), line_y2.get()], color_combo.current(),
##                   method_combo.current()))
##    line_btn.place(relx=0, rely=0.485, relwidth=0.3, relheight=0.08)
##
##    #Спектр
##    menu_label_spectr = Label(text="Спектр:", anchor='w', bg='#6b7a0a')
##    menu_label_spectr.place(relx=0, rely=0.6, relwidth=0.3, relheight=0.05)
##
##    label_len = Label(root, text="Длина:", anchor='c',
##                              bg='#6b7a0a')
##    label_len.place(relx=0, rely=0.655, relwidth=0.15, relheight=0.06)
##    len_spectr = Entry(root, bg='#6b7a0a')
##    len_spectr.place(relx=0.155, rely=0.655, relwidth=0.14, relheight=0.06)
##
##    label_angle = Label(root, text="Угол:", anchor='c',
##                             bg='#6b7a0a')
##    label_angle.place(relx=0, rely=0.722, relwidth=0.15, relheight=0.06)
##    angle_spectr = Entry(root, bg='#6b7a0a')
##    angle_spectr.place(relx=0.155, rely=0.722, relwidth=0.14, relheight=0.06)
##
##    spectr_btn = Button(text="Построить спектр",
##                      bg='#6b7a0a',
##                      activebackground='#6b7a0a',
##                      command=lambda: drawSpectr(len_spectr.get(),
##                      color_combo.current(), angle_spectr.get(),
##                      method_combo.current()))
##    spectr_btn.place(relx=0, rely=0.79, relwidth=0.3, relheight=0.08)
##
##    #Диаграмма
##    plt_1_btn = Button(text="Диаграмма ступенчатости", bg='#6b7a0a',
##                    activebackground='#6b7a0a',
##                    command=lambda: step_diagram(len_spectr.get()))
##
##    plt_1_btn.place(relx=0, rely=0.91, relwidth=0.3, relheight=0.08)

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
    #menu.add_command(label="Построить с шагом")#, command=special_add)
    menu.add_command(label="Выход", command=root.destroy)

    #Команды
    #root.bind("<Control-z>", lambda e: last_event(e))

    root.mainloop()

if __name__ == "__main__":
    main()
