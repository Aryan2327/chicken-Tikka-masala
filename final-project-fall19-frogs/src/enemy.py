import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img_file, increase_speed=0):
        """
        Stores data for the enemy class
        :param x: the x position of the enemy
        :param y: the y position of the enemy
        :param img_file: image file of the enemy
        :param increase_speed: increases the speed if the level increases
        :return: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(img_file), (15,15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.dir = 1
        self.increase_speed = increase_speed

    def update(self):
        """
        Updates the movement of the enemy
        :param: None
        :return: None
        """

        if self.rect.x > 662:
            self.rect.y += 50
            self.dir = -1
            self.speed += self.increase_speed
        elif self.rect.x < 50:
            self.rect.y += 50
            self.dir = 1
            self.speed += self.increase_speed
        self.rect.x += self.speed * self.dir
        pygame.time.delay(1)

