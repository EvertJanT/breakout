import tkinter as tk
from tkinter import TclError
import time, random, sys
import numpy as np
from tkinter import IntVar

global score
score=0

class Scherm1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.title('BreakOut')
        master.geometry("250x700+400+50")
        self.logo = tk.PhotoImage(file="bricks.gif")
        self.label = tk.Label(image=self.logo).pack()
        self.button1 = tk.Button(self.frame, text = 'start', width = 25, command = self.new_window)
        self.button1.pack()
        global gebruiker_invoer1 
        gebruiker_invoer1 = 700
        label1 = tk.Label(self.frame, text='hoogte')
        label1.pack()
        self.invoerSpinner1 = tk.Spinbox(self.frame,
                                        from_=650,
                                        to=2000,
                                        increment=25,
                                        textvariable = gebruiker_invoer1,
                                        command=self.invoer,
                                        wrap=True)
        self.invoerSpinner1.pack()
        global gebruiker_invoer2 
        gebruiker_invoer2 = 500
        label2 = tk.Label(self.frame, text='breedte')
        label2.pack()
        self.invoerSpinner2 = tk.Spinbox(self.frame,
                                        from_=450,
                                        to=2000,
                                        increment=25,
                                        textvariable = gebruiker_invoer2,
                                        command=self.invoer,
                                        wrap=True)
        self.invoerSpinner2.pack()
        global gebruiker_invoer3
        gebruiker_invoer3 = 2.0
        label3 = tk.Label(self.frame, text='snelheid')
        label3.pack()
        self.invoerSpinner3 = tk.Spinbox(self.frame,
                                        from_=1.0,
                                        to=8.0,
                                        increment=0.5,
                                        textvariable = gebruiker_invoer3,
                                        command=self.invoer,
                                        wrap=True)
        self.invoerSpinner3.pack()

        self.button2 = tk.Button(self.frame, text='stop', width = 25)
        self.button2['command'] = self.button_clicked
        self.button2.pack()
        self.frame.pack()

    def invoer(self):
        global gebruiker_invoer1, gebruiker_invoer2, gebruiker_invoer3
        huidige_invoer1 = self.invoerSpinner1.get()
        huidige_invoer2 = self.invoerSpinner2.get()
        huidige_invoer3 = self.invoerSpinner3.get()
        gebruiker_invoer1 = huidige_invoer1
        gebruiker_invoer2 = huidige_invoer2
        gebruiker_invoer3 = huidige_invoer3
        
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Scherm2(self.newWindow)
    def button_clicked(self):
        self.master.destroy()

