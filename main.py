from tkinter import *
from random import choice
from time import perf_counter

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#62db2d"
FOOD_COLOR = "#f92a2a"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append((0, 0))

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        # Creating a list with all coordinates for given hieght and width 
        # and finding spaces without snake in it
        # This is done in order to prevent food appearing inside the body of a snake
        all_coord = []
        for i in range(GAME_WIDTH//SPACE_SIZE):
            for j in range(GAME_HEIGHT//SPACE_SIZE):
                all_coord.append((i * SPACE_SIZE, j * SPACE_SIZE))

        empty_space = set(all_coord).difference(set(snake.coordinates))
        self.coordinates = choice(list(empty_space))

        x = self.coordinates[0]
        y = self.coordinates[1]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")

        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

# Adding timer so that snake won't turn left-right, up-down if user puts 
# multiple command before next_turn() is finished i.e. down-left (heading right) under 100 ms
last_dir = 0
def change_direction(new_direction):
    global last_dir
    global direction

    if new_direction == "left":
        if direction != "right" and perf_counter() - last_dir >= SPEED/1000:
            direction = new_direction
            last_dir = perf_counter()
            
    elif new_direction == "right":
        if direction != "left" and perf_counter() - last_dir >= SPEED/1000:
            direction = new_direction
            last_dir = perf_counter()

    elif new_direction == "up":
        if direction != "down" and perf_counter() - last_dir >= SPEED/1000:
            direction = new_direction
            last_dir = perf_counter()

    elif new_direction == "down":
        if direction != "up" and perf_counter() - last_dir >= SPEED/1000:
            direction = new_direction
            last_dir = perf_counter()
    
def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2,font=("Consolas", 50), text="GAME OVER", fill="red")
    canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2 + 50,font=("Consolas", 20), text="press R to restart", fill="red")

    global game
    game = False

def restart():
    global game
    if game == False:
        canvas.delete(ALL)

        global direction
        direction = "right"

        global snake
        global food
        snake = Snake()
        food = Food()
        next_turn(snake,food)

        global score
        score = 0
        label.config(text=f"Score: {score}")

        game = True

window = Tk()

window.title("Snake Game")
window.iconbitmap("snake_icon.ico")
window.resizable(False, False)

score = 0
direction = "right"

label = Label(window, text=f"Score: {score}", font=("Consolas, 20"))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Centers window on the screen excluding titlebar
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
titlebar_height = window.winfo_rooty() - window.winfo_y()
x = int((screen_width/2 - window_width/2))
y = int((screen_height/2 - window_height/2 - titlebar_height))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Right>", lambda event: change_direction("right"))

window.bind("<w>", lambda event: change_direction("up"))
window.bind("<a>", lambda event: change_direction("left"))
window.bind("<s>", lambda event: change_direction("down"))
window.bind("<d>", lambda event: change_direction("right"))

window.bind("<r>", lambda event: restart())
window.bind("<р>", lambda event: restart())

snake = Snake()
food = Food()
next_turn(snake,food)

window.mainloop()