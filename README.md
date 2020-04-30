TODO

# Move to .py and improve GOOD
# Check everything working GOOD

# Review code, refactor imports, PYLINT!

# Add testing
# Use pylint
# Proper readme
# Push to Git


# ### Read me ###
# See https://github.com/jmausolf/poshmark_sharing READ_ME.md for proper styling and content
# 
# 


# Rules to customise by? https://wizardofodds.com/games/blackjack/calculator/


Define baseline of player advantage
# Player advantage - how do we define this? We could define % of time they are up or down over 1 hand?
# That would only reflect basic strategy and not payouts still. So % 

# For every $100 you bet how much will you win or lose?
# DEPENDS HOW YOU BET THE $100? BET SIZING?

# Aces and fives have the biggest effect on player/casino odds so can do ok by just counting them

# Measure expected value per 100 hands (in an hour)
# Player advantage is how much on average as a % they are up after 1 hour

# Run 10k simulations of 100 rounds
# Take standard deviation of the results too
# Plot distribution with bars and best fit of normal distribution curve based on mean and sd

# Playing more than 100 rounds would increase odds, add ability to alter that. TC=0 at start ofc. Penetration less key too

# Bet spread is key btw
# Player advantage seems to be pretty subjective



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