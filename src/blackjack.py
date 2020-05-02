import random
from formatting import colour
from bj_io import InputOutput
from players import *
from card_count import Card_Counter
from strategy import BasicStrategy
# Imports are slightly messy due to creation in Jupyter - could refactor


class Deck():
    '''Deck class used to store and manipulate a data type emulating a
    playing card deck'''
    def __init__(self, num_of_decks=1):
        self.deck = [i % 52 for i in range(num_of_decks*52)]
        self.discard_deck = []

    def shuffle(self):
        random.shuffle(self.deck)

    def card_num_or_face(self, num):
        num_or_face = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6',
                       6: '7', 7: '8', 8: '9', 9: '10', 10: 'Jack',
                       11: 'Queen', 12: 'King'}
        return num_or_face[num % 13]

    def card_suit(self, num):
        suits = {0: 'Hearts', 1: 'Diamonds', 2: 'Clubs', 3: 'Spades'}
        return suits[num//13]

    def new_card_suit(self, num):
        suits = {0: '\u2665',  # Hearts
                 1: '\u2662',  # Diamonds
                 2: '\u2663',  # Clubs
                 3: '\u2664'}  # Spades
        return suits[num//13]

    def read_card(self, num, formatted=True):
        # For use  in Jupyter or console able to show fontweights only
        if formatted:
            if (self.card_suit(num) in ['Hearts', 'Diamonds']):
                col_text = colour.RED + colour.BOLD
            else:
                col_text = colour.BOLD
        return col_text + self.card_num_or_face(num) + ' of ' + \
            self.new_card_suit(num) + colour.END


class Blackjack():
    '''Blackjack game simulator. Default ruleset is based off of a liberal
    Vegas shoe but customisable'''
    def __init__(self, players, num_of_decks=6,
                 blackjack_payout=1.5, win_payout=1, push_payout=0,
                 loss_payout=-1, surrender_payout=-0.5,
                 dealer_stand_on_hard=17, dealer_stand_on_soft=17,
                 shuffle_deck=True,
                 late_surrender=True, early_surrender=False,
                 player_bankroll=1000, reshuffle_penetration=0.75,
                 human_player=True, print_to_terminal=True,
                 min_bet=1, bet_spread=8,
                 dealer_peeks_for_bj=False,
                 strategy_name='hi_lo'):

        self.num_of_decks = num_of_decks
        self.human_player = human_player
        self.print_to_terminal = print_to_terminal

        self.min_bet = min_bet
        self.bet_spread = bet_spread

        self.dealer_peeks_for_bj = dealer_peeks_for_bj
        self.strategy_name = strategy_name

        # Initiate deck object
        self.deck_obj = Deck(num_of_decks)

        # Create player objects for each player
        self.players = []
        for i, player_name in enumerate(players):
            self.players.append(Player(name=player_name, num=i+1,
                                bankroll=player_bankroll))

        # Card counting class to initiate
        self.card_counter = Card_Counter(self, total_decks=self.num_of_decks,
                                         strategy_name=strategy_name,
                                         min_bet=self.min_bet,
                                         bet_spread=self.bet_spread,
                                         num_players=len(self.players))

        # Initiate input/output means
        self.inputoutput = InputOutput(self.card_counter,
                                       print_to_terminal=print_to_terminal)

        # Create dealer object
        self.dealer = Dealer()

        # Initiate payout parameters
        self.blackjack_payout = blackjack_payout
        self.win_payout = win_payout
        self.push_payout = push_payout
        self.loss_payout = loss_payout
        self.surrender_payout = surrender_payout

        # Other rules
        self.dealer_stand_on_hard = dealer_stand_on_hard
        self.dealer_stand_on_soft = dealer_stand_on_soft

        # Surrender rules - late is the norm. Early is +0.6% advantage
        self.late_surrender = late_surrender
        self.early_surrender = early_surrender

        # Shuffle parm
        self.reshuffle_penetration = reshuffle_penetration

        # Shuffle deck
        if shuffle_deck:
            self.shuffle()

    def shuffle(self, discard_top_card=True, re_add_discard_deck=False):
        if re_add_discard_deck:  # Add discard deck back
            for _ in range(len(self.deck_obj.discard_deck)):
                self.deck_obj.deck.append(self.deck_obj.discard_deck.pop())
            self.card_counter.deck_refreshed()  # inform card_counter class

        self.deck_obj.shuffle()  # Shuffle deck
        if discard_top_card:  # Discard top card
            self.deck_obj.discard_deck.append(self.deck_obj.deck.pop())

    def display_deck(self):
        for card in self.deck_obj.deck:
            print(self.deck_obj.read_card(card))

    def deal_card(self, player, update_values=True):
        # Deal new card
        new_card = self.deck_obj.deck.pop()
        player.current_hand.append(new_card)

        # Update hand values
        if update_values:
            self.update_hand_values(player)

        # Send new card to card_counter class
        self.card_counter.next_card(new_card)

        return new_card

    def update_hand_values(self, player):
        player.hand_values = self.get_player_value(player.current_hand)
        player.hand_best_value = self.best_player_value(player)

    def is_blackjack(self, card1, card2):
        if (card1 < 0) or (card2 < 0):  # If ace in value calc
            return False
        card1_value = card1 % 13
        card2_value = card2 % 13

        # Ace = 0, 10-King = 9-12
        condition = \
            ((card1_value == 0 and card2_value >= 9 and card2_value <= 12) or
             (card2_value == 0 and card1_value >= 9 and card1_value <= 12))
        if condition:
            return True
        return False

    def get_player_value(self, player_hand, first_run=True):
        if len(player_hand) > 1:
            if self.is_blackjack(player_hand[0], player_hand[1]):
                return 'Blackjack'

        if first_run:
            # Store as list so can have multiple if soft values.
            # Class variable for recursion
            self.player_values = []

        player_value = 0
        for i, card in enumerate(player_hand):
            card_value = card % 13
            if card_value == 0:  # Ace
                new_hand_1 = player_hand.copy()
                new_hand_2 = player_hand.copy()

                new_hand_1[i] = -1  # Ace as 1
                new_hand_2[i] = -2  # Ace as 11

                self.get_player_value(new_hand_1, first_run=False)
                self.get_player_value(new_hand_2, first_run=False)

                break
            else:
                if card == -1:  # Then this is soft 1 ace
                    card_value = 1
                elif card == -2:  # Then this is soft 11 ace
                    card_value = 11
                elif card_value >= 9:  # Then this is 10 or face card
                    card_value = 10
                else:  # Any other card increment by 1 for correct number
                    card_value += 1

                player_value += card_value
        else:  # If there wasn't a 0 signifying un-declared Ace then append
            self.player_values.append(player_value)

        if first_run:
            return self.player_values

    def best_player_value(self, player):
        # If Blackjack
        if player.hand_values == 'Blackjack':
            return player.hand_values

        # If only 1 then return value
        if len(player.hand_values) == 1:
            return player.hand_values[0]
        else:  # Max value less than 21
            best_value = player.hand_values[0]
            for value in player.hand_values[1:]:
                if value > best_value and value <= 21:
                    best_value = value
            return best_value

    def get_dealer_input(self, dealer_value):
        # Dealer play adjusted by ruleset inputs

        # Hard values
        if len(dealer_value) == 1:
            if dealer_value[0] >= self.dealer_stand_on_hard:
                return 1  # STAND
            else:
                return 0  # HIT

        # Soft values
        for value in dealer_value:
            if value >= self.dealer_stand_on_soft and value <= 21:
                return 1  # STAND
        return 0  # HIT

    def player_play(self, player, i=None, print_to_console=True):
        turn_complete = False
        while not turn_complete:
            if print_to_console:
                self.inputoutput.player_current_hand(player, self.deck_obj)

                self.inputoutput.dealer_current_hand(self.dealer,
                                                     self.deck_obj)

            if player.hand_values == 'Blackjack':  # player has blackjack
                self.inputoutput.blackjack()
                turn_complete = True
            elif min(player.hand_values) > 21:  # player went bust
                self.inputoutput.bust()
                turn_complete = True
            else:
                # Check if player can split
                split = False

                if len(player.current_hand) == 2:
                    card1 = self.deck_obj.card_num_or_face(
                        player.current_hand[0])
                    card2 = (self.deck_obj.card_num_or_face(
                        player.current_hand[1]))
                    if card1 == card2:
                        split = True

                # Check if player can insure
                can_insure = False
                if self.dealer.current_hand[0] % 13 == 0:
                    if len(player.current_hand) == 2:
                        can_insure = True

                # Player action
                if type(player) is Player or type(player) is Player_Split:
                    player_action = self.inputoutput.get_player_input(
                        player, split, can_insure, self.deck_obj,
                        self.dealer, human_player=self.human_player)
                elif type(player) is Dealer:
                    player_action = self.get_dealer_input(player.hand_values)

                if player_action == 0:  # HIT
                    print_to_console = False  # Don't print full hand next run
                    new_card = self.deal_card(player)  # Deal next card

                    self.inputoutput.hit(new_card, self.deck_obj, player)

                elif player_action == 1:  # STAND
                    turn_complete = True
                elif player_action == 2:  # DOUBLE DOWN
                    # Double player's bet
                    assert (player.bankroll >= player.bet * 2) and (len(
                        player.current_hand) <= 2)
                    player.bet = player.bet * 2

                    # Deal new card
                    new_card = self.deal_card(player)  # Deal next card
                    turn_complete = True  # User's turn complete

                    # Output double down to player
                    self.inputoutput.double_down(new_card, self.deck_obj,
                                                 player)

                elif player_action == 3:  # SPLIT
                    assert (len(player.current_hand) == 2) and \
                        (self.deck_obj.card_num_or_face(player.current_hand[0])
                         == (self.deck_obj.card_num_or_face(player.
                             current_hand[1])))
                    # If player can split then create new player_split objects
                    # for each and add them to self.players
                    player_split_1 = Player_Split(player, 1)
                    player_split_2 = Player_Split(player, 2)

                    # Update hand values
                    self.update_hand_values(player_split_1)
                    self.update_hand_values(player_split_2)

                    # Delete cards from original player's hand
                    player.current_hand = []

                    # Add new players to the self.players list so they are
                    # called right after this loop
                    for i, ele in enumerate(self.players):
                        if ele is player:
                            self.players.insert(i+1, player_split_1)
                            self.players.insert(i+2, player_split_2)

                    # Output split move to user
                    self.inputoutput.split(player)

                    turn_complete = True

                elif player_action == 4:  # SURRENDER
                    # Must be first player move and whether works vs blackjack
                    # is early/late parameter
                    assert len(player.current_hand) <= 2
                    player.hand_best_value = 'Surrender'

                    # Output surrender move to user
                    self.inputoutput.surrender(player)

                    turn_complete = True

                elif player_action == 5:  # INSURANCE
                    # Insurance against face up Ace gets you half bet back if
                    # blackjack. Usually never optimal.
                    # Note: insurance is only worthwhile if more 10 cards than
                    # non in deck
                    # Insure for half of current bet by default: could make
                    # dynamic in future

                    # First turn
                    assert self.deck_obj.card_num_or_face(
                        self.dealer.current_hand[0]) == 'Ace'  # First turn
                    # Enough cash
                    assert player.bankroll >= (player.bet + player.bet//2)
                    # Insurance hasn't been taken
                    assert player.insurance_bet == 0
                    player.insurance_bet = player.bet//2

                    # Output insurance move to user
                    self.inputoutput.insurance(player)

                else:
                    raise ValueError('Error: player action is not an \
                        integer 0-4')

        if self.print_to_terminal:
            print('')

    def compare_hands(self, player, dealer):
        # Takes in hands and returns and payout

        if player.hand_best_value == 'Blackjack':  # Player blackjack
            if dealer.hand_best_value == 'Blackjack':  # Dealer blackjack
                return self.push_payout
            else:
                return self.blackjack_payout

        if dealer.hand_best_value == 'Blackjack':  # Dealer only blackjack
            if player.hand_best_value == 'Surrender' and self.early_surrender:
                return self.surrender_payout
            else:
                return self.loss_payout

        if player.hand_best_value == 'Surrender':  # Late surrender
            return self.surrender_payout

        if player.hand_best_value > 21:  # Player went bust
            return self.loss_payout
        elif dealer.hand_best_value > 21:  # Dealer went bust
            return self.win_payout

        if dealer.hand_best_value == player.hand_best_value:  # Same value
            return self.push_payout
        elif player.hand_best_value > dealer.hand_best_value:  # Player >
            return self.win_payout
        elif player.hand_best_value < dealer.hand_best_value:  # Dealer >
            return self.loss_payout
        else:
            raise ValueError('Error: player and dealer best value not \
                compatible')

    def discard_hand(self, player):
        while len(player.current_hand) > 0:
            self.deck_obj.discard_deck.append(player.current_hand.pop())

    def discard_all_hands(self):
        for player in self.players:
            self.discard_hand(player)
        self.discard_hand(self.dealer)

    def take_bets(self):
        # 1. Bet amount is logged into private variable
        for player in self.players:
            player.bet = self.inputoutput.get_user_bets(
                player,
                human_player=self.human_player
                )

    def check_insurance_payout(self, player):
        if player.insurance_bet > 0:
            if self.dealer.hand_best_value == 'Blackjack':
                return player.insurance_bet * 2
            else:
                return player.insurane_bet * -1
        return 0

    def play_hand(self):
        # 2. Dealer gives 1 card to player (each player if multiple)
        for player in self.players:
            self.deal_card(player)

        # 3. Dealer gives 1 card to themself face up
        self.deal_card(self.dealer)

        # 4. Dealer gives 2nd card to player (each player if multiple)
        for player in self.players:
            self.deal_card(player)

        # 5. Dealer gives 2nd card to themself. Dealt face down so don't
        # reveal to player
        self.deal_card(self.dealer)

        # 6. Dealer peeks / does not peek for Blackjack
        if self.dealer_peeks_for_bj:
            if self.dealer.hand_best_value == 'Blackjack':
                pass
        else:
            # 7. Players are prompted on move
            for i, player in enumerate(self.players):
                self.player_play(player, i)

        # 8. Dealer plays
        self.inputoutput.dealer_flip_card(self.dealer, self.deck_obj)

        self.player_play(self.dealer, print_to_console=False)

        # 9. Review player hands and payout money
        for i, player in enumerate(self.players):
            if len(player.current_hand) > 0:  # as long as hand wasn't split
                # Get payout rate
                player_payout = self.compare_hands(player, self.dealer)
                original_bankroll = int(player.get_bankroll())
                new_bankroll = int(original_bankroll +
                                   player_payout * player.bet)

                self.inputoutput.player_current_hand_vs_dealer(
                    player, self.dealer, self.deck_obj)

                self.inputoutput.payout(
                    player, player_payout, original_bankroll, new_bankroll)

                # Any insurance
                insurance_payout = self.check_insurance_payout(player)
                self.inputoutput.insurance_payout(player, insurance_payout)

                # Update player bankroll
                player.update_bankroll(
                    player_payout * player.bet + insurance_payout)
                player.bet = 0
                player.insurance_bet = 0

        # 10. Put all cards into discard deck
        self.discard_all_hands()

        # 11. Delete any split players
        self.players = [player
                        for player in self.players
                        if type(player) is Player]
        for player in self.players:
            player.reset_children()

        # 12. Check if deck needs to be reshuffled
        pen = self.num_of_decks*52 * (1 - self.reshuffle_penetration)
        if len(self.deck_obj.deck) <= pen:
            self.shuffle(re_add_discard_deck=True)

    def play_round(self):
        self.take_bets()

        self.play_hand()

    def play_game(self, rounds=1):
        self.inputoutput.welcome()

        for _ in range(rounds):
            self.play_round()
