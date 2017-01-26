import sys

from core.configuration import config
from core.simulation.simulation import *


def read_configuration():
    return config.Config.from_config_file("config.json")


def entrypoint():
    configuration = read_configuration()
    simulation = Simulation(configuration)
    simulation.mainloop()


def main():
    entrypoint()
    # try:
    #     entrypoint()
    # except Exception as e:
    #     print("{0}, message : {1}".format(sys.stderr, e))
    #     return 2

if __name__ == "__main__":
    sys.exit(main())
