// Interactive Python projects for kids — ideas adapted from
// geeksforgeeks.org/python/python-projects-beginner-to-advanced/
// (Number Guessing Game, Rock Paper Scissors, Fun Fact Generator,
// Simple Calculator, Hangman, Attendance Tracker). All are text-based
// so they run in the browser via Pyodide, with input() bridged to a
// real prompt() dialog for genuine interactivity.
//
// Each project is a walkthrough: 1) problem statement, 2) numbered
// steps to follow, 3) a code stage with a scaffold to finish.
window.PP_PROJECTS = [
  {
    id: "P1",
    title: "Number Guessing Game",
    emoji: "🎯",
    learn: ["random.randint()", "while loops", "if / elif / else", "input() and int()"],
    problem: "The computer secretly picks a number between 1 and 20. Your program must let the player guess again and again — saying \"Too high!\" or \"Too low!\" — until they guess it exactly. Then print how many tries it took.",
    steps: [
      { title: "Pick the secret number", text: "Use random.randint(1, 20) and store it in a variable, e.g. secret = random.randint(1, 20)." },
      { title: "Set up a tries counter", text: "Make a variable tries = 0 to count how many guesses the player makes." },
      { title: "Start a loop", text: "Use a while loop that keeps going until the guess is correct — for example while True:, and break out of it once they're right." },
      { title: "Ask for a guess", text: "Inside the loop, use guess = int(input(\"Your guess: \")) and add 1 to tries." },
      { title: "Compare and hint", text: "If the guess is too high, print \"Too high!\". Too low, print \"Too low!\". Correct? Print how many tries it took and stop the loop." },
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
    id: "P2",
    title: "Rock Paper Scissors",
    emoji: "✊",
    learn: ["random.choice()", "input()", "comparing strings", "if / elif / else"],
    problem: "Play one round of Rock, Paper, Scissors against the computer. Ask the player to type their choice, let the computer pick randomly, then decide and print who won.",
    steps: [
      { title: "Make the choices list", text: "choices = [\"rock\", \"paper\", \"scissors\"]" },
      { title: "Get the player's choice", text: "Use input(), e.g. player = input(\"rock, paper, or scissors? \")." },
      { title: "Get the computer's choice", text: "Use computer = random.choice(choices), and print it so the player can see what it picked." },
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
  {
    id: "P3",
    title: "Fun Fact Generator",
    emoji: "🎲",
    learn: ["lists", "random.choice()", "print()"],
    problem: "Build a little app that shows a random fun fact every time it runs.",
    steps: [
      { title: "Make a list of facts", text: "Write at least 5 fun facts as strings inside a list called facts." },
      { title: "Pick one at random", text: "Use fact = random.choice(facts) to grab a single fact from the list." },
      { title: "Print it nicely", text: "Show it with a friendly message, e.g. print(\"Did you know? \" + fact)." },
    ],
    starter:
`import random

facts = [
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
    learn: ["input()", "float()", "if / elif / else", "arithmetic operators"],
    problem: "Ask the player for two numbers and an operator (+, -, *, /), then do the math and print the answer.",
    steps: [
      { title: "Get the first number", text: "a = float(input(\"First number: \"))" },
      { title: "Get the operator", text: "op = input(\"Operator (+ - * /): \")" },
      { title: "Get the second number", text: "b = float(input(\"Second number: \"))" },
      { title: "Do the right math", text: "Use if/elif to check op against \"+\", \"-\", \"*\", \"/\" and calculate the answer." },
      { title: "Print the answer", text: "Show it clearly, e.g. print(a, op, b, \"=\", answer)." },
    ],
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
    learn: ["while loops", "strings", "in / not in", "counting down"],
    problem: "Pick a secret word. The player guesses one letter at a time. Show their progress as blanks and letters, and stop after 6 wrong guesses or a fully-guessed word.",
    steps: [
      { title: "Set up the word and tries", text: "word = \"python\", guessed = \"\", tries = 6" },
      { title: "Build the loop", text: "while tries > 0, keep asking for letters — you can stop early once the word is fully guessed." },
      { title: "Take a guess", text: "letter = input(\"Guess a letter: \"), then guessed = guessed + letter." },
      { title: "Show progress", text: "Build a string that shows each letter of word if it's in guessed, or \"_\" if not — e.g. \"p _ t h _ n\"." },
      { title: "Lose a try on a miss", text: "If the letter isn't in word, subtract 1 from tries." },
      { title: "End the game", text: "Print \"You win!\" if every letter was guessed, or reveal the word if tries ran out." },
    ],
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
    learn: ["lists", "for loops", "input()", "counting"],
    problem: "You have a class list. Ask if each student is present, then print how many showed up and who they are.",
    steps: [
      { title: "Make the class list", text: "students = [\"Aarav\", \"Zara\", \"Ishaan\", \"Maya\"]" },
      { title: "Make an empty list for who's present", text: "present = []" },
      { title: "Loop through every student", text: "for name in students:" },
      { title: "Ask and record", text: "input(name + \" here? (y/n): \") — if the answer is \"y\", add the name to present with present.append(name)." },
      { title: "Print the summary", text: "Show how many are present out of len(students), then print the list of present students." },
    ],
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
