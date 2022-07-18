import enum
import random

def print_nicely(answer, missing):
  y = answer
  for l in y:
    if l in missing:
      y = y.replace(l, "_")
  return y

class WedgeType(enum.Enum):
  PRIZE = 1
  LOSE_TURN = 2
  BANKRUPT = 3

class Wedge:

    def __init__(self, wedge_type, amount = 0):
        self.type = wedge_type
        self.amount = amount   

    def __repr__(self):
        if self.type == WedgeType.PRIZE:
            return str(self.amount)
        elif self.type == WedgeType.LOSE_TURN:
            return "LOSE A TURN"
        else:
            return "BANKRUPT"



# returns a list of all wedges
def generate_wedges(prize_amounts):
  wedges = [
    Wedge(WedgeType.BANKRUPT),
    Wedge(WedgeType.LOSE_TURN),
  ]
  for prize_amount in prize_amounts:
    wedges.append(Wedge(WedgeType.PRIZE, prize_amount))
  return wedges


class Answer:

    def __init__(self, category, answer):
        self.category = category
        self.answer = answer


def load_words(filename):
    answers = []
    with open(filename) as r:
        ls = r.readlines()

        current_category = "no category"
        for i, line in enumerate(ls):
            line = line.replace("\n", "")

            # the line is blank, ignore it
            if not any(line):
                continue

            # this is a delimiter, ignore it
            if "=" in line:
                continue

            # this line denotes the start of a category, so update the category name for future answers
            if "[" in line:
                current_category = line.replace("]", "").replace("[", "")
                continue

            answer = Answer(current_category, line)
            answers.append(answer)

    return answers

class Player:
    def __init__(self, name):
        self.name = name
        self.winnings = 0
        self.bank = 0
        self.skip = False
        self.correct = True

    def __repr__(self):
        return self.name

    def end_loser(self):
        self.bank = 0

    def end_winner(self):
        self.winnings += self.bank
        print(self.name + ", you have won", str(self.bank)+". Altogether you have", str(self.winnings)+".")

class Round:

    def __init__(self, answer, category):
        self.answer = answer
        self.category = category
        self.end = False
        self.vowels = []
        self.consonants = []

    def reset_letters(self):
        self.vowels = ["A", "E", "I", "O", "U"]
        self.consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]

    def spin(self, player):

        if not any(self.consonants):
          print("There are no remaining consonants...")
          return
        
        wedges = generate_wedges([2500, 3500, 900, 600, 500, 300, 650, 750, 850, 950, 1000, 1250, 1500, 2000])
        wedge = wedges[random.randint(0, len(wedges)-1)]
        print("You spun the wheel and it landed on "+str(wedge)+"!")
        if wedge.type == WedgeType.BANKRUPT:
            player.bank = 0
            player.correct = False
        elif wedge.type == WedgeType.LOSE_TURN:
            player.skip = True
            player.correct = False
        else:
            print("The consonants remaining are:")
            print(" ".join(self.consonants))
            guess = input("Choose a consonant: ")
            guess = guess.upper()
            while guess not in self.consonants:
                guess = input("Please choose a consonant from the list above: ")
                guess = guess.upper()
            if guess not in self.answer:
                print("Sorry, your letter is not in the answer.")
                player.correct = False
            else:
                n = self.answer.count(guess)
                player.bank += (n * wedge.amount)
                if n == 1:
                  print("Your letter appears once!")
                else:
                  print("Your letter appears", n, "times!")
            self.consonants.remove(guess)

    def buy(self, player):
        if not any(self.vowels):
          print("There are no remaining vowels...")
          return
        if player.bank >= 250:
          print("The vowels remaining are: ")
          print(" ".join(self.vowels))
          choice = input("Choose a vowel: ")
          choice = choice.upper()
          while choice not in self.vowels:
              choice = input("Please choose a vowel from the list above: ")
              choice = choice.upper()
          if choice not in self.answer:
              print("Sorry, your letter is not in the answer.")
              player.correct = False
          else:
              n = self.answer.count(choice)
              if n == 1:
                print("Your letter appears once!")
              else:
                print("Your letter appears", n, "times!")
          self.vowels.remove(choice)
          player.bank -= 250
        else:
          print("Sorry, vowels cost 250... You don't have enough money.")

    def guess_answer(self, player):
        guess = input("Make your guess: ")
        guess = guess.upper()
        if guess == self.answer:
            print("Congratulations, you correctly guessed the answer!")
            player.end_winner()
            self.end = True
        elif guess == "DEEZ NUTS":
          print("nice")
          player.correct = False
          player.name = "xXCoolDude"+player.name+"Xx"
        else:
            print("You guessed incorrectly.")
            player.correct = False

title_stars = "*" * 20
title = "* WHEEL OF FORTUNE *"
title_stars = title_stars.center(59)
title =  title.center(59)
print(title_stars)
print(title)
print(title_stars)

