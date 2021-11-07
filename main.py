import pygame
import sys
from config import *
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./ttf/微軟正黑體.ttf", 48)
        self.running = True

        self.character_sprite_sheet = Sprite_sheet("./img/character.png")
        self.terrain_sprite_sheet = Sprite_sheet("./img/terrain.png")
        self.enemy_sprite_sheet = Sprite_sheet("./img/enemy.png")
        self.attack_sprite_sheet = Sprite_sheet("./img/attack.png")
        self.intro_background = pygame.image.load("./img/introbackground.png")
        self.go_background = pygame.image.load("./img/gameover.png")

    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            i -= 10
            for j, column in enumerate(row):
                j -= 25
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "H":
                    Hole(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):
        ''' a new game starts '''
        self.playing = True

        # ?
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.holes = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()

    def events(self):
        ''' game loop events '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y-TILESIZE)
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y+TILESIZE)
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x-TILESIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x+TILESIZE, self.player.rect.y)

    def update(self):
        ''' game loop update '''
        self.all_sprites.update()

    def draw(self):
        ''' game loop draw '''
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        ''' game loop '''
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT-60, 150, 50, WHITE, BLACK, "Restart", 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        
        title = self.font.render("蟹蟹闖天關", True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2-50))
        play_button = Button(WIN_WIDTH/2-50, WIN_HEIGHT/2-15, 100, 50, WHITE, BLACK, "Play", 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()



if __name__ == "__main__":
    g = Game()
    g.intro_screen()
    g.new()
    while g.running:
        g.main()
        g.game_over()

    pygame.quit()
    sys.exit()