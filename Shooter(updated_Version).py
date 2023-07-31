import tkinter as tk
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

class ScoreCard(tk.Canvas):
   def __init__(self,master,width=200,height=200,enemy_name=None,shooter_name=None):
      super().__init__(master,width=width,height=height)
      self.__master = master
      self.__width = width
      self.__height = height
      self.__enemy_name = "enemy 1" if not enemy_name else enemy_name
      self.__shooter_name = "shooter 1" if not shooter_name else shooter_name
      self.__id=None
      self.__sc_text=None
      self.__score=0
      self.__text = self.create_text(width/2,height/2,text="enemy:"+self.__enemy_name+"\nshooter:"+self.__shooter_name)
   
   def design(self,x,y):
      if self.__width/2-x<=50 and  self.__height/2-y<=50:
         self.__animate_screen(x,y,"blue")
      else:
         self.__animate_screen(x,y,"yellow")
         self.after(10,lambda:self.design(x+1,y+1))
   
   def __animate_screen(self,x,y,color):
      self.delete(self.__id)
      self.delete(self.__text)
      self.delete(self.__sc_text)
      self.__id=self.create_rectangle(self.__width/2-x,self.__height/2-y,self.__width/2+x,self.__height/2+y,fill=color)
      self.__text=self.create_text(self.__width/2,self.__height/2-15-y,text="enemy:"+self.__enemy_name+"\nshooter:"+self.__shooter_name)
      self.__sc_text=self.create_text(self.__width/2,self.__height/2,text="score:"+str(self.__score))
      self.update()
   
   def put_score(self,score):
      self.__score=score
      self.delete(self.__sc_text)
      self.__sc_text=self.create_text(self.__width/2,self.__height/2,text="score:"+str(self.__score))
      self.update()

def distance(x1,y1,x2,y2):
   return ((x1-x2)**2 + (y1-y2)**2)**0.5

def accel_decel(speedx=1,speedy=1,command=None):
   global s
   if command=="a":s*=speedx
   elif command=="d":s/=speedx

def score_card_display():
   global close_score_card_Bt
   score_card1.grid(row=0,column=4)
   score_card1.design(0,0)
   display_score_Bt.config(state="disabled")
   close_score_card_Bt = tk.Button(a,text="close",command=close_score_card)
   close_score_card_Bt.grid(row=1,column=3,columnspan=2)
   

def close_score_card():
   score_card1.grid_forget()
   close_score_card_Bt.grid_forget()
   display_score_Bt.config(state="normal")
     

a = tk.Tk()
a.title("shooter game")
c = tk.Canvas(a,width=500,height=500)
score_card1=ScoreCard(a,500,500)
b = Ball(c,30,100,100,"red").draw()
c.grid(row=0,column=0)
display_score_Bt = tk.Button(a, text="display score", command=score_card_display)
display_score_Bt.grid(row=1,column=0)
x=b.getX()
s=1
score=0
enemy_life=100
shooter_life=100
h=1
l=None
closer=False
fix_x,fix_y=None,None
o=None
o1=None
is_shot=False
bullet_x,bullet_y=0,0
bullets=8
msg=" remaining"
msg_text=None
enemy_life_msg=None
is_hit=False
t=0

def check_dis(ball,e):
  global closer
  color="black"
  if distance(e.x,e.y,ball.getX(),ball.getY())<=b.getRadius():closer=True
  else:closer=False
c.bind("<Motion>",lambda e:check_dis(b,e))


def fix_point(e):
  global o,fix_x,fix_y
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
    global x, h, closer, is_shot, bullet_x, bullet_y, bullets, msg, msg_text, enemy_life_msg,enemy_life,fix_x, fix_y, o,o1,t,score
    c.delete(enemy_life_msg)
    enemy_life_msg = c.create_text(350,20,text="enemy life:"+str(enemy_life))
    if distance(b.getX(),b.getY(),bullet_x,bullet_y)<=b.getRadius()+10:is_hit=True
    elif distance(b.getX(),b.getY(),bullet_x,bullet_y)>=b.getRadius()+10:
       is_hit=False
       t=0
    if not closer:
        b.move(x, b.getY())
        if b.getX() >= 500 - b.getRadius():
            h = -1
        elif b.getX() <= b.getRadius():
            h = 1
        if fix_x and fix_y:
            if is_shot:
                if bullets <= 0:
                    a.unbind("<Key-a>")
                else:
                   if bullet_y>=b.getY():a.unbind("<Key-a>")
                   else:
                      a.bind("<Key-a>",shoot)
                      if is_hit and t<1:
                         t+=1
                         b.setRadius(b.getRadius()*0.5)
                         enemy_life-=0.5*enemy_life
                         score+=10
                         
                bullet_y -= 1   
                c.delete(o1)
                c.delete(msg_text)
                o1 = c.create_oval(bullet_x - 10, bullet_y - 10, bullet_x + 10, bullet_y + 10, fill="blue")
                msg_text = c.create_text(100, 20, text="bullets "+str(bullets) + msg)
        x += h * s
    elif closer:
        b.move(b.getX(), b.getY())
    score_card1.put_score(score)
    a.after(10, animate)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Shooter Game, Hello from the shooter game community")
    parser.add_argument("-ac","--add_canvas",action="store_true",help="add canvas to record your progress")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    animate()
    if not args.add_canvas:display_score_Bt.config(state="disabled")
    else:display_score_Bt.config(state="normal")
    a.mainloop()

