import pygame
class Simulation:
    def __init__(self,configuration):
        """Read configuration and do sth with it"""
        pass

    def open_window(self,configData):
        pygame.init()
        return pygame.display.set_mode((800,600))

    def refresh(self,window):
        window.fill((211,211,211))
        pygame.display.flip()
        

    def recalculate(self):
        pass
    def start(self):
        window = self.open_window(configData="sth")
        while True:
            self.recalculate()
            self.refresh(window)
            pygame.time.Clock().tick(1)

