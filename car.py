import random
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Button, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

currentProfit = 0
profit = "Profit: " + str(currentProfit)
repairFlag = 0
totalProfit = 0
totalIters = 0
kek = []
interval = 100
i = 0

class Car(object):
    def __init__(self,repairFlag):
        self.mass = random.uniform(1.0,4.0)

        if (repairFlag == 0):                       #если дорога не ремонтируется
            self.gate = random.randint(0,1)         #то машина выбирает куда ехать 0-бесплатная, 1-платная
        elif(repairFlag == 1):                      #если ремонтируется платная дорога
            self.gate = 0                           #едет только по бесплатной
        elif(repairFlag == 2):                      #если ремонтируется бесплатная дорога
            self.gate = 1                            #едет только по платной
        else:                                       #если ремонтируются обе дороги
            self.gate = -1                          #не едет

        if (self.gate <= 0):
            self.cost = 0
        else:
            self.cost = self.mass * 1.8

    def addParams(self):
        global totalIters, totalProfit, currentProfit
        currentProfit = self.cost - 1.0
        totalProfit += self.cost - 1
        totalProfit = round(totalProfit,3)
        totalIters += 1

    def printArgs(self):
        print("Mass: ", self.mass, "\nGate: ", self.gate, "\nCost: ", self.cost)

car = Car(1)
#####Парочка функций для кнопок#########

def BreakPaidRoad(event): #
    global repairFlag, car
    if repairFlag == 2 or repairFlag == -1:
        repairFlag = -1
    else:
        repairFlag = 1
        canLight2.itemconfig(oval1, fill = "green")
    canLight1.itemconfig(oval, fill = "red")

def FixPaidRoad(event): #
    global repairFlag
    if repairFlag == 1 or repairFlag == 0:
        repairFlag = 0
    else:
        repairFlag = 2
        canLight1.itemconfig(oval, fill = "green")

def BreakFreeRoad(event): #
    global repairFlag
    if repairFlag == 1 or repairFlag == -1:
        repairFlag = -1
    else:
        repairFlag = 2
        canLight1.itemconfig(oval, fill = "green")
    canLight2.itemconfig(oval1, fill = "red")

def FixFreeRoad(event): #
    global repairFlag
    if repairFlag == 2 or repairFlag == 0:
        repairFlag = 0
    else:
        repairFlag = 1
        canLight2.itemconfig(oval1, fill = "green")

########################################

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

##########Функция для ограничения нарисованных точек на графике##########

def makeNewItem(car1):
    global car, repairFlag, kek, totalProfit, totalIters
    car1.addParams()
    kek.append([totalIters,totalProfit])
    if len(kek) > 30:
        del kek[0]

#######################################################################

tk = Tk()

tk.resizable(0, 0)
############## Отрисовка новых значений графика ########################

def animate(i):
    makeNewItem(car)
    xs = []
    ys = []
    for index,line in enumerate(kek):
        xs.append(line[0])
        ys.append(line[1])
    ax1.clear()
    ax1.plot(xs, ys)
    plt.xlabel('time')
    plt.ylabel('Profit')
    plt.title('Profit over time graph')

####################################################################

#######################Лампочка аварии и кнопки для вкл/выкл ##################
canButtom1 = Canvas(tk, width = 20, height = 5)
canButtom1.place(x = 0, y = 200)

canButtom2 = Canvas(tk, width = 25, height = 5)
canButtom2.place(x = 0, y = 300)

canLight1 = Canvas(tk, width = 55, height = 55)
canLight1.place(x = 100, y = 100)
oval = canLight1.create_oval(5, 5, 55, 55,
                     fill="white")

canLight2 = Canvas(tk, width = 55, height = 55)
canLight2.place(x = 0, y = 100)
oval1 = canLight2.create_oval(5, 5, 55, 55,
                     fill="green")

b = Button(canButtom1, text = 'Ремонт платной дороги', width = 20, height = 2, bg = "Black",foreground = "white")
b.pack(side = 'right')
b.bind(sequence="<Button-1>", func = BreakPaidRoad)

b1 = Button(canButtom1, text = 'Платная дорога работает', width = 20, height = 2, bg = "Black",foreground = "white")
b1.pack(side = 'left')
b1.bind(sequence="<Button-1>", func = FixPaidRoad)

b2 = Button(canButtom2, text = 'Ремонт бесплатной дороги', width = 25, height = 2, bg = "Black",foreground = "white")
b2.pack(side = 'right')
b2.bind(sequence="<Button-1>", func = BreakFreeRoad)

b3 = Button(canButtom2, text = 'Бесплатная дорога работает', width = 25, height = 2, bg = "Black",foreground = "white")
b3.pack(side = 'left')
b3.bind(sequence="<Button-1>", func = FixFreeRoad)
###########################################################################


########################Вывод профита ##########################

def textUpdate():
    global currentProfit, totalProfit
    profit = "Current Profit: " + str(round(currentProfit,3)) + "\nTotal Profit: " + str(totalProfit)
    textprofit.config(text = profit)
    textprofit.after(interval - 50, textUpdate)

textprofit = Label(tk,text = profit)
textprofit.place(x = 0, y = 0)
textprofit.after(interval - 50, textUpdate)

######################################################

################################ Движение машинки ########################

def carMove(can):
    global i, car, repairFlag
    len = 47
    if i < 470:
        can.move("car", len, 0)
        can.after(interval, carMove, can)
        i += len
    elif repairFlag == -1:
        can.delete("car")
        car = Car(repairFlag)
        can.after(interval, carMove, can)
    else:
        can.delete("car")
        car = Car(repairFlag)
        if repairFlag == 0:
            if car.gate == 0:
                canLight1.itemconfig(oval, fill = "white")
                canLight2.itemconfig(oval1, fill = "green")
            elif car.gate == 1:
                canLight1.itemconfig(oval, fill = "green")
                canLight2.itemconfig(oval1, fill = "white")
        carDraw(can, car.gate)
        can.after(interval, carMove, can)
        i = 0
###################################################################

################################ Отрисовка картинок ######################

def carDraw(can, gate):

    points = [# точки для колес машины на экране
        110, 50, 110, 40, 120, 40, 120, 50,
        150, 50, 150, 40, 160, 40, 160, 50,
        160, 80, 160, 90, 150, 90, 150, 80,
        120, 80, 120, 90, 110, 90, 110, 80,
        ]

    points2 = [# точки для контура машины на экране
        100, 50, 170, 50,
        170, 80, 100, 80,
        ]

    points3 = [# точки для крыши машины на экране
        130, 60, 150, 65, 130, 70
        ]

    can.create_polygon(# колеса машины
        points, outline='black',
        fill='black', width=2,
        tag = "car"
        )

    can.create_polygon( # контур машины
        points2, outline='red',
        fill='green', width=2,
        tag = "car"
        )

    can.create_polygon( # крыша машины
        points3, outline='red',
        fill='orange', width=2,
        tag = "car"
    )

    if gate == 0:
        can.place(x = 424, y = 0)
    else:
        can.place(x = 424, y = 100)

can4 = Canvas(tk, width = 600, height = 200)

carDraw(can4, car.gate)
func = carMove(can4)
can4.after(interval,func)
#######################################################################

################################ Cам график в GUI ##########################
can = Canvas(tk, width = 800, height = 600)
can.place(x = 424, y = 240)
canvas = FigureCanvasTkAgg(fig, can)
canvas.get_tk_widget().grid(column=0,row=1)

ani = animation.FuncAnimation(fig, animate, interval = interval)

###########################################################################
tk.geometry('1024x720')
tk.mainloop()
