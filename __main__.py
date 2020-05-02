from blackjack import Blackjack

# In[]
# Initiate a playable game in the terminal #
from blackjack import Blackjack


blackjack = Blackjack(players=['Jack', 'Kath'], dealer_peeks_for_bj=False)

blackjack.play_game()



# In[]
# ### Initiate a simulated game in the terminal ###
blackjack = Blackjack(players=['Jack', 'Kath'], human_player=False)

blackjack.play_game(rounds=3)


# In[]
# Simulate a strategy over a long game
import simulations

simulations.simulate(num_rounds=208_000, players=['Player ' + str(i+1) for i in range(10)], player_bankroll=100_000,
         min_bet=25, bet_spread=16, strategy_name='zen')


# In[]
# Simulate a strategy over many games and view distribution of results
# Can use this to see how penetration impacts, player position, strategy, etc.
# Tons of possibilities. Show a few examples and leave rest for user to explore.

simulations.simulate2(num_rounds=100, num_sims=1000, players=['Player 1', 'Player 2', 'Player 3'], player_bankroll=10_000, 
         min_bet=10, bet_spread=16, strategy_name='zen', showfig=False)


# In[]
# Run all strategy simulations
strategies = ['hi_lo', 'ace_five', 'hi_opt_1', 'hi_opt_2', 'ko', 'omega_2', 'opp', 'red_7', 'zen']

results = {}
for strategy in strategies:
    pa, sd = simulations.simulate2(num_rounds=100, num_sims=1000, players=['Player 1', 'Player 2', 'Player 3'], player_bankroll=10_000, 
              min_bet=10, bet_spread=16, strategy_name=strategy)
    
    results[strategy] = [pa, sd]

print(results)

# In[]

# TODO Demonstrate simulation with a custom ruleset 