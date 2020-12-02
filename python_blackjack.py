import os
import random
import numpy as np


dealer_hand = []
player_hand = []
hand = []
policy = {}
actions = ['h', 's']

deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*6


def deal(deck):
	hand = []
	for i in range(2):
		random.shuffle(deck)
		card = deck.pop()
		if card == 11:card = "J"
		if card == 12:card = "Q"
		if card == 13:card = "K"
		if card == 14:card = "A"
		hand.append(card)
	return hand

def play_again():
	global dealer_hand, player_hand, deck
	again = input("Do you want to play again? (Y/N) : ").lower()
	if again == "y":
		dealer_hand = []
		player_hand = []
		deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*6
		game()
	else:
		print("Bye!")
		exit()

def total(hand):
	total = 0
	for card in hand:
		if card == 'J' or card == 'Q' or card == 'K':
			total += 10
		elif card == 'A':
			if total >= 11:
				total += 1
			else: 
				total += 11
		else:
			total += card
	return total 

def hit(hand):
	card = deck.pop()
	if card == 11:
		card = "J"
	if card == 12:
		card = "Q"
	if card == 13:
		card = "K"
	if card == 14:
		card = "A"
	hand.append(card)
	return hand

def clear():
	if os.name == 'nt':
		os.system('CLS')
	if os.name == 'posix':
		os.system('clear')

