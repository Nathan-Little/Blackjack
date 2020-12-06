import os
import random
import numpy as np
import pickle5 as pickle

dealer_hand = []
player_hand = []
hand = []
policy = {}
actions = ['h', 's']

deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

# deal cards
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

# calculate the numerical value of a hand
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
		return 1
	elif total(dealer_hand) == 21:
		return -1
	else:
		return 0

def score(dealer_hand, player_hand):
	if total(player_hand) == 21:
		return 1
	elif total(dealer_hand) == 21:
		return -1
	elif total(player_hand) > 21:
		return -1
	elif total(dealer_hand) > 21:
		return 1
	elif total(player_hand) < total(dealer_hand):
		return -1
	elif total(player_hand) > total(dealer_hand):
		return 1
	elif total(player_hand) == total(dealer_hand):
		return 0
	else:
		return 0

def printFinalScore(dealer_hand, player_hand):
	if total(player_hand) == 21:
		print("Player got blackjack!")
		return 1
	elif total(dealer_hand) == 21:
		print("Dealer got blackjack!")
		return -1
	elif total(player_hand) > 21:
		print("Player busted!")
		return -1
	elif total(dealer_hand) > 21:
		print("Dealer busted!")
		return 1
	elif total(player_hand) < total(dealer_hand):
		print("Dealer got higher total! Player loses!")
		return -1
	elif total(player_hand) > total(dealer_hand):
		print("Player got higher total! Dealer loses!")
		return 1
	elif total(player_hand) == total(dealer_hand):
		print("Tie!")
		return 0
	else:
		print("Tie")
		return 0

def play_game_with_qbot_policy(num_games, policy_string):
	global deck, policy, actions
	player_total = 0
	dealer_hand = []
	player_hand = []
	wins, ties, losses = 0, 0, 0
	# load in trained policy
	policy = load_obj(policy_string)
	# print(policy)

	for i in range(num_games):
		# deal hands
		dealer_hand = deal(deck)
		player_hand = deal(deck)

		# check if either player has blackjack
		if is_blackjack(dealer_hand, player_hand) == 0:

			# Retrieve current state
			player_total, dealer_card, ace_bool = evaluateHands(dealer_hand, player_hand)

			# -----Choose index of A from S using policy derived from Q------
			curr_action_index = get_action(player_total, dealer_card, ace_bool)
			print("Current State:")
			print([player_total, dealer_card, ace_bool])
			
			# Use index of A to get A
			curr_action = actions[curr_action_index]
			print("First action: ")
			print(curr_action)

			# Player hits
			while curr_action == 'h' and player_total < 21:
				
				player_total, dealer_card, ace_bool = evaluateHands(dealer_hand, player_hand)
				# check if player busted
				print("Player's Hand: ")
				print(player_hand)
				print("Player total: " + str(player_total))
				print("Dealer's hand: ")
				print(dealer_hand)
				print("Dealer's first card: " + str(dealer_card))
				print("ace bool: " + str(ace_bool))
				print("\n")

				if player_total > 21:
    				### Return later
					# How to update if player busts?????
					# calculate the reward for when the player busts
					# Reward should be based on observable info
					printFinalScore(dealer_hand, next_player_hand)

					continue

				# -----Choose A from S using policy derived from Q------
				curr_action_index = get_action(player_total, dealer_card, ace_bool)
				
				curr_action = actions[curr_action_index]

				print("Next action:")
				print(curr_action)
				# print("Curr action: " + curr_action)
				# ------Take action A------
				if curr_action == 'h':

					next_player_hand = hit(player_hand)

					
					player_hand = next_player_hand

			print("------BUST OR STAND------")

			next_player_hand = player_hand
			
			while total(dealer_hand) < 17:
				next_dealer_hand = hit(dealer_hand)
			
			if total(dealer_hand) >= 17:
				next_dealer_hand = dealer_hand
			
			# reward = score(next_dealer_hand, player_hand)
			# -----Observe S------
			# - Get the new player total and the new ace bool

			# Now, how do we handle the dealer? We are basing our states off the assumption, that the player
			# would only ever see the dealer's first card

			# Set the new state the player is in
			
			
			# Calculate final reward
			final_score = printFinalScore(next_dealer_hand, next_player_hand)

			if final_score == 1:
				wins += 1
			elif final_score == 0:
				ties += 1
			else:
				losses += 1
			
			# Reset table
			dealer_hand = []
			player_hand = []
			player_total = 0
			deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
	
	print("Wins: ")
	print(wins)
	print("Ties: ")
	print(ties)
	print("Losses: ")
	print(losses)
	
