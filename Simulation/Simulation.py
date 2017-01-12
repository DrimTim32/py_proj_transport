import time
class Simulation:
    def __init__(self,configuration):
        """Read configuration and do sth with it"""
        pass

    def __recalculate(self):
        pass

    def start(self):
        while True:
            print("IM WORKING")
            time.sleep(60)
            for _ in range(10):
                self.__recalculate()


