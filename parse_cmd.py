import argparse
import textwrap

from lib.blackjack import Blackjack  # pylint: disable=import-error


def parse(simulation=False):
    # Parse in any command line arguments for the game
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--players", default=3, type=int,
                        help=textwrap.dedent('''\
                        Number of players
                        Default is 3
                        :: For example, to change to 1 player:
                        -p 1
                        '''))

    parser.add_argument("-b", "--bankroll", default=10_000, type=int,
                        help=textwrap.dedent('''\
                        Adjust the starting bankroll of players
                        Default is 1000
                        :: For example, to change starting bankroll to 100,000:
                        -b 100000
                        '''))

    parser.add_argument("-d", "--decks", default=6, type=int,
                        help=textwrap.dedent('''\
                        Number of decks the dealer plays with
                        Default is 6
                        :: For example, to change decks to 2:
                        -d 2
                        '''))

    parser.add_argument("-pe", "--penetration", default=0.75, type=float,
                        help=textwrap.dedent('''\
                        Penetration of deck before shuffle
                        Default is 0.75
                        :: For example, to change to shuffle at 0.5:
                        -pe 0.5
                        '''))

    parser.add_argument("-bp", "--blackjack_payout", default=1.5, type=float,
                        help=textwrap.dedent('''\
                        Payout ratio of blackjack
                        Default is 1.5 (3 to 2)
                        :: For example, to 1.2 (6 to 5):
                        -bp 1.2
                        '''))

    parser.add_argument("-wp", "--win_payout", default=1, type=float,
                        help=textwrap.dedent('''\
                        Default payout of a standard hand win
                        Default is 1
                        :: For example, to change to 0.8:
                        -wp 0.8
                        '''))

    parser.add_argument("-pp", "--push_payout", default=0, type=float,
                        help=textwrap.dedent('''\
                        Default payout of a push
                        Default is 0
                        :: For example, to change to dealer wins:
                        -pp -1
                        '''))

    parser.add_argument("-lp", "--loss_payout", default=-1, type=float,
                        help=textwrap.dedent('''\
                        Default payout of a loss
                        Default is -1
                        :: For example, to change it to half a loss:
                        -lp -0.5
                        '''))

    parser.add_argument("-sp", "--surrender_payout", default=-0.5, type=float,
                        help=textwrap.dedent('''\
                        Default payout of a surrender
                        Default is -0.5
                        :: For example, to change to full surrender payout:
                        -sp 1
                        '''))

    parser.add_argument("-sh", "--stand_on_hard", default=17, type=int,
                        help=textwrap.dedent('''\
                        What hard total the dealer will stand on
                        Default is 17
                        :: For example, to change to stand on h18 (hit on h17):
                        -sh 18
                        '''))

    parser.add_argument("-ss", "--stand_on_soft", default=17, type=int,
                        help=textwrap.dedent('''\
                        What soft total the dealer will stand on
                        Default is 17
                        :: For example, to change to stand on s18 (hit on s17):
                        -ss 18
                        '''))

    parser.add_argument("-ls", "--late_surrender", default=True,
                        action="store_false",
                        help=textwrap.dedent('''\
                        Whether late surrender is allowed
                        Default is True
                        :: To change to False simply input -ls, example:
                        -ls
                        '''))

    parser.add_argument("-es", "--early_surrender", default=False,
                        action="store_true",
                        help=textwrap.dedent('''\
                        Whether early surrender is allowed
                        Default is False
                        :: To change to False simply input -es, example:
                        -es
                        '''))

    parser.add_argument("-dp", "--dealer_peaks", default=False,
                        action="store_true",
                        help=textwrap.dedent('''\
                        Whether the dealer peaks for blackjack or not
                        Default is False
                        :: To change to False simply input -dp, example:
                        -dp
                        '''))

    parser.add_argument("-r", "--rounds", default=100, type=int,
                        help=textwrap.dedent('''\
                        Number of rounds in the blackjack game
                        Default is 100
                        :: For example, to change to 30:
                        -r 30
                        '''))

    # Get extra arguments if simulation
    if simulation:
        parser = parse_simulation_params(parser)

    # Receive the args
    args = parser.parse_args()

    # Print ruleset
    print('Ruleset: {}'.format(vars(args)))

    # Create the blackjack game to return
    blackjack = create_blackjack(args, simulation)

    # Possible additional rulesets:
    # https://wizardofodds.com/games/blackjack/calculator/

    return args, blackjack


def parse_simulation_params(parser):
    parser.add_argument("-mb", "--min_bet", default=1, type=int,
                        help=textwrap.dedent('''\
                        Minimum bet the card counting strategy will employ
                        Default is 1
                        :: For example, to change to 10:
                        -mb 10
                        '''))

    parser.add_argument("-bs", "--bet_spread", default=16, type=int,
                        help=textwrap.dedent('''\
                        The bet spread the card counting strategy will employ
                        Default is 16
                        :: For example, to change to 32:
                        -bs 32
                        '''))

    parser.add_argument("-s", "--strategy", default="hi_lo", type=str,
                        help=textwrap.dedent('''\
                        The precoded strategy to employ
                        Default is hi_lo. For a full list see the README.md
                        :: For example, to change to omega_2:
                        -s omega_2
                        '''))

    parser.add_argument("-cs", "--custom_strategy", default=[], type=list,
                        help=textwrap.dedent('''\
                        Implement a custom strategy
                        Default is none.
                        :: For example, to change to omega_2:
                        -s omega_2
                        '''))

    parser.add_argument("-sim", "--simulations", default=1000, type=int,
                        help=textwrap.dedent('''\
                        Number of games to simulate
                        Default is 1000
                        :: For example, to change to 10000:
                        -sim 10000
                        '''))

    return parser


def create_blackjack(args, sim):
    player_list = ['Player {}'.format(i+1) for i in range(args.players)]

    if sim:
        min_bet = args.min_bet
        bet_spread = args.bet_spread
        strategy_name = args.strategy
    else:
        min_bet = 1
        bet_spread = 8
        strategy_name = "hi_lo"

    blackjack = Blackjack(players=player_list,
                          num_of_decks=args.decks,
                          blackjack_payout=args.blackjack_payout,
                          win_payout=args.win_payout,
                          push_payout=args.push_payout,
                          loss_payout=args.loss_payout,
                          surrender_payout=args.surrender_payout,
                          dealer_stand_on_hard=args.stand_on_hard,
                          dealer_stand_on_soft=args.stand_on_soft,
                          late_surrender=args.late_surrender,
                          early_surrender=args.early_surrender,
                          player_bankroll=args.bankroll,
                          reshuffle_penetration=args.penetration,
                          dealer_peeks_for_bj=args.dealer_peaks,

                          print_to_terminal=False if sim else True,
                          human_player=False if sim else True,

                          min_bet=min_bet,
                          bet_spread=bet_spread,
                          strategy_name=strategy_name,
                          )

    # Note: human player could be set False in normal game to play as machine

    return blackjack
