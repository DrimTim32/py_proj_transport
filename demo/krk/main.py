"""This file contains main file for Cracow demo"""
import sys
import time

sys.path.append('../../')
from core.configuration.config import Config
from core.simulation import simulation as sim


def read_configuration():
    """Reads configuration from json file"""
    return Config.from_config_file("config.json")


def entrypoint():
    """Main entrypoint for application, here logic is executed"""
    configuration = read_configuration()
    simulation = sim.Simulation(configuration)
    while True:
        simulation.refresh()
        time.sleep(0.2)


def main():
    """Start function"""
    try:
        entrypoint()
    except Exception as exception_info:
        print("{0}, message : {1}".format(sys.stderr, exception_info))
        return 2


if __name__ == "__main__":
    sys.exit(main())
