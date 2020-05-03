import argparse
import textwrap

from lib.blackjack import Blackjack  # pylint: disable=import-error

if __name__ == "__main__":
    # Parse in any command line arguments for thegame
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--players", default=1, type=int,
                        help=textwrap.dedent('''\
                        Number of players
                        Default is 1
                        :: For example, to change to 3 players:
                        -p 3
                        '''))

    parser.add_argument("-b", "--bankroll", default=1000, type=int,
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
                        :: For example, to change to shuffle at 50%:
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

    parser.add_argument("-lp", "--loss_payout", default=1, type=float,
                        help=textwrap.dedent('''\
                        Default payout of a loss
                        Default is -1
                        :: For example, to change it to half a loss:
                        -lp -0.5
                        '''))

    parser.add_argument("-sp", "--surrender_payout", default=0.5, type=float,
                        help=textwrap.dedent('''\
                        Default payout of a surrender
                        Default is 0.5
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

    # Receive the args
    args = parser.parse_args()

    # Adjust player arg
    if type(args.players) is int:
        args.players = ['Player {}'.format(i+1) for i in range(args.players)]
    else:
        raise TypeError('-p --players type must be int or list not {}'
                        .format(type(args.players)))

    # Initiate blackjack game
    blackjack = Blackjack(players=args.players,
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
                          )

    # Plays 100 hands or until bust by default
    blackjack.play_game()
