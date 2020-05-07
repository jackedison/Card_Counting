import parse_cmd  # pylint: disable=import-error
from lib.blackjack import Blackjack  # pylint: disable=import-error
from lib import simulations  # pylint: disable=import-error

if __name__ == "__main__":
    args, _ = parse_cmd.parse(simulation=True)

    # Initiate simulation
    simulations.simulate_games(args=args)
