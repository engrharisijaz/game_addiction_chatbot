
import random
import time

# # Define card values
suits = ['♦', '♥', '♣', '♠']
values = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
cards = [f'{value}{suit}' for suit in suits for value in values]
random.shuffle(cards)

# Deal cards and set up piles
player1_hand = [cards.pop() for _ in range(4)]
player2_hand = [cards.pop() for _ in range(4)]
draw_pile = cards
discard_pile = [draw_pile.pop()]

# Define card values
def card_value(card):
    """Convert card to its numerical value for comparison, with special values for certain Kings."""
    value, suit = card[:-1], card[-1]
    
    if value == 'K':
        if suit in ['♦', '♥']:  
            return 0
        elif suit in ['♠', '♣']:  
            return 15
    elif value == 'J':
        return 11
    elif value == 'Q':
        return 12
    elif value == 'A':
        return 1
    else:
        return int(value)

def display_hand(hand):
    """Display a player's hand, hiding the all cards."""
    return ' '.join(['?' if i < 4 else hand[i] for i in range(len(hand))])

def final_hand(hand):
    
    return ' '.join(['?' if i < 0 else hand[i] for i in range(len(hand))])

def calculate_score(hand):
    """Calculate the total score of a player's hand, with special values for certain Kings."""
    score = 0
    for card in hand:
        value, suit = card[:-1], card[-1]
        
        if value == 'K':
            if suit in ['♦', '♥']:  # King of Diamonds or Hearts
                score += 0
            elif suit in ['♠', '♣']:  # King of Spades or Clubs
                score += 15
        elif value in ['J', 'Q']:
            score += 10
        elif value == 'A':
            score += 1
        else:
            score += int(value)  # Convert numeric card values directly to integers and add to score
    return score

def peek_at_two_cards(hand, player1_hand, player2_hand, discard_pile ):
    """Temporarily display the first two cards of a hand."""
    print("Peeking at two cards: ", hand[0], hand[1])
    time.sleep(3)  # Pause for 5 seconds
    for i in range(10):
        print("\n")
    display_game_state(player1_hand, player2_hand, discard_pile)
    return

player1_peeked = False
player2_peeked = False

def peek_at_card(hand, player_num):
    """Allow a player to peek at one of their own cards."""
    print(f"Player {player_num}, choose a card to peek at (1-{len(hand)}):")
    card_index = int(input()) - 1
    if card_index in range(len(hand)):
        print(f"Your card is: {hand[card_index]}")
    else:
        print("Invalid choice. You missed your chance to peek.")

def spy_on_other_player(other_hand):
    """Spy on another player's card."""
    print(f"Choose a card to spy on (1-{len(other_hand)}):")
    card_index = int(input()) - 1
    if card_index in range(len(other_hand)):
        print(f"The other player's card is: {other_hand[card_index]}")
    else:
        print("Invalid choice. You missed your chance to spy.")

def swap_cards(hand, other_hand):
    """Swap a card with an opponent's card."""

    print(f"Choose your card to swap (1-{len(hand)}) and the opponent's card to swap (1-{len(other_hand)}):")
    from_index, to_index = map(int, input().split())
    from_index -= 1
    to_index -= 1
    if from_index in range(4) and to_index in range(4):
        # Perform the swap
        print(f"Swapped your card {hand[from_index]} with the opponent's card {other_hand[to_index]}.")
        hand[from_index], other_hand[to_index] = other_hand[to_index], hand[from_index]
    else:
        print("Invalid choice. No cards were swapped.")

def get_card_value(card):
    """Extract the value of a card as a string for comparison purposes."""
    return card[:-1]  # Return everything except the last character (the suit)

def attempt_match(hand, indices, discard_pile, card):
    """Attempt to match multiple cards in a player's hand based on provided indices.
    If the cards match, remove them from the hand and add them to the discard pile."""

    # Extract card values at the provided indices
    selected_values = [get_card_value(hand[i]) for i in indices]
        
    # Check if all selected card values are the same
    if all(value == selected_values[0] for value in selected_values):
        # If they match, remove the cards from the hand and add to the discard pile
        for index in sorted(indices, reverse=True):
            # Remove card from hand and add to discard pile
            discard_pile.append(hand.pop(index))
        
        hand.append(card)
        return print('"Success: The selected cards match in value and have been moved to the discard pile."')
    else:
        discard_pile.append(card)
        return print('"Failure: The selected cards do not match in value."') 

