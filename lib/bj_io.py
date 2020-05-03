from .strategy import BasicStrategy


class InputOutput():
    '''InputOutput class to control any input or output while playing
       Blackjack. Options to print to terminal or not for large simulations.
       Segregation of code into its own class allows a UI to be implemented
       here in the future'''
    def __init__(self, card_counter, print_to_terminal=True):
        self.card_counter = card_counter
        self.basicstrategy = BasicStrategy()

        self.print_to_terminal = print_to_terminal

    def terminal(self, msg):
        if self.print_to_terminal:
            print(msg)

    def welcome(self):
        self.terminal('Welcome to Blackjack')

    def get_player_input(self, player, split, can_insure, deck_obj, dealer,
                         human_player=True):
        while True:
            if human_player:
                value = input('Player {} ({}) what is is your move? '
                              '(HIT, STAND, DD, SPLIT, SURR, INSUR): '
                              .format(player.num, player.name))
                value = value.upper()  # Uppercase it

                if 'HIT' in value:
                    return 0
                elif 'STAND' in value:
                    return 1
                elif 'DD' in value:
                    if self.can_double_down(player):
                        return 2
                elif 'SPLIT' in value:
                    if split is True:
                        return 3
                    else:
                        print('You cannot split with a {}'.format(
                            self.hand_to_print(deck_obj, player.current_hand)))
                elif 'SURR' in value:
                    if self.can_surrender(player):
                        return 4
                elif 'INSUR' in value:
                    if can_insure(player, dealer, deck_obj):
                        return 5
                else:
                    print('Incorrect input. Please try again.')
            else:  # Machine
                move = self.basicstrategy.get_move(player, dealer)
                if move == 'H':  # Hit
                    return 0
                elif move == 'S':  # Stand
                    return 1
                elif move == 'D':  # Double down
                    if self.can_double_down(player):
                        return 2
                    else:
                        self.terminal('Hit instead')
                        return 0  # Hit if no bankroll to double down
                elif move == 'P':  # Split
                    if split is True:
                        return 3
                    else:
                        raise ValueError('Basic strategy trying to split non \
                            splittable hand')
                elif move == 'SS':  # Surrender
                    if self.can_surrender(player):
                        return 4
                    else:
                        raise ValueError('Basic strategy is trying to \
                            surrender')
                elif move == 'U':  # Insurance
                    if self.can_insure(player, dealer, deck_obj):
                        return 5
                    else:
                        raise ValueError('Basic strategy is trying to insure')
                else:
                    raise ValueError('Basic strategy returning non programmed \
                        move ({})'.format(move))

                raise ValueError('No computer player implemented')

    def can_double_down(self, player):
        if player.bankroll < player.bet * 2:
            self.terminal('Bankroll not enough to double')
            return False
        elif len(player.current_hand) > 2:
            self.terminal('You cannot double down unless you are on the first \
                turn')
            return False
        else:
            return True

    def can_surrender(self, player):
        if len(player.current_hand) <= 2:
            return True
        else:
            self.terminal('You cannot surrender unless you are on the first \
                turn')
            return False

    def can_insure(self, player, dealer, deck_obj):
        if deck_obj.card_num_or_face(dealer.current_hand[0]) != 'Ace':
            self.terminal('You can only insure if dealer has face up Ace')
            return False
        elif player.bankroll < (player.bet + player.bet//2):
            self.terminal('You do not have enough bankroll to insure')
            return False
        elif player.insurance_bet != 0:
            self.terminal('You have already taken insurance on this hand')
            return False
        else:
            return True

    def hand_to_print(self, deck_obj, player_hand):
        str_to_print = deck_obj.read_card(player_hand[0])
        for hand in player_hand[1:]:
            str_to_print += ' and {}'.format(deck_obj.read_card(hand))
        return str_to_print

    def new_card_dealt(self, player_name, player_num):
        pass

    def player_current_hand(self, player, deck_obj):
        str_to_print = 'Player {} ({}): You have {} - {}'.format(
            player.num, player.name,
            self.hand_to_print(deck_obj, player.current_hand),
            player.hand_values)
        self.terminal(str_to_print)

    def player_current_hand_vs_dealer(self, player, dealer, deck_obj):
        str_to_print = 'Player {} ({}): You have {} - {} vs dealer {}'.format(
            player.num, player.name,
            self.hand_to_print(deck_obj, player.current_hand),
            player.hand_best_value, dealer.hand_best_value)
        self.terminal(str_to_print)

    def dealer_current_hand(self, dealer, deck_obj):
        self.terminal('Dealer has a ' +
                      deck_obj.read_card(dealer.current_hand[0]))

    def blackjack(self):
        self.terminal('Blackjack!')

    def bust(self):
        self.terminal('Bust!')

    def hit(self, new_card, deck_obj, player):
        self.terminal('HIT: next card {} - {}'.format(
            deck_obj.read_card(new_card), player.hand_values))

    def double_down(self, new_card, deck_obj, player):
        self.terminal('Player {} ({}) double down. Player bet doubled from \
            ${} to ${}'.format(player.num, player.name,
                               player.bet//2, player.bet))
        self.terminal('HIT: next card {} - {}'.format(
            deck_obj.read_card(new_card), player.hand_values))

        # Check if they got a blackjack or went bust and if so tell them
        if player.hand_values == 'Blackjack':
            self.blackjack()
        elif min(player.hand_values) > 21:  # player went bust
            self.bust()

    def split(self, player):
        self.terminal('Player {} ({}) split'.format(player.num, player.name))

    def surrender(self, player):
        self.terminal('Player {} ({}) surrender. Half bet (${}) forfeited'.
                      format(player.num, player.name, player.bet//2))

    def insurance(self, player):
        pass

    def dealer_flip_card(self, dealer, deck_obj):
        self.terminal('Dealer goes:')
        self.terminal('Dealer has {}'.format(
            deck_obj.read_card(dealer.current_hand[0])))
        self.terminal('Dealer flips over {} - {}'.format(
            deck_obj.read_card(dealer.current_hand[1]),
            dealer.hand_values))

    def payout(self, player, player_payout, original_bankroll, new_bankroll):
        self.terminal('Bet of ${} payout {}x. Bankroll ${}->${}'.format(
            player.bet, player_payout, original_bankroll, new_bankroll))

    def insurance_payout(self, player, insurance_payout):
        if insurance_payout > 0:  # Insurance bet taken and won
            self.terminal('Insurance bet of ${} won. Paid out ${}'.format(
                player.insurance_bet, insurance_payout))
        elif insurance_payout < 0:  # Insurance bet taken and loss
            self.terminal('Insurance bet of ${} lost'.format(
                player.insurance_bet))
        else:  # No insurance bet taken
            pass

    def start_hand(self, round):
        self.terminal('Hand {}'.format(round))

    def end_hand(self, round):
        self.terminal('Hand {} finished\n'.format(round))

    def get_user_bets(self, player, human_player=True):
        collecting_input = True
        while collecting_input:
            # Get user input
            if human_player:
                bet = input('Player {} ({}) place your bet (Bankroll ${}): '.
                            format(player.num, player.name, player.bankroll))
            else:
                bet = self.card_counter.get_suggested_bet()
                self.terminal(('Player {} ({}) has bankroll ${} and bet ${}): '
                               .format(player.num, player.name,
                                       player.bankroll, bet)))
            try:
                bet = int(bet)
            except TypeError:
                print('Incorrect input, please input an integer')

            # Check they have enough
            if player.bankroll < bet:
                print('{} you do not have enough bankroll to bet ${}. '
                      'Current bankroll ${}'.format(player.name, bet,
                                                    player.bankroll))
            else:
                collecting_input = False

        self.terminal('')
        return bet
