import sys
from math import sqrt, pi
from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, messagebox, Menu

WIDTH = 900
HEIGHT = 600
RADIUS = 3

EPS = 1e-8

RESULT = False

last_activity = []


TASK = "Из заданного на плоскости множества точек выбрать три различные " \
       "точки так, чтобы разность между площадью круга, " \
       "ограниченного окружностью, проходящей через эти три точки, " \
       "и площадью треугольника с вершинами в этих точках была минимальной."

def geron(a, b, c):
    p = (a + b + c) / 2
    return sqrt(p*(p-a)*(p-b)*(p-c))

def len_side(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def is_one_line(x_1, x_2, x_3, y_1, y_2, y_3):
    try:
        if (x_3 - x_1) / (x_2 - x_1) == (y_3 - y_1) / (y_2 - y_1):
            return True
    except:
        pass
    return False

def solution(listbox, dots_list):
    global RESULT
    if not RESULT:
        if len(dots_list) == 0:
            messagebox.showerror("Ошибка", "Нет точек.")
        elif len(dots_list) == 1:
            messagebox.showerror("Ошибка", "Введена только 1 точка. Нужно минимум 3.")
        elif len(dots_list) == 2:
            messagebox.showerror("Ошибка", "Введена только 2 точка. Нужно минимум 3.")
        else:
            flag1 = False
            flag2 = True
            min_rez = []
            min_cx, min_cy, min_r = 0, 0, 0
            points = [[dots_list[i], dots_list[j], dots_list[k]]\
                for i in range(len(dots_list)-2)\
                for j in range(i+1, len(dots_list)-1)\
                for k in range(j+1, len(dots_list))]
            # загнали их в тройки абсолютно все возможные. переборомм

            for z in points: # по каждой тройке посчитаем параметры окружности
                x1, y1 = z[0]
                x2, y2 = z[1]
                x3, y3 = z[2]

                if is_one_line(x1, x2, x3, y1, y2, y3):
                    flag1 = True
                    continue

                flag2 = False
                side1 = len_side(x1, x2, y1, y2)
                side2 = len_side(x2, x3, y2, y3)
                side3 = len_side(x1, x3, y1, y3)
                St = geron(side1, side2, side3)


                Cx = -(1/2)*(y1*(x2**2-x3**2+y2**2-y3**2)\
                    +y2*(-x1**2+x3**2-y1**2+y3**2)\
                    +y3*(x1**2-x2**2+y1**2-y2**2))\
                    /(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))
                Cy = (1/2)*(x1*(x2**2-x3**2+y2**2-y3**2)\
                    +x2*(-x1**2+x3**2-y1**2+y3**2)\
                    +x3*(x1**2-x2**2+y1**2-y2**2))\
                    /(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))

                R = sqrt((x1-Cx)**2 + (y1 - Cy)**2)
                So = pi*R**2

                if min_rez:
                    if min_rez[0] > abs(St-So):
                        min_rez[0] = abs(St-So)
                        min_rez[1] = z
                        min_cx = Cx
                        min_cy = Cy
                        min_r = R
                        mSt = St
                        mSo = So
                else:
                    min_rez.append(abs(St-So))
                    min_rez.append(z)
                    min_cx = Cx
                    min_cy = Cy
                    min_r = R
                    mSt = St
                    mSo = So

            if (flag1 == True and flag2 == True):
                 messagebox.showinfo("Ошибка", "Точки на одной прямой")
                 return
            canvas.create_oval(min_cx - min_r, min_cy - min_r,\
                    min_cx + min_r, min_cy + min_r,
                    fill="red", outline="red", width=1)

            canvas.create_polygon(min_rez[1][0],min_rez[1][1],min_rez[1][2],\
                                    fill="#000", outline="#000", width=1)

            RESULT = True

            St = round(mSt, 3)
            So = round(mSo, 3)
            res = round(abs(mSt-mSo), 3)
            messagebox.showinfo("Пояснение", f"Площадь треугольнка: {St}\nПлощадь круга: {So}\nРазница площадей: {res}")

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

def listbox_select_event(event, listbox, dots_list):
    global RESULT
    if not RESULT:
        try:
            draw(dots_list, dots_list[listbox.curselection()[0]])
        except:
            messagebox.showerror("Ошибка", "Невозможно выбрать элемент в listbox(RESULT = False)")


