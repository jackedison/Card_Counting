class BasicStrategy():
    '''Class to implement Edward Thorps basic Blackjack strategy. Used by
    machine based on current hand.'''
    def __init__(self):
        # H = Hit, S = Stand, D = Double down, P = Split
        self.basicstrategy_dic = {
            '2': {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H',
                  8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '3': {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H',
                  8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '4': {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H',
                  8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '5': {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H',
                  8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '6': {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H',
                  8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '7': {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H',
                  8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '8': {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H',
                  8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '9': {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H',
                  8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '10': {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D',
                   8: 'D', 9: 'D', 10: 'H', 11: 'H'},
            '11': {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D',
                   8: 'D', 9: 'D', 10: 'D', 11: 'H'},
            '12': {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H',
                   8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '13': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H',
                   8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '14': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H',
                   8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '15': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H',
                   8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '16': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H',
                   8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '17': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                   8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            '18': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                   8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            '19': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                   8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            '20': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                   8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            '21': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                   8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            'A,2': {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            'A,3': {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            'A,4': {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            'A,5': {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            'A,6': {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            'A,7': {2: 'S', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'S',
                    8: 'S', 9: 'H', 10: 'H', 11: 'H'},
            'A,8': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                    8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            'A,9': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                    8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            'A,10': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                     8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            '2,2': {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '3,3': {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '4,4': {2: 'H', 3: 'H', 4: 'H', 5: 'P', 6: 'P', 7: 'H',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '5,5': {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D',
                    8: 'D', 9: 'D', 10: 'H', 11: 'H'},
            '6,6': {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'H',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '7,7': {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P',
                    8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            '8,8': {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P',
                    8: 'P', 9: 'P', 10: 'P', 11: 'P'},
            '9,9': {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'S',
                    8: 'P', 9: 'P', 10: 'S', 11: 'S'},
            'T,T': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S',
                    8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            'A,A': {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P',
                    8: 'P', 9: 'P', 10: 'P', 11: 'P'},
        }

    def get_move(self, player, dealer):
        dealer_card = self.get_dealer_card(dealer)

        # Check whether player has splitable hand
        if len(player.current_hand) == 2 and \
                player.current_hand[0] % 13 == player.current_hand[1] % 13:
            player_card = self.get_player_card(player.current_hand[0])
            hand = player_card + ',' + player_card
        elif len(player.hand_values) > 1:  # Check if player has an ace
            # Hand value [1] will always be 1 ace at 11, rest at 1.
            # e.g. A-2-A treated like an ace-3
            hand_minus_ace = player.hand_values[1] - 11
            if hand_minus_ace == 0:
                hand = '11'  # split A-A so have Ace vs dealer, treat as an 11
            elif hand_minus_ace <= 10:
                hand = 'A,' + str(hand_minus_ace)
            else:
                hand = str(hand_minus_ace+1)  # A-10-2 is just 13, not A,12
        else:   # Any other value
            hand = str(player.hand_values[0])

        return self.basicstrategy_dic[hand][dealer_card]

    def get_dealer_card(self, dealer):
        dealer_card = dealer.current_hand[0] % 13

        if dealer_card == 0:  # Ace
            return 11
        elif dealer_card < 9:  # Number card
            return dealer_card+1
        else:
            return 10  # 10, J, Q, K

    def get_player_card(self, card):
        player_card = card % 13

        if player_card == 0:  # Ace
            return 'A'
        elif player_card < 9:  # Number card
            return str(player_card+1)
        else:
            return 'T'  # 10, J, Q, K
