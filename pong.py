import pygame, sys, random

# General Setup
pygame.init()
clock = pygame.time.Clock()

# Display Settings
display_width = 854
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
text_color = (200,200,200)

# Class
class Block(pygame.sprite.Sprite):
	def __init__(self,path,x_pos,y_pos):
		super().__init__()
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Player(Block):
	def __init__(self,path,x_pos,y_pos,speed):
		super().__init__(path,x_pos,y_pos)
		self.speed = speed
		self.movement = 0

	def display_constrain(self):
		if self.rect.top <= 5:
			self.rect.top = 5
		if self.rect.bottom >= display_height - 5:
			self.rect.bottom = display_height - 5

	def update(self,ball_group):
		self.rect.y += self.movement
		self.display_constrain()

class Ball(Block):
	def __init__(self,path,x_pos,y_pos,speed_x,speed_y,paddles):
		super().__init__(path,x_pos,y_pos)
		self.speed_x = speed_x * random.choice((-1,1))
		self.speed_y = speed_y * random.choice((-1,1))
		self.paddles = paddles
		self.active = False
		self.score_time = 0

	def update(self):
		if self.active:
			self.rect.x += self.speed_x
			self.rect.y += self.speed_y
			self.collisions()
		else:
			self.restart_counter()
		
	def collisions(self):
		if self.rect.top <= 0 or self.rect.bottom >= display_height:
			pygame.mixer.Sound.play(pong_sound1)
			self.speed_y *= -1

		if pygame.sprite.spritecollide(self,self.paddles,False):
			pygame.mixer.Sound.play(pong_sound2)
			collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
			if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
				self.speed_x *= -1
			if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
				self.speed_x *= -1
			if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
				self.rect.top = collision_paddle.bottom
				self.speed_y *= -1
			if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
				self.rect.bottom = collision_paddle.top
				self.speed_y *= -1

	def reset_ball(self):
		self.active = False
		self.speed_x *= random.choice((-1,1))
		self.speed_y *= random.choice((-1,1))
		self.score_time = pygame.time.get_ticks()
		self.rect.center = (display_width/2,display_height/2)
		pygame.mixer.Sound.play(hit_sound)

	def restart_counter(self):
		current_time = pygame.time.get_ticks()
		countdown_number = 3

		if current_time - self.score_time <= 700:
			countdown_number = 3
		if 700 < current_time - self.score_time <= 1400:
			countdown_number = 2
		if 1400 < current_time - self.score_time <= 2100:
			countdown_number = 1
		if current_time - self.score_time >= 2100:
			self.active = True

		time_counter = font.render(str(countdown_number),True,text_color)
		time_counter_rect = time_counter.get_rect(center = (display_width/2,display_height/2 + 50))
		pygame.draw.rect(display,bg_color,time_counter_rect)
		display.blit(time_counter,time_counter_rect)

class Opponent(Block):
	def __init__(self,path,x_pos,y_pos,speed):
		super().__init__(path,x_pos,y_pos)
		self.speed = speed

	def update(self,ball_group):
		if self.rect.top < ball_group.sprite.rect.y:
			self.rect.y += self.speed
		if self.rect.bottom > ball_group.sprite.rect.y:
			self.rect.y -= self.speed
		self.constrain()

	def constrain(self):
		if self.rect.top <= 5: self.rect.top = 5
		if self.rect.bottom >= display_height - 5: self.rect.bottom = display_height - 5

class GameManager:
	def __init__(self,ball_group,paddle_group):
		self.player_score = 0
		self.opponent_score = 0
		self.ball_group = ball_group
		self.paddle_group = paddle_group

	def run_game(self):
		# Drawing the game objects
		self.paddle_group.draw(display)
		self.ball_group.draw(display)

		# Updating the game objects
		self.paddle_group.update(self.ball_group)
		self.ball_group.update()
		self.reset_ball()
		self.draw_score()

	def reset_ball(self):
		if self.ball_group.sprite.rect.right >= display_width:
			self.opponent_score += 1
			self.ball_group.sprite.reset_ball()
		if self.ball_group.sprite.rect.left <= 0:
			self.player_score += 1
			self.ball_group.sprite.reset_ball()

	def draw_score(self):
		player_score = font.render(str(self.player_score),True,text_color)
		opponent_score = font.render(str(self.opponent_score),True,text_color)

		player_score_rect = player_score.get_rect(midleft = (display_width / 2 + 40,display_height/2))
		opponent_score_rect = opponent_score.get_rect(midright = (display_width / 2 - 40,display_height/2))

		display.blit(player_score,player_score_rect)
		display.blit(opponent_score,opponent_score_rect)

# Game Variables
player = Player('sprites/paddle.png', 10, display_height/2, 5)
opponent = Opponent('sprites/paddle.png', display_width - 10, display_height/2 - 50, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('sprites/ball.png', display_width/2, display_height/2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)

# Sound
pong_sound1 = pygame.mixer.Sound('sound/pong_1.wav')
pong_sound2 = pygame.mixer.Sound('sound/pong_2.wav')
hit_sound = pygame.mixer.Sound('sound/hit.wav')

player_score = 0
opponent_score = 0

# Run Game
while True :
    # Input Handler
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_w:
                player.movement -= player.speed
            if event.key == pygame.K_s:
                player.movement += player.speed
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_w:
                player.movement += player.speed
            if event.key == pygame.K_s:
                player.movement -= player.speed

    # Background
    display.fill(bg_color)

    # Run The Game
    game_manager.run_game()
    
    # Update Window
    pygame.display.update()
    clock.tick(fps)