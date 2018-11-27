import readline
import random
import sqlite3


db = sqlite3.Connection('cards.sql')
sql = db.execute
sql('DROP TABLE IF EXISTS cards;')
sql('CREATE TABLE cards(card, who);')

points = {'A': 1, 'J': 10, 'Q': 10, 'K': 10}
for n in range(2, 11):
    points.update({n: n})


def score(who):
    cards = sql('SELECT card FROM cards WHERE who == ?;', [who])
    return hand_score([card[0] for card in cards.fetchall()])

def hand_score(hand):
    scores = sum([points[card] for card in hand])
    if scores <= 11 and 'A' in hand:
        return scores + 10
    return scores   

def bust(who):
    '''return if the player or dealer is busted'''
    return score(who) > 21


def deal(card, who):
    sql('INSERT INTO cards VALUES (?, ?)', [card, who])
    db.commit()

player, dealer = 'Player', 'Dealer'

def play(deck):
    '''Play a hand of BlackJack'''
    deal(deck.pop(), player)
    deal(deck.pop(), player)
    deal(deck.pop(), dealer)
    hidden_card = deck.pop()

    while 'y' in input('You have ' + str(score(player)) + '. Hit?\n').lower():
        deal(deck.pop(), player)
        if bust(player):
            print('Yeeeehah!', player, 'has', score(player), 'and went bust!')
            dealer_wins += 1
            return 

    deal(hidden_card, dealer)
    while score(dealer) < 17:
        deal(deck.pop(), dealer)
        if bust(dealer):
            print('WOOAH!', dealer, 'went bust!')
            player_wins += 1
            return
    return win(player, dealer)
    

def win(player, dealer):
    player_score = score(player)
    dealer_score = score(dealer)
    print(player, player_score, 'and', dealer, dealer_score)
    if player_score > dealer_score:
        print(player, 'won!')
        player_wins += 1
    else:
        print(dealer, 'won!')
        dealer_wins += 1

def print_wins(who):
    if who == 'Player':
        return 'Player ' + player_wins + ' wins.'
    else:
        return 'Dealer ' + dealer_wins + 'wins.'

'''TAKING TURNS'''

while True:
    sql('DROP TABLE IF EXISTS cards;')
    sql('CREATE TABLE cards(card, who);')

    print('Shuffling the deck......')

    deck = 4 * (list (points.keys()))
    random.shuffle(deck)

    player_wins, dealer_wins = 0, 0
    while len(deck) > 15:
        print('\nDealingggggg')
        play(deck)
        sql('UPDATE cards SET who == "DISCARD";')
        db.commit()
    
    print('\nTally:', print_wins(player), print(dealer))
    print('\n****Starting a NEW game****')




