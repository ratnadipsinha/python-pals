// Interactive Python projects for 8-year-old coders. Loosely inspired by
// geeksforgeeks.org/python/python-projects-beginner-to-advanced/, simplified
// in language and scope, and ordered easiest -> hardest to match what a kid
// would have already learned in the chapters (print/strings, then numbers,
// then lists, then loops). All are text-based so they run in the browser
// via Pyodide, with input() bridged to a real prompt() dialog.
window.PP_PROJECTS = [
  {
    id: "P1",
    title: "Project 1: Greeting Card",
    emoji: "🎉",
    learn: ["print()", "input()", "joining words with +"],
    problem: "Make a fun greeting card! Ask for the player's name, then print a big colorful hello message just for them.",
    steps: [
      { title: "Ask for their name", text: "Use input() to ask a question:  name = input(\"What is your name? \")" },
      { title: "Say hello", text: "Print a friendly greeting using their name, like:  print(\"Hello, \" + name + \"! 🎉\")" },
      { title: "Add more fun", text: "Print 2 more lines for the card — a joke, a compliment, or a silly fact — and use their name again!" },
    ],
    starter:
`name = input("What is your name? ")

# TODO: print a big hello message using their name
# TODO: print 2 more fun lines for the card!
`,
  },
  {
    id: "P2",
    title: "Project 2: Lucky Number Picker",
    emoji: "🍀",
    learn: ["random.randint()", "print()", "variables"],
    problem: "Give the player a lucky number for today! Pick a random number between 1 and 100 and show it to them in a fun way.",
    steps: [
      { title: "Pick a random number", text: "lucky = random.randint(1, 100)" },
      { title: "Show it off", text: "Print something like:  print(\"Your lucky number today is\", lucky, \"🍀\")" },
      { title: "Make it silly", text: "Add one more fun line — what could that lucky number mean today?" },
    ],
    starter:
`import random

# TODO: pick a random lucky number between 1 and 100
# TODO: print it with a fun message
# TODO: add one more silly line to make it fun!
`,
  },
  {
    id: "P3",
    title: "Project 3: Silly Joke Machine",
    emoji: "😂",
    learn: ["lists", "random.choice()", "print()"],
    problem: "Build a joke machine! Store some silly jokes in a list, then print a random one every time it runs.",
    steps: [
      { title: "Make a jokes list", text: "Write at least 4 silly jokes as strings inside a list called jokes." },
      { title: "Pick one at random", text: "joke = random.choice(jokes)" },
      { title: "Tell the joke", text: "Print it with something fun, like:  print(\"Here's a joke for you: \" + joke)" },
    ],
    starter:
`import random

jokes = [
    "Why did the computer go to the doctor? It had a virus!",
    "What do you call a bear with no teeth? A gummy bear!",
    # TODO: add 2 more silly jokes of your own!
]

# TODO: pick a random joke and print it
`,
  },
  {
    id: "P4",
    title: "Project 4: Candy Counter",
    emoji: "🍬",
    learn: ["lists", "for loops", "counting"],
    problem: "You have a bag of candy to share with your friends! Ask each friend if they want a piece, then count how many you gave away.",
    steps: [
      { title: "Make a list of friends", text: "friends = [\"Ana\", \"Leo\", \"Mia\"]" },
      { title: "Start a candy counter", text: "candy_given = 0" },
      { title: "Ask each friend", text: "for friend in friends: — ask  input(friend + \", do you want candy? (y/n): \")" },
      { title: "Count the candy", text: "If they say \"y\", add 1 to candy_given." },
      { title: "Show the total", text: "Print how many pieces of candy you gave away in total!" },
    ],
    starter:
`friends = ["Ana", "Leo", "Mia"]
candy_given = 0

# TODO: for each friend, ask if they want candy
# TODO: if they say "y", add 1 to candy_given
# TODO: print how many pieces of candy you gave away
`,
  },
  {
    id: "P5",
    title: "Project 5: Guess My Number",
    emoji: "🎯",
    learn: ["while loops", "if / elif / else", "input() and int()"],
    problem: "The computer secretly picks a number between 1 and 20. Keep guessing until you get it right — the computer will tell you \"Too high!\" or \"Too low!\" each time.",
    steps: [
      { title: "Pick the secret number", text: "secret = random.randint(1, 20)" },
      { title: "Start a tries counter", text: "tries = 0 — this will count how many guesses you make." },
      { title: "Guess in a loop", text: "Use while True: to keep asking  guess = int(input(\"Your guess: \"))  until it's right. Add 1 to tries each time." },
      { title: "Give hints", text: "If the guess is too big, print \"Too high!\". Too small, print \"Too low!\"." },
      { title: "Celebrate!", text: "When they guess it, print how many tries it took, then stop the loop with break." },
    ],
    starter:
`import random

secret = random.randint(1, 20)

print("I'm thinking of a number between 1 and 20!")

# TODO: keep asking the player to guess until they get it right.
#   guess = int(input("Your guess: "))
# TODO: after each guess, print "Too high!" or "Too low!"
# TODO: when they get it right, print how many tries it took!
`,
  },
  {
    id: "P6",
    title: "Project 6: Rock Paper Scissors",
    emoji: "✊",
    learn: ["random.choice()", "input()", "if / elif / else"],
    problem: "Play one round of Rock, Paper, Scissors against the computer. Type your choice, let the computer pick randomly, then find out who won.",
    steps: [
      { title: "Make the choices list", text: "choices = [\"rock\", \"paper\", \"scissors\"]" },
      { title: "Get the player's choice", text: "player = input(\"rock, paper, or scissors? \")" },
      { title: "Get the computer's choice", text: "computer = random.choice(choices) — print it so you can see what it picked." },
      { title: "Handle a tie", text: "If player == computer, print \"It's a tie!\" and stop there." },
      { title: "Decide the winner", text: "Check the 3 winning combos — rock beats scissors, scissors beats paper, paper beats rock — and print who won." },
    ],
    starter:
`import random

choices = ["rock", "paper", "scissors"]

# TODO: ask the player: player = input("rock, paper, or scissors? ")
# TODO: computer picks randomly: computer = random.choice(choices)
# TODO: print what the computer chose
# TODO: figure out who wins and print the result!
#   (rock beats scissors, scissors beats paper, paper beats rock)
`,
  },
];