def init_input_window():
    input_window = Tk()
    input_window.geometry("200x200")
    input_window.resizable(False, False)
    x_label = Label(input_window, text="X:")
    x_label.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.2)
    x_input = Entry(input_window)
    x_input.focus()
    x_input.place(relx=0.3, rely=0.1, relwidth=0.6, relheight=0.2)
    y_label = Label(input_window, text="Y:")
    y_label.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.2)
    y_input = Entry(input_window)
    y_input.place(relx=0.3, rely=0.4, relwidth=0.6, relheight=0.2)
    return input_window, x_input, y_input

def new_dot(listbox, dots_list):
    global RESULT
    if not RESULT:
        listbox.selection_clear(0, END)
        dot_window, dot_x, dot_y = init_input_window()

        add_but = Button(dot_window, text="Добавить",
                         command=lambda: add_dot(listbox, dots_list, dot_x.get(), dot_y.get(), END))
        add_but.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)

        dot_window.mainloop()

def add_dot(listbox, dots_list, x, y, index, re=0):
    global RESULT
    if not RESULT:
        try:
            #listbox.selection_clear(0, END)
            dot_str = "(%-3.1f, %-3.1f)" % (float(x), float(y))
            if index != END or index == len(dots_list):
                listbox.delete(index)
                tmp = dots_list.pop(index)
                dots_list.insert(index, [float(x), float(y)])
                if re != 1:
                    last_activity.append(("CHANGE", index, tmp, [float(x), float(y)]))
            else:
                dots_list.append([float(x), float(y)])
                if re != 1:
                    last_activity.append(("ADD", len(dots_list) - 1, [float(x), float(y)]))
            listbox.insert(index, dot_str)
            draw(dots_list, None) #ошибка здесь
        except:
            messagebox.showerror("Ошибка", "Неверно введены координаты точки")

def add_dot_event(event, listbox, dots_list):
    global RESULT
    if not RESULT:
        try:
            add_dot(listbox, dots_list, event.x, event.y, END)
        except:
            messagebox.showerror("Ошибка", "Ошибка добавления")

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


def del_dot(listbox, dots_list, re=0):
    global RESULT
    if not RESULT:
        try:
            index = listbox.curselection()[0]
            tmp = dots_list.pop(index)
            listbox.delete(index)
            draw(dots_list, None)
            if re != 1:
                last_activity.append(("DEL", index, tmp))
        except:
            messagebox.showerror("Ошибка", "Не выбрана точка для удаления")

def del_all_dots(listbox, dots_list):
    global RESULT
    if not RESULT:
        if len(dots_list) != 0:
            listbox.delete(0, END)
            deleted_dots = []
            for i in range(len(dots_list)):
                deleted_dots.append(dots_list[i].copy())
            dots_list.clear()
            draw(dots_list, None)
            last_activity.append(("DEL_ALL", deleted_dots))

def change_dot(listbox, dots_list):
    global RESULT
    if not RESULT:
        try:
            index = listbox.curselection()[0]
        except:
            messagebox.showerror("Ошибка", "Не выбрана точка для изменения")
            return

        dot_win, x, y = init_input_window()

        change_but = Button(dot_win, text="Изменить",
                            command=lambda: add_dot(listbox, dots_list, x.get(), y.get(), index))
        change_but.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)

        dot_win.mainloop()

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
            elif act[0] == 'ADD':
                dots_list.pop(act[1])
                dots_listbox.delete(act[1])
            elif act[0] == 'CHANGE':
                dots_list.pop(act[1])
                dots_listbox.delete(act[1])
                dots_list.insert(act[1], act[2])
                dot_str = "(%-3.1f, %-3.1f)" % (act[2][0], act[2][1])
                dots_listbox.insert(act[1], dot_str)
            else:
                print("ERRORxx")
            draw(dots_list, None)
    else:
        RESULT = False
        draw(dots_list, None)
        for i in range(len(dots_list) - 1):
            x = listbox.get(i)
            x = '(' + '{:3.1f}, {:3.1f}'.format(dots_list[i][0], dots_list[i][1]) + ')'
            listbox.delete(i)
            listbox.insert(i, x)
        x = listbox.get(len(dots_list) - 1)
        x = '(' + '{:3.1f}, {:3.1f}'.format(dots_list[len(dots_list) - 1][0], dots_list[len(dots_list) - 1][1]) + ')'
        listbox.delete(len(dots_list) - 1)
        listbox.insert(END, x)

