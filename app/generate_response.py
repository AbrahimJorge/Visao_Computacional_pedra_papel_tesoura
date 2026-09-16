from random import choice

def computer_choice():
    computer_options = ["Tesoura", "Papel", "Pedra"]

    choice_option = choice(computer_options)
    print(choice_option)

    return choice_option

