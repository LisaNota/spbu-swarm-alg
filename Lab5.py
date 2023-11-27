#!/usr/bin/env python
# coding: utf-8

import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class piece(object):
    """
    Класс, описывающий одну частицу
    """
    def __init__(self, swarm):
        """
        swarm - экземпляр класса Swarm, хранящий параметры алгоритма, список частиц и лучшее значение роя в целом
        curr_position - текущее положение частицы. Инициализируется случайно
        local_best_position - лучшее положение частицы. Инициализируется начальной позицией
        local_best_position - лучшее значение целевой функции частицы. 
        Инициализируется значением из начальной позиции
        velocity - скорость частицы
        """
        self.curr_position = np.random.rand(2) * (swarm.maxvalues - swarm.minvalues) + swarm.minvalues
        self.local_best_position = self.curr_position
        self.local_best_fitness = swarm.get_final_finc(self.curr_position)
        self.velocity = self.init_velocity(swarm)

    def init_velocity(self, swarm):
        """
        Инициализация скорости частицы
        """
        minval = -(swarm.maxvalues - swarm.minvalues)
        maxval = (swarm.maxvalues - swarm.minvalues)
        return np.random.rand(2) * (maxval - minval) + minval

    def next_iteration(self, swarm):
        """
        Перемещение частицы
        """
        # Весовой коэффициент лучшей позиции частицы
        rnd_curr_best_position = np.random.rand(2)
        
        # Весовой коэффициент лучшей позиции среди всего роя
        rnd_global_best_position = np.random.rand(2)
    
        # Коррекция скорости
        veloRatio = swarm.local_velocity_ratio + swarm.global_velocity_ratio
        commonRatio = (2.0 * swarm.curr_velocity_ratio /
                       (np.abs(2.0 - veloRatio - np.sqrt(veloRatio ** 2 - 4.0 * veloRatio))))

        # Рассчет новой скорости
        newVelocity_part2 = (commonRatio *
                             swarm.local_velocity_ratio *
                             rnd_curr_best_position *
                             (self.local_best_position - self.curr_position))

        newVelocity_part3 = (commonRatio *
                             swarm.global_velocity_ratio *
                             rnd_global_best_position *
                             (swarm.global_best_position - self.curr_position))

        self.velocity = commonRatio * self.velocity + newVelocity_part2 + newVelocity_part3
        self.curr_position += self.velocity
        
        # Обновление локальной и глобальной лучших позиций и функций
        final_finc = swarm.get_final_finc(self.curr_position)
        if self.local_best_fitness is None or final_finc < self.local_best_fitness:
            self.local_best_position = self.curr_position
            self.local_best_fitness = final_finc

        if swarm.global_best_fitness is None or final_finc < swarm.global_best_fitness:
            swarm.global_best_position = self.curr_position
            swarm.flobal_best_fitness = final_finc


# In[3]:


class Swarm:
    """
    Класс роя частиц
    """

    def __init__(self, swarmsize, minvalues, maxvalues, curr_velocity_ratio, local_velocity_ratio, global_velocity_ratio):
        """
        swarmsize - размер роя
        minvalues, maxvalues - нижние и верхние границы поиска
        curr_velocity_ratio - коэффициент текущей скорости частицы
        local_velocity_ratio - коэффициент локального лучшего значения
        global_velocity_ratio - коэффициент глобального лучшего значения
        global_best_fitness - лучшее значение целевой функции, найденное всеми частицами
        global_best_position - лучшее значение частицы
        """
        self.swarmsize = swarmsize
        self.minvalues = np.array(minvalues)
        self.maxvalues = np.array(maxvalues)
        self.curr_velocity_ratio = curr_velocity_ratio
        self.local_velocity_ratio = local_velocity_ratio
        self.global_velocity_ratio = global_velocity_ratio
        self.global_best_fitness = float('inf')
        self.global_best_position = None
        self.swarm = self.create_swarm()

    def create_swarm(self):
        """
        Создание роя частиц
        """
        return [piece(self) for _ in range(self.swarmsize)]

    def next_iteration(self):
        """
        Перемещение каждой частицы
        """
        for piece in self.swarm:
            piece.next_iteration(self)

    def final_finc(self, position):
        """
        Целевая функция, которую необходимо минимизировать
        """
        result = 2 * (position[0] ** 3) + 4 * position[0] * (position[1] ** 3) - 10 * position[0] * position[1] + \
                 position[1] ** 2
        return result if result is not None else float('inf')

    def get_final_finc(self, position):
        """
        Определение лучшей позиции частицы и лучшего целевого значения
        """
        final_finc = self.final_finc(position)

        if self.global_best_fitness is None or final_finc < self.global_best_fitness:
            self.global_best_fitness = final_finc
            self.global_best_position = position
        return final_finc


