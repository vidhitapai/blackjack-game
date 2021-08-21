import random

Game_is_Active = True

Player_name = input("Before we begin, what is your name?\n")

chips_value = 10000

suits = ('♥', '♦', '♠', '♣')
ranks = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}

#Classes

class Card:
  def __init__(self, suits, ranks):
    self.suit = suits
    self.rank = ranks

  def __repr__(self):
    return self.rank + self.suit


class Deck:
  def __init__(self):
    self.deck = []
    for suit in suits:
      for rank in ranks:
        self.deck.append(Card(suit, rank))

  def __repr__(self):
    return str(self.deck)

  def shuffle(self):
    random.shuffle(self.deck)

  def deal(self):
    draw_card = self.deck.pop()
    return draw_card


class Hand:
  def __init__(self):
    self.cards = []
    self.value = 0
    self.aces = 0

  def add_card(self, card):
    self.cards.append(card)
    self.value += values[card.rank]
    if card.rank == 'A':
      self.aces += 1
    
  def adjust_for_ace(self):
    while self.value > 21 and self.aces:
      self.value -= 10
      self.aces -= 1


class Chips:
  def __init__(self):
    global chips_value
    self.total = chips_value
    self.bet = 0

  def win_bet(self):
    self.total += self.bet

  def lose_bet(self):
    self.total -= self.bet
  

#Functions

def take_bet(Chips):
  while True:
    try: 
      Chips.bet = int(input('How much would you like to Bet? \n'))
      assert Chips.bet > 0
    except AssertionError:
      print("The value entered is negative! Please enter a positive value \n")
    except ValueError:
      print("Enter a valid Number please!\n")
    except:
      print("Something went wrong :( Please try again! \n")
    else:
      if Chips.bet > Chips.total:
        print("Oops!!! Your bet cannot exceed 10000\n")
      else:
        break


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def Hit_or_Stand(deck,hand):
  global Game_is_Active
  while True:
    x = input("\nWould you like to Hit or Stand? Enter your choice! \n")
    if x[0].lower() == 'h':
      hit(deck,hand)

    elif x[0].lower() == 's':
      print("The player stands, dealer is now playing!")
      Game_is_Active = False

    else:
      print("Sorry! Please enter an appropriate word")
      continue

    break


def show_Dealer(Player, Dealer):
  print("\nPlayer's Hand:")
  for i in range(len(Player.cards)):
    print("", Player.cards[i])
  print("\nDealer's Hand:")  
  print(" |Hidden Card|")
  print("", Dealer.cards[1])


def show_all(Player, Dealer):
  print("\nPlayer's Hand:")
  for i in range(len(Player.cards)):
    print("\n", Player.cards[i])
  print("\nDealer's Hand:")
  for i in range(len(Dealer.cards)):
    print("\n", Dealer.cards[i])

        
def Player_busts(Player, Dealer, chips):
  global Player_name
  print("\nOh noooo! %s busts :(" % Player_name)
  chips.lose_bet()

def Player_wins(Player, Dealer, chips):
  global Player_name
  print("\nYayyyyy! %s wins :)" % Player_name)
  chips.win_bet()

def Dealer_busts(Player, Dealer, chips):
  global Player_name
  print("\nWooohooo! Dealer busts :)")
  chips.win_bet()

def Dealer_wins(Player, Dealer, chips):
  global Player_name
  print("\nOooops! Dealer wins :(")
  chips.lose_bet()
     
def push(Player, Dealer):
  global Player_name
  print("\nOoooooh.... It's a push! %s and the dealer tie!" % Player_name)
      
  
#Gameplay
  
while True:
  #global Player_name
  print("\nYayy! Let's play Blackjack, %s!" % Player_name)
  
  instructions = input("\nDo you wish to read the rules of Blackjack? Enter Yes or No \n")
  if instructions[0].lower() == 'y':
    file = open("instructions.txt")
    contents = file.read()
    file.close()
    print(contents)
    print("Press enter to continue...")
    input()
  elif instructions[0].lower() == 'n':
    pass

  print("\n")
  deck = Deck()
  deck.shuffle()

  Player_hand = Hand()
  Player_hand.add_card(deck.deal())
  Player_hand.add_card(deck.deal())
    
  Dealer_hand = Hand()
  Dealer_hand.add_card(deck.deal())
  Dealer_hand.add_card(deck.deal())
    
  Player_chips = Chips()

  #Ask Player for Bet Amount
  take_bet(Player_chips)
  show_Dealer(Player_hand, Dealer_hand)
    
  while Game_is_Active: 
    # Prompt
    Hit_or_Stand(deck, Player_hand)
      
    # Show cards (but keep one dealer card hidden)
    show_Dealer(Player_hand, Dealer_hand) 
        
    if Player_hand.value > 21:
      Player_busts(Player_hand, Dealer_hand, Player_chips)
      break 

  if Player_hand.value <= 21:
    while Dealer_hand.value < 17:
      hit(deck, Dealer_hand)
        
    show_all(Player_hand, Dealer_hand)

    #Winning Situations
    if Dealer_hand.value > 21:
      Dealer_busts(Player_hand, Dealer_hand, Player_chips)
          
    elif Dealer_hand.value > Player_hand.value:
      Dealer_wins(Player_hand, Dealer_hand, Player_chips)

    elif Dealer_hand.value < Player_hand.value:
      Player_wins(Player_hand, Dealer_hand, Player_chips)  
    
    else:
      push(Player_hand, Dealer_hand)

    if Player_hand.value > 21:
      Player_busts(Player_hand, Dealer_hand, Player_chips)
    

  print("\n%s now has" %Player_name, Player_chips.total, "Chips")
  chips_value = Player_chips.total
  
  #New Game Prompt
  new_game = input("\n25 din mai paisa double! Paisa hi paisa hogaaaa :) \n%s, would you like to play another game? \nEnter Yes or No\n" % Player_name)
  if new_game[0].lower() == "y":
    Game_is_Active = True
    continue
  else:
    print('\nThank you for playing Blackjack, %s. Have a great day!' % Player_name)
    break