# Miscellaneous code for testing during development

# In[]: Is it faster to append and refer to a dictionary or 2 lists?
import random
from timeit import default_timer

players = ['Player 1', 'Player 2', 'Player 3']
sims = 1000000


def timer(func):
    def wrapper_timer(*args, **kwargs):
        start = default_timer()
        result = func(*args, **kwargs)
        end = default_timer()
        print('Function \'{}\' took {:.7f}s to run'.format(func.__name__,
              end-start))
        return result
    return wrapper_timer()


@timer
def test_list():
    lst = [[] for player in players]
    for _ in range(sims):
        for i, _ in enumerate(players):
            lst[i].append(i)


@timer
def test_dic():
    dic = {player: [] for player in players}
    for _ in range(sims):
        for i, player in enumerate(players):
            dic[player].append(i)

# Conclusion: they are about the same so use dic/hash table for readability

# In[]: Kelly Criterion simulation tests of mathematical proof


odds_to_win = 0.8
static_bet_size = 0.8


def win_or_loss():
    return random.random() <= odds_to_win


def gamble(times, starting_cash, print_cash=True):
    cash = starting_cash
    bet_size = static_bet_size
    for _ in range(times):
        bet = bet_size*cash
        if win_or_loss():
            cash += bet
        else:
            cash -= bet
        if print_cash:
            print('$ {:,.0f}'.format(cash))

    return cash


def gamble_kelly_criterion(times, starting_cash, print_cash=True):
    cash = starting_cash
    bet_size = (odds_to_win*2)-1
    for _ in range(times):
        bet = bet_size*cash
        if win_or_loss():
            cash += bet
        else:
            cash -= bet
        if print_cash:
            print('$ {:,.0f}'.format(cash))

    return cash


def test_kelly_criterion():
    '''Simple snippet to test the Kelly Criterion vs other gambling ratios'''
    kelly_wins = 0
    for _ in range(1000):
        result = gamble(times=100, starting_cash=1000, print_cash=False)
        result2 = gamble_kelly_criterion(times=100, starting_cash=1000,
                                         print_cash=False)
        if result2 > result:
            kelly_wins += 1

    print('Kelly criterion beats {:.0f}% bet {} times out of 1000'.
          format(static_bet_size*100, kelly_wins))


# In[]: Code to convert Edward O Thorps basic strategy from 1960s Beat the
# Dealer to dic/JSON for use in BasicStrategy method


def read_basic_strat():
    string = '''
4	H	H	H	H	H	H	H	H	H	H
5	H	H	H	H	H	H	H	H	H	H
6	H	H	H	H	H	H	H	H	H	H
7	H	H	H	H	H	H	H	H	H	H
8	H	H	H	H	H	H	H	H	H	H
9	H	D	D	D	D	H	H	H	H	H
10	D	D	D	D	D	D	D	D	H	H
11	D	D	D	D	D	D	D	D	D	H
12	H	H	S	S	S	H	H	H	H	H
13	S	S	S	S	S	H	H	H	H	H
14	S	S	S	S	S	H	H	H	H	H
15	S	S	S	S	S	H	H	H	H	H
16	S	S	S	S	S	H	H	H	H	H
17	S	S	S	S	S	S	S	S	S	S
18	S	S	S	S	S	S	S	S	S	S
19	S	S	S	S	S	S	S	S	S	S
20	S	S	S	S	S	S	S	S	S	S
21	S	S	S	S	S	S	S	S	S	S
A,2	H	H	H	D	D	H	H	H	H	H
A,3	H	H	H	D	D	H	H	H	H	H
A,4	H	H	D	D	D	H	H	H	H	H
A,5	H	H	D	D	D	H	H	H	H	H
A,6	H	D	D	D	D	H	H	H	H	H
A,7	S	D	D	D	D	S	S	H	H	H
A,8	S	S	S	S	S	S	S	S	S	S
A,9	S	S	S	S	S	S	S	S	S	S
2,2	P	P	P	P	P	P	H	H	H	H
3,3	P	P	P	P	P	P	H	H	H	H
4,4	H	H	H	P	P	H	H	H	H	H
5,5	D	D	D	D	D	D	D	D	H	H
6,6	P	P	P	P	P	H	H	H	H	H
7,7	P	P	P	P	P	P	H	H	H	H
8,8	P	P	P	P	P	P	P	P	P	P
9,9	P	P	P	P	P	S	P	P	S	S
T,T	S	S	S	S	S	S	S	S	S	S
A,A	P	P	P	P	P	P	P	P	P	P
            '''

    dic = {}
    count = 12
    next_row_header = ''
    for char in string:
        if ord(char) is not 10:
            if count == 12:  # New row
                if ord(char) is not 9:
                    next_row_header += char
                else:
                    row_header = next_row_header
                    next_row_header = ''
                    dic[row_header] = {}
                    count = 2
            else:
                if ord(char) is not 9:
                    dic[row_header][count] = char
                    count += 1

    for key in dic:
        print('\'{}\': '.format(key), end='')
        print(dic[key], end='')
        print(',')