# In[4]:


def inserted(place, num):
    place.delete(0, tk.END)
    place.insert(0, str(num))


# In[5]:


def creating():
    """
    Функция для создания и отображения роя
    """
    global swarm, ax, scatter, canvas_widget

    # Использование данных из интерфейса
    curr_velocity_ratio = float(currVeloc.get())
    local_velocity_ratio = float(localBest.get())
    global_velocity_ratio = float(globalBest.get())
    swarm_size = int(cntPieces.get())

    # Создание роя
    swarm = Swarm(swarm_size, [-10, -10], [5, 5], curr_velocity_ratio, local_velocity_ratio, global_velocity_ratio)

    # Визуализация
    ax.clear()
    ax.set_xlim(-10, 5)
    ax.set_ylim(-10, 5)
    ax.set_title("Положение роя")
    scatter = ax.scatter([], [], color='blue', marker='o')
    canvas_widget.get_tk_widget().update_idletasks()
    positions = np.array([piece.curr_position for piece in swarm.swarm])
    scatter.set_offsets(positions)
    canvas_widget.draw()


def make_iterations(n):
    """
    Функция для отображения перемещения частиц
    """
    global swarm, ax, scatter, canvas_widget

    # Обновление счетчика совершенных итераций
    it = int(txt4.get())
    txt4.delete(0, tk.END)
    entry_var.set(str(it + n))

    for _ in range(n):
        swarm.next_iteration()

    # Обновление графика
    positions = np.array([piece.curr_position for piece in swarm.swarm])
    scatter.set_offsets(positions)
    canvas_widget.draw()
    best_position = swarm.global_best_position
    best_fitness = swarm.global_best_fitness

    canvas2.delete("all")
    canvas2.create_text(10, 10, anchor="nw", text=f"Лучшее решение: {best_position}\nЗначение функции: {best_fitness}",
                        font=("Arial", 10), fill="black")


# In[20]:


root = tk.Tk()
root.title("Роевой интеллект для поиска минимума функции")
root.geometry('800x450')

#####     Рамки    ######

canvas = tk.Canvas(root, width=1000, height=1000, borderwidth=0, highlightthickness=0)
canvas.place(relx=0, rely=0.0)

line1 = canvas.create_line(0, 180, 800, 180)
line2 = canvas.create_line(350, 0, 350, 450)

#########################

#####    Рисунок    #####

fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.set_facecolor('white')
ax.tick_params(axis='both', labelsize=8)

ax.set_xlim(-10, 5)
ax.set_ylim(-10, 5)
ax.set_title("Положение роя")

canvas_widget = FigureCanvasTkAgg(fig, master=root)
canvas_widget.get_tk_widget().place(relx=0.5, rely=0.42)


##### Окно настроек #####

lbl = tk.Label(root, text="Предварительные настройки", font=("Arial", 11) )
lbl.place(relx=0.1, rely=0.01)

lblfunc = tk.Label(root, text="Функция:", font=("Arial", 10))
lblfunc.place(relx=0.027, rely=0.075)

