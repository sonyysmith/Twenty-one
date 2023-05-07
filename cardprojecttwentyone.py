'''Project: Twenty One Game:
Course: CS 1410-X03
Name: Emerson Smith
Due Date: Feb 22, 2023

Description:
For this project you will implement a game of
Twenty-One with a dealer and one player using classes and
objects to create the game.
'''
import os
import random


class Card:
    '''This defines each possible variation of card'''
    def __init__(self, suit, value, numeric_value):
        self.suit = suit
        self.value = value
        self.numeric_value = numeric_value
        self.hidden = False

    def unhide(self):
        self.hidden = False
        
    def hide(self):
        '''Hides the dealers last card'''
        self.hidden = True
    def __str__ (self):
        return """------------------
|                |
| %2s             |
|                |
|                |
|                |
|                |
|       %1s        |
|                |
|                |
|                |
|                |
|             %2s |
|                |
------------------""" % ("?" if self.hidden else self.value,'' if self.hidden else self.suit, '?' if self.hidden else self.value)

class Deck:
    '''Creates the deck the dealer uses'''

    def __init__(self):
        self.cards = []
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        suits_values = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}
        cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        numeric_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
        for suit in suits:
            for card in cards:
                self.cards.append(Card(suits_values[suit], card, numeric_values[card]))

    def hit(self):
        '''The hit function'''
        return self.cards.pop()

    def shuffle(self):
        '''Shuffle function'''
        random.shuffle(self.cards)



class Hand:
    '''The hand class that adds card to the hand'''

    def __init__(self):
        self.Deck = Deck()
        self.cards = []


    def add(self, card, hidden):
        '''Adds the cards'''
        if hidden:
            card.hide()
        self.cards.append(card)
    def __str__ (self):
        card_pic = []
        final_image = ''
        for card in self.cards:
            card_pic.append(str(card))
        card_split = [card.split("\n") for card in card_pic]
        zipped = zip(*card_split)
        for elems in zipped:
            final_image += ("   ".join(elems)) + "\n"
        return final_image

    def __len__(self):
        return len(self.cards)

    def total_sum(self):
        '''Total sum of cards'''
        total = 0
        for card in self.cards:
            if not card.hidden:
                if card.value == 'A' and 21 - total < 11:
                    total += 1
                else:
                    total += card.numeric_value
        return total

class Dealer:
    '''Dealer Class'''
    def __init__(self):
        self.hand = Hand()
        self.deck = Deck()
        self.deck.shuffle()
    
    def deal(self):
        '''deals the cards'''
        return self.deck.hit()
    
    def __str__(self):
        '''Prints the dealer card and score'''
        return str(self.hand) + "\nDEALER SCORE = %s" % (self.hand.total_sum())

    def hidden_change(self):
        '''Changes the hidden function'''
        for card in self.hand.cards:
            card.unhide()


class Player:
    '''Player plays a hand, player can either stand or hit'''
    def __init__(self):
        self.hand = Hand()
    
    def __str__(self):
        '''Prints the cards and player score'''
        return str(self.hand) + "\nPLAYER SCORE = %s" %(self.hand.total_sum())
class Game:
    '''Class to run the game'''
    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()
    
    def run(self):
        '''Runs the game, adds the players and dealers cards while hiding one of them'''
        self.player.hand.add(self.dealer.deal(), False)
        self.dealer.hand.add(self.dealer.deal(), False)
        self.player.hand.add(self.dealer.deal(), False)
        self.dealer.hand.add(self.dealer.deal(), True)

    def game_running(self):
        '''Runs the game'''
        return self.game_running == True

def clear():
   """Clear the console."""
   # for windows
   if os.name == 'nt':
      _ = os.system('cls')
   # for mac and linux, where os.name is 'posix'
   else:
      _ = os.system('clear')

def main():
    '''Main function'''
    run_the_game = True
    deck = Deck()
    game = Game()
    game.run()
    deck.shuffle()
    print(str(game.player))
    print(str(game.dealer))
    while run_the_game:
        while game.player.hand.total_sum() <= 21:
            if game.dealer.hand.total_sum() >= 17:
                if game.player.hand.total_sum() >= 17:
                    if game.dealer.hand.total_sum() > game.player.hand.total_sum():
                        print("The dealer wins!")
                        run_the_game = False
                        break
                    else:
                        print("The player wins!")
                        run_the_game = False
                        break
            if game.player.hand.total_sum() == 21:
                print("The player wins!")
                run_the_game = False
                break
            play = input("Would you like to stand or hit?: ").lower()
            if play == "stand":
                print(game.dealer.hand.total_sum())
                while game.dealer.hand.total_sum() < 17 or game.player.hand.total_sum() >= game.dealer.hand.total_sum():
                    game.dealer.hidden_change()
                    if game.dealer.hand.total_sum() <= game.player.hand.total_sum() and game.dealer.hand.total_sum() < 17:
                        game.dealer.hand.add(game.dealer.deal(), False)
                    print(game.player)
                    print(game.dealer)
                    if game.dealer.hand.total_sum() == 21:
                        print("The dealer wins!")
                        run_the_game = False
                        return
                    elif game.dealer.hand.total_sum() > 21:
                        print("The dealer busts, the player wins!")
                        run_the_game = False
                        return
                    elif game.dealer.hand.total_sum() > game.player.hand.total_sum():
                        print("The dealer wins!")
                        run_the_game = False
                        return
                    elif game.dealer.hand.total_sum() <= game.player.hand.total_sum() and game.dealer.hand.total_sum() >= 17 and game.dealer.hand.total_sum() != game.player.hand.total_sum():
                        print("The player wins!")
                        run_the_game = False
                        return
                    elif game.dealer.hand.total_sum() == game.player.hand.total_sum() and game.dealer.hand.total_sum() >= 17:
                        print("It's a tie!")
                        run_the_game = False
                        return
            elif play == "hit":
                game.player.hand.add(game.dealer.deal(), False)
                print(game.player)
                print(game.dealer)
                if game.player.hand.total_sum() > 21:
                    print("The player busts!")
                    return
                elif game.player.hand.total_sum() == 21:
                    print("The player wins!")
                    return
            else:
                print("please enter whether you would like to stand or hit.")
        if game.dealer.hand.total_sum() == 21 and game.player.hand.total_sum() == 21:
            print("Its a tie!")
            return

if __name__ == '__main__':
    main()