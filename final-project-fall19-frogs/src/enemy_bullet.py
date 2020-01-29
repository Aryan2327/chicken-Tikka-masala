import pygame

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self):
        """
        Stores the enemy bullet data
        :param: None
        :return: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 10])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self, height_of_screen):
        """
        Updates the movement of the bullet
        :param height_of_screen: the height of the screen to prevent the bullet from going forward infinitely
        :return: None
        """
        self.rect.y += self.speed

        # Get rid bullets going below the screen
        if self.rect.y > height_of_screen:
            self.kill()