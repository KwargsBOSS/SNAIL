import pygame
from sys import exit
from random import randint ,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_walk_index = 0
        self.image=self.player_walk[self.player_walk_index]
        self.rect=self.image.get_rect(midbottom= (80,300))
        self.gravity=0
        self.jump=pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump.set_volume(0.01)
    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom>=300:
            self.gravity=-20
            self.jump.play()


    def apply_gravity(self):
        self.gravity+=1
        self.rect.y +=self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom=300

    def animation(self):
        if self.rect.bottom<300:
            self.image=self.player_jump
        else:
            self.player_walk_index+=0.1
            if self.player_walk_index>=len(self.player_walk):
                self.player_walk_index=0
            self.image=self.player_walk[int(self.player_walk_index)]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type =='fly':
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos=210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos=300

        self.animation_index=0
        self.image=self.frames[self.animation_index]
        self.rect=self.image.get_rect(midbottom=(randint(900,1100),y_pos))

    def animation(self):
        self.animation_index+=0.1
        if self.animation_index>=len(self.frames):
            self.animation_index=0
        self.image=self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <=-100:
            self.kill()


    def update(self):
        self.animation()
        self.rect.x-=6
        self.destroy()

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f"score: {current_time}",False,(100,100,100)).convert_alpha()
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collisions_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()
#setup
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('snail runner')
clock= pygame.time.Clock()
#world objects
sky_test= pygame.image.load('graphics/Sky.png').convert_alpha()
ground_test= pygame.image.load('graphics/ground.png').convert_alpha()
#fonts
test_font = pygame.font.Font('font/Pixeltype.ttf',60)

game_active= False
start_time=0
score=0

#group
player=pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group=pygame.sprite.Group()


#intro when game over
player_stand= pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_scaled=pygame.transform.rotozoom(player_stand,0,1.6)
player_stand_rect=player_stand_scaled.get_rect(center = (400,200))

game_name=test_font.render('SNAIL RUNNER',False,(0,0,0)).convert_alpha()
game_name_rect=game_name.get_rect(center= (400,80))

game_message=test_font.render('-- PRESS SPACE TO START RUNNING --',False,(250,100,78)).convert_alpha()
game_message_rect=game_message.get_rect(center= (400,340))

#timer
obstacles_timer=pygame.USEREVENT +1
pygame.time.set_timer(obstacles_timer,1500) #1500 is in miliseconds

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not(game_active):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active=True
                start_time = int(pygame.time.get_ticks()/1000)

        if game_active:
            if event.type == obstacles_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

    if game_active:
        screen.blit(sky_test,(0,0))
        screen.blit(ground_test,(0,300))
        score = display_score()

        #class
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        #collisions
        game_active=collisions_sprite()

    else:
        screen.fill((64,80,112))
        screen.blit(player_stand_scaled,player_stand_rect)
        screen.blit(game_name,game_name_rect)
        score_message = test_font.render(f"YOUR SCORE: {score}", False, (200, 200, 100)).convert_alpha()
        score_message_rect = score_message.get_rect(center=(400, 340))
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)

