import sys

from configuration import config
from drawing.gui import GUI
from simulation.simulation import Simulation


def read_configuration(path):
    """Reads configuration from file in path"""
    return config.Config.from_config_file(path)


def entry_point(path):
    """
    Entry point for application
    """

    configuration = read_configuration(path)
    print("Configuration readed succesfully.")
    simulation = Simulation(configuration)
    GUI(simulation).run()
    exit()


def main():
    """This is main method for this file"""
    path = "config.json"
    if len(sys.argv) < 2:
        print("Configuration file is not provided, using default.")
    else:
        path = sys.argv[1]
    entry_point(path)
    try:
        pass
    except Exception as exc:
        print("{0}, message : {1}".format(sys.stderr, exc))
        return 2

if __name__ == "__main__":
    main()
