import pygame as pg
import sys
# accesses the data from other files in the project
from os import path
from Settings import *
from Sprites import *
from Utils import *



# the game class that will be instantiated in order to run the game...
class Game:
    def __init__(self):
        pg.init()
        # setting up pygame screen using tuple value for width height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.game_cooldown = Cooldown(5000)
        self.levels = ['level1.txt', 'level2.txt', 'level3.txt']
        self.current_level = 0

    
    # a method is a function tied to a Class
# path: has all these thing stored and we can use it acess directories and load data
    def load_data(self, map):
        # allows images to be generated
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.wall_img = pg.image.load(path.join(self.img_dir, 'Wall.png')).convert_alpha()
        self.Player_img = pg.image.load(path.join(self.img_dir, 'sprite_sheet.png')).convert_alpha()
        self.Mob_img = pg.image.load(path.join(self.img_dir, 'Mob_Sprite.png')).convert_alpha()
        self.map = Map(path.join(self.game_dir, map))
                    
    def next_level(self, map):
        # deletes all objects so they don't appear in the next level
        for w in self.all_walls:
            w.kill()
        for m in self.all_mobs:
            m.kill()
        for p in self.all_powerups:
            p.kill()
        self.player.kill()
        self.load_data(map)
        # builds the level
        # loops through every tile type on the map and creates the sprites
        for row, tiles in enumerate(self.map.data):
            # assigns a symbol for each object and generates said object when it detects the symbol
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)

    def new(self):
        self.load_data(self.levels[0])
        # builds the level
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                     # call class constructor without assiging variable...when
                     Wall(self, col, row)
                if tile == 'P':
                     self.player = Player(self, col, row)
                if tile == 'M':
                     Mob(self, col, row)
                    
        self.run()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events() # input
            self.update() # game logic
            self.draw() # render

    def events(self):
        # detects all key presses and if it is running
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                print("i can get mouse input")
                print(event.pos)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_k:
                    print("i can determine when keys are pressed")
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_k:
                    print("i can determine when keys are released")
    


    def quit(self):
        pass

    def update(self):
        # changes levels, doesn't work for now
        self.all_sprites.update()
        if len(self.all_mobs) == 0:
            self.current_level +=1
            if self.current_level < len(self.levels)-1:
                self.current_level = 0
            else:
                self.next_level(self.levels[self.current_level])
                

    
    def draw(self):
        self.screen.fill(BROWN)
        # self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        # self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()


pg.quit()
