
class Card_Counter():
    '''Class implementing various card counting strategies as well as enabling custom strategy input.
       Count will be updated every time a new card is dealt in the BlackJack class'''
    def __init__(self, blackjack_game, total_decks, 
                 strategy_name=None, custom_strategy=None,
                 min_bet=1, bet_spread=8,
                 value_of_each_hand_observed=-1,
                 num_players=3
                 ):
        
        self.blackjack_game = blackjack_game  # running blackjack game to refer to
        self.total_decks = total_decks
        self.local_deck = []  # local deck of dealt cards
        
        self.min_bet = min_bet
        self.bet_spread = bet_spread
                        
        self.card_dic = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8',
                 8: '9', 9: '10', 10: 'Jack', 11: 'Queen', 12: 'King'}
        
        # Lists of counting strategy weightings from Ace to King
        self.strategies = {'hi_lo': [-1, 1, 1, 1, 1, 1, 0, 0, 0, -1, -1, -1, -1],
                         'ace_five': [-1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                         'hi_opt_1': [0, 0, 1, 1, 1, 1, 0, 0, 0, -1, -1, -1, -1],
                         'hi_opt_2': [-2, 1, 1, 2, 2, 1, 1, 0, 0, -1, -1, -1, -1],  # note: not a balanced system
                         'insurance': [4, 4, 4, 4, 4, 4, 4, 4, 4, -9, -9, -9, -9],
                         'ko': [-1, 1, 1, 1, 1, 1, 1, 0, 0, -1, -1, -1, -1],
                         'omega_2': [0, 1, 1, 2, 2, 2, 1, 0, -1, -2, -2, -2, -2],  # One of the best
                         'opp': [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # not balanced and subtracts value per hand played
                         'red_7': [-1, 1, 1, 1, 1, 1, 0.5, 0, 0, -1, -1, -1, -1],  # Red 7s (or just 0.5) also count as +1 and no need TC
                         'zen': [-1, 1, 1, 2, 2, 2, 1, 0, 0, -2, -2, -2, -2]
                        }
        
        self.value_of_each_hand_observed = value_of_each_hand_observed # Used for OPP
        self.num_players = num_players

        if strategy_name is None:
            if custom_strategy is None:
                raise ValueError('No strategy or custom value strategy allocated')
            else:  # User has input their own custom strategy
                assert custom_strategy is type(list) and len(custom_strategy) == 13
                self.strategy = custom_strategy  # Allow user to input their own ruleset
                self.strategy_name = 'Custom strategy'
        else:
            self.strategy_name = strategy_name.lower()
            strategy = self.strategies.get(self.strategy_name)
            if strategy is None:
                raise ValueError('Strategy {} not in directory of strategies'.format(self.strategy_name))
            else:
                self.strategy = strategy
                
        # Refresh deck to reset all parameters
        self.deck_refreshed()
                
    def next_card(self, card):
        # Update local copy of deck
        self.local_deck.append(card)
        
        # Run all desired card counting strategies
        self.update_count(card)
        
        # Get strategy bet
        self.get_suggested_bet()

    def deck_refreshed(self):
        # Clear local deck of seen cards
        self.local_deck = []
        self.running_count = self.true_count = self.hands_observed = 0
        self.num_cards = self.total_decks*52
        self.num_hands_seen = 0
    
    def update_count(self, card, num_decks=None):
        # Keep a running count dependent on strategy and vary bets based on running total and number of decks left in play
        # The higher the count, the more high cards the deck has left, the higher chance for player blackjack 3:2
        # Additionally, if the hand is low and you are 16v10 can take the hit knowing higher chance of low card
        # Don Schlesinger's Illiustrious 18 with most important can be found here: 
        # https://wizardofodds.com/games/blackjack/card-counting/high-low/
        
        card_val = card % 13
        
        # Update the count according to the strategy
        self.running_count += self.strategy[card_val]

        # Hi lo uses true count so update that
        self.num_cards -= 1 # number of cards left in deck
        self.num_decks = self.num_cards/52. # number of decks left as a float
    
        self.true_count = self.running_count / self.num_decks  # true count as float
        
        # Num of hands for opp and other strategies. Players + dealer each turn
        self.num_hands_seen += (self.value_of_each_hand_observed * (self.num_players+1))
        
    def get_suggested_bet(self):
        # Hi lo is the most well known strategy. Bet based on True Count.
        # Here we scale bet to min_bet * bet spread if true count > 2
        if self.strategy_name=='hi_lo':
            suggested_bet = self.min_bet if self.true_count < 2 else self.min_bet*self.bet_spread
            return suggested_bet
        
        # Ace five is the simplest strategy, +1 for 5, -1 for A.
        # A/5 are the highest impact cards on each end. Just use running count here.
        elif self.strategy_name=='ace_five':
            suggested_bet = self.min_bet if self.running_count < 2 else self.min_bet*self.bet_spread
            return suggested_bet
        
        # Highly optimum card counting system drops the aces and the twos from hi_lo
        elif self.strategy_name=='hi_opt_1':
            suggested_bet = self.min_bet if self.true_count < 2 else self.min_bet*self.bet_spread
            return suggested_bet
        
        # More advanced hi_op with +2s
        elif self.strategy_name=='hi_opt_2':
            suggested_bet = self.min_bet if self.true_count < 2 else self.min_bet*self.bet_spread
            return suggested_bet
        
        # Count as to whether it is valuable to take insurance.
        # TC > 5 as benchmark for insurance. Really 1:5, 2:9, 6:25, 8:33
        # https://www.888casino.com/blog/side-bets/card-counting-blackjack-insurance
        elif self.strategy_name=='insurance':
            raise ValueError('Insurance count done seperately')
        
        # ko is an unbalanced system. Less AP than hi_lo but no need to TC.
        elif self.strategy_name=='ko':
            suggested_bet = self.min_bet if self.running_count < 2 else self.min_bet*self.bet_spread
            return suggested_bet
        
        # omega_2 use TC
        elif self.strategy_name=='omega_2':
            suggested_bet = self.min_bet if self.true_count < 2 else self.min_bet*self.bet_spread
            return suggested_bet
        
        # opp Not balanced and subtracts an amount per hand played
        # Add 1 for every low card dealt. Subtract 1 for every player including the dealer.
        # If count > 6 increase bet
        elif self.strategy_name=='opp':
            suggested_bet = self.min_bet if (self.running_count + self.num_hands_seen) < 6 else                             self.min_bet*self.bet_spread
            return suggested_bet
        
        # red_7 - 80% of hi lo and no need for true count
        elif self.strategy_name=='red_7':
            suggested_bet = self.min_bet if self.running_count < 2 else self.min_bet*self.bet_spread
            return suggested_bet
        
        # zen - basic balanced strategy with true count
        elif self.strategy_name=='zen':
            suggested_bet = self.min_bet if self.true_count < 2 else self.min_bet*self.bet_spread
            return suggested_bet
        

        # Do Kelly Criterion by default for bet sizing as its most profitable
        # Odds of winning (i.e. 60%) * 2 = 120% - 1 = 20%. Bet 20% of current bankroll
        # Odds of winning (i.e. 90%) * 2 = 180% - 1 = 80%. Bet 80% of current bankroll
        # To do this with blackjack need to know odds of how much you would win since bj/splits/dd pay different
        # Do either with combinatorics or simulate by running strategy 1000 times?
        # If simulating do confidence intervals and see how many times need to run based on possible outcomes
        # Would need to simulate the hand without the deck updating to see how much can expect to win/lose
        # Maybe just do bet spread for now and consider odds and Kelly Criterion later
        
        # Should track bankroll by turn and log it so can plot and calc variance for SCORE
        