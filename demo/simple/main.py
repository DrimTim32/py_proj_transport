import sys
import time


if "core" not in sys.path[0]:
    if "\\" in sys.path[0]:
        sys.path.insert(0, '..\\..\\core')
    else:
        sys.path.insert(0, '../../core')

from configuration import config
from simulation.simulation import Simulation


def read_configuration():
    return config.Config.from_config_file("config.json")


def entrypoint():
    configuration = read_configuration()
    simulation = Simulation(configuration)
    while True:
        simulation.refresh()
        time.sleep(0.2)


def main():
    try:
        entrypoint()
    except Exception as e:
        print("{0}, message : {1}".format(sys.stderr, e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
