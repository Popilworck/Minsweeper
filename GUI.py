from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk 
import random,pickle,numpy,os
import fuckit as fr
window = Tk()
o = lambda a: a/1536
p = lambda a: a/888
flags=ImageTk.PhotoImage(Image.open(rf'{os.getcwd()}\flag.png'))
mine = ImageTk.PhotoImage(Image.open(rf'{os.getcwd()}\mine.png'))
def setup(a,b):
    pos=[]
    for i in range(a):
        pos.append([0 for i in range(b)])
    mines = random.choices([(i,j) for i in range(b) for j in range(a)],k=99)
    for i in mines:
        pos[i[1]][i[0]]=-1
    poss=numpy.array(pos)
    for i in enumerate(pos):
        #print(i)
        for j in range(len(i[1])):
            if i[1][j]==-1:
                for k in ('1','-1'):#left and right
                    exec(f"""with fr:
    if j+{k}>=0:            
        if pos[i[0]][j+{k}] !=-1:
            pos[i[0]][j+{k}]+=1
""")
                for k in ('-1','1'):#up and down
                    exec(f"""with fr:
    if i[0]+{k}>=0:
        if pos[i[0]+{k}][j]!=-1:
            pos[i[0]+{k}][j]+=1
""")            
                
                '''for k in ('-1','1'):#diagonals
                    for l in ('-1','1'):
                        exec(f"""with fr:
    if j-1>=0 and i[0]-1>=0:
        if pos[i[0]+{k}][j+{l}] !=-1:
             pos[i[0]+{k}][j+{l}] +=1
""")'''
                with fr:
                    if pos[i[0]+1][j+1] !=-1:#bottom right
                        pos[i[0]+1][j+1] +=1
                with fr:
                    if j-1>=0:
                        if pos[i[0]+1][j-1] !=-1: #bottom left
                            pos[i[0]+1][j-1]+=1
                with fr:
                    if i[0]-1>=0:
                        if pos[i[0]-1][j+1] !=-1:#top right
                            pos[i[0]-1][j+1]+=1
                with fr:
                    if i[0]-1 >=0 and j -1 >=0:# top left
                        if pos[i[0]-1][j-1] !=-1:
                            pos[i[0]-1][j-1]+=1
#    poss=numpy.array(pos)
 #   print(poss)
    with open('pos.dat','wb') as f:
        pickle.dump(pos,f)
setup(16,30)
flag=[]
for i in range(16):
    flag.append([0 for i in range(30)])
def check_flagged(a,b,img='flags'):
    if is_flagged(a,b):
        flag[a][b]=0
        exec(f"button_{a}_{b}.configure(image='')")
    else: 
        flag[a][b]=-1
        exec(f"button_{a}_{b}.configure(image={img})")
def is_flagged(a,b):
    return 1 if flag[a][b]== -1 else 0
def num(a,b):
    with open('pos.dat','rb') as f:
        pos1 = pickle.load(f)
        return ( pos1[a][b])
def write(a,b):
    exec(f"button_{a}_{b}.configure(text=num({a},{b}))")
def check_mine(a,b):
    with open('pos.dat','rb') as f:
        pos1 = pickle.load(f)
        return 1 if pos1[a][b] == -1 else 0
def test():
    with open('pos.dat','rb') as f:
        pos1 = pickle.load(f)
    for i in enumerate(pos1):
        #print(i)
        for j in range(len(i[1])):
            if i[1][j]==-1:
                check_flagged(i[0],j,img='mine')
a=0 
for  j in range(20+20,800+20,50):#rows
    b=0
    for i in range(15,1500+15,50):#columns
        h=f'button_{a}_{b}'
        exec(f'global {h}')
        exec(f'{h} = Button(window,font=("Inter ExtraBold", 20 * -1,"bold"),borderwidth = 10,)')
        exec(f'{h}.place(relx=o(i),rely=p(j),width=50,height=50)')
        exec(f'{h}.bind("<Button-3>",lambda a: check_flagged({a},{b}))')
        exec(f'''def sub{a}{b}():
    if is_flagged({a},{b}):
        pass
    else:
        if check_mine({a},{b}):
            test()
            messagebox.showerror("Game Over","You stepped on a mine :(")
            
            window.destroy()
        else: 
            write({a},{b})
             ''')
        exec(f'{h}.configure(command=sub{a}{b})')
        b+=1
    a+=1

window.bind('<Escape>',lambda a:window.destroy())
window.attributes('-fullscreen',True)
window.mainloop()
