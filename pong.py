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
font = pygame.font.Font('font.ttf', 15)

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

# Game Variables
ball = pygame.Rect(display_width/2 - 8, display_height/2 - 8, 16, 16)
player = pygame.Rect(5, display_height/2 - 50, 7, 100)
opponent = pygame.Rect(display_width - 10, display_height/2 - 50, 7, 100)
ball_speed_x = 4
ball_speed_y = 4
player_speed = 0
player_2_speed = 0
opponent_speed = 6

# Sound
pong_sound1 = pygame.mixer.Sound('sound/pong_1.wav')
pong_sound2 = pygame.mixer.Sound('sound/pong_2.wav')
hit_sound = pygame.mixer.Sound('sound/hit.wav')

# Score Var
player_score = 0
opponent_score = 0

# Timer Var
score_time = True

# Functions
def ball_mechanics():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    # Pong Ball Mechanics
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= display_height:
        pong_sound1.play()
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= display_width:
        ball_start()

    # Pong Timer
    if ball.left <= 5 :
        hit_sound.play()
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    if ball.right >= display_width - 5 :
        hit_sound.play()
        player_score += 1
        score_time = pygame.time.get_ticks()

    # Pong Collide Mechanic
    if ball.colliderect(player) or ball.colliderect(opponent):
        pong_sound2.play()
        ball_speed_x *= -1

def player_mechanics():
    # player Mechanic
    player.y += player_speed
    if player.top <= 5 : 
        player.top = 5
    if player.bottom >= display_height - 5 : 
        player.bottom = display_height - 5

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
    
def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    # Timer When Ball Restarts
    current_time = pygame.time.get_ticks()
    ball.center = (display_width/2, display_height/2)

    # Timer Display
    if current_time - score_time < 700:
        number_three = font.render('3', True, light_grey)
        display.blit(number_three, (display_width/2 - 6, display_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = font.render('2', True, light_grey)
        display.blit(number_two, (display_width/2 - 6, display_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = font.render('1', True, light_grey)
        display.blit(number_one, (display_width/2 - 7, display_height/2 + 20))

    if current_time - score_time < 2100 :
        ball_speed_x = 0
        ball_speed_y = 0
    else :
        ball_speed_y = 4 * random.choice((-1,1))
        ball_speed_x = 4 * random.choice((-1,1))
        score_time = None

# Run Game
while True :
    # Input Handler
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_w:
                player_speed -= 3
            if event.key == pygame.K_s:
                player_speed += 3
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_w:
                player_speed += 3
            if event.key == pygame.K_s:
                player_speed -= 3

    # Call Out Functions
    ball_mechanics()
    player_mechanics()
    ai_mechanics()

    # Background
    display.fill(bg_color)

    # Score Visuals
    player_text = font.render(f"{player_score}", True, light_grey)
    display.blit(player_text, (290, 220))
    opponent_text = font.render(f"{opponent_score}", True, light_grey)
    display.blit(opponent_text, (335, 220))

    # Game Visuals
    pygame.draw.rect(display, light_grey, player)
    pygame.draw.rect(display, light_grey, opponent)
    pygame.draw.ellipse(display, light_grey, ball)
    pygame.draw.aaline(display, light_grey, (display_width/2, 0), (display_width/2, display_height)) 

    # Timer and Start
    if score_time :
        ball_start()
    
    # Update Window
    pygame.display.update()
    clock.tick(fps)