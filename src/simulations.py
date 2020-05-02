# ### Simulate many hands with a card counting strategy ###

from modelling import plot_hands
from modelling import plot_distr
from blackjack import Blackjack
import numpy as np

# Option to modify:
# * Num players
# * Position of player
# * Rulesets for all kinds of things
# * Bet spread
# * Scale bet spreead based on TC multiplier (harder to offer user input)
# * Card counting strategy


def simulate(num_rounds, min_bet=1, bet_spread=8, player_bankroll=1000,
             players=[''], strategy_name='hi_lo'):

    # Initiate the Blackjack game object
    blackjack = Blackjack(players=players, player_bankroll=player_bankroll,
                          human_player=False, print_to_terminal=False,
                          min_bet=min_bet, bet_spread=bet_spread)

    # Player the number of rounds
    min_bankrolls = [player_bankroll for player in players]
    arr_bankroll = [[] for player in players]
    ax_freq = num_rounds//2000+1  # Aim for 2000 data points to plot
    for i in range(num_rounds):  # Play each hand from here to track parameters
        for j, player in enumerate(players):
            min_bankrolls[j] = min(min_bankrolls[j],
                                   blackjack.players[j].bankroll)

            if i % ax_freq == 0:  # Only take ~2000 data points to plot
                arr_bankroll[j].append(blackjack.players[j].bankroll)

        blackjack.play_round()

    # Check the results
    for i, player in enumerate(blackjack.players):
        gains = 0
        print('Player {} ({}) started with ${:,.0f} and ended with ${:,.0f}'.
              format(player.num, player.name, player_bankroll,
                     player.bankroll))
        gains += player.bankroll - player_bankroll

        print('Total gains ${:,.0f} with ${} min_bet, {}x bet spread, {} card \
               counting over {:,} hands'.format(
               gains, min_bet, bet_spread, strategy_name, num_rounds))
        print('Min bankroll ${:,.0f}, so max drawdown was ${:,.0f} [{:.2f}%]'.
              format(min_bankrolls[i], player_bankroll-min_bankrolls[i],
                     (player_bankroll-min_bankrolls[i])/player_bankroll*100))

        print('')

    hands_pr_hr = 100
    hrs_per_day = 8
    working_days_per_yr = 260
    yrs = num_rounds * len(blackjack.players) / \
        hands_pr_hr / hrs_per_day / working_days_per_yr
    print('{:.1f}yrs of {}h working days playing {} hands of Blackjack per \
        hour total'.format(yrs, hrs_per_day, hands_pr_hr))

    plot_hands(players, arr_bankroll)


# ### Simulate distribution and player win rate of many hands ###

def simulate2(num_rounds, num_sims, min_bet=1, bet_spread=8,
              player_bankroll=10_000,
              players=[''], strategy_name='hi_lo', showfig=False):

    # Store params to save fig later
    params = '{}_{}rounds_{}sims_{}minbet_{}betspread_{}startingbankroll'\
        .format(strategy_name, num_rounds, num_sims, min_bet, bet_spread,
                player_bankroll)

    final_bankrolls = {player: [] for player in players}
    for _ in range(num_sims):
        # Initiate the Blackjack game object
        blackjack = Blackjack(players=players, player_bankroll=player_bankroll,
                              human_player=False, print_to_terminal=False,
                              min_bet=min_bet, bet_spread=bet_spread,
                              strategy_name=strategy_name)

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
    player_advantage = (mean_bankroll - player_bankroll) / player_bankroll

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
