import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, name, x, y, img_file):
        """
        stores the data for the ship
        :param name: Name of the ship
        :param x: the x position of the ship
        :param y: the y position of the ship
        :param img_file: the image of the ship
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(img_file), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.name = name
        self.speed = 10
        self.health = 5

    def move_right(self):
        """
        moves the ship if the right arrow key is pressed
        ":param" None
        :return: None
        """
        self.rect.x += self.speed

    def move_left(self):
        """
        moves the ship if the left arrow key is pressed
        :param: None
        :return: None
        """
        self.rect.x -= self.speed

