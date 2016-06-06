# -*- coding: utf-8 -*-
"""
Created on Mon Jun 06 11:27:51 2016

@author: v-wujin
"""
import matplotlib.pyplot as plt
import pandas as pd

'''This script demonstrates simulations of coin flipping'''
import random
from scipy.stats import truncnorm

# let's create a fair coin object that can be flipped:

class Coin(object):
    sides = [str(int(n)) for n in list(truncnorm(a=0, b=1, scale=100).rvs(size=100))] # Mine (non-strings don't work?!)
    last_result = None

    def flip(self):
        '''call coin.flip() to flip the coin and record it as the last result'''
        self.last_result = result = random.choice(self.sides)
        return result

# let's create some auxilliary functions to manipulate the coins:

def create_coins(number):
    '''create a list of a number of coin objects'''
    return [Coin() for _ in range(number)]

def flip_coins(coins):
    '''side effect function, modifies object in place, returns None'''
    for coin in coins:
        coin.flip()

def count_heads(flipped_coins):
    return sum(coin.last_result == '1' for coin in flipped_coins)

def count_tails(flipped_coins):
    return sum(coin.last_result == '2' for coin in flipped_coins)


def main():
    coins = create_coins(1000)
    dist = []
    for i in range(100):
        flip_coins(coins)
        n = count_heads(coins) 
        dist.append(n) 
        
    pd.Series(dist).hist()
    plt.show() 

if __name__ == '__main__':
    main()