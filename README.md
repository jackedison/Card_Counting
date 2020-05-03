<img src="https://cdn.pixabay.com/photo/2015/11/07/11/08/cards-1030852_1280.jpg" alt="Blackjack" width="640" height="425">


# Blackjack Card Counting Strategy Monte Carlo & Terminal Human/Machine Playable Game

This package allows for Monte Carlo simulation of **Blackjack card counting strategies**. Rulesets, strategies, and simulation parameters are all adjustable to meet user preferences. Default parameters run under a liberal Vegas shoe.

Simulations using this package provide a clear representation of the player's winrate as well as the distribution of play. By adjusting parameters the user can compare rulesets, strategies, player position, bet spreads, and more.

# Getting started
### Prerequisites

* Python 3.7.3+
* [numpy](https://numpy.org/) v1.18.3+
* [scipy](https://www.scipy.org/) v1.4.1+
* [matplotlib](https://matplotlib.org/) v3.2.1+

If package installation is required they may be installed by running:
* `pip install -r requirements.txt`.

### Setup

In terminal (mac) or command prompt (windows) clone the repository with:
* `git clone https://github.com/jackedison/Card_Counting`

Then change directory to the cloned repository:
* `cd Card_Counting`

# Simulate

Once you have cloned to a local repository you are ready to begin running simulations.

There are 3 modules which the user can run from command line:

1. play_blackjack.py
2. simulate_blackjack.py
3. simulate_distr.py

## Play Blackjack in the terminal - play_blackjack.py

The most simple feature is the ability to play blackjack in the terminal. This allows you to test functionality and ruleset responses.

To play run `python3 play_blackjack.py`

By default this will run a blackjack game under a liberal Vegas shoe, that is:
* 6 decks
* 75% penetration
* 3 to 2 blackjack payout
* Dealer stands on soft 17

### Argparse adjustments
Game parameters and ruleset can be adjusted through command line using argparse.

#### Example 1: Adjust the number of players: -p
Default number of players is 1. 

For example, to adjust the number of players to 3:

`python3 play_blackjack.py -p 3`

#### Example 2: Adjust the penetration: -pe
Default penetration is 0.75 (75% of deck).

For example, to adjust the penetration to 50%:

`python3 play_blackjack.py -pe 0.5`

#### Example 3: Dealer peaks for blackjack: -dp
Default dealer does **not** peak for blackjack.

Note for a boolean you do not need to input a flag after the argument. For example, to enable peak for blackjack:

`python3 play_blackjack.py -dp`

#### All current Argparse parameters

| Parameter                  	| Arg 	| Default 	| Type  	|
|----------------------------	|-----	|---------	|-------	|
| Number of players          	| -p  	| 1       	| int   	|
| Starting bankroll          	| -b  	| 1000    	| int   	|
| Number of decks            	| -d  	| 6       	| int   	|
| Deck penetration           	| -pe 	| 0.75    	| float 	|
| Blackjack payout           	| -bp 	| 1.5     	| float 	|
| Win payout                 	| -wp 	| 1       	| float 	|
| Push payout                	| -pp 	| 0       	| float 	|
| Loss payout                	| -lp 	| 1       	| float 	|
| Surrender payout           	| -sp 	| 0.5     	| float 	|
| Dealer stands on hard      	| -sh 	| 17      	| int   	|
| Dealer stands on soft      	| -ss 	| 17      	| int   	|
| Late surrender allowed     	| -ls 	| True    	| bool  	|
| Early surrender allowed    	| -es 	| False   	| bool  	|
| Dealer peaks for blackjack 	| -dp 	| False   	| bool  	|

## Simulate card counting strategies - simulate_blackjack.py

The principal purpose of this package is to enable simulations of millions of hands. This allows for the testing of card counting strategies under specific rulesets, returning player win rates and session distributions.

To simulate run `python3 simulate_blackjack.py`





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






## Possible extensions

This project is by no means complete and there are almost endless possibilities for extension. This project allows for a framework to build from. Highlighted below are areas I feel would be best to target next.

Smart machine moves can be computed in 3 ways:
1. Make bet based on basic strategy
2. Make bet based on optimal play for current deck - computed by simulations
3. Make bet based on optimal play for current deck - computed by efficient combinatorics of current deck
 
* Currently the machine player plays on basic strategy as this is a better representation of how a card counter would play in a casino. However, extending this code to play the optimal play based on remaining deck would enable odds checking vs absolute optimal play as well as optimal bet sizing using Kelly Criterion.

* A closer proxy to optimal play would be to use derivatives of basic strategy based on current count. These could also be generated as an extension to this piece of work using combinatorics.

* Kelly Criterion, as the most efficient bet sizing, based on current bankroll could be implemented here alongside the above. This could be replicated in casino play once derivatives of basic strategy are mastered. 

* Extra rulesets could be allowed such as those found here: https://wizardofodds.com/play/blackjack-v2/ and https://www.qfit.com/blackjack-rules-surrender.htm


* Implement insurance count to further get odds for AP

* Could implement bet scaling / Kelly criterion

* Add proper testing (unit tests etc.) - if project is further developed



Kelly Criterion, to achieve a 13.5% risk of ruin

SCORE is an acronym, coined by Don Schlesinger, for Standardized Comparison Of Risk and Expectation. 

It is defined as the advantage squared divided by the variance. The SCORE may also be interpreted as the expected hourly win per hand for a player with a $10,000 bankroll, who sizes his bets according to the Kelly Criterion, to achieve a 13.5% risk of ruin.

https://wizardofodds.com/games/blackjack/ace-five-count/



Style guidelines used for the code are pylint and pycodestyle (pep8 vscode).