def print_results(dealer_hand, player_hand):
	clear()
	print("The dealer has a " + str(dealer_hand) + " for a total of " + str(total(dealer_hand)))
	print("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))

def is_blackjack(dealer_hand, player_hand):
	if total(player_hand) == 21:
		print_results(dealer_hand, player_hand)
		print("Congratulations! You got a Blackjack!\n")
		play_again()
	elif total(dealer_hand) == 21:
		print_results(dealer_hand, player_hand)
		print("Sorry, you lose. The dealer got a blackjack.\n")
		play_again()

def score(dealer_hand, player_hand):
	if total(player_hand) == 21:
		# print_results(dealer_hand, player_hand)
		print("Congratulations! You got a blackjack!\n")
		return 1
	elif total(dealer_hand) == 21:
		# print_results(dealer_hand, player_hand)
		print("Sorry, you lose. The dealer got a blackjack.\n")
		return -1
	elif total(player_hand) > 21:
		# print_results(dealer_hand, player_hand)
		print("Sorry. You busted. You lose.\n")
		return -1
	elif total(dealer_hand) > 21:
		# print_results(dealer_hand, player_hand)
		print("The dealer busted. You win!\n")	
		return 1
	elif total(player_hand) < total(dealer_hand):
		# print_results(dealer_hand, player_hand)
		print("Sorry. Your score isn't higher than the dealer. You lose.\n")
		return -1
	elif total(player_hand) > total(dealer_hand):
		# print_results(dealer_hand, player_hand)
		print("Congratulations. Your score is higher than the dealer. You win!\n")
		return 1
	elif total(player_hand) == total(dealer_hand):
		print("You tied!")
		return 0
	else:
		return 0

def game():
	choice = 0
	clear()
	print("Welcome to Blackjack!\n")
	deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 6
	dealer_hand = deal(deck)
	player_hand = deal(deck)
	while choice != "q":
		print("The dealer is showing a " + str(dealer_hand[0]))
		print("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
		is_blackjack(dealer_hand, player_hand)
		###
		choice = input("Do you want to [H]it, [S]tand, or [Q]uit: ").lower()
		# Use Q bot to determine if the bot should stay or hit
		# choice = qbot(dealer_hand, player_hand)
		###
		clear()
		if choice == "h":
			hit(player_hand)
			while total(dealer_hand) < 17:
				hit(dealer_hand)
			score(dealer_hand, player_hand)
			play_again()
		elif choice == "s":
			while total(dealer_hand) < 17:
				hit(dealer_hand)
			score(dealer_hand, player_hand)
			play_again()
		elif choice == "q":
			print("Bye!")
			exit()

def qbot(dealer_hand, player_hand, numEpisodes):
	global policy, actions
	currReward = 0
	currAction = ''
	policy = initializeQ()

	for i in range(numEpisodes):

		currAction = get_action(dealer_hand, player_hand)
		if currAction == 'h':
			hit(player_hand)
			currReward = score(dealer_hand, player_hand)
			player_total, aceBool = evaluateHands(dealer_hand, player_hand)
			policy[[player_total, dealer_card, aceBool, currAction]][1] += currReward



		elif currAction == 's':
			while total(dealer_hand) < 17:
				hit(dealer_hand)
			currReward = score(dealer_hand, player_hand)
			player_total, dealer_card, aceBool = evaluateHands(dealer_hand, player_hand)
			policy[[player_total, dealer_card, aceBool, currAction]][1] += currReward

def evaluateAllHandsOnlyFirstForDealer(dealer_hand, player_hand):
	aceBool = containsAce(player_hand)
	player_total = 0
	for card in player_hand:
		if card == 'J':player_total += 10
		elif card == 'Q':player_total += 10
		elif card == 'K':player_total += 10
		elif card == 'A':player_total += 11 # assume that aces are eleven, initially, decide whether it is 11 or 1 later
		else: 
			player_total += card
	
	dealer_card = None
	if dealer_hand[0] == 'J': dealer_card = 10
	elif dealer_hand[0] == 'Q': dealer_card = 10
	elif dealer_hand[0] == 'K': dealer_card = 10
	elif dealer_hand[0] == 'A': dealer_card = 11
	else:
		dealer_card = dealer_hand[0]

	return player_total, dealer_card, aceBool

def evaluatePlayerHandOnly(dealer_hand, player_hand):
	aceBool = containsAce(player_hand)
	player_total = 0
	for card in player_hand:
		if card == 'J':player_total += 10
		elif card == 'Q':player_total += 10
		elif card == 'K':player_total += 10
		elif card == 'A':player_total += 11 # assume that aces are eleven, initially, decide whether it is 11 or 1 later
		else: 
			player_total += card

	return player_total, dealer_card, aceBool

def get_action(dealer_hand, player_hand):
	player_total, dealer_card, aceBool = evaluateAllHandsOnlyFirstForDealer(dealer_hand, player_hand)
		
	possRewards = []
	for possAction in actions:
		possRewards.append(policy[[player_total, dealer_card, aceBool, possAction]][1])

	possAltRewards = []
	if aceBool:
		for possAction in actions:
			possAltRewards.append(policy[[player_total - 10, dealer_card, aceBool, possAction]][1])
	
	if max(possAltRewards) >= max(possRewards):
		possRewards = possAltRewards

	currActionIndex = np.argmax(possRewards) 
	# use argmax on a list of all the possible rewards to choose currAction
	
	return actions[currActionIndex]
    		
def containsAce(player_hand):
	if 'A' in player_hand:
		return 1
	return 0

def initializeQ():
	# initialize Q(s,a) in dictionary where state -> action (maybe move to helper)
	# playerHand, Dealer, isSoft (1-> soft)
	
	possibleTotals = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
	possibleDealerFirstCard = [2, 3, 4, 5, 6, 7, 8, 9, 10, 14]
	tempStates = []
	for i in possibleTotals:
		for j in possibleDealerFirstCard:
			tempStates.append([i,j])
	
	states = []
	for i in tempStates:
		for j in range(2):
			# Keys are [playerTotal, dealerFirstCard, aceBool, Action]
			states.append(i + [j] + [['h', 's'][j]])

	for i in range(len(states)):
		# values are [action, reward]
		policy[states[i]] = ['h', 0]

	return policy

if __name__ == "__main__":
	qbot([],[], 1)
	# game()



	

# Initialize Q(s, a) arbitrarily
# Repeat (for each episode):
# 	Choose a from s using policy derived from QTake action a, 
# 	observe r, and s'Q(s, a) ⇐Q(s, a) +  [r +  maxa'Q(s', a') ­ Q(s, a)]
# 	s ⇐s
# 	'until s is terminal

# 	States are values
# 	policies are determined by value -> action (h,s)