from browser import document, html, bind
from browser.local_storage import storage

import random, re

def update_scores():

    global rounds_won, rounds_lost, rounds_total

    # Playing stats updated in the document
    document['rounds_won'].clear()
    document['rounds_lost'].clear()
    document['rounds_total'].clear()

    document['rounds_won'] <= rounds_won
    document['rounds_lost'] <= rounds_lost
    document['rounds_total'] <= rounds_total

    # Playing stats updated in storage as well
    storage['rounds_won'] = str(rounds_won)
    storage['rounds_lost'] = str(rounds_lost)
    storage['rounds_total'] = str(rounds_total)

def check_input(self):

    # Only a single digit from 1 to 5 can be submitted (otherwise the button for submission will be disabled)
    is_valid_input = re.match(r"^[1-5]$", document['guess_input'].value)
    if is_valid_input is not None:
        del document['guess_btn'].attrs['disabled']
    else:
        document['guess_btn'].attrs['disabled'] = 'disabled'

def play_round(self):

    global rounds_won, rounds_lost, rounds_total

    computer_choice = str(random.randint(1,5))

    player_choice = document['guess_input'].value

    document['guess_para'].clear()

    if (player_choice == computer_choice):
        rounds_won += 1
        document['guess_para'] <= f'You won! You played "{player_choice}" and the secret number was "{computer_choice}".'
    else:
        rounds_lost += 1
        document['guess_para'] <= f'You lost! You played "{player_choice}" and the secret number was "{computer_choice}".'
    rounds_total += 1

    update_scores()
    
    document['guess_input'].value = ''

    document['guess_btn'].attrs['disabled'] = 'disabled'
    
    if storage['rounds_total'] == '1':
        del document['history_btn'].attrs['disabled']
    

def delete_history(self):
    global rounds_won, rounds_lost, rounds_total

    rounds_won = 0
    rounds_lost = 0
    rounds_total = 0

    update_scores()

    document['guess_para'].clear()

    document['history_btn'].attrs['disabled'] = 'disabled'

# Root Area setup (dividing the page)
document['root'] <= html.H1('Guess The Number')
document['root'] <= html.P('Find the number between 1 and 5 to win the round.')
document['root'] <= html.DIV(id = 'guess_area')
document['root'] <= html.DIV(id = 'history_area')

# Guess Area setup (playing field)
document['guess_area'] <= html.INPUT(id = 'guess_input')
document['guess_input'].attrs['maxlength'] = '1'
document['guess_input'].bind('input', check_input)
document['guess_area'] <= html.BUTTON(id = 'guess_btn')
document['guess_btn'].textContent = 'Guess'
document['guess_btn'].attrs['disabled'] = 'disabled' # The button will be clickable when the input holds a valid number
document['guess_btn'].bind('click', play_round)
document['guess_area'] <= html.P(id = 'guess_para')

# History Area setup (playing stats)
document['history_area'] <= html.P('Rounds won: <span id="rounds_won"></span>')
document['history_area'] <= html.P('Rounds lost: <span id="rounds_lost"></span>')
document['history_area'] <= html.P('Total rounds: <span id="rounds_total"></span>')
document['history_area'] <= html.BUTTON(id = 'history_btn')
document['history_btn'].textContent = 'Clear History'
document['history_btn'].bind('click', delete_history)

# Stats setup (stats kept in local storage)
try:
    storage['rounds_won']
except:
    storage['rounds_won'] = '0'

try:
    storage['rounds_lost']
except:
    storage['rounds_lost'] = '0'

try:
    storage['rounds_total']
except:
    storage['rounds_total'] = '0'

document['rounds_won'] <= storage['rounds_won']
document['rounds_lost'] <= storage['rounds_lost']
document['rounds_total'] <= storage['rounds_total']

rounds_won = int(storage['rounds_won'])
rounds_lost = int(storage['rounds_lost'])
rounds_total = int(storage['rounds_total'])

# If stats have been reset, the button is useless, hence disabled
if storage['rounds_total'] == '0':
    document['history_btn'].attrs['disabled'] = 'disabled'