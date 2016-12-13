import sys

from Simulation import Simulation


def read_configuration():
    pass

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