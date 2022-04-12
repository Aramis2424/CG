import sys
from math import sqrt, pi, cos, sin, radians
import copy
from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, messagebox, Menu

WIDTH = 1000
HEIGHT = 600
RADIUS = 3

EPS = 1e-8

RESULT = False

last_activity = []

TASK = "Нарисовать рисунок медведицы, затем его переместить, "+\
        "промасштабировать, повернуть."

def exit_prog():
    sys.exit()

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

    #dots_list = read_dots(file_name)

    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №3")
    root.minsize(WIDTH, HEIGHT)
    root["bg"] = "#6b5a45"

    #Центр масштабирования и поворота
    label_zoom_center = Label(root, text="Меню",
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
    menu.add_command(label="Выход", command=exit_prog)

    #Команды
    root.bind("<Control-z>", lambda e:\
                last_event(e, last_activity, last_center_place))

    #draw_picture_by_dots(dots_list)

##    #Центр экрана
##    canvas.create_oval(CENTER[0] - RADIUS, CENTER[1] - RADIUS,\
##                       CENTER[0] + RADIUS, CENTER[1] + RADIUS,
##                       fill="red", outline="red", width=1)

    root.mainloop()

if __name__ == "__main__":
    main()




'''


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
menu.add_command(label="Построить с шагом")#, command=special_add)



'''









