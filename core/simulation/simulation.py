import time


class Simulation:
    def __init__(self, configuration):
        """Read configuration and do sth with it"""
        self.finished = False

    def update(self):
        pass

    def mainloop(self):
        while not self.finished:
            print("IM WORKING")
            time.sleep(10)
            self.update()
