// Interactive Python projects for kids — ideas adapted from
// geeksforgeeks.org/python/python-projects-beginner-to-advanced/
// (Number Guessing Game, Rock Paper Scissors, Fun Fact Generator,
// Simple Calculator, Hangman, Attendance Tracker). All are text-based
// so they run in the browser via Pyodide, with input() bridged to a
// real prompt() dialog for genuine interactivity.
window.PP_PROJECTS = [
  {
    id: "P1",
    title: "Number Guessing Game",
    emoji: "🎯",
    blurb: "The computer picks a secret number — can your code guess it in the fewest tries?",
    learn: ["random.randint()", "while loops", "if / elif / else", "input() and int()"],
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
    id: "P2",
    title: "Rock Paper Scissors",
    emoji: "✊",
    blurb: "Play the classic hand game against the computer.",
    learn: ["random.choice()", "input()", "comparing strings", "if / elif / else"],
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
  {
    id: "P3",
    title: "Fun Fact Generator",
    emoji: "🎲",
    blurb: "Build a list of fun facts and print a random one every time you run it.",
    learn: ["lists", "random.choice()", "print()"],
    starter:
`facts = [
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries aren't.",
    "A day on Venus is longer than its year.",
    # TODO: add 3 more fun facts of your own!
]

# TODO: pick a random fact with random.choice(facts) and print it.
`,
  },
  {
    id: "P4",
    title: "Simple Calculator",
    emoji: "🧮",
    blurb: "Ask for two numbers and an operator, then do the math.",
    learn: ["input()", "float()", "if / elif / else", "arithmetic operators"],
    starter:
`# TODO: ask for the first number:  a = float(input("First number: "))
# TODO: ask for an operator:       op = input("Operator (+ - * /): ")
# TODO: ask for the second number: b = float(input("Second number: "))
# TODO: do the right math based on op, then print the answer.
`,
  },
  {
    id: "P5",
    title: "Hangman (mini)",
    emoji: "🔤",
    blurb: "Guess the secret word one letter at a time before you run out of tries.",
    learn: ["while loops", "strings", "in / not in", "counting down"],
    starter:
`word = "python"
guessed = ""
tries = 6

# TODO: loop while tries > 0 and you haven't guessed every letter:
#   letter = input("Guess a letter: ")
#   guessed = guessed + letter
#   show the word so far, e.g. "p _ t h _ n"
#   if the letter isn't in the word, tries = tries - 1
# TODO: print "You win!" or "Out of tries! The word was ..." at the end.
`,
  },
  {
    id: "P6",
    title: "Attendance Tracker",
    emoji: "📋",
    blurb: "Take a class list, mark who's present, and print a summary.",
    learn: ["lists", "for loops", "input()", "counting"],
    starter:
`students = ["Aarav", "Zara", "Ishaan", "Maya"]
present = []

# TODO: for each name in students, ask input(name + " here? (y/n): ")
#   if they say "y", add the name to present
# TODO: after the loop, print how many are present out of len(students)
# TODO: print the list of present students
`,
  },
];
