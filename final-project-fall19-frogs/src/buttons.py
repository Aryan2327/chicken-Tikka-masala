import pygame


class StartButton(pygame.sprite.Sprite):
    def __init__(self, img_file):
        """
        Stores data for the start button
        :param img_file: the image file for the start button
        :return None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_file)
        self.rect = self.image.get_rect()
        self.rect.y = 250
        self.rect.x = 275

class QuitButton(pygame.sprite.Sprite):
    def __init__(self, img_file):
        """
        Stores data for the quit button
        :param img_file: the image file for the quit button
        :return NOne
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_file)
        self.rect = self.image.get_rect()
        self.rect.y = 330
        self.rect.x = 110