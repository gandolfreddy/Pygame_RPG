import math
import pygame
import random
from config import *


class Sprite_sheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        ## important: "self._layer" instead of "self.layer"
        self._layer = PLAYER_LAYER
        # ?
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = x*TILESIZE,  y*TILESIZE
        self.width, self.height = TILESIZE, TILESIZE

        self.x_change, self.y_change = 0, 0

        self.facing = "down"
        self.animation_loop = 0

        self.image = self.game.character_sprite_sheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect(x=self.x, y=self.y)

        self.down_animations = [self.game.character_sprite_sheet.get_sprite(3, 2, self.width, self.height),
                                self.game.character_sprite_sheet.get_sprite(35, 2, self.width, self.height),
                                self.game.character_sprite_sheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.character_sprite_sheet.get_sprite(3, 34, self.width, self.height),
                              self.game.character_sprite_sheet.get_sprite(35, 34, self.width, self.height),
                              self.game.character_sprite_sheet.get_sprite(68, 34, self.width, self.height)]
  
        self.left_animations = [self.game.character_sprite_sheet.get_sprite(3, 98, self.width, self.height),
                                self.game.character_sprite_sheet.get_sprite(35, 98, self.width, self.height),
                                self.game.character_sprite_sheet.get_sprite(68, 98, self.width, self.height)]
                           
        self.right_animations = [self.game.character_sprite_sheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.character_sprite_sheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.character_sprite_sheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemies()

        self.rect.x += self.x_change
        self.collide_obstacles('x')
        self.rect.y += self.y_change
        self.collide_obstacles('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = "down"

    def collide_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_obstacles(self, direction):
        hits_blocks = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits_holes = pygame.sprite.spritecollide(self, self.game.holes, False)
        if hits_blocks or hits_holes:
            hits = hits_blocks or hits_holes
            if direction == "x":
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
            if direction == "y":
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_sprite_sheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_sprite_sheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_sprite_sheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_sprite_sheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = y*TILESIZE, y*TILESIZE
        self.width, self.height = TILESIZE, TILESIZE

        self.x_change, self.y_change = 0, 0

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_sprite_sheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect(x=self.x, y=self.y)

        self.left_animations = [self.game.enemy_sprite_sheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_sprite_sheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_sprite_sheet.get_sprite(68, 98, self.width, self.height)]
        self.right_animations = [self.game.enemy_sprite_sheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.enemy_sprite_sheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.enemy_sprite_sheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_obstacles()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change, self.y_change = 0, 0

    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"

    def animate(self):
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_sprite_sheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_sprite_sheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def collide_obstacles(self):
        hits_blocks = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits_holes = pygame.sprite.spritecollide(self, self.game.holes, False)
        if hits_blocks or hits_holes:
            hits = hits_blocks or hits_holes
            if self.facing == "left":
                self.rect.x = hits[0].rect.left - self.rect.width
                self.facing = "right"
            if self.facing == "right":
                self.rect.x = hits[0].rect.right
                self.facing = "left"


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = x*TILESIZE, y*TILESIZE
        self.width, self.height = TILESIZE, TILESIZE

        self.image = self.game.terrain_sprite_sheet.get_sprite(30*32, 14*32, self.width, self.height)
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Hole(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.holes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = x*TILESIZE, y*TILESIZE
        self.width, self.height = TILESIZE, TILESIZE

        self.image = self.game.terrain_sprite_sheet.get_sprite(32*18, 32*0, self.width, self.height)
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y= x*TILESIZE, y*TILESIZE
        self.width, self.height = TILESIZE, TILESIZE

        self.image = self.game.terrain_sprite_sheet.get_sprite(32*2, 32*11, self.width, self.height)
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("./ttf/CONSOLA.TTF", fontsize)
        self.content = content

        self.x, self.y = x, y
        self.width, self.height = width, height

        self.fg, self.bg = fg, bg

        # button background
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        
        # button text
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        return self.rect.collidepoint(pos) and pressed[0]


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_SPEED
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = x, y
        self.width, self.height = TILESIZE, TILESIZE
        
        self.animation_loop = 1

        self.image = self.game.attack_sprite_sheet.get_sprite(0, 32, self.width, self.height)
        self.rect = self.image.get_rect(x=self.x, y=self.y)

        self.down_animations = [self.game.attack_sprite_sheet.get_sprite(  0, 32, self.width, self.height),
                                self.game.attack_sprite_sheet.get_sprite( 32, 32, self.width, self.height),
                                self.game.attack_sprite_sheet.get_sprite( 64, 32, self.width, self.height),
                                self.game.attack_sprite_sheet.get_sprite( 96, 32, self.width, self.height),
                                self.game.attack_sprite_sheet.get_sprite(128, 32, self.width, self.height)]

        self.up_animations = [self.game.attack_sprite_sheet.get_sprite(  0,  0, self.width, self.height),
                              self.game.attack_sprite_sheet.get_sprite( 32,  0, self.width, self.height),
                              self.game.attack_sprite_sheet.get_sprite( 64,  0, self.width, self.height),
                              self.game.attack_sprite_sheet.get_sprite( 96,  0, self.width, self.height),
                              self.game.attack_sprite_sheet.get_sprite(128,  0, self.width, self.height)]

        self.left_animations = [self.game.attack_sprite_sheet.get_sprite(  0, 96, self.width, self.height),
                                self.game.attack_sprite_sheet.get_sprite( 32, 96, self.width, self.height),
                                self.game.attack_sprite_sheet.get_sprite( 64, 96, self.width, self.height),
                                self.game.attack_sprite_sheet.get_sprite( 96, 96, self.width, self.height),
                                self.game.attack_sprite_sheet.get_sprite(128, 96, self.width, self.height)]

        self.right_animations = [self.game.attack_sprite_sheet.get_sprite(  0, 64, self.width, self.height),
                                 self.game.attack_sprite_sheet.get_sprite( 32, 64, self.width, self.height),
                                 self.game.attack_sprite_sheet.get_sprite( 64, 64, self.width, self.height),
                                 self.game.attack_sprite_sheet.get_sprite( 96, 64, self.width, self.height),
                                 self.game.attack_sprite_sheet.get_sprite(128, 64, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing
        
        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        

        
        
        
        