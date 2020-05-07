import parse_cmd  # pylint: disable=import-error
from lib.blackjack import Blackjack  # pylint: disable=import-error

if __name__ == "__main__":
    args, blackjack = parse_cmd.parse()

    # Plays 100 hands or until bust by default
    blackjack.play_game(args.rounds)
