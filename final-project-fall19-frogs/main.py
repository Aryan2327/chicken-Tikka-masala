#import your controller
import pygame
from src import controller


def main():
    """
    runs the controller
    :param: none
    :return: None
    """
    #Create an instance on your controller object
    pygame.init()
    main_window = controller.Controller()
    main_window.mainloop()
main()