def play_turn(player_num, hand, other_hand, draw_pile, discard_pile, allow_cabo=True):
    global player1_peeked, player2_peeked
    
    print(f"\nPlayer {player_num}'s turn. Your hand: {display_hand(hand)}")
    
    # Allow each player to peek at their cards once at the beginning of their first turn
    if player_num == 1 and not player1_peeked:
        peek_at_two_cards(hand, player1_hand, player2_hand, discard_pile )
        player1_peeked = True  # Ensure peeking happens only once for player 1
    elif player_num == 2 and not player2_peeked:
        peek_at_two_cards(hand, player1_hand, player2_hand, discard_pile )
        player2_peeked = True  # Ensure peeking happens only once for player 2
    
    # Ask about calling Cabo
    if allow_cabo:
        cabo_call = input("Do you want to call Cabo? (yes/no): ").lower()
        if cabo_call == 'yes':
            return True  # Indicate that Cabo was called

    # Draw from either the draw pile or the discard pile
    draw_choice = input("Draw from the draw pile or discard pile? (draw/discard): ").lower()
    if draw_choice == 'discard' and len(discard_pile) > 0:
        card = discard_pile.pop()
        print(f"You picked {card} from the discard pile.")
        # Automatically keep the card drawn from the discard pile
        keep_card = 'yes'
    else:
        card = draw_pile.pop()
        print(f"You drew a {card} from the draw pile.")
        # Ask if they want to keep the card only if it's drawn from the draw pile
        keep_card = input("Do you want to keep the drawn card? (yes/no): ").lower()

    # Process of replacing a card or discarding the drawn card
    if keep_card == 'yes':
        matching = input("Do you want to attempt matching cards in your hand? (yes/no): ").lower()
        if matching == 'yes':
             input_indices = input("Enter the card positions to match, separated by space (e.g., 1 2 for the first and second cards): ")
             indices = [int(index.strip()) - 1 for index in input_indices.split()]  # Convert to 0-based indices
             attempt_match(hand, indices, discard_pile, card)
        else:
             replace_index = int(input(f"Which card to replace? (1-{len(hand)}): ")) - 1
             if 0 <= replace_index < len(hand):
                discarded_card = hand[replace_index]  # Store replaced card
                print(f"Replaced card {hand[replace_index]} with {card}.")
                hand[replace_index] = card  # Replace card in hand
                discard_pile.append(discarded_card)  # Add the replaced card to the discard pile
             else:
                print("Invalid choice. Discarding the drawn card.")
                discarded_card = card
                discard_pile.append(discarded_card)  # Add the drawn card to the discard pile if replacement choice is invalid
    else:  # This condition is true if the card is drawn and the player chooses not to keep it
        discarded_card = card
        print(f"Discarded the drawn card: {card}")
        discard_pile.append(card)  # Add the discarded card to the discard pile

    # Trigger card effect if applicable
    if (draw_choice == 'draw' and keep_card != 'yes'):
        trigger_card_effect(discarded_card, hand, other_hand, player_num)

    return False  # Indicate that Cabo was not called


def trigger_card_effect(card, hand, other_hand, player_num):
    """Function to trigger special card effects based on the card's value."""
    value = card_value(card)
    if value in [7, 8]:  # Peek
        peek_at_card(hand, player_num)
    elif value in [9, 10]:  # Spy
        spy_on_other_player(other_hand)
    elif value in [11, 12]:  # Swap
        swap_cards(hand, other_hand)


def display_game_state(player1_hand, player2_hand, discard_pile):
    """Display the current state of the game, including both players' hands and the discard pile."""
    print("\nCurrent game state:")
    print(f"Player 1's hand: {display_hand(player1_hand)}")
    print(f"Player 2's hand: {display_hand(player2_hand)}")
    print(f"Discard Pile Top Card: {discard_pile[-1] if discard_pile else 'None'}\n")

def game_loop():
    global player1_hand, player2_hand, draw_pile, discard_pile
    game_over = False
    cabo_called = False
    
    display_game_state(player1_hand, player2_hand, discard_pile)
    while not game_over:
        # Play turn for Player 1
        if play_turn(1, player1_hand, player2_hand, draw_pile, discard_pile, not cabo_called):
            cabo_called = True
            print("Player 1 called Cabo! Player 2 gets one final turn.")
            play_turn(2, player2_hand, player1_hand, draw_pile, discard_pile, allow_cabo=False)
            game_over = True

        display_game_state(player1_hand, player2_hand, discard_pile)  # Display state after Player 1's turn

        # Play turn for Player 2
        if not game_over and play_turn(2, player2_hand, player1_hand, draw_pile, discard_pile, not cabo_called):
            cabo_called = True
            print("Player 2 called Cabo! Player 1 gets one final turn.")
            play_turn(1, player1_hand, player2_hand, draw_pile, discard_pile, allow_cabo=False)
            game_over = True

        display_game_state(player1_hand, player2_hand, discard_pile)  # Display state after Player 2's turn

    # Calculate and display final scores after the game ends
    display_game_state(player1_hand, player2_hand, discard_pile)  # Display final hands
    
    # Calculate and display final scores after the game ends
    
    player1_score = calculate_score(player1_hand)
    player2_score = calculate_score(player2_hand)
    print("\nFinal Hand")
    print(f"Player 1's hand: {final_hand(player1_hand)} ")
    print(f"Player 2's hand: {final_hand(player2_hand)} ")
    print("\nGame over.")
    print(f"Player 1's score: {player1_score}")
    print(f"Player 2's score: {player2_score}")

    # Determine the winner or if it's a tie
    if player1_score < player2_score:
        print("Player 1 wins!")
    elif player2_score < player1_score:
        print("Player 2 wins!")
    else:
        print("It's a tie!")

# Start the game loop
game_loop()
