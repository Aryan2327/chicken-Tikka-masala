import pygame

class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, img_file):
        """
        Stores data for the boss
        :param img_file : the image file
        :return none

        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(img_file), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = -60
        self.rect.y = 60
        self.speed = 1

    def update(self, screen_width):
        """
        Updates the the movement of the boss
        :param screen_width: width of the image
        :return: None
        """
        self.rect.x += self.speed

        # Get rid of boss going off screen
        if self.rect.x > screen_width:
            self.kill()


