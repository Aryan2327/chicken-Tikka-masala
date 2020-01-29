import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        """
        Stores data for the bullet class
        :param: None
        :return None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 10])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        """
        updates the movement of the bullet
        :param: None
        :return: None
        """
        self.rect.y -= self.speed

        # Get rid of bullet moving above screen

        if self.rect.y < 0:
            self.kill()

