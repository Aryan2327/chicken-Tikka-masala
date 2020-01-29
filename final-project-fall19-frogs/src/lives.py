import pygame

class Lives(pygame.sprite.Sprite):
    def __init__(self, x, y, img_file):
        """
        Stores the data for the lives of the user ship
        :param: x: the x position of the lives
        :param: y: the y position of the lives
        :param: img_file: the image of the lives
        :return: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(img_file), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
