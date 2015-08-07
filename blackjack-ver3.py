'''

BlackJack Game

User Stories:

1) User can play the blackjack game in terminal against the dealer
2) Dealer automatically plays his hand with a fixed algorithm (If it's 16 or below they hit, if it's above 16, they stay)
3) User can play the blackjack game repeatedly
4) User can choose to hit or stay
5) User can see what cards they have been dealt
6) User can only see one dealer card, not the bottom card

Tips:
1) Aces can count as an eleven or a one - but it only counts as a one if your score is over 21
2) Research random.shuffle()
3) You are not allowed to code until you design your program!
4) Research __radd__ - it is a built-in method in Python

Extension:
1) Multiple users can play blackjack game in terminal in a turn-based game
2) Consider using the stack data structure
3) User can bet dollar amounts in the blackjack game


'''
import random

card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
card_suits = ('c', 'd', 'h', 's')

border = "***********************************************"

def triple_border():
    for x in range(3):
        print(border)

class Deck:
    def __init__(self):
        self.stack = []
        self.shuffle()

    def shuffle(self):
        self.stack = [Card(value, suit) for value in card_values.keys() for suit in card_suits]
        #creates array of all 52 unique combinations
        random.shuffle(self.stack)

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.name = ("%s%s" % (self.value, self.suit))
    def __add__(self, other):
        return card_values[self.value] + card_values[other.value]
    def __radd__(self, other):
        if type(other) == int:
            return card_values[self.value] + other
        else:
            return card_values[self.value] + card_values[other.value]

class Player:
    def __init__(self, name):
        self.name = name
        self.up_cards = []
        self.twenty_one = False #if total is ever 21, automatically stand
        self.natural = False
        self.total = 0
        self.has_aces = 0
        self.busted = False
        self.money = 1000.0
        self.bet = 50

    def new_hand(self, card1, card2):
        self.busted = False
        self.twenty_one = False
        self.natural = False
        self.up_cards = []
        self.up_cards.append(card1)
        self.up_cards.append(card2)
        self.update_total()
        if self.total == 21:
            self.twenty_one = True
            self.natural = True
            return "BLACKJACK"

    def update_total(self):
        self.total = 0
        self.has_aces = 0
        for card in self.up_cards:
            self.total += card_values[card.value]
            if card.value == 'A':
                self.has_aces += 1
        while self.total > 21:
            if self.has_aces == 0:
                self.bust()
                break
            else:
                self.total -= 10
                self.has_aces -= 1
        if self.total == 21:
            self.twenty_one = True

    def display_hand(self):
        if self.has_aces:
            print("("),
            for card in self.up_cards:
                print card.name,
            print(") - soft %d" % (self.total))
        else:
            print("("),
            for card in self.up_cards:
                print card.name,
            print(") - %d" % (self.total))

    def hit(self, card):
        print("%s hits and receives %s." % (self.name, card.name))
        self.up_cards.append(card)
        self.update_total()

    def stand(self):
        print("%s stands." % self.name)

    def bust(self):
        self.display_hand()
        print("%s busts." % self.name)
        print(border)
        self.busted = True

