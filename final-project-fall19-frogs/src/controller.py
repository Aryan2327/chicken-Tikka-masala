import sys
import pygame
import random
import json
from src import bullet
from src import ship
from src import enemy
from src import buttons
from src import lives
from src import enemy_bullet
from src import boss_enemy


class Controller:
    def __init__(self, width= 712, height= 600):
        """
        Initializes all sprites needed for the games and sets up the game.
        :param width(int): Width of the screen
        :param height(int): Height of the screen
        :return None
        """
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.menu_background = pygame.image.load("assets/BattleFrog_titlescreen.png")
        self.game_background = pygame.image.load("assets/background.png")
        self.lose_background = pygame.image.load("assets/end_screen.png")
        self.win_background = pygame.image.load("assets/victoryroyale.png")

        self.start_button = buttons.StartButton("assets/startbutton.jpg")
        self.quit_button = buttons.QuitButton("assets/quitbutton.png")
        self.exit2_button = buttons.QuitButton("assets/exit2button.png")

        # Initialize score
        self.score = 0
        self.multiplier = 1

        # Initialize the ship
        self.ship = ship.Ship("Pepe", 310, 520, "assets/ship.jpg")

        # Add bullets to the sprite group
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Generates the rows of enemies
        self.enemies = pygame.sprite.Group()
        self.group1, self.group2, self.group3 = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

        self.create_enemies(0, 10)

        self.enemies.add(self.group1, self.group2, self.group3)
        self.enemies_copy1 = self.enemies.copy()

        # Create lives
        self.lives = pygame.sprite.Group()
        for i in range(self.ship.health):
            self.lives.add(lives.Lives(30 * i, 10, 'assets/ship.jpg'))

        # Create boss
        self.boss_enemy = boss_enemy.BossEnemy('assets/boss_enemy.jpg')

        # Begin on level 1
        self.level = 1

        self.all_sprites = pygame.sprite.Group((self.ship,) + tuple(self.enemies) + tuple(self.lives))

        # Immediately go to menu screen
        self.state = "MENU"

    def create_enemies(self, increase_speed, num_enemies):
        """
        Creates the enemies and sets up their positions in the game.
        :param increase_speed(int): Increases the speed by a factor of x
        :param num_enemies(int): Number of enemies per row
        :return: None
        """
        x_pos = 60
        y_pos = 100
        for i in range(2):
            for j in range(num_enemies):
                self.group1.add(enemy.Enemy(x_pos, y_pos, "assets/enemy.jpg", increase_speed))
                x_pos += 50
            y_pos += 50
            x_pos = 60

        for i in range(2):
            for j in range(num_enemies):
                self.group2.add(enemy.Enemy(x_pos, y_pos, "assets/enemy.jpg", increase_speed))
                x_pos += 50
            y_pos += 50
            x_pos = 60

        for i in range(2):
            for j in range(num_enemies):
                self.group3.add(enemy.Enemy(x_pos, y_pos, "assets/enemy.jpg", increase_speed))
                x_pos += 50
            y_pos += 50
            x_pos = 60

    def next_level(self, current_level):
        """
        Resets the sprites in order to set up for the next level.
        :param current_level(int): Defines which level the user is currently on
        :return: None
        """
        self.ship = ship.Ship("Pepe", 310, 520, "assets/ship.jpg")

        self.enemies = pygame.sprite.Group()
        self.group1, self.group2, self.group3 = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

        if current_level == 2:
            self.create_enemies(1, 10)
        elif current_level == 3:
            self.create_enemies(1, 12)

        self.enemies.add(self.group1, self.group2, self.group3)

        self.lives = pygame.sprite.Group()
        for i in range(self.ship.health):
            self.lives.add(lives.Lives(30 * i, 10, 'assets/ship.jpg'))

        self.boss_enemy = boss_enemy.BossEnemy('assets/boss_enemy.jpg')

        self.all_sprites = pygame.sprite.Group((self.ship,) + tuple(self.enemies) + tuple(self.lives))

    def mainloop(self):
        """
        Determines the state and enters the respective loop.
        :param: None
        :return: None
        """
        while True:
            if self.state == "GAME":
                self.gameloop()
            elif self.state == "LOSE":
                self.lose_loop()
            elif self.state == "WIN":
                self.win_loop()
            elif self.state == "MENU":
                self.menuloop()

    def menuloop(self):
        """
        Creates an interactive menu screen.
        :param: None
        :return: None
        """
        pygame.mixer.music.load("assets/sounds/menu_song.ogg")
        pygame.mixer.music.play()
        while self.state == "MENU":
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    if self.start_button.rect.collidepoint(event.pos):
                        self.state = "GAME"
                    elif self.quit_button.rect.collidepoint(event.pos):
                        sys.exit()
            self.screen.blit(self.menu_background, (0, 0))
            self.screen.blit(self.start_button.image, self.start_button.rect)
            self.screen.blit(self.quit_button.image, self.quit_button.rect)

            json_file = open('assets/highscore.json', 'r')
            my_data = json.load(json_file)

            font = pygame.font.SysFont(None, 30, True)
            high_score = font.render("High Score: " + str(my_data["High Score"]), False, (255, 255, 255))
            self.screen.blit(high_score, (self.width / 2 - 100, 50))
            pygame.display.flip()

    def gameloop(self):
        """
        Runs the game.
        :param: None
        :return: None
        """
        pygame.key.set_repeat(1, 50)
        clock = pygame.time.Clock()
        while self.state == "GAME":

            # Pressing the keys
            for event in pygame.event.get():
                self.screen.blit(self.game_background, (0, 0))
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.ship.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.ship.move_right()
                    elif event.key == pygame.K_SPACE:
                        if len(self.bullets) < 5:
                            pygame.mixer.music.load("assets/sounds/Shooting.ogg")
                            pygame.mixer.music.play()
                            b = bullet.Bullet()
                            b.rect.x, b.rect.y = self.ship.rect.centerx, self.ship.rect.centery
                            self.bullets.add(b)

            # check for all kinds of collisions
            enemy_hits = pygame.sprite.groupcollide(self.enemies, self.bullets, dokilla=True, dokillb=True)
            ship_hits = pygame.sprite.spritecollide(self.ship, self.enemy_bullets, True)
            ship_enemy_collisions = pygame.sprite.spritecollide(self.ship, self.enemies, True)
            boss_hits = pygame.sprite.spritecollide(self.boss_enemy, self.bullets, True)

            if boss_hits:
                pygame.mixer.music.load("assets/sounds/Explosion.ogg")
                pygame.mixer.music.play()
                self.boss_enemy.kill()
                self.multiplier += 1

            for hit in enemy_hits:
                pygame.mixer.music.load("assets/sounds/Explosion.ogg")
                pygame.mixer.music.play()
                self.score += 100 * self.multiplier

            if ship_hits or ship_enemy_collisions:
                pygame.mixer.music.load("assets/sounds/Damaged.ogg")
                pygame.mixer.music.play()
                lives = self.lives.sprites()
                lives[-1].kill()
                self.ship.health -= 1
                if self.ship.health == 0:
                    self.state = "LOSE"

            # Create movement for the enemy groups (try to make delay)
            self.group1.update()
            self.group2.update()
            self.group3.update()

            # Enemies randomly fire
            if len(self.enemies) < 20:
                chance = 100
            else:
                chance = 10
            if random.randrange(0, chance) == 0:
                all_enemies = self.enemies.sprites()
                try:
                    random_enemy = random.choice(all_enemies)
                except IndexError:
                    pass
                else:
                    enemy_b = enemy_bullet.EnemyBullet()
                    enemy_b.rect.center = random_enemy.rect.center
                    self.enemy_bullets.add(enemy_b)

            # Accessing the number of sprites
            if len(self.enemies) == 31:
                self.all_sprites.add(self.boss_enemy)
                if random.randrange(0, 5) == 5:
                    boss_enemy_b = enemy_bullet.EnemyBullet()
                    boss_enemy_b.rect.center = self.boss_enemy.rect.center
                    self.enemy_bullets.add(boss_enemy_b)

            if len(self.enemies) == 0:
                if self.level == 3:
                    self.state = "WIN"
                else:
                    self.level += 1
                    self.next_level(self.level)

            # Update sprites
            self.bullets.update()
            self.enemy_bullets.update(self.height)

            if len(self.enemies) < 31:
                self.boss_enemy.update(self.width)

            self.screen.blit(self.game_background, (0, 0))

            # display score
            font = pygame.font.SysFont(None, 30, True)
            score = font.render('Score:' + str(self.score), False, (255, 255, 255))
            level = font.render('Level:' + str(self.level), False, (255, 255, 255))
            self.screen.blit(score, (self.width - 200, self.height - 570))
            self.screen.blit(level, (300, 10))

            self.bullets.draw(self.screen)
            self.enemy_bullets.draw(self.screen)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

    def lose_loop(self):
        """
        Displays the "gameover" screen when the player loses
        :param: None
        :return: None
        """
        # Display new screen over here: "Game Over..."
        self.ship.kill()
        self.screen.blit(self.lose_background, (0,0))

        json_file = open('assets/highscore.json', 'r')
        my_data = json.load(json_file)
        if self.score > my_data["High Score"]:
            my_data["High Score"] = self.score
        json_file.close()

        json_file = open('assets/highscore.json', 'w')
        json.dump(my_data, json_file)
        json_file.close()

        font = pygame.font.SysFont(None, 60, True)
        your_score = font.render("Your Score: " + str(self.score), False, (0, 0, 0))

        self.screen.blit(your_score, (200, 500))
        self.screen.blit(self.exit2_button.image, self.exit2_button.rect)

        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    if self.exit2_button.rect.collidepoint(event.pos):
                        sys.exit()

    def win_loop(self):
        """
        Displays the ending screen when the player wins.
        :param: None
        :return: None
        """
        self.ship.kill()
        self.screen.blit(self.win_background, (0, 0))

        json_file = open('assets/highscore.json', 'r')
        my_data = json.load(json_file)
        if self.score > my_data["High Score"]:
            my_data["High Score"] = self.score
        json_file.close()

        json_file = open('assets/highscore.json', 'w')
        json.dump(my_data, json_file)
        json_file.close()

        font = pygame.font.SysFont(None, 30, True)
        your_score = font.render("Your Score:" + str(self.score), False, (0, 0, 0))

        self.screen.blit(your_score, (200, 500))
        self.screen.blit(self.exit2_button.image, self.exit2_button.rect, (250, 600))

        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    if self.exit2_button.rect.collidepoint(event.pos):
                        sys.exit()

