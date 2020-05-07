# ### simulate_game many hands with a card counting strategy ###
import numpy as np

from .modelling import plot_hands
from .modelling import plot_distr
from .blackjack import Blackjack

# Option to modify:
# * Num players
# * Position of player
# * Rulesets for all kinds of things
# * Bet spread
# * Scale bet spreead based on TC multiplier (harder to offer user input)
# * Card counting strategy


def simulate_game(blackjack, num_rounds):

    # Collect variables from blackjack game for future reference
    players = [player.name for player in blackjack.players]
    player_bankroll = blackjack.players[0].bankroll
    min_bet = blackjack.min_bet
    bet_spread = blackjack.bet_spread
    strategy_name = blackjack.strategy_name

    # Player the number of rounds
    min_bankrolls = [player_bankroll for player in players]
    arr_bankroll = [[] for player in players]
    hand_num = [[] for player in players]
    ax_freq = num_rounds//2000+1  # Aim for 2000 data points to plot
    for i in range(num_rounds):  # Play each hand from here to track parameters
        for j, player in enumerate(players):
            min_bankrolls[j] = min(min_bankrolls[j],
                                   blackjack.players[j].bankroll)

            if i % ax_freq == 0:  # Only take ~2000 data points to plot
                arr_bankroll[j].append(blackjack.players[j].bankroll)
                hand_num[j].append(i+1)

        blackjack.play_round()

    # Check the results
    for i, player in enumerate(blackjack.players):
        gains = 0
        print('Player {} ({}) started with ${:,.0f} and ended with ${:,.0f}'.
              format(player.num, player.name, player_bankroll,
                     player.bankroll))
        gains += player.bankroll - player_bankroll

        print('Total gains ${:,.0f} with ${} min_bet, {}x bet spread, {} card '
              'counting over {:,} hands'.format(
               gains, min_bet, bet_spread, strategy_name, num_rounds))
        print('Min bankroll was ${:,.0f}, a drawdown of ${:,.0f} [{:.2f}%]'.
              format(min_bankrolls[i], player_bankroll-min_bankrolls[i],
                     (player_bankroll-min_bankrolls[i])/player_bankroll*100))

        print('')

    plot_hands(players, arr_bankroll, hand_num)


# ### simulate_game distribution and player win rate of many hands ###

def simulate_games(args, showfig=False):

    # Intepret terminal parser inputs
    num_rounds = args.rounds
    num_sims = args.simulations

    players = ['Player {}'.format(i+1) for i in range(args.players)]

    # Store params to save fig later
    params = '{}_{}rounds_{}sims_{}minbet_{}betspread_{}startingbankroll'\
        .format(args.strategy, num_rounds, num_sims, args.min_bet,
                args.bet_spread, args.bankroll)

    final_bankrolls = {player: [] for player in players}
    for _ in range(num_sims):
        # Initiate the Blackjack game object
        blackjack = Blackjack(players=players,
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

                              print_to_terminal=False,
                              human_player=False,

                              min_bet=args.min_bet,
                              bet_spread=args.bet_spread,
                              strategy_name=args.strategy,
                              )

        # Play the number of rounds in sim
        for _ in range(num_rounds):
            blackjack.play_round()

        # Add player's final bankrolls to dic
        for player in blackjack.players:
            final_bankrolls[player.name].append(player.bankroll)

    # Compute mean of each player and mean overall
    mean_bankrolls = {player: np.mean(final_bankrolls[player])
                      for player in players}
    mean_bankroll = np.mean([mean_bankrolls[key] for key in mean_bankrolls])

    # Compute standard deviation of each player and standard deviation overall
    std_bankrolls = {player: np.std(final_bankrolls[player])
                     for player in players}
    std_bankroll = np.std([bankroll for value in final_bankrolls.values()
                          for bankroll in value])  # Confusing List comprehens

    # Player advantage calc
    player_advantage = (mean_bankroll - args.bankroll) / args.bankroll

    # Plot distributions
    plot_distr(final_bankrolls, mean_bankrolls, std_bankrolls, mean_bankroll,
               std_bankroll, params, player_advantage, showfig)

    for player in players:
        print('Mean final bankroll for {} was ${:,.2f}'
              .format(player, mean_bankrolls[player]))
        print('Standard deviation for {} was {:.2f}'
              .format(player, std_bankrolls[player]))
        print('')

    print('Overall mean: ${:,.2f} and std: {:.2f}'.format(mean_bankroll,
                                                          std_bankroll))

    print('Estimated player advantage {:.2f}%'.format(player_advantage*100))

    return player_advantage, std_bankroll
