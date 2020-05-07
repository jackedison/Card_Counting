import parse_cmd  # pylint: disable=import-error
from lib.blackjack import Blackjack  # pylint: disable=import-error
from lib import simulations  # pylint: disable=import-error

if __name__ == "__main__":
    args, blackjack = parse_cmd.parse(simulation=True)

    # Override class variables in advance of simulation
    blackjack.human_player = False
    blackjack.inputoutput.print_to_terminal = False

    # Initiate simulation
    simulations.simulate_game(blackjack=blackjack,
                              num_rounds=args.simulations,
                              )
