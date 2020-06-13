import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Labirynt")
wn.setup(700, 700)
turtle.register_shape("player-left.gif")
turtle.register_shape("player-right.gif")
turtle.register_shape("enemy.gif")
turtle.register_shape("coin.gif")

#ŻÓŁW KTORY RYSUJE LABIRYNT
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.pu()
        self.speed(0)

#GRACZ
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("player-right.gif")
        self.color("blue")
        self.pu()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        x_cord = self.xcor()
        y_cord = self.ycor()+24
        if (x_cord, y_cord) not in walls:
            self.goto(x_cord, y_cord)

    def go_down(self):
        x_cord = self.xcor()
        y_cord = self.ycor()-24
        if (x_cord, y_cord) not in walls:
            self.goto(x_cord, y_cord)

    def go_right(self):
        x_cord = self.xcor()+24
        y_cord = self.ycor()
        self.shape("player-right.gif")
        if (x_cord, y_cord) not in walls:
            self.goto(x_cord, y_cord)

    def go_left(self):
        x_cord = self.xcor()-24
        y_cord = self.ycor()
        self.shape("player-left.gif")
        if (x_cord, y_cord) not in walls:
            self.goto(x_cord, y_cord)
    
    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2) + (b**2))
        if distance < 5:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

#NAGRODA
class Reward(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("coin.gif")
        self.color("gold")
        self.pu()
        self.gold = 100
        self.goto(x,y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

#WYJŚCIE
class Exit(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.pu()
        self.goto(x, y)

#PRZECIWNIK
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("enemy.gif")
        self.color("red")
        self.pu()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == 'up':
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0 
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() > self.ycor():
                self.direction = "up"
            elif player.ycor() < self.ycor():
                self.direction = "down"
                
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in exitPos:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])
        turtle.ontimer(self.move, t = random.randint(100, 300))
    
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def is_close(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        if distance < 75:
            return True
        else:
            return False

#Klasa do wypisywania ekranu końcowego
class EndScreen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.pu()
        self.home()
        
    def viewScreen(self, tekst):
        FONT_SIZE = 50
        FONT = ("Arial", FONT_SIZE, "bold")
        self.home()
        self.sety(-FONT_SIZE/2)
        self.write(tekst, align="center", font=FONT)
        self.hideturtle()
        screen = Screen()
        screen.exitonclick()
        
levels = [""]
#MAPA POZIOMU
level_1 = [
'XXXXXXXXXXXXXXXXXXXXXXXXX',
'XP XXXXXXX          XXXXX',
'X  XXXXXXX  XXXXXX  XXXXX',
'X       XX  XXXXXX  XXXXX',
'X       XX  XXX        XX',
'XXXXXX  XX  XXXE       XX',
'XXXXXX  XX  XXXXXX  XXXXX',
'XXXXXX  XX    XXXX  XXXXX',
'XTTXXX        XXXXT XXXXX',
'X  XXX  XXXXXXXXXXXXXXXXX',
'X         XXXXXXXXXXXXXXX',
'XT               XXXXXXXX',
'XXXXXXXXXXXX     XXXXXTTX',
'XXXXXXXXXXXXXXX  XXXXX  X',
'XXXE XXXXXXXXXX         X',
'XXXT                    X',
'XXXT        XXXXXXXXXXXXX',
'XXXXXXXXXX  XXXXXXXXXXXXX',
'XXXXXXXXXX              X',
'XXE  XXXXXT            TX',
'XX   XXXXXXXXXXXXX  XXXXX',
'XX     XXXXXXXXXXX  XXXXX',
'XX           XXX        X',
'XXXXT                   W',
'XXXXXXXXXXXXXXXXXXXXXXXXX'
]

levels.append(level_1)
walls = []
rewards = []
enemies = []
exits = []
exitPos = []

#RYSOWANIE LABIRYNTU
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            pole = level[y][x]
            screen_x = -288 + (x*24)
            screen_y = 288 - (y*24)

            if pole == 'X':
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
            if pole == 'P':
                player.goto(screen_x, screen_y)
            if pole == 'T':
                rewards.append(Reward(screen_x, screen_y))
            if pole == 'E':
                enemies.append(Enemy(screen_x, screen_y))
            if pole == 'W':
                exitPos.append((screen_x, screen_y))
                exits.append(Exit(screen_x, screen_y))

pen = Pen()
player = Player()
wn.tracer(0)
setup_maze(levels[1])
wn.tracer(1)
turtle.listen()
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
wn.tracer(0)

for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

while True:
    for reward in rewards:
        if player.is_collision(reward):
            player.gold += reward.gold
            print(f"Masz {player.gold} monet!")
            reward.destroy()
            rewards.remove(reward)

    for enemy in enemies:
        if player.is_collision(enemy):
            wn.clear()
            ending = EndScreen()
            ending.viewScreen("ZGINĄŁEŚ!")
            print("Zginąłeś")
            player.destroy()
    
    for exit in exits:
        if player.is_collision(exit):
            player.destroy()
            wn.clear()
            ending = EndScreen()
            ending.viewScreen("WYGRAŁEŚ")
            print(f"Masz {player.gold} monet!")
    wn.update()
