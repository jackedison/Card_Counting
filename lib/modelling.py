from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from scipy.stats import norm
import numpy as np
import os


def plot_hands(players, data, hand_num, showfig=False):
    #hand_num = [[i for i in range(1, len(data[0])+1)] for player in players]

    if not showfig:
        plt.ioff()

    plt.figure(figsize=(18, 9))

    for i, _ in enumerate(players):
        plt.plot(hand_num[i], data[i])

    plt.plot([1, hand_num[0][-1]], [data[0][0], data[0][0]],
             linestyle='dashed')

    plt.xlabel('Hands', fontsize=18)
    plt.ylabel('Player Bankroll', fontsize=18)
    plt.title('Player bankrolls through session', fontweight='heavy',
              fontsize=20)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.xlim(0, hand_num[0][-1])

    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))

    plt.legend([name for name in players], fontsize=16)

    fig_loc = 'Figures' + os.sep
    file_name = 'player_bankrolls.png'
    plt.savefig('{}{}'.format(fig_loc, file_name), bbox_inches='tight')

    print('Matplotlib figures saved to {}'.format(fig_loc))

    if not showfig:
        plt.close()


def plot_distr(data, means, stds, mean, std, params, player_advantage,
               showfig=False):

    if not showfig:
        plt.ioff()

    fig, axs = plt.subplots(2, 2, figsize=(20, 10))
    fig.tight_layout(pad=-5)

    # Plot distribution of final bankrolls of all players
    if len(data) > 1:
        ax = axs[0][0]
        all_data = [bankroll for value in data.values() for bankroll in value]

        ax.hist(all_data, bins='sqrt', color='green', density=True)

        # Add best fit gaussian distr.
        x = np.linspace(min(all_data), max(all_data), 100)
        y = norm.pdf(x, mean, std)
        ax.plot(x, y, color='red', linewidth=3, linestyle='dashed')

        ax.xaxis.set_minor_locator(AutoMinorLocator())

        ax.grid(axis='x', which='both')

        ax.set_title('All round simulations', fontsize=17)
        ax.set_xlabel('Final bankroll', fontsize=16)

        # Add text
        plt.text(0.67, 0.95, 'Player advantage: {:.2f}%'.
                 format(player_advantage*100),
                 transform=ax.transAxes, fontsize=14)
        plt.text(0.67, 0.9, 'Standard deviation: ${:.2f}'.format(std),
                 transform=ax.transAxes, fontsize=14)

    # Plot distribution of final bankrolls for each player
    for i, player in enumerate(data):
        nrow = (i+1)//2
        ncol = (i+1) % 2
        ax = axs[nrow][ncol]

        ax.hist(data[player], bins='sqrt', density=True)

        # Add best fit gaussian distr.
        x = np.linspace(min(data[player]), max(data[player]), 100)
        y = norm.pdf(x, mean, std)
        ax.plot(x, y, color=(1, 0.35, 0.35), linewidth=3, linestyle='dashed')

        ax.xaxis.set_minor_locator(AutoMinorLocator())

        ax.grid(axis='x', which='both')

        ax.set_title('{} round simulations'.format(player), fontsize=17)
        ax.set_xlabel('Final bankroll', fontsize=16)

    # Adjust fig formatting and save
    plt.subplots_adjust(hspace=0.2, wspace=0.2)

    import os

    fig_loc = 'Figures' + os.sep
    file_name = '{}.png'.format(params)
    plt.savefig('{}{}'.format(fig_loc, file_name), bbox_inches='tight')

    print('Matplotlib figures saved to {}'.format(fig_loc))

    if not showfig:
        plt.close(fig)
