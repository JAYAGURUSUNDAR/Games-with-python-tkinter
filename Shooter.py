import tkinter as tk
import numpy as np
import argparse


class Ball:
   def __init__(self,canvas,radius,x,y,color):
      self.__can=canvas
      self.__x=x
      self.__y=y
      self.__r=radius
      self.__c=color
      self.__id=None
      
   def draw(self):
      self.__id=self.__can.create_oval(self.__x-self.__r,self.__y-self.__r,self.__x+self.__r,self.__y+self.__r,fill=self.__c)
      return self
   
   def move(self,x,y):
      if self.__id:
         self.__can.delete(self.__id)
      self.__x=x
      self.__y=y
      self.draw()
      self.__can.update()
      
   
   def getX(self):return self.__x
   def getY(self):return self.__y
   def getRadius(self): return self.__r
   def setRadius(self,r): self.__r=r 

s=1
def accel_decel(speedx=1,speedy=1,command=None):
   global s
   if command=="a":s*=speedx
   elif command=="d":s/=speedx
   


a = tk.Tk()
a.title("simple shooter game")
c = tk.Canvas(a,width=500,height=500)
b = Ball(c,30,100,100,"red").draw()
c.grid(row=0,column=0,columnspan=2)
acc_Bt=tk.Button(a,text="accelerate",command=lambda :accel_decel(speedx=2,command="a"))
acc_Bt.grid(row=1,column=0)
dec_Bt=tk.Button(a,text="decelerate",command=lambda :accel_decel(speedx=2,command="d"))
dec_Bt.grid(row=1,column=1)
x=b.getX()
h=1
l=None
l1=None
closer=False
fix_x,fix_y=None,None
o=None
o1=None
is_shot=False
bullet_x,bullet_y=0,0
bullets=8
msg=" remaining"
msg_text=None
is_hit=False
t=0

def check_dis(ball,e):
  global closer
  color="black"
  if np.sqrt((b.getX()-e.x)**2 + (b.getY()-e.y)**2)<=b.getRadius():closer=True
  elif np.sqrt((b.getX()-e.x)**2 + (b.getY()-e.y)**2)>=b.getRadius():closer=False
c.bind("<Motion>",lambda e:check_dis(b,e))

def auto_acc():
   accel_decel(speedx=np.random.randint(1,3),command="a")
   a.after(5000,auto_acc)
   

def fix_point(e):
  global o,l1,fix_x,fix_y
  c.delete(o)
  o=c.create_oval(e.x-5,e.y-5,e.x+5,e.y+5,fill="black")
  c.update()
  fix_x,fix_y=e.x,e.y
c.bind("<B1-Motion>",fix_point)


def shoot(e):
  global is_shot,bullet_x,bullet_y,bullets,msg
  bullet_x,bullet_y=fix_x,fix_y
  bullets-=1
  if bullets==0:msg=" no more bullets"
  is_shot=True
  
a.bind("<Key-a>",shoot)
msg_text=c.create_text(150,20,text="bullets "+str(bullets)+msg)

def animate():
    global x, h, closer, is_shot, bullet_x, bullet_y, bullets, msg, msg_text, fix_x, fix_y, o, l1,o1,t
    if np.sqrt((bullet_y-b.getY())**2+(bullet_x-b.getX())**2)<=b.getRadius()+10:is_hit=True
    elif np.sqrt((bullet_y-b.getY())**2+(bullet_x-b.getX())**2)>=b.getRadius()+10:
       is_hit=False
       t=0
    if not closer:
        b.move(x, b.getY())
        if b.getX() >= 500 - b.getRadius():
            h = -1
        elif b.getX() <= b.getRadius():
            h = 1
        if fix_x and fix_y:
            c.delete(l1)
            l1 = c.create_line(fix_x, fix_y, b.getX(), b.getY(), fill="blue")
            if is_shot:
                if bullets <= 0:
                    a.unbind("<Key-a>")
                else:
                   if bullet_y>=b.getY():a.unbind("<Key-a>")
                   else:
                      a.bind("<Key-a>",shoot)
                      if is_hit and t<2:
                         t+=1
                         b.setRadius(b.getRadius()-1)
                bullet_y += -1   
                c.delete(o1)
                c.delete(msg_text)
                o1 = c.create_oval(bullet_x - 10, bullet_y - 10, bullet_x + 10, bullet_y + 10, fill="blue")
                msg_text = c.create_text(150, 20, text="bullets "+str(bullets) + msg)
        x += h * s
    elif closer:
        b.move(b.getX(), b.getY())
    a.after(10, animate)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Shooter Game, Hello from the shooter game community")
    parser.add_argument("-g", "--gui", action="store_true", help="Open the GUI")
    parser.add_argument("-dg","--disableDBT",action="store_true",help="open the GUI with disabled Decelerate Button")
    parser.add_argument("-a", "--auto_accel",action="store_true",help="automatically accelerate the balls motion after every 5 seconds")
    parser.add_argument("-ac","--add_canvas",action="store_true",help="add canvas to record your progress")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    if args.gui:
        animate()
        if args.disableDBT:
           dec_Bt.config(state="disabled")
        if args.auto_accel:
           acc_Bt.config(state="disabled")
           a.after(5000,auto_acc)
        if args.add_canvas:
           c1 = tk.Canvas(a, width=200,height=500)
           c1.grid(row=0,column=2)
        a.mainloop()
    else:
        pass 