class Game:
    def __init__(self):
        self.game_deck = None
        self.players_array = []
        self.dealer = Player("DEALER")

    def setup(self):
        num_players = None
        while type(num_players) != int or num_players == 0 or num_players > 6:
            try:
                num_players = int(raw_input("How many players (1-6)? "))
            except:
                continue
        self.players_array.append(self.dealer) # dealer is player 0, index 0
        for number in range(1, num_players + 1):
            player_prompt = "Player %d, please enter your name: " % number
            self.players_array.append(Player(raw_input(player_prompt)))
        triple_border()
        print("Initializing blackjack game for:")
        print("DEALER")
        for index, player in enumerate(self.players_array[1:], 1):
            print("Player %d: %s ($%.2f)" % (index, player.name, player.money))
        triple_border()
        self.game_deck = Deck()

    def run(self):
        self.setup()
        user_input = ''
        while user_input != 'q':
            print("Enter 'd' to deal or 'q' to quit.")
            user_input = raw_input("> ").lower()
            if user_input == 'd':
                self.deal()
                if not self.check_for_21():
                    self.play()
                    self.dealer_turn()
                self.show_results()

    def check_for_21(self): #ends the game immediately if dealer and/or all players are dealt natural blackjack
        winners_array = []
        for player in self.players_array:
            if player.natural:
                winners_array.append(player)
        if winners_array: #correct sentence structure depending on number of natural blackjacks
            if len(winners_array) == 1:
                for player in winners_array:
                    print ("%s" % player.name),
                print("was dealt natural blackjack.")
            elif len(winners_array) == 2:
                for player in winners_array[:-1]:
                    print ("%s" % player.name),
                print("and %s" % winners_array[-1].name),
                print("were dealt natural blackjack.")
            else:
                for player in winners_array[:-1]:
                    print ("%s," % player.name),
                print("and %s" % winners_array[-1].name),
                print("were dealt natural blackjack.")
            print(border)
        if self.dealer.natural:
            return True
        if len(winners_array) == len(self.players_array) - 1: #all players except dealer have natural blackjack
            return True
        return False

    def set_bets(self):
        for index, player in enumerate(self.players_array[1:], 1):
            if player.bet > int(player.money):
                player.bet = int(player.money)
            print("Player %d: %s ($%.2f) - betting $%d per hand" % (index, player.name, player.money, player.bet))
        player_choice = ''
        while player_choice != 'b' and player_choice != 'c':
            player_choice = raw_input("Change (b)et amounts or (c)ontinue with current amounts? ").lower()
        if player_choice == 'c':
            return
        while True:
            if len(self.players_array) > 2:
                player_choice = 0
                while player_choice not in range(1, (len(self.players_array))):
                    try:
                        player_choice = int(raw_input("Change which player number's bet amount? "))
                    except:
                        continue
            else:
                player_choice = 1 #if only one player left, don't ask which player's bets to change
            current_player = self.players_array[player_choice]
            print("Player %d: %s ($%.2f) - betting $%d per hand" % (player_choice, current_player.name, current_player.money, current_player.bet))
            current_player.bet = 0
            while current_player.bet not in range(1, int(current_player.money) + 1):
                current_player.bet = int(raw_input("Bet how much per hand? "))
            if len(self.players_array) > 2:
                player_choice = ''
                while player_choice != 'y' and player_choice != 'n':
                    player_choice = raw_input("Change another player's bet amount? (Y/N): ").lower()
                if player_choice == 'y':
                    continue
                if player_choice == 'n':
                    return
            return

    def deal(self):
        self.game_deck.shuffle()
        self.set_bets()
        print("Initial deal:")
        print(border)
        card1 = self.game_deck.stack.pop()
        card2 = self.game_deck.stack.pop()
        if self.dealer.new_hand(card1, card2) == "BLACKJACK":
                print("%s (%s %s) - DEALER BLACKJACK!!!" % (self.dealer.name, self.dealer.up_cards[0].name, self.dealer.up_cards[1].name))
        else:
            print("%s (__ %s) - showing %d" % (self.dealer.name, self.dealer.up_cards[1].name, card_values[self.dealer.up_cards[1].value]))
        for player in self.players_array[1:]:
            card1 = self.game_deck.stack.pop()
            card2 = self.game_deck.stack.pop()
            if player.new_hand(card1, card2) == "BLACKJACK":
                print("%s (%s %s) - NATURAL BLACKJACK!!!" % (player.name, player.up_cards[0].name, player.up_cards[1].name))
            else:
                print("%s (%s %s) - %d" % (player.name, player.up_cards[0].name, player.up_cards[1].name, player.total))
        triple_border()

    def play(self):
        for player in self.players_array[1:]: #not including dealer
            if player.twenty_one:
                continue
            else:
                player_choice = ''
                player_prompt = "%s, would you like to (h)it or (s)tand? " % player.name
                while player_choice != 's' and not player.busted and not player.twenty_one:
                    print("%s (__ %s) - showing %d" % (self.dealer.name, self.dealer.up_cards[1].name, card_values[self.dealer.up_cards[1].value]))
                    player.display_hand()
                    player_choice = raw_input(player_prompt).lower()
                    if player_choice == 'h':
                        player.hit(self.game_deck.stack.pop())
                if player_choice == 's':
                    player.stand()
                    print(border)
                if player.twenty_one:
                    print("%s stands on 21." % player.name)
                    print(border)

    def dealer_turn(self):
        all_busted = True #if all players have busted, dealer doesn't take a turn
        for player in self.players_array[1:]:
            if not player.busted:
                all_busted = False
        if all_busted:
            return
        self.dealer.display_hand()
        while self.dealer.total < 17 and not self.dealer.busted:
            self.dealer.hit(self.game_deck.stack.pop())
            self.dealer.display_hand()
        if not self.dealer.busted:
            self.dealer.stand()

    def show_results(self):
        triple_border()
        print("Results:")
        if self.dealer.natural:
            for player in self.players_array[1:]:
                if player.natural:
                    print("%s - PUSH" % player.name),
                else:
                    print("%s - LOSE" % player.name),
                    player.money -= player.bet
                print("($%.2f)" % player.money)
        elif self.dealer.busted:
            for player in self.players_array[1:]:
                if player.busted:
                    print("%s - LOSE" % player.name),
                    player.money -= player.bet
                elif player.natural:
                    print("%s - NATURAL BLACKJACK, WIN 3:2" % player.name),
                    player.money += player.bet * 1.5
                else:
                    print("%s - WIN" % player.name),
                    player.money += player.bet
                print("($%.2f)" % player.money)
        else:
            for player in self.players_array[1:]:
                if player.natural:
                    print("%s - NATURAL BLACKJACK, WIN 3:2" % player.name),
                    player.money += player.bet * 1.5
                elif player.busted:
                    print("%s - BUST (LOSE)" % player.name),
                    player.money -= player.bet
                elif player.total > self.dealer.total:
                    print("%s - WIN" % player.name),
                    player.money += player.bet
                elif player.total == self.dealer.total:
                    print("%s - PUSH" % player.name),
                else:
                    print("%s - LOSE" % player.name),
                    player.money -= player.bet
                print("($%.2f)" % player.money)
        for player in self.players_array[1:]: #remove players with no money left
            if player.money <= 0:
                print("%s is out of money. Goodbye!" % player.name)
                self.players_array.remove(player)
        if len(self.players_array) == 1:
            print("All players out of money. Game over!")
            quit()
        triple_border()

blackjack = Game()
blackjack.run()