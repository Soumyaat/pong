# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos= [0,0]  #[WIDTH/2,HEIGHT/2]
ball_vel=[0,0]
paddle1_pos = [[0, 200], [8, 200]]
paddle2_pos = [[591, 200],[599, 200]]
paddle1_vel=0
paddle2_vel=0
score1=0
score2=0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[WIDTH/2,HEIGHT/2]
      
    if direction=="right":
       ball_vel[0] = random.randrange(2, 4)      
    else:
       ball_vel[0] = (-1)*random.randrange(2, 4) 
       
    ball_vel[1] = (-1)*random.randrange(1, 3) 


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1=0
    score2=0
    spawn_ball("right")
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    
    if (ball_pos[1]>HEIGHT-BALL_RADIUS-1):
        ball_vel[1]=-ball_vel[1]
    
    gutter_right = (ball_pos[0] >= ((WIDTH-PAD_WIDTH)-BALL_RADIUS)-1)
    gutter_left = (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH)    
    if gutter_right:
        gutter_right="F"
        spawn_ball("left")
    if gutter_left: 
        gutter_left='F'
        spawn_ball("right")
    
    # draw paddles
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], 80, "White")
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], 80, "White")
   
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[0][1] >= HALF_PAD_HEIGHT and paddle1_vel <= 0:
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
    elif paddle1_vel > 0 and paddle1_pos[0][1] <= HEIGHT - 1 - HALF_PAD_HEIGHT:
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel

    if paddle2_pos[0][1] >= HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
    elif paddle2_vel > 0 and paddle2_pos[0][1] <= HEIGHT - 1 - HALF_PAD_HEIGHT:
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
    
 
    # determine whether paddle and ball collide    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos[0][1] - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos[0][1] + HALF_PAD_HEIGHT:
            ball_vel[0] = (-1.1)*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else :
            score2 += 1
            print ball_pos[1], paddle1_pos[0][1] - HALF_PAD_HEIGHT, paddle1_pos[0][1] + HALF_PAD_HEIGHT
            spawn_ball("right")

    if ball_pos[0] >= WIDTH - 1 - BALL_RADIUS - PAD_WIDTH - 1:
        if (ball_pos[1] >= paddle2_pos[0][1] - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle2_pos[0][1] + HALF_PAD_HEIGHT):
            ball_vel[0] = (-1.1)*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else :
            score1 += 1
            print ball_pos[1], paddle2_pos[0][1] - HALF_PAD_HEIGHT, paddle2_pos[0][1] + HALF_PAD_HEIGHT
            spawn_ball("left")
    
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    # draw scores
    canvas.draw_text(str(score1),[150, 40], 30, "White")
    canvas.draw_text(str(score2),[450, 40], 30, "White")
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
      paddle1_vel = -8
    if key == simplegui.KEY_MAP["s"]:
      paddle1_vel = 8
      flag1 = True
    if key == simplegui.KEY_MAP["up"]:
      paddle2_vel = -8
    if key == simplegui.KEY_MAP["down"]:
      paddle2_vel = 8

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w" or "s"]:
      paddle1_vel = 0
    if key == simplegui.KEY_MAP["up" or "down"]:
      paddle2_vel = 0
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
