import fuckit as fr
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk 
import random,pickle,os
window = Tk()
o = lambda a: a/1536
p = lambda a: a/888
flags=ImageTk.PhotoImage(Image.open(rf'{os.getcwd()}\minesweeper\flag.png'))
mine = ImageTk.PhotoImage(Image.open(rf'{os.getcwd()}\minesweeper\mine.png'))
@fr
def change(i,j,pos,a,b):
        if i+a>=0 and j+b>=0 :
            pos[i+a][j+b]+=1 if pos[i+a][j+b]!=-1 else 0
def place(pos):
    for i in range(len(pos)):
        for j in range(len(pos[i])):
            if (pos[i][j]) == -1:
                change(i,j,pos,0,1)#right
                change(i,j,pos,0,-1)#left
                change(i,j,pos,1,0)#down
                change(i,j,pos,-1,0)#up
                for k in (-1,1):#diagonals
                    for l in (-1,1):
                        change(i,j,pos,k,l)
def setup(a,b):
    pos=[]
    for i in range(a):
        pos.append([0 for i in range(b)])
    mines = random.choices([(i,j) for i in range(b) for j in range(a)],k=99)
    for i in mines:
        pos[i[1]][i[0]]=-1
    place(pos)

setup(16,30)
flag=[]
flagcount=0
foundcount=0
def falg(a,b):
    for i in range(a):
        flag.append([0 for i in range(b)])
falg(16,30)

def check_flagged(a,b,img='flags'):
    global flagcount
    if is_flagged(a,b):
        flag[a][b]=0
        exec(f"button_{a}_{b}.configure(image='')")
        flagcount-=1
    else: 
        if flagcount<100:
            flag[a][b]=-1
            flagcount+=1
            exec(f"button_{a}_{b}.configure(image={img})")

def is_flagged(a,b):
    return 1 if flag[a][b]== -1 else 0

def write(a,b):
    global foundcount
    foundcount+=1
    with open('pos.dat','rb') as f:
        pos1 = pickle.load(f)
        exec(f"button_{a}_{b}.configure(text=pos1[{a}][{b}])")


def check_mine(a,b):
    with open('pos.dat','rb') as f:
        pos1 = pickle.load(f)
        return 1 if pos1[a][b] == -1 else 0

def loss():
    with open('pos.dat','rb') as f:
        pos1 = pickle.load(f)
    for i in enumerate(pos1):
        for j in range(len(i[1])):
            if i[1][j]==-1:
                exec(f"button_{i[0]}_{j}.configure(image=mine)")
def show():
    with open('pos.dat','rb') as f:
        pos1 = pickle.load(f)
    for i in enumerate(pos1):
        #print(i)
        for j in range(len(i[1])):
            if i[1][j]==-1:
                check_flagged(i[0],j)

a=0 
for  j in range(20+20,800+20,50):#rows
    b=0
    for i in range(15,1500+15,50):#columns
        h=f'button_{a}_{b}'
        exec(f'global {h}')
        exec(f'{h} = Button(window,font=("Inter ExtraBold", 20 * -1,"bold"),borderwidth = 10,)')
        exec(f'{h}.place(relx=o(i),rely=p(j),width=50,height=50)')
        exec(f'{h}.bind("<Button-3>",lambda a: check_flagged({a},{b}))')
        exec(f'''def sub{a}_{b}():
    if is_flagged({a},{b}):
        pass
    else:
        if check_mine({a},{b}):
            loss()
            messagebox.showerror("Game Over","You stepped on a mine :(")
            window.destroy()
        else: 
            global foundcount,flagcount
            if foundcount == 16*30-99 and flagcount==99:
                messagebox.showinfo("Game Over","Congratulations!! You have won the game")
            write({a},{b})''')
        exec(f'{h}.configure(command=sub{a}_{b})')
        b+=1
    a+=1
show()
window.bind('<Escape>',lambda a:window.destroy())
window.attributes('-fullscreen',True)
window.mainloop()