lblfunc2 = tk.Label(root, text="2x[1]^3 + 4x[1]x[2]^3-10x[1]x[2]+x[2]^3", font=("Arial", 10))
lblfunc2.place(relx=0.12, rely=0.075)

lblk = tk.Label(root, text="Коэффициент текущей скорости:", font=("Arial", 10))
lblk.place(relx=0.027, rely=0.155)

currVeloc = tk.Entry(root,width=7)
currVeloc.insert(0, "0.3")
currVeloc.place(relx=0.35, rely=0.16)

lblk2 = tk.Label(root, text="Коэф-т локального лучшего значения:", font=("Arial", 10))
lblk2.place(relx=0.027, rely=0.235)

localBest = tk.Entry(root,width=7) 
localBest.insert(0, "2")
localBest.place(relx=0.35, rely=0.24)

lblk2 = tk.Label(root, text="Коэф-т глобального лучшего значения:", font=("Arial", 10))
lblk2.place(relx=0.027, rely=0.235)

globalBest = tk.Entry(root,width=7) 
globalBest.insert(0, "5")
globalBest.place(relx=0.35, rely=0.24)

lblk3 = tk.Label(root, text="Количество частиц:", font=("Arial", 10))
lblk3.place(relx=0.027, rely=0.315)

cntPieces = tk.Spinbox(root, from_=10, to=500, width=5)
cntPieces.place(relx=0.35, rely=0.32)

########################

##### Управление  ######

lbl4 = tk.Label(root, text="Управление", font=("Arial", 11))
lbl4.place(relx=0.16, rely=0.42)

but = tk.Button(root, text="Создать частицы", width=42, 
                command=creating,
                bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but.place(relx=0.03, rely=0.5)

lbl5 = tk.Label(root, text="Количество итераций:", font=("Arial", 10))
lbl5.place(relx=0.027, rely=0.59)

cntIt = tk.Spinbox(root, from_=1, to=5000, width=5)
cntIt.place(relx=0.35, rely=0.6)

but1 = tk.Button(root, text="1", width=8, 
                 command=lambda: inserted(cntIt, 1),
                 bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but1.place(relx=0.03, rely=0.67)

but2 = tk.Button(root, text="10", width=8, 
                 command=lambda: inserted(cntIt, 10),
                 bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but2.place(relx=0.13, rely=0.67)

but3 = tk.Button(root, text="100", width=8, 
                 command=lambda: inserted(cntIt, 100),
                 bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but3.place(relx=0.23, rely=0.67)

but4 = tk.Button(root, text="1000", width=8, 
                 command=lambda: inserted(cntIt, 1000),
                 bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but4.place(relx=0.328, rely=0.67)

but = tk.Button(root, text="Рассчитать", width=42, 
                command=lambda: make_iterations(int(cntIt.get())),
                bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but.place(relx=0.03, rely=0.77)

lbl5 = tk.Label(root, text="Количество выполненных итераций:", font=("Arial", 10))
lbl5.place(relx=0.027, rely=0.865)

cnt = 0
entry_var = tk.StringVar()
txt4 = tk.Entry(root, width=7, textvariable=entry_var, state='disabled', disabledbackground="white", fg="black")
txt4.place(relx=0.35, rely=0.87)
entry_var.set(str(cnt))

########################

#####  Результат  ######

lbl6 = tk.Label(root, text="Результаты", font=("Arial", 11))
lbl6.place(relx=0.65, rely=0.01)

lbl5 = tk.Label(root, text="Лучшее решение достигается в точке:", font=("Arial", 10))
lbl5.place(relx=0.465, rely=0.075)

canvas2 = tk.Canvas(root, width=393, height=100, bg="white", borderwidth=1, highlightbackground="#CCCCCC", highlightthickness=2)
canvas2.place(relx=0.465, rely=0.14)

########################


root.mainloop()