def play_game_with_qbot_policy(num_games, policy_string):
	global deck, policy, actions
	player_total = 0
	dealer_hand = []
	player_hand = []
	wins, ties, losses = 0, 0, 0
	# load in trained policy
	policy = load_obj(policy_string)
	# print(policy)

	for i in range(num_games):
		# deal hands
		dealer_hand = deal(deck)
		player_hand = deal(deck)

		# check if either player has blackjack
		if is_blackjack(dealer_hand, player_hand) == 0:

			# Retrieve current state
			player_total, dealer_card, ace_bool = evaluateHands(dealer_hand, player_hand)

			# -----Choose index of A from S using policy derived from Q------
			curr_action_index = get_action(player_total, dealer_card, ace_bool)
			print("Current State:")
			print([player_total, dealer_card, ace_bool])
			
			# Use index of A to get A
			curr_action = actions[curr_action_index]
			print("First action: ")
			print(curr_action)

			# Player hits
			while curr_action == 'h' and player_total < 21:
				
				player_total, dealer_card, ace_bool = evaluateHands(dealer_hand, player_hand)
				# check if player busted
				print("Player's Hand: ")
				print(player_hand)
				print("Player total: " + str(player_total))
				print("Dealer's hand: ")
				print(dealer_hand)
				print("Dealer's first card: " + str(dealer_card))
				print("ace bool: " + str(ace_bool))
				print("\n")

				if player_total > 21:
    				### Return later
					# How to update if player busts?????
					# calculate the reward for when the player busts
					# Reward should be based on observable info
					printFinalScore(dealer_hand, next_player_hand)

					continue

				# -----Choose A from S using policy derived from Q------
				curr_action_index = get_action(player_total, dealer_card, ace_bool)
				
				curr_action = actions[curr_action_index]

				print("Next action:")
				print(curr_action)
				# print("Curr action: " + curr_action)
				# ------Take action A------
				if curr_action == 'h':

					next_player_hand = hit(player_hand)

					
					player_hand = next_player_hand

			print("------BUST OR STAND------")

			next_player_hand = player_hand
			
			while total(dealer_hand) < 17:
				next_dealer_hand = hit(dealer_hand)
			
			if total(dealer_hand) >= 17:
				next_dealer_hand = dealer_hand
			
			# reward = score(next_dealer_hand, player_hand)
			# -----Observe S------
			# - Get the new player total and the new ace bool

			# Now, how do we handle the dealer? We are basing our states off the assumption, that the player
			# would only ever see the dealer's first card

			# Set the new state the player is in
			
			
			# Calculate final reward
			final_score = printFinalScore(next_dealer_hand, next_player_hand)

			if final_score == 1:
				wins += 1
			elif final_score == 0:
				ties += 1
			else:
				losses += 1
			
			# Reset table
			dealer_hand = []
			player_hand = []
			player_total = 0
			deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
	
	print("Wins: ")
	print(wins)
	print("Ties: ")
	print(ties)
	print("Losses: ")
	print(losses)

