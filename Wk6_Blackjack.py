# Mini-project #6 - Blackjack

import simplegui
import random
import math

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


# initialize some useful global variables
in_play = False
outcome = "" # who wins or loses
query = "Hit or stand?" # what to ask the player
bet = 10
player_score, dealer_score, score = 0, 0, 0
bet_level = "Betting amount $" + str(bet)

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_list = [] # create Hand object

    def __str__(self):
        str_hand = ""
        # return a string representation of a hand
        for card in self.hand_list:
            str_hand += " " + str(card)
        return "Hand contains" + str_hand

    def add_card(self, card):
        self.hand_list.append(card) # add a card object to a hand
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        list_val = 0
        has_Ace = False
        
        # loops through the hand and also flags
        # if there's an Ace        
        for cards in self.hand_list:
            rank = cards.get_rank()
            list_val += VALUES[rank]
            if rank == "A":
                has_Ace = True
        
        # if has an Ace and hand value is <= 11
        # add 10 (score one Ace as 11)
        if list_val <= 11 and has_Ace:
            list_val += 10
        
        return list_val
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for cards in self.hand_list:
            cards.draw(canvas, [pos[0] + i*CARD_SIZE[0] + 10, pos[1]])
            i += 1


# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(x,y) for x in SUITS for y in RANKS]

    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.deck)   

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        str_deck = ""
        for cards in self.deck:
            str_deck += " " + str(cards)
        return "Deck contains:" + str_deck 

# this is called to calculate if the game 
# has ended and who has won
def calculate_outcome(button_type):
    global player_score, dealer_score, score, outcome, query, in_play, bet
       
    # player hits - checks if player > 21
    # note - the game does not automatically stop
    # just because the player reaches 21

    if button_type == "hit":
        if player_score > 21:
            outcome = "Busted! Dealer wins"
            query = "New deal?"
            score -= bet
            in_play = False
        else:
            query = "Hit or stand?"
    
    # player stays   
    # calculates the player and dealer hands
    
    elif button_type == "stay":   
        query = "New deal?"
        
        if player_score == dealer_score:
            outcome = "Tie! Dealer wins"
            score -= bet
            
        # this section checks if the dealer busts
        # or who is closer to 21
        elif dealer_score > 21 or 21 % player_score < 21 % dealer_score:
            outcome = "Congrats! Player wins"
            score += bet
        else:
            outcome = "Dealer wins"
            score -= bet
        

#define event handlers for buttons
def deal():
    global outcome, query, in_play, deck, score, player_hand, dealer_hand
    
    # if the player hits "deal" when a hand
    # is in play - player loses
    if in_play:
        outcome = "Re-deal? You automatically lost!"
        query = "Hit Deal again to start"
        score -= bet
        in_play = False
        return
    
    query = "Hit or stand?"
    in_play = True    
    deck = Deck()
    deck.shuffle()

    # deals a pair of cards to dealer and player
    player_hand, dealer_hand = Hand(), Hand()    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global query, player_score, in_play, deck, player_hand

    if in_play:
        player_hand.add_card(deck.deal_card()) 
        player_score = player_hand.get_value()
        calculate_outcome("hit")
    else:
        query = "Game over - hit Deal"

            
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global query, player_score, dealer_score, in_play, deck, player_hand, dealer_hand
    player_score = player_hand.get_value()
    dealer_score = dealer_hand.get_value()       
    
    if in_play:
        while dealer_score < 17:
            dealer_hand.add_card(deck.deal_card())
            dealer_score = dealer_hand.get_value() 
        calculate_outcome("stay")
    else:
        query = "Game over - hit Deal"
    in_play = False
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome
    canvas.draw_text('BLACKJACK', (50, 80), 40, 'Red', 'sans-serif')
    canvas.draw_text('Winnings: ', (350, 80), 30, 'White', 'sans-serif')
    if score >= 0:
        canvas.draw_text('$' + str(score), (500, 80), 30, 'White', 'sans-serif')
    else:
        canvas.draw_text('($' + str(score) + ')', (500, 80), 30, 'Red', 'sans-serif')
    canvas.draw_text('Dealer', (50, 150), 20, 'Black', 'sans-serif')
    canvas.draw_text('Player', (50, 350), 20, 'Black', 'sans-serif')
    
    player_hand.draw(canvas, [50, 400])
    dealer_hand.draw(canvas, [50, 200])
   
    if in_play:
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [60+CARD_BACK_SIZE[0]/2, 200+CARD_BACK_SIZE[1]/2], CARD_BACK_SIZE)
        canvas.draw_text(query, (300, 350), 20, 'Black', 'sans-serif')
    else:
        canvas.draw_text(query, (300, 350), 20, 'Black', 'sans-serif')
        canvas.draw_text(outcome, (250, 150), 20, 'Black', 'sans-serif')  


# increase or decrease the bet amount by $10.
# Bets cannot be lower than $10
def increase_bet():
    global bet
    bet += 10
    bet_label.set_text("Betting amount $" + str(bet))
    bet_label2.set_text("")
    
def decrease_bet():
    global bet
    if bet > 10:
        bet -= 10
        bet_label.set_text("Betting amount $" + str(bet))
        bet_label2.set_text("")
    else:
        bet_label.set_text("Betting amount $" + str(bet))
        bet_label2.set_text("Betting amount cannot be less than $10")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label("")
frame.add_button("Increase Bet", increase_bet, 200)
frame.add_button("Decrease Bet", decrease_bet, 200)
frame.add_label("")
bet_label = frame.add_label(bet_level)
bet_label2 = frame.add_label("")
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric