import sys

from Simulation import Simulation
from Configuration.Config import Config


def read_configuration():
    return Config.from_config_file("../Configuration/config.json")

def entrypoint():
    configuration = read_configuration()
    simulation = Simulation(configuration)
    simulation.start()

def main():
        try:
            entrypoint()
        except Exception as e:
            print("{0}, message : {1}".format(sys.stderr,e))
            return 2

if __name__ == "__main__":
    sys.exit(main())