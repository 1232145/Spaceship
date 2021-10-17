import pygame
from random import randint, choice
from pygame.constants import KEYDOWN

pygame.init()

#fps
clock = pygame.time.Clock()
fps = 60 

#settings
rows = 15
cols = 5
score = 0
level = ""
press = "PRESS 'E' or 'N' or 'H' or 'V' to set difficulty and play"
ending = "You survive. Press 'Esc' to exit the game"

#game window
screen_width = 850
screen_height = 850

#colors
red = (255, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)

#text display
font = pygame.font.Font(None , 40)
line = pygame.font.Font(None, 23)
instruct = pygame.font.Font(None, 35)

def display_level(x, y):
	displayLv = font.render("Difficulty: " + str(level), True, white)
	screen.blit(displayLv, (x, y))
def display_score(x, y):
	point = font.render("Scores: " + str(score), True, white)
	screen.blit(point, (x, y))
def display_text(x, y):
	text = line.render("Press 'Esc' to quit the game", True, white)
	screen.blit(text, (x, y))
def display_pause(x, y):
	toPause = line.render("'P' to pause the game", True, white)
	screen.blit(toPause, (x, y))
def display_shoot(x, y):
	toShoot = line.render("'Spacebar' to shoot", True, white)
	screen.blit(toShoot, (x, y))
def display_play(x, y):
	displayChangeLv = instruct.render(str(press), True, white)
	screen.blit(displayChangeLv, (x, y))
def display_end(x, y):
	end = instruct.render(str(ending), True, white)
	screen.blit(end, (x, y))
def display_lose(x, y):
	losing = instruct.render("You lose. Press 'Esc' to exit the game", True, white)
	screen.blit(losing, (x, y))

#screen display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('First Game!')

#background images
background_img = pygame.image.load('Project/img/123.jpg')

#function for drawing background
def draw_bg():
	screen.blit(background_img, (0,0))

#Player
class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Project/img/rsz_2copy.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
		self.shot = pygame.time.get_ticks()

	def movement(self):
		speed = 6.75 #movement speed
		cooldown = 275 #attack speed, decrease = faster
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += speed
		if key[pygame.K_UP] and self.rect.top > 0:
			self.rect.y -= speed
		if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
			self.rect.y += speed
		cool_down = pygame.time.get_ticks()
		if key[pygame.K_SPACE] and cool_down - self.shot > cooldown:
			bullet = ammo(self.rect.centerx, self.rect.top)
			bullet_group.add(bullet)
			self.shot = cool_down
		
		#hitbox(ignore transparent background)
		self.mask = pygame.mask.from_surface(self.image)

	#drawing health
	def update(self):
		#draw on "screen", color "red", cordinate ( X, bottomshipY + 10), (width, length)
		pygame.draw.rect(screen, red, (self.rect.x, self.rect.bottom + 10, self.rect.width, 15))
		#override the color red with green
		if self.health_remaining > 0:
			#health_remaining/health_start < 1 if health_remaining - value
			pygame.draw.rect(screen, green, (self.rect.x, self.rect.bottom + 10, int(self.rect.width * (self.health_remaining / self.health_start)), 15))

