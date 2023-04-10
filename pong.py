import pygame, sys, random

# General Setup
pygame.init()
clock = pygame.time.Clock()

# Display Settings
display_width = 640
display_height = 480
display = pygame.display.set_mode((display_width,display_height))

# Icon and Name
icon = pygame.image.load('icon.jpg')
pygame.display.set_caption('Pong')
pygame.display.set_icon(icon)

# Variables
fps = 60

# Font
font = pygame.font.Font('font.ttf', 20)

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

# Game Variables
ball = pygame.Rect(display_width/2 - 8, display_height/2 - 8, 16, 16)
player_1 = pygame.Rect(5, display_height/2 - 50, 7, 100)
opponent = pygame.Rect(display_width - 10, display_height/2 - 50, 7, 100)
ball_speed_x = 4
ball_speed_y = 4
player_1_speed = 0
player_2_speed = 0
opponent_speed = 4

# Timer
countdown_time = 3
start_timer = pygame.time.get_ticks()

# Functions
def ball_mechanics():
    global ball_speed_x, ball_speed_y

    # Pong Ball Mechanics
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= display_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= display_width:
        ball.center = (display_width/2, display_height/2)
        ball_speed_y *= random.choice((-1,1))
        ball_speed_x *= random.choice((-1,1))

    # Pong Collide Mechanic
    if ball.colliderect(player_1) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_mechanics():
    # Player_1 Mechanic
    player_1.y += player_1_speed
    if player_1.top <= 5 : 
        player_1.top = 5
    if player_1.bottom >= display_height - 5 : 
        player_1.bottom = display_height - 5

def ai_mechanics():
    # AI Mechanics
    if opponent.top < ball.y :
        opponent.top += opponent_speed
    if opponent.bottom > ball.y :
        opponent.top -= opponent_speed
    if opponent.top <= 5 : 
        opponent.top = 5
    if opponent.bottom >= display_height - 5 : 
        opponent.bottom = display_height - 5 

# Run Game
while True :
    # Input Handler
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_w:
                player_1_speed -= 5
            if event.key == pygame.K_s:
                player_1_speed += 5
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_w:
                player_1_speed += 5
            if event.key == pygame.K_s:
                player_1_speed -= 5

    # Visuals
    display.fill(bg_color)
    pygame.draw.rect(display, light_grey, player_1)
    pygame.draw.rect(display, light_grey, opponent)
    pygame.draw.ellipse(display, light_grey, ball)
    pygame.draw.aaline(display, light_grey, (display_width/2, 0), (display_width/2, display_height)) 

    # Call Out Functions
    ball_mechanics()
    player_mechanics()
    ai_mechanics()
    
    # Update Window
    pygame.display.update()
    clock.tick(fps)