def qbot(num_episodes):
	global policy, actions, deck
	
	# initialize
	final_reward = 0
	curr_action_index = None
	
	alpha = .4
	discount = 1
	player_total = 0
	dealer_hand = []
	player_hand = []

	# initialize the policy
	policy = initializeQ()

	for i in range(num_episodes):
		# deal cards
		dealer_hand = deal(deck)
		player_hand = deal(deck)

		player_total, dealer_card, ace_bool = evaluateHands(dealer_hand, player_hand)

		curr_state = (player_total, dealer_card, ace_bool)
		
		# Find the index of the action that the policy says to play
		curr_action_index = get_action(player_total, dealer_card, ace_bool)
		
		# Find the action to play
		curr_action = actions[curr_action_index]
		
		# initialize states and actions lists
		curr_states_list = []
		next_states_list = []
		curr_actions_list = []
		next_actions_list = []

		# print("is_blackjack????")
		# print(is_blackjack(dealer_hand,player_hand))

		# check if game is already over
		if is_blackjack(dealer_hand, player_hand) == 0:
			
			# Get the state components
			player_total, dealer_card, ace_bool = evaluateHands(dealer_hand, player_hand)
			
			# Player chooses to hit until stand is chosen
			while curr_action == 'h' and player_total < 21:
				
		
				# print("Player's Hand: ")
				# print(player_hand)
				# print("Player total: " + str(player_total))
				# print("Dealer's hand: ")
				# print(dealer_hand)
				# print("Dealer's first card: " + str(dealer_card))
				# print("ace bool: " + str(ace_bool))
				# print("\n")


				# check if player busted from their last move - Game is over if so
				if player_total > 21:
    				
					# Calculate final reward
					final_reward = score(dealer_hand, next_player_hand)

					# update the Q(s, a) estimated reward which caused the bust
					policy[curr_state][curr_action_index] += alpha * (final_reward + (discount * policy[next_state][next_action_index] - policy[curr_state][curr_action_index]))

					continue
				
				# Set the current state
				curr_state = (player_total, dealer_card, ace_bool)

				# Find the index of the action that the policy says to play
				curr_action_index = get_action(player_total, dealer_card, ace_bool)
				
				# Find the action to play
				curr_action = actions[curr_action_index]
				
				# print("Curr action: " + curr_action)

				# Take best action
				if curr_action == 'h':
					
					# hit
					next_player_hand = hit(player_hand)

					# print("Next player hand:")
					# print(next_player_hand)
				
					# Get the next state components
					next_player_total, next_ace_bool = evaluatePlayer(next_player_hand)

					# print("Next player total: ")
					# print(next_player_total)

					# Set the new state the player is in
					next_state = (next_player_total, dealer_card, next_ace_bool)
					
					# print("Next state: ")
					# print(next_state)

					# Find the next best action the policy says to take
					next_action_index = get_action(next_player_total, dealer_card, next_ace_bool)
					
					# Append the states and actions to their lists
					if next_state not in next_states_list and curr_state not in curr_states_list:
						next_states_list.append(next_state)
						curr_states_list.append(curr_state)

						curr_actions_list.append(curr_action_index)
						next_actions_list.append(next_action_index)
					
					# Update player_hand, player_total, and ace_bool
					player_hand = next_player_hand
					player_total = next_player_total
					ace_bool = next_ace_bool

					# print("Curr States List: ")
					# print(curr_states_list)
					# print("Next States List: ")
					# print(next_states_list)
					

			# At this point - the player has chosen to stand
			next_player_hand = player_hand

			# Dealer hits until dealer's hand is over 17
			while total(dealer_hand) < 17:
				next_dealer_hand = hit(dealer_hand)
			
			# In case that dealer's hand was above 17 off the start
			if total(dealer_hand) >= 17:
				next_dealer_hand = dealer_hand
			
			# Set the new state the player is in
			next_state = (player_total, getDealerCard(next_dealer_hand[0]), ace_bool)

			# Find the next best action to take
			next_action_index = get_action(player_total, getDealerCard(next_dealer_hand[0]), ace_bool)
			
			# Add states and actions to their lists
			if next_state not in next_states_list and curr_state not in curr_states_list:
					next_states_list.append(next_state)
					curr_states_list.append(curr_state)
					
					curr_actions_list.append(curr_action_index)
					next_actions_list.append(next_action_index)
			
			# Calculate final reward since game is over
			final_reward = score(next_dealer_hand, next_player_hand)
			
			# Pass backwards through the states and actions; update the policy for each (s, a)
			for i in range(len(next_states_list) - 1, -1, -1):
				
				policy[curr_states_list[i]][curr_actions_list[i]] += alpha * (final_reward + (discount * policy[next_states_list[i]][next_actions_list[i]] - policy[curr_states_list[i]][curr_actions_list[i]]))

			# Reset game
			dealer_hand = []
			player_hand = []
			player_total = 0
			curr_action = None
			deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4

			# print("Curr States List: ")
			# print(curr_states_list)
			# print("Next States List: ")
			# print(next_states_list)
			# print("Curr Actions List: ")
			# print(curr_actions_list)
			# print("Next Actions List: ")
			# print(next_actions_list)
			# print(policy)

			
	save_obj(policy, "policy3Rework")
	print(policy)

