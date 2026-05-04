import pygame as pg
from pygame.sprite import Sprite
from Settings import *
from Utils import *
from os import path

vec = pg.math.Vector2
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
    
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collided = pg.sprite.collide_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y': 
        hits = pg.sprite.spritecollide(sprite, group, False, collided = pg.sprite.collide_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_players
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_image()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        self.jumping = False
        self.walking = False
        self.last_update = 0
        self.current_frame = 0
        if self.spritesheet:
            self.load_image()
        else:
            self.standing_frames = [self.image]
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_p]:
            p = Projectile(self.game, self.pos.x, self.pos.y, vec(1,1))
            p = Projectile(self.game, self.pos.x, self.pos.y, vec(0,-1))
            p = Projectile(self.game, self.pos.x, self.pos.y, vec(-1,1))
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
    def load_image(self):
        self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE,TILESIZE), self.spritesheet.get_image(TILESIZE,0,TILESIZE,TILESIZE)]
        self.death_frame = [self.spritesheet.get_image(TILESIZE*2,0,TILESIZE,TILESIZE), self.spritesheet.get_image(TILESIZE*3,0,TILESIZE,TILESIZE)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)
        # for frame in self.moving_frames:
        #     frame.set_colorkey(BLACK)
    # def animate(self): #GIF
    #     now = pg.time.get_ticks()
    #     if not self.jumping and not self.walking:
    #         if now - self.last_update > 350:
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #             bottom = self.rect.bottom
    #             self.image = self.standing_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom
    def state_check(self):
        if self.vel != vec(0,0):
            self.moving = True
        else: 
            self.moving = False
    def update(self):
        self.get_keys()
        self.state_check()
        #self.animate()
        # when it collides with a wall, it pushes it back
        self.rect.center = self.pos 
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, True) # dies if it hits a mob, got help from ChatGPT
        if hits:
            self.kill()
            self.game.game_over = True
            pg.quit

# This function checks for x and y collisions in sequence and sets the position 


# enemies
class Mob(Sprite): #Elm Leaf Beetle
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Mob_Sprite.png"))
        self.load_image()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = PLAYER_SPEED * 50
        self.hit_rect = PLAYER_HIT_RECT 
        self.pricked = 0
    def update(self):
        direction = self.game.player.pos - self.pos
        # normalize keeps the speed consistently at one as otherwise, the speed would depend on the distance from the player
        if direction.length() != 0:
            direction = direction.normalize()
        self.vel = direction * self.speed * self.game.dt

        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        insect_pin = hits = pg.sprite.spritecollide(self, self.game.all_projectiles, True) # help from ChatGPT
        if insect_pin: 
            self.pricked += 1
            if self.pricked >= 20:
                self.kill()
        self.rect.center = self.pos
    def load_image(self):
        self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE,TILESIZE), self.spritesheet.get_image(TILESIZE,0,TILESIZE,TILESIZE)]
        #self.moving_frames = [self.spritesheet.get_image(TILESIZE*2,0,TILESIZE,TILESIZE), self.spritesheet.get_image(TILESIZE*3,0,TILESIZE,TILESIZE)]

class Snail(Sprite): #Garden Snail
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Snail_Sprite.png"))
        self.load_image()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = PLAYER_SPEED * 25
        self.hit_rect = PLAYER_HIT_RECT 
        self.pricked = 0
    def update(self):
        direction = self.game.player.pos - self.pos
        # normalize keeps the speed consistently at one as otherwise, the speed would depend on the distance from the player
        if direction.length() != 0:
            direction = direction.normalize()
        self.vel = direction * self.speed * self.game.dt

        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        insect_pin = hits = pg.sprite.spritecollide(self, self.game.all_projectiles, True) # help from ChatGPT
        if insect_pin: 
            self.pricked += 1
            if self.pricked >= 40:
                self.kill()
        self.rect.center = self.pos
    def load_image(self):
        self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE,TILESIZE), self.spritesheet.get_image(TILESIZE,0,TILESIZE,TILESIZE)]

class Butterfly(Sprite): #Small White
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "Butterfly_Sprite.png"))
        self.load_image()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = PLAYER_SPEED * 25
        self.hit_rect = PLAYER_HIT_RECT 
        self.pricked = 0
    def update(self):
        direction = self.game.player.pos - self.pos
        # normalize keeps the speed consistently at one as otherwise, the speed would depend on the distance from the player
        if direction.length() != 0:
            direction = direction.normalize()
        self.vel = direction * self.speed * self.game.dt

        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        
        # self.hit_rect.centerx = self.pos.x
        # collide_with_walls(self, self.game.all_walls, 'x')
        # self.hit_rect.centery = self.pos.y
        # collide_with_walls(self, self.game.all_walls, 'y')
        insect_pin = hits = pg.sprite.spritecollide(self, self.game.all_projectiles, True) # help from ChatGPT
        if insect_pin: 
            self.pricked += 1
            if self.pricked >= 20:
                self.kill()
        self.rect.center = self.pos
    def load_image(self):
        self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE,TILESIZE), self.spritesheet.get_image(TILESIZE,0,TILESIZE,TILESIZE)]

# objects
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        # self.image = pg.Surface((TILESIZE, TILESIZE ))
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        pass
 


class Projectile(Sprite):
    def __init__(self, game, x, y, vel):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/2, TILESIZE/2))
        self.image.fill(LEAF_GREEN)
        self.rect = self.image.get_rect()
        self.vel = vel 
        self.pos = vec(x,y)
        self.speed = 500
        self.rect.center = self.pos
    def update(self):
        self.pos += self.vel * self.speed * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.all_walls): # deletes itself if it collides with a wall
            self.kill()
    
#Mob ideas:
# Elm Leaf Beetle - generic enemy that chases player
# Garden Snail - slower but more health
# Small White - bypass walls but less health
# Mediterranean Mantis - Boss that can rush forward and can also bypass walls, but takes longer to bypass them