#Player_bullet											
class ammo(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Project/img/ammo_a.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
	
	def update(self):
		self.rect.y -= 10
		#checking if player bullet collide with objects
		if pygame.sprite.spritecollide(self, enemies_group, True):
			self.kill()
			global score
			if Player.health_remaining <= 0:
				score += 0
			else:
				if level == 'easy':
					score += 20
				if level == 'normal':
					score += 40
				if level == 'hard':
					score += 60
				if level == 'veteran':
					score += 80
			if Player.health_remaining > 0:
				Player.health_remaining += 0.2
		#eliminate bullets ouside the screen
		if self.rect.bottom < 0:
			self.kill()

#enemies
class enemies(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Project/img/enemy_' + str(randint(1, 3)) + '.png') 
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move = 1
		#count the number of step that enemies move
		self.move_counter = 0
		
	def update(self):
		global score
		if Player.health_remaining > 0 and level != "":
			self.rect.x += self.move
		else:
			self.rect.x += 0
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			#changing direction of X by multiplying with -1
			self.move *= -1
			#enemies spawn from the middle, move 75 pixel to the right and 150 pixel to the left and repeat
			self.move_counter *= self.move
			if Player.health_remaining <= 0 or level == "":
				self.rect.y += 0
			else:
				self.rect.y += 15
		if self.rect.y > screen_height:
			self.kill()
			score -= 100

#enemies_bullet
class enemies_ammo(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		if level == 'easy' or level == 'normal':
			self.image = pygame.image.load('Project/img/ammo_1.png')
		if level == 'veteran' or level == 'hard':
			self.image = pygame.image.load('Project/img/ammo_2.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
	
	def update(self):
		if Player.health_remaining <= 0:
			self.rect.y += 0
		else:
			if level == 'easy':
				self.rect.y += 5.25
			if level == 'normal':
				self.rect.y += 5.75
			if level == 'hard':
				self.rect.y += 6.25
			if level == 'veteran':
				self.rect.y += 6.75
		if pygame.sprite.spritecollide(self, Player_group, False, pygame.sprite.collide_mask):
			if level == 'easy':
				#7 hits kill
				Player.health_remaining -= 0.45
			if level == 'normal':
				#6 hits kill
				Player.health_remaining -= 0.5
			if level == 'hard':
				#5 hits kill
				Player.health_remaining -= 0.6
			if level == 'veteran':
				#4 hits kill
				Player.health_remaining -= 0.725
			self.kill()
		if self.rect.top > screen_height:
			self.kill()

#container
Player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
enemies_bullet_group = pygame.sprite.Group()

#generate enemy
def create_enemy():
	for y in range(rows):
		for x in range(cols):
			#spawnpoint = (corX + distance between corX, corY + distance between corY)
			enemy = enemies(125 + x * 150, -2500 + y * 125)
			enemies_group.add(enemy)
create_enemy()

#enemy shoot
def enemy_shoot():
	#time recorded from the beginning
	start_time = pygame.time.get_ticks()
	if level == 'easy':
		if start_time > 1000 and len(enemies_bullet_group) < 30  and len(enemies_group) > 0:
			#randomly choose an enemy in the sprite_group to shoot
			enemy_attack = choice(enemies_group.sprites())
			#draw enemy bullet
			enemy_shot = enemies_ammo(enemy_attack.rect.centerx, enemy_attack.rect.bottom)
			enemies_bullet_group.add(enemy_shot)
	if level == 'normal':
		if start_time > 1000 and len(enemies_bullet_group) < 50  and len(enemies_group) > 0:
			enemy_attack = choice(enemies_group.sprites())
			enemy_shot = enemies_ammo(enemy_attack.rect.centerx, enemy_attack.rect.bottom)
			enemies_bullet_group.add(enemy_shot)		
	if level == 'hard':
		#if there is one enemy left, they shoot like a minigun!!
		if start_time > 1000 and len(enemies_bullet_group) < 65  and len(enemies_group) > 0:
			enemy_attack = choice(enemies_group.sprites())
			enemy_shot = enemies_ammo(enemy_attack.rect.centerx, enemy_attack.rect.bottom)
			enemies_bullet_group.add(enemy_shot)
	if level == 'veteran':
		if start_time > 1000 and len(enemies_bullet_group) < 75  and len(enemies_group) > 0:
			enemy_attack = choice(enemies_group.sprites())
			enemy_shot = enemies_ammo(enemy_attack.rect.centerx, enemy_attack.rect.bottom)
			enemies_bullet_group.add(enemy_shot)			

#create Player
Player = Player(int(screen_width/2), screen_height - 100, 3)
Player_group.add(Player)

#Pausing
def pause():
	#something is wrong here but still works as intended??
	pause = True
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == KEYDOWN:
				if event.key == pygame.K_p:
					pause = False
				if event.key == pygame.K_ESCAPE:
					pygame.quit()

#main function
def main():
	run = True
	while run:
		
		clock.tick(fps)
		#draw background
		draw_bg()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
			if event.type == KEYDOWN:
				global level
				global press
				if event.key == pygame.K_ESCAPE:
					run = False
				if event.key == pygame.K_p:
					pause()
				if event.key == pygame.K_e:
					level = 'easy'
					press = ""
				if event.key == pygame.K_n:
					level = 'normal'
					press = ""
				if event.key == pygame.K_h:
					level = 'hard'
					press = ""
				if event.key == pygame.K_v:
					level = 'veteran'
					press = ""
		
		#End the game if player loses all health or all enemies are destroyed
		if Player.health_remaining <= 0:
			display_lose(screen_height/2 - 220, screen_width/2 - 80)
		if len(enemies_group) <= 0:
			display_end(screen_height/2 - 240, screen_width/2 - 90)

		#check if Player collide with enemies_group
		if pygame.sprite.spritecollide(Player, enemies_group, True):
			if level == 'easy':
				Player.health_remaining -= 1
			if level == 'normal':
				Player.health_remaining -= 2
			if level == 'hard':
				Player.health_remaining -= 3
			if level == 'veteran':
				Player.health_remaining -= 4

		Player.update()
		Player.movement()
		Player_group.draw(screen)

		bullet_group.draw(screen)
		bullet_group.update()
		
		enemies_group.update()
		enemies_group.draw(screen)

		enemies_bullet_group.update()
		enemies_bullet_group.draw(screen)
		enemy_shoot()

		display_score(10, 50)
		display_level(10, 10)
		display_text(screen_height - 210, 10)
		display_pause(screen_height - 165, 30)
		display_shoot(screen_height - 165, 50)
		display_play(screen_height/2 - 285, screen_width/2 - 80)

		pygame.display.update()
		
if __name__ == "__main__":
	main()