def edit_event(listbox, dots_list):
    global RESULT
    if RESULT:
        RESULT = False
        draw(dots_list, None)
        for i in range(len(dots_list) - 1):
            x = listbox.get(i)
            x = '(' + '{:3.1f}, {:3.1f}'.format(dots_list[i][0], dots_list[i][1]) + ')'
            listbox.delete(i)
            listbox.insert(i, x)
        x = listbox.get(len(dots_list) - 1)
        x = '(' + '{:3.1f}, {:3.1f}'.format(dots_list[len(dots_list) - 1][0], dots_list[len(dots_list) - 1][1]) + ')'
        listbox.delete(len(dots_list) - 1)
        listbox.insert(END, x)


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


def draw_picture_by_dots(figure):
    for form in figure:
        for dot in form:
            canvas.create_polygon(form, fill="#148012", outline="#fff", width=3)

def main():

    global dots_list, dots_listbox, canvas
    dots_list = []


    file_name = 'dots.txt'
    figure_arr = read_dots(file_name)
    #print(figure_arr)

    for form in figure_arr:
        for dot in figure_arr:
            dots_list.extend(dot)
    #print(dots_list)



    #Окно
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.title("Лабораторная работа №1")
    root.minsize(WIDTH, HEIGHT)
    root["bg"] = "#6b5a45"

    #Label`ы
    inf_label_1 = Label(root, text="Точки:", bg='#6b5a45')
    inf_label_1.place(relx=0, rely=0, relwidth=0.3, relheight=0.05)

    #List_box
    dots_listbox = Listbox(font = ("Times", 14), bg="#6b5a45",\
                        highlightbackground="#6b5a45",
                        highlightthickness=5)
    dots_listbox.place(relx=0, rely=0.05, relwidth=0.3, relheight=0.6)
    dots_listbox.bind("<<ListboxSelect>>",
            lambda e, a=dots_listbox, b=dots_list: listbox_select_event(e, a, b))

    #Кнопки
    add_btn = Button(text="Добавить", width=9, height=2, bg='#6b5a45',\
                    activebackground='#6b5a45',
                    command=lambda: new_dot(dots_listbox, dots_list))
    add_btn.place(relx=0, rely=0.65, relwidth=0.3, relheight=0.08)

    del_btn = Button(text="Удалить", width=9, height=2, bg='#6b5a45',\
                    activebackground='#6b5a45',
                     command=lambda: del_dot(dots_listbox, dots_list))
    del_btn.place(relx=0, rely=0.73, relwidth=0.3, relheight=0.08)

    change_btn = Button(text="Изменить", width=9, height=2, bg='#6b5a45',\
                    activebackground='#6b5a45',
                        command=lambda: change_dot(dots_listbox, dots_list))
    change_btn.place(relx=0, rely=0.81, relwidth=0.3, relheight=0.08)

    solve_btn = Button(text="Решить задачу!", width=9, height=2, bg='#6b5a45',\
                    activebackground='#6b5a45',
                       command=lambda: solution(dots_listbox, dots_list))
    solve_btn.place(relx=0, rely=0.89, relwidth=0.3, relheight=0.1)

    #Canvas
    canvas = Canvas(root, bg="#148012", highlightthickness=4, highlightbackground="#6b3e07")
    canvas.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
    canvas.bind("<Button-1>", lambda e, a=dots_listbox, b=dots_list: add_dot_event(e, a, b))

    #Меню
    menu = Menu(root)
    root.config(menu=menu)
    menu.add_command(label="Задание", command=lambda:\
                        messagebox.showinfo("Задание", TASK))
    menu.add_command(label="Автор",command=lambda:\
                        messagebox.showinfo("Автор", "Симонович Р.Д. ИУ7-44Б"))
    menu.add_command(label="Очистить холст", command=lambda:\
                        del_all_dots(dots_listbox, dots_list))
    menu.add_command(label="Отменить решение", command=lambda a=dots_listbox, x=dots_list: edit_event(a, x))

    #Команды
    root.bind("<Control-z>", lambda e: previous_state_event(e, dots_list))
    root.bind("<Up>", scale_up)
    root.bind("<Down>", scale_down)

    draw_picture_by_dots(figure_arr)
    root.mainloop()

if __name__ == "__main__":
    main()