def getDealerCard(dealer_card):
		if dealer_card == 'J': dealer_card = 10
		elif dealer_card == 'Q': dealer_card = 10
		elif dealer_card == 'K': dealer_card = 10
		elif dealer_card == 'A': dealer_card = 11
		return dealer_card + 10

def evaluateHands(dealer_hand, player_hand):
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

	# add ten to dealer card for hidden card assumption
	return player_total, dealer_card + 10, aceBool

def evaluatePlayer(player_hand):
	aceBool = containsAce(player_hand)
	player_total = 0
	for card in player_hand:
		if card == 'J':player_total += 10
		elif card == 'Q':player_total += 10
		elif card == 'K':player_total += 10
		elif card == 'A':player_total += 11 # assume that aces are eleven, initially, decide whether it is 11 or 1 later
		else: 
			player_total += card

	return player_total, aceBool


# good to go
def get_action(player_total, dealer_card, aceBool):
		
	possRewards = policy[(player_total, dealer_card, aceBool)]

	if aceBool:
		possAltRewards = policy[(player_total - 10, dealer_card, aceBool)]
	
		if max(possAltRewards) >= max(possRewards):
			possRewards = possAltRewards
	
	eps = .1
	p = np.random.random() 
	if p < eps: 
		currActionIndex = np.random.choice(len(actions)) 
	else: 
		currActionIndex = np.argmax(possRewards) 

	return currActionIndex
	# print("Poss rewards: ")
	# print(possRewards)
	# Sum up rewards (first making them positive)
	# reward_sum = 0
	# for i in possRewards:
	# 	if i < 0:
	# 		i = i * -1
	# 	reward_sum += i
	
	# print("Reward sum: ")
	# print(reward_sum)
	
	# divide each reward by the total
	# choice_probs = []
	# for i in possRewards:
	# 	prob = (i * -1)/ reward_sum
	# 	if prob < 0:
	# 		prob *= -1
	# 	choice_probs.append(prob)
	
	# print("Probs: ")
	# print(choice_probs)
	# choose action according to the probability distribution 
	
	
	
    		
def containsAce(player_hand):
	if 'A' in player_hand:
		return 1
	return 0

def initializeQ():
	# initialize Q(s,a) in dictionary where state -> action (maybe move to helper)
	# playerHand, Dealer, isSoft (1-> soft)
	# 
	possibleTotals = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
	possibleDealerFirstCard = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
	
	tempStates = []
	for i in possibleTotals:
		for j in possibleDealerFirstCard:
			tempStates.append((i,j))
	
	states = []
	for i in tempStates:
		for j in range(2):
			# Keys are [playerTotal, dealerFirstCard, aceBool]
			states.append(i + (j,))

	for i in range(len(states)):
		# values are [reward for 'h', reward for 's']
		policy[states[i]] = [1, 1]

	return policy

if __name__ == "__main__":
	# qbot(100000)
	play_game_with_qbot_policy(100000, "policy3Rework")
	# game()