class Scherm2:
    global xpos, snelheid_bal, score
    def __init__(self, master):
        global score
        breedte = 1400
        hoogte  = 500
        hoogte = int(gebruiker_invoer1)
        breedte = int(gebruiker_invoer2)
        snelheid_bal = 1
        snelheid_bal = float(gebruiker_invoer3)

        self.master = master
        self.frame = tk.Frame(self.master)
        master.title('speelveld')
        master.geometry(str(breedte) + 'x'+ str(hoogte) + '+650+50')
        self.quitButton = tk.Button(self.frame, text = 'Stop', width = 25,
                                    command = self.close_windows)

        self.quitButton.pack()
        
        mijnCanvas = tk.Canvas(self.frame, bg="white", height=hoogte, width=breedte)
        mijnCanvas.pack()
           
        self.frame.pack()
        
            
        class Bumper:
            global xpos, score
            def __init__(self, xpos, breedte, hoogte):
                self.muis_x = 0
                self.muis_y = 0
                self.xpos = xpos
                self.y = hoogte-90
                self.width = breedte
                self.height = hoogte
                self.vorm_b = mijnCanvas.create_rectangle(xpos-40, hoogte-90, xpos+40, hoogte-80, fill='blue')

            def update_locatie(self):
                global pos_bumper, xpos
                v=5
                try:
                    richting = mijnCanvas.winfo_pointerx() 
                except TclError:
                    sys.exit()
                    pass
                pos_bumper = mijnCanvas.coords(self.vorm_b)
                self.muis_x=0
                    
                if richting <650+breedte/2-50:
                    self.muis_x=-v
                if richting > 650+breedte/2+50:
                    self.muis_x=v
                if pos_bumper[2] > (breedte-10):
                    self.muis_x = -v
                if pos_bumper[0] < 10:
                    self.muis_x = v
                mijnCanvas.move(self.vorm_b, self.muis_x, self.muis_y)


        class Tile:
            kleuren = ['blue', 'red', 'green', 'yellow']
            kleuren = ["snow", "ghost white", "white smoke", "gainsboro", "floral white",
                        "old lace", "linen", "antique white", "papaya whip", "blanched almond",
                        "bisque", "peach puff", "navajo white", "moccasin", "cornsilk",
                        "ivory", "lemon chiffon", "seashell", "honeydew", "mint cream",
                        "azure", "alice blue", "lavender", "lavender blush", "misty rose",
                        "dark slate gray", "dim gray", "slate gray", "light slate gray", "gray",
                        "light grey", "midnight blue", "navy", "cornflower blue", "dark slate blue",
                        "slate blue", "medium slate blue", "light slate blue", "medium blue",
                        "royal blue", "blue", "dodger blue", "deep sky blue", "sky blue",
                         "light sky blue", "steel blue", "light steel blue", "light blue"]
            def __init__(self, x, y, width, height):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.fill = random.choice(self.kleuren)
                self.id = mijnCanvas.create_rectangle(x, y, x+width, y+height, fill=self.fill)

            def hit(self, ball):
                mijnCanvas.delete(self.id)
                # remove the tile from the canvas    

            def draw(self):
                if self.is_visible:
                    pass
                # Code to draw the tile
    
        class Ball:
            global score
            def __init__(self, x, y, radius, vx, vy):
                self.x = x
                self.y = y
                self.radius = radius
                self.vorm = mijnCanvas.create_oval(self.x-self.radius, self.y -self.radius,self.x +self.radius,self.y+self.radius, fill='green')
                self.vx = vx
                self.vy = vy

            def move(self):
                self.x += self.vx
                self.y += self.vy
                mijnCanvas.move(self.vorm, self.vx, self.vy)
            
            def check_collision_tile(self, tile):
                global score
                botsing = mijnCanvas.find_overlapping(tile.x, tile.y, tile.x+tile.width, tile.y+tile.height)
                #register = 0 
                if len(botsing) != 1 and self.y<500:
                    self.vy *= -1
                    tile.hit(self)
                    if self.y == 400:
                        score+=1
                    return 
                return False

            def handle_collision(self, tiles):
                global score
                #score +=1
                for tile in tiles:
                    if self.check_collision_tile(tile):
                        pass
                register = 0
                # Code to handle ball-tile collision, e.g., update velocity, score, etc.
                #return score

            def update_zijkanten(self):
                pos = mijnCanvas.coords(self.vorm)
                if pos[2] >= (breedte-10) or (pos[0] ) <= 10:
                    self.vx *= -1
                if pos[3] >= (hoogte-40) or (pos[1]) <= 10:
                    self.vy *= -1

            def update_bumper(self):
                global pos_bumper
                botsing = mijnCanvas.find_overlapping(pos_bumper[0], pos_bumper[1],pos_bumper[2],pos_bumper[3])
                if len(botsing) != 1:
                    self.vy *= -1


       # Create tiles
        tiles = []

        for i in range(0, 900, 80):
            for j in range(0, 300, 30):
                tile = Tile(i,j,50,20)
                tiles.append(tile)

        # Create ball
        ball = Ball(400, 400, 10, snelheid_bal,snelheid_bal)                             

        # Create bumper
        global pos_bumper
        pos_bumper = (100,100,110,110)
        bumper_x = 200
        muis_x = 200
        bumper = Bumper(bumper_x,breedte,hoogte)
        bumper.vorm_b
        

        while True:
            global reset
            reset = 0
            snelheid = 0.01
            bumper.vorm_b
            bumper.update_locatie()
            ball.move()
            ball.update_zijkanten()
            ball.update_bumper()
            for tile in tiles:
                if ball.check_collision_tile(tile):
                    ball.handle_collision(tiles)
                else:
                    pass
            ball.handle_collision(tiles)
            if ball.y > hoogte-90:
                score = score - 10
            #print(score)
            time.sleep(snelheid)
            self.frame.update()

    def close_windows(self):
        self.master.destroy()


def main(): 
    root = tk.Tk()
    app = Scherm1(root)
    root.mainloop()

if __name__ == '__main__':
    main()
