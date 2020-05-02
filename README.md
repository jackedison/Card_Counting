![](https://images.unsplash.com/photo-1559813195-53f6dccb5c95?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=3300&q=80)

# Blackjack Card Counting Strategy Simulator & Terminal Human/Machine Playable Game

This package allows for the simulation of **Blackjack card counting strategies**. By default the simulations will run under a liberal Vegas shoe ruleset, however, almost any parameter in this package (ruleset, strategy, simulations) can be alterred to the user's preferences.

Simulations using this package provide a clear representation of the player's winrate as well as the distribution of play. By adjusting parameters the user can compare rulesets, strategies, player position, bet spreads, and more.

Included card counting strategies and their parameter names are:
* [hi_lo](https://wizardofodds.com/games/blackjack/card-counting/high-low/)
* [ace_five](https://wizardofodds.com/games/blackjack/ace-five-count/)
* [hi_opt_1](https://www.countingedge.com/card-counting/hi-opt-1/)
* [hi_opt_2](https://www.countingedge.com/card-counting/hi-opt-2/)
* [ko](https://www.onlineblackjackrealmoney.org/card-counting/knock-out)
* [omega_2](https://www.gamingtheodds.com/blackjack/card-counting/systems/omega-2)
* [opp](http://www.blackjackforumonline.com/content/Easy_OPP_Card_Counting_System.htm)
* [red_7](https://www.gamblingonline.com/blackjack/card-counting/)
* [zen](https://www.onlineblackjackrealmoney.org/card-counting/zen-count)

Users may also input their own custom card counting strategy with the following syntax:
* `TODO`

When running simulations the player will play according to Edward Thorp's basic strategy contingent on the ruleset (for doubling, splitting, insuring, etc.)

# Getting started
### Prerequisites

* Python 3.7.3+
* [numpy](https://numpy.org/) v1.18.3+
* [scipy](https://www.scipy.org/) v1.4.1+
* [matplotlib](https://matplotlib.org/) v3.2.1+

To install the package requirements run `pip install -r requirements.txt`.

TODO
* Proper execution of main methods
* Proper readme
* Push to Git (remove .gitignore files)




Additional Rules to customise by? https://wizardofodds.com/games/blackjack/calculator/


### Player Advantage
Define baseline of player advantage
Player advantage - how do we define this? We could define % of time they are up or down over 1 hand?
That would only reflect basic strategy and not payouts still. So % 

For every $100 you bet how much will you win or lose?
DEPENDS HOW YOU BET THE $100? BET SIZING?

Aces and fives have the biggest effect on player/casino odds so can do ok by just counting them

Measure expected value per 100 hands (in an hour)
Player advantage is how much on average as a % they are up after 1 hour

Run 10k simulations of 100 rounds
Take standard deviation of the results too
Plot distribution with bars and best fit of normal distribution curve based on mean and sd

Playing more than 100 rounds would increase odds, add ability to alter that. TC=0 at start ofc. Penetration less key too

Bet spread is key btw
Player advantage seems to be pretty subjective



# Kelly Criterion, to achieve a 13.5% risk of ruin
# SCORE is an acronym, coined by Don Schlesinger, for Standardized Comparison Of Risk and Expectation. 
# It is defined as the advantage squared divided by the variance. The SCORE may also be interpreted as 
# the expected hourly win per hand for a player with a $10,000 bankroll, who sizes his bets according 
# to the Kelly Criterion, to achieve a 13.5% risk of ruin.

# https://wizardofodds.com/games/blackjack/ace-five-count/


# ### Possible extensions ###
# Smart machine moves can be computed in 3 ways:
# 1. Make bet based on basic strategy
# 2. Make bet based on optimal play for current deck - computed by simulations
# 3. Make bet based on optimal play for current deck - computed by efficient combinatorics of current deck
# 
# Currently the machine player plays on basic strategy as this is a better representation of how a card counter would play in a casino. However, extending this code to play the optimal play based on remaining deck would enable odds checking vs absolute optimal play as well as optimal bet sizing using Kelly Criterion.
# 
# A closer proxy to optimal play would be to use derivatives of basic strategy based on current count. These could also be generated as an extension to this piece of work using combinatorics.
# 
# Kelly Criterion, as the most efficient bet sizing, based on current bankroll could be implemented here alongside the above. This could be replicated in casino play once derivatives of basic strategy are mastered. 

# Extra rulesets could be allowed such as those found here: https://wizardofodds.com/play/blackjack-v2/ and https://www.qfit.com/blackjack-rules-surrender.htm
# 

# Implement insurance count to further get odds for AP

# Could implement bet scaling / Kelly criterion

# Add unit testing


# Style guidelines used are pylint and pycodestyle (pep8 vscode)