################################
# Creating the game state

valid = False
while not valid:
    player_number = input("\nHow many people would like to play? ")
    try:
        int(player_number)
        valid = True
    except Exception as error:
        print("Please type your answer as a number.")

player_number = int(player_number)

players = []
for n in range(player_number):
    name = input("Type a player's name: ")
    player = Player(name)
    players.append(player)

valid = False
while not valid:
    rounds_number = input("How many rounds would you like to play? ")
    try:
        int(rounds_number)
        valid = True
    except Exception as error:
        print("Please type your answer as a number.")

rounds_number = int(rounds_number)

answers = load_words("wof.txt")

################################
# Running the game

for round_number in range(1, rounds_number + 1):

    # pick a random answer
    for player in players:
      player.end_loser()
    print("\nWelcome to round", round_number)
    answer = answers[random.randint(0, len(answers)-1)]

    round = Round(answer.answer, answer.category)
    round.reset_letters()
    for player in players:
      player.skip = False

    while not round.end:
      for player in players:
        
        if player.skip:
          print("\n"+player.name, "skips their turn.")
          player.skip = False
          continue
        ########

        player.correct = True
        while player.correct and not round.end:
          valid = False
          formatted = print_nicely(round.answer, round.vowels + round.consonants)
          if " " in round.answer:
            print("\nPHRASE:", formatted)
          else:
            print("\nWORD:", formatted)
          print("CATEGORY:", round.category)
          print("\n"+player.name, "has", player.bank, "in the bank.")
          while not valid:
            select = input(player.name + ", what would you like to do?\n1 Spin the wheel\n2 Buy a vowel\n3 Guess the answer\n")
            if select == "1" or select == "2" or select == "3":
              valid = True
            else:
              print("Please enter either 1, 2 or 3")
          if select == "1":
            round.spin(player)
          elif select == "2":
            round.buy(player)
          elif select == "3":
            round.guess_answer(player)

        if round.end:
          break

n = 0

for player in players:
  if player.winnings > n:
    winner = player
    n = player.winnings
x = 0
for player in players:
  if player.winnings == winner.winnings:
    x += 1
if x > 1:
  print("\nIt was a draw. Thanks for playing!")
else:
  print("\nThe winner is", winner.name, "with a total of", str(winner.winnings)+"!")

  yes = ["y", "yes", "yeah", "yep", "yup"]
  no = ["n", "no", "nah", "nope"]
  valid = False
  while valid == False:
    answer = input("\n" + winner.name + ", would you like to play the final round? ")
    answer = answer.lower()
    if answer in yes or answer in no:
      valid = True
    else:
      print("Sorry, I don't understand...")
  
  if answer in no:
    print("Thanks for playing!")
  else:
    print("\nWelcome to the final round!")
    answer = answers[random.randint(0, len(answers)-1)]
    round = Round(answer.answer, answer.category)
    round.reset_letters()
    round.consonants.remove("R")
    round.consonants.remove("S")
    round.consonants.remove("T")
    round.consonants.remove("L")
    round.consonants.remove("N")
    round.vowels.remove("E")
    formatted = print_nicely(round.answer, round.vowels + round.consonants)
    if " " in round.answer:
      print("\nPHRASE:", formatted)
    else:
      print("\nWORD:", formatted)
    print("CATEGORY:", round.category)
    print("\nThe consonants remaining are:")
    print(" ".join(round.consonants))
    guess = input("Choose your first consonant: ")
    guess = guess.upper()
    while guess not in round.consonants:
      guess = input("Please choose a consonant from the list above: ")
      guess = guess.upper()
    round.consonants.remove(guess)
    guess = input("Choose your second consonant: ")
    guess = guess.upper()
    while guess not in round.consonants:
      guess = input("Please choose a consonant from the list above: ")
      guess = guess.upper()
    round.consonants.remove(guess)
    guess = input("Choose your third consonant: ")
    guess = guess.upper()
    while guess not in round.consonants:
      guess = input("Please choose a consonant from the list above: ")
      guess = guess.upper()
    round.consonants.remove(guess)
    print("The vowels remaining are:")
    print(" ".join(round.vowels))
    guess = input("Choose a vowel: ")
    guess = guess.upper()
    while guess not in round.vowels:
      guess = input("Please choose a vowel from the list above: ")
      guess = guess.upper()
    round.vowels.remove(guess)
    formatted = print_nicely(round.answer, round.vowels + round.consonants)
    if " " in round.answer:
      print("\nPHRASE:", formatted)
    else:
      print("\nWORD:", formatted)
    print("CATEGORY:", round.category)
    guess = input("Guess the answer: ")
    guess = guess.upper()
    if guess == round.answer:
      print("Congratulations, you correctly guessed the answer!")
    else:
      print("Better luck next time! The answer was", round.answer)
    print("\nThanks for playing!")