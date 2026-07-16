"""
Python Pals - A playful Python learning app for kids (age 8+)
11 chapters. Theory on top, hands-on "Run the code" puzzles below.
Runs on Windows 10/11 with only the Python standard library (Tkinter).
"""

import io
import json
import os
import sys
import random
import threading
import webbrowser
import contextlib
from datetime import date
import tkinter as tk
from tkinter import font as tkfont

try:
    import winsound  # Windows only
except Exception:
    winsound = None

APP_NAME = "Python Pals"
SAVE_DIR = os.path.join(os.path.expanduser("~"), ".python_pals")
SAVE_FILE = os.path.join(SAVE_DIR, "progress.json")


def _resource(name):
    """Path to a bundled file (works both from source and a PyInstaller .exe)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


# ---------- Happy / oops sounds (non-blocking, Windows) ----------
def play_sound(kind):
    if not winsound:
        return
    def _run():
        try:
            if kind == "win":
                for f in (660, 880, 1175):
                    winsound.Beep(f, 110)
            elif kind == "good":
                winsound.Beep(880, 90)
                winsound.Beep(1175, 120)
            elif kind == "oops":
                winsound.Beep(300, 160)
        except Exception:
            pass
    threading.Thread(target=_run, daemon=True).start()

# ---------- Colors (playful) ----------
C = {
    "bg":     "#fef6e4",
    "panel":  "#ffffff",
    "ink":    "#2b2036",
    "muted":  "#7a6f86",
    "grape":  "#7b5cff",
    "bubble": "#ff7eb6",
    "sun":    "#ffcf56",
    "mint":   "#3ddc97",
    "sky":    "#4cc9f0",
    "line":   "#efe3d0",
    "editor": "#1e1830",
    "code":   "#c8ffd9",
}

# ---------- Curriculum: 11 chapters ----------
# Each puzzle: prompt, starter code, and a check function using the captured output.
CHAPTERS = [
    {
        "title": "Hello Kids Python",
        "emoji": "👋",
        "youtube": "https://www.youtube.com/watch?v=2muFvgBlNSY&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=1",
        "theory": [
            "Welcome to Python! Python is a programming language that lets you tell the computer what to do.",
            "The most important keyword in Python is  print( )  — it SHOWS things on the screen.",
            "To use print, put what you want to show inside the round brackets ( ).",
            "If you're showing words (called STRINGS), put them in quotes \" \".",
            "Look at these examples 👇",
            '   print("Hello")         →  shows:  Hello',
            '   print("Kids Python")   →  shows:  Kids Python',
            '   print("Welcome!")      →  shows:  Welcome!',
            '   print("I love Python") →  shows:  I love Python',
            "Remember: print( ) shows things. Quotes \" \" hold words.",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Print the word  Hello  on the screen.",
             "starter": 'print("Hello")', "expect": "Hello"},
            {"prompt": "Puzzle 2: Print your favorite animal, like  cat  or  dog.",
             "starter": 'print("cat")', "expect_any": True},
            {"prompt": "Puzzle 3: Print the word  Python.",
             "starter": 'print("Python")', "expect": "Python"},
            {"prompt": "Puzzle 4: Print  I love coding.",
             "starter": 'print("I love coding")', "expect": "I love coding"},
            {"prompt": "Puzzle 5: Print  Good morning.",
             "starter": 'print("Good morning")', "expect": "Good morning"},
            {"prompt": "Puzzle 6: Print your own name.",
             "starter": 'print("Sam")', "expect_any": True},
            {"prompt": "Puzzle 7: Print  Wow!",
             "starter": 'print("Wow!")', "expect": "Wow!"},
            {"prompt": "Puzzle 8: Print  Hello, world!",
             "starter": 'print("Hello, world!")', "expect": "Hello, world!"},
            {"prompt": "Puzzle 9: Print the word  banana.",
             "starter": 'print("banana")', "expect": "banana"},
            {"prompt": "Puzzle 10: Print  Yes.",
             "starter": 'print("Yes")', "expect": "Yes"},
            {"prompt": "Puzzle 11: Print the city you live in.",
             "starter": 'print("Delhi")', "expect_any": True},
            {"prompt": "Puzzle 12: Print  Bye.",
             "starter": 'print("Bye")', "expect": "Bye"},
        ],
    },
    {
        "title": "Strings",
        "emoji": "🔤",
        "youtube": "https://www.youtube.com/watch?v=u2S5kIsAjLM&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=2",
        "theory": [
            "A STRING is text — words and letters inside quotes \" \".",
            "Strings can be short or long, and they can contain numbers too.",
            "You can use print( ) to show strings on the screen.",
            "You can also JOIN (combine) strings using the  +  sign.",
            "Look at these examples 👇",
            '   print("Hello")           →  shows:  Hello',
            '   print("Python is fun")   →  shows:  Python is fun',
            '   print("123")             →  shows:  123',
            '   name = "Alice"\n   print(name)   →  shows:  Alice',
            '   print("Hello" + " " + "World")  →  shows:  Hello World',
            "Key: quotes make a STRING. Without quotes, Python thinks it\'s a number or name.",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Print two lines:  Hi  then  Bye",
             "starter": 'print("Hi")\nprint("Bye")', "expect": "Hi\nBye"},
            {"prompt": "Puzzle 2: Print the number  100  (no quotes!).",
             "starter": "print(100)", "expect": "100"},
            {"prompt": "Puzzle 3: Print three lines:  A  then  B  then  C",
             "starter": 'print("A")\nprint("B")\nprint("C")', "expect": "A\nB\nC"},
            {"prompt": "Puzzle 4: Print the number  7.",
             "starter": "print(7)", "expect": "7"},
            {"prompt": "Puzzle 5: Print  Red  then  Green  on two lines.",
             "starter": 'print("Red")\nprint("Green")', "expect": "Red\nGreen"},
            {"prompt": "Puzzle 6: Print the numbers  1  2  3  each on its own line.",
             "starter": 'print(1)\nprint(2)\nprint(3)', "expect": "1\n2\n3"},
            {"prompt": "Puzzle 7: Print  Cat  Dog  Fish  on three lines.",
             "starter": 'print("Cat")\nprint("Dog")\nprint("Fish")', "expect": "Cat\nDog\nFish"},
            {"prompt": "Puzzle 8: Print the number  42.",
             "starter": "print(42)", "expect": "42"},
            {"prompt": "Puzzle 9: Print the number  0.",
             "starter": "print(0)", "expect": "0"},
            {"prompt": "Puzzle 10: Print  Line1  then  Line2.",
             "starter": 'print("Line1")\nprint("Line2")', "expect": "Line1\nLine2"},
            {"prompt": "Puzzle 11: Print the big number  999.",
             "starter": "print(999)", "expect": "999"},
            {"prompt": "Puzzle 12: Print  One  Two  Three  on three lines.",
             "starter": 'print("One")\nprint("Two")\nprint("Three")', "expect": "One\nTwo\nThree"},
        ],
    },
    {
        "title": "Numbers",
        "emoji": "🔢",
        "youtube": "https://www.youtube.com/watch?v=OMAmgNmJB9c&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=3",
        "theory": [
            "Numbers in Python are used for math and counting. No quotes needed!",
            "You can use these math operators:  +  (add)  -  (subtract)  *  (multiply)  /  (divide)",
            "Use print( ) to show the RESULT of math on the screen.",
            "Python does math just like a calculator!",
            "Look at these examples 👇",
            "   print(5 + 3)       →  shows:  8",
            "   print(10 - 4)      →  shows:  6",
            "   print(3 * 4)       →  shows:  12",
            "   print(20 / 4)      →  shows:  5.0",
            "   print(2 + 3 * 4)   →  shows:  14  (multiply first, then add)",
            "Numbers do NOT need quotes. Math operators work left to right (with some rules).",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Make a box called  age  that holds  8,  then print it.",
             "starter": "age = 8\nprint(age)", "expect": "8"},
            {"prompt": "Puzzle 2: Put your name in a box called  name  and print it.",
             "starter": 'name = "Sam"\nprint(name)', "expect_any": True},
            {"prompt": "Puzzle 3: Make a box  color = \"red\"  and print it.",
             "starter": 'color = "red"\nprint(color)', "expect": "red"},
            {"prompt": "Puzzle 4: Put  5  in a box called  x  and print it.",
             "starter": "x = 5\nprint(x)", "expect": "5"},
            {"prompt": "Puzzle 5: Make a box  pet = \"dog\"  and print it.",
             "starter": 'pet = "dog"\nprint(pet)', "expect": "dog"},
            {"prompt": "Puzzle 6: Put  10  in a box called  num  and print it.",
             "starter": "num = 10\nprint(num)", "expect": "10"},
            {"prompt": "Puzzle 7: Make a box  fruit = \"apple\"  and print it.",
             "starter": 'fruit = "apple"\nprint(fruit)', "expect": "apple"},
            {"prompt": "Puzzle 8: Put  3  in a box called  a  and print it.",
             "starter": "a = 3\nprint(a)", "expect": "3"},
            {"prompt": "Puzzle 9: Make a box  word = \"hello\"  and print it.",
             "starter": 'word = "hello"\nprint(word)', "expect": "hello"},
            {"prompt": "Puzzle 10: Put  100  in a box called  score  and print it.",
             "starter": "score = 100\nprint(score)", "expect": "100"},
            {"prompt": "Puzzle 11: Make a box  best = \"pizza\"  and print it.",
             "starter": 'best = "pizza"\nprint(best)', "expect": "pizza"},
            {"prompt": "Puzzle 12: Put your favorite food in a box called  food  and print it.",
             "starter": 'food = "mango"\nprint(food)', "expect_any": True},
        ],
    },
    {
        "title": "Variables",
        "emoji": "📦",
        "youtube": "https://www.youtube.com/watch?v=rdagUxtTn-U&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=4",
        "theory": [
            "A VARIABLE is a container (like a box) that STORES a value to use later.",
            "Create a variable using the  =  sign:   variablename = value",
            "The name goes on the LEFT, the value goes on the RIGHT.",
            "Variable names can be words, numbers (but not first), or underscores _ .",
            "Look at these examples 👇",
            '   age = 10              →  variable \"age\" holds the number 10',
            '   name = "Alice"        →  variable \"name\" holds the string Alice',
            '   color = "blue"        →  variable \"color\" holds the string blue',
            "   score = 100           →  variable \"score\" holds the number 100",
            '   print(age)            →  shows:  10  (no quotes around age)',
            "Use the variable name (NO quotes) when you want to see or use its value.",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Print the answer to  7 + 5.",
             "starter": "print(7 + 5)", "expect": "12"},
            {"prompt": "Puzzle 2: Print how much is  6 times 3.",
             "starter": "print(6 * 3)", "expect": "18"},
            {"prompt": "Puzzle 3: Print the answer to  10 - 4.",
             "starter": "print(10 - 4)", "expect": "6"},
            {"prompt": "Puzzle 4: Print the answer to  8 + 2.",
             "starter": "print(8 + 2)", "expect": "10"},
            {"prompt": "Puzzle 5: Print how much is  5 times 5.",
             "starter": "print(5 * 5)", "expect": "25"},
            {"prompt": "Puzzle 6: Print the answer to  100 - 1.",
             "starter": "print(100 - 1)", "expect": "99"},
            {"prompt": "Puzzle 7: Print the answer to  3 + 4 + 5.",
             "starter": "print(3 + 4 + 5)", "expect": "12"},
            {"prompt": "Puzzle 8: Print how much is  9 times 2.",
             "starter": "print(9 * 2)", "expect": "18"},
            {"prompt": "Puzzle 9: Print the answer to  12 - 6.",
             "starter": "print(12 - 6)", "expect": "6"},
            {"prompt": "Puzzle 10: Print how much is  2 times 10.",
             "starter": "print(2 * 10)", "expect": "20"},
            {"prompt": "Puzzle 11: Print the answer to  15 + 15.",
             "starter": "print(15 + 15)", "expect": "30"},
            {"prompt": "Puzzle 12: Print how much is  7 times 7.",
             "starter": "print(7 * 7)", "expect": "49"},
        ],
    },
    {
        "title": "Lists",
        "emoji": "📋",
        "youtube": "https://www.youtube.com/watch?v=TZUYanphUmU&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=5",
        "theory": [
            "A LIST holds MANY items in ONE container, inside square brackets [ ].",
            "Items in a list are separated by commas and can be strings or numbers.",
            "Each item has a POSITION (index). Counting starts at 0, not 1!",
            "Use list[0] to get the FIRST item, list[1] for the SECOND, etc.",
            "Look at these examples 👇",
            '   fruits = ["apple", "banana", "cherry"]   →  a list of 3 fruits',
            '   print(fruits[0])        →  shows:  apple  (the first fruit)',
            '   print(fruits[1])        →  shows:  banana (the second fruit)',
            '   numbers = [1, 2, 3, 4]  →  a list of 4 numbers',
            "   len(fruits)             →  shows:  3  (how many items in the list)",
            "Use for loops to go through EVERY item: for item in list:",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Glue  Py  and  thon  to print  Python.",
             "starter": 'print("Py" + "thon")', "expect": "Python"},
            {"prompt": "Puzzle 2: Print  I love code  by gluing words with spaces.",
             "starter": 'print("I" + " " + "love" + " " + "code")', "expect": "I love code"},
            {"prompt": "Puzzle 3: Glue  sun  and  flower  to print  sunflower.",
             "starter": 'print("sun" + "flower")', "expect": "sunflower"},
            {"prompt": "Puzzle 4: Glue  cat  and  dog  to print  catdog.",
             "starter": 'print("cat" + "dog")', "expect": "catdog"},
            {"prompt": "Puzzle 5: Print  Hello there  (glue with a space in between).",
             "starter": 'print("Hello" + " " + "there")', "expect": "Hello there"},
            {"prompt": "Puzzle 6: Glue  rain  and  bow  to print  rainbow.",
             "starter": 'print("rain" + "bow")', "expect": "rainbow"},
            {"prompt": "Puzzle 7: Glue  ice  and  cream  to print  icecream.",
             "starter": 'print("ice" + "cream")', "expect": "icecream"},
            {"prompt": "Puzzle 8: Print  Good job  (glue with a space).",
             "starter": 'print("Good" + " " + "job")', "expect": "Good job"},
            {"prompt": "Puzzle 9: Glue  foot  and  ball  to print  football.",
             "starter": 'print("foot" + "ball")', "expect": "football"},
            {"prompt": "Puzzle 10: Glue  star  and  fish  to print  starfish.",
             "starter": 'print("star" + "fish")', "expect": "starfish"},
            {"prompt": "Puzzle 11: Glue  Ha  three times to print  HaHaHa.",
             "starter": 'print("Ha" + "Ha" + "Ha")', "expect": "HaHaHa"},
            {"prompt": "Puzzle 12: Glue your first and last name with a space and print it.",
             "starter": 'print("Sam" + " " + "Roy")', "expect_any": True},
        ],
    },
    {
        "title": "Logical Conditions and Booleans",
        "emoji": "✅",
        "youtube": "https://www.youtube.com/watch?v=TeAUYpkFoh0&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=6",
        "theory": [
            "BOOLEANS are values that are either True or False — yes or no.",
            "A CONDITION asks a yes/no question by COMPARING things.",
            "Use these COMPARISON OPERATORS:",
            "   ==  (equal)   !=  (not equal)   >  (greater)   <  (less)",
            "   >=  (greater or equal)   <=  (less or equal)",
            "Look at these examples 👇",
            "   5 > 3          →  True   (5 is bigger than 3)",
            "   10 < 5         →  False  (10 is not smaller than 5)",
            "   7 == 7         →  True   (7 equals 7)",
            "   4 != 9         →  True   (4 does not equal 9)",
            "IMPORTANT: use  ==  (TWO equals) to compare, and  =  (ONE equals) to assign.",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Print whether  10  is greater than  4.",
             "starter": "print(10 > 4)", "expect": "True"},
            {"prompt": "Puzzle 2: Print whether  5  equals  8.",
             "starter": "print(5 == 8)", "expect": "False"},
            {"prompt": "Puzzle 3: Print whether  3  is less than  9.",
             "starter": "print(3 < 9)", "expect": "True"},
            {"prompt": "Puzzle 4: Print whether  7  equals  7.",
             "starter": "print(7 == 7)", "expect": "True"},
            {"prompt": "Puzzle 5: Print whether  2  is greater than  10.",
             "starter": "print(2 > 10)", "expect": "False"},
            {"prompt": "Puzzle 6: Print whether  100  is less than  50.",
             "starter": "print(100 < 50)", "expect": "False"},
            {"prompt": "Puzzle 7: Print whether  6  equals  6.",
             "starter": "print(6 == 6)", "expect": "True"},
            {"prompt": "Puzzle 8: Print whether  4  is greater than  1.",
             "starter": "print(4 > 1)", "expect": "True"},
            {"prompt": "Puzzle 9: Print whether  8  is less than  8.",
             "starter": "print(8 < 8)", "expect": "False"},
            {"prompt": "Puzzle 10: Print whether  5  equals  5.",
             "starter": "print(5 == 5)", "expect": "True"},
            {"prompt": "Puzzle 11: Print whether  9  is greater than  3.",
             "starter": "print(9 > 3)", "expect": "True"},
            {"prompt": "Puzzle 12: Print whether  1  equals  2.",
             "starter": "print(1 == 2)", "expect": "False"},
        ],
    },
    {
        "title": "If Statements",
        "emoji": "🔀",
        "youtube": "https://www.youtube.com/watch?v=K9CpWEWYXt4&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=7",
        "theory": [
            "An IF STATEMENT lets your program make DECISIONS based on conditions.",
            "If a condition is True, the code block runs. If False, it skips.",
            "Format:   if condition:\n                code_to_run",
            "The code under the if MUST be INDENTED (pushed in with spaces).",
            "You can also use  else  for code that runs if the condition is False.",
            "Look at these examples 👇",
            '   age = 10\n   if age >= 10:\n       print("You are old enough!")   →  You are old enough!',
            '   score = 5\n   if score > 10:\n       print("You won!")   →  (nothing shows, condition is False)',
            '   if 7 < 10:\n       print("7 is less than 10")   →  7 is less than 10',
            "Remember: indent the code inside the if block with spaces or tabs.",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: If  age  (which is 8) is more than 7, print  Big kid!",
             "starter": 'age = 8\nif age > 7:\n    print("Big kid!")', "expect": "Big kid!"},
            {"prompt": "Puzzle 2: If  score  is 100, print  Perfect!",
             "starter": 'score = 100\nif score == 100:\n    print("Perfect!")', "expect": "Perfect!"},
            {"prompt": "Puzzle 3: x is 5. If  x > 0,  print  Positive.",
             "starter": 'x = 5\nif x > 0:\n    print("Positive")', "expect": "Positive"},
            {"prompt": "Puzzle 4: num is 10. If  num == 10,  print  Ten.",
             "starter": 'num = 10\nif num == 10:\n    print("Ten")', "expect": "Ten"},
            {"prompt": "Puzzle 5: age is 6. If  age < 7,  print  Little star.",
             "starter": 'age = 6\nif age < 7:\n    print("Little star")', "expect": "Little star"},
            {"prompt": "Puzzle 6: temp is 30. If  temp > 20,  print  Hot.",
             "starter": 'temp = 30\nif temp > 20:\n    print("Hot")', "expect": "Hot"},
            {"prompt": "Puzzle 7: coins is 5. If  coins == 5,  print  Five coins.",
             "starter": 'coins = 5\nif coins == 5:\n    print("Five coins")', "expect": "Five coins"},
            {"prompt": "Puzzle 8: speed is 3. If  speed < 10,  print  Slow.",
             "starter": 'speed = 3\nif speed < 10:\n    print("Slow")', "expect": "Slow"},
            {"prompt": "Puzzle 9: lives is 1. If  lives > 0,  print  Keep going.",
             "starter": 'lives = 1\nif lives > 0:\n    print("Keep going")', "expect": "Keep going"},
            {"prompt": "Puzzle 10: n is 8. If  n == 8,  print  Eight.",
             "starter": 'n = 8\nif n == 8:\n    print("Eight")', "expect": "Eight"},
            {"prompt": "Puzzle 11: score is 50. If  score > 40,  print  You passed.",
             "starter": 'score = 50\nif score > 40:\n    print("You passed")', "expect": "You passed"},
            {"prompt": "Puzzle 12: rain is True. If  rain,  print  Take umbrella.",
             "starter": 'rain = True\nif rain:\n    print("Take umbrella")', "expect": "Take umbrella"},
        ],
    },
    {
        "title": "For Loop Statements",
        "emoji": "🔁",
        "youtube": "https://www.youtube.com/watch?v=Mhc9_AbP5ks&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=8",
        "theory": [
            "A FOR LOOP repeats code a certain number of times automatically.",
            "Instead of typing the same code over and over, you write it ONCE inside a loop.",
            "Format:   for variable in sequence:\n                code_to_repeat",
            "The variable holds the CURRENT VALUE in each loop cycle.",
            "Common use:  for i in range(n):  repeats n times (i goes 0, 1, 2, ... n-1).",
            "Look at these examples 👇",
            '   for i in range(3):\n       print("Python")   →  Python, Python, Python',
            "   for i in range(5):\n       print(i)          →  0, 1, 2, 3, 4",
            '   for fruit in ["apple", "banana"]:\n       print(fruit)  →  apple, banana',
            "Use loops to avoid repeating code and to handle big lists easily.",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Print  Hi  three times using a loop.",
             "starter": 'for i in range(3):\n    print("Hi")', "expect": "Hi\nHi\nHi"},
            {"prompt": "Puzzle 2: Print the numbers  0 1 2 3 4  (each on its own line).",
             "starter": "for i in range(5):\n    print(i)", "expect": "0\n1\n2\n3\n4"},
            {"prompt": "Puzzle 3: Print  Go  two times using a loop.",
             "starter": 'for i in range(2):\n    print("Go")', "expect": "Go\nGo"},
            {"prompt": "Puzzle 4: Print  Yay  four times using a loop.",
             "starter": 'for i in range(4):\n    print("Yay")', "expect": "Yay\nYay\nYay\nYay"},
            {"prompt": "Puzzle 5: Print the numbers  0 1 2  using a loop.",
             "starter": "for i in range(3):\n    print(i)", "expect": "0\n1\n2"},
            {"prompt": "Puzzle 6: Print  1 2 3  using  range(1, 4).",
             "starter": "for n in range(1, 4):\n    print(n)", "expect": "1\n2\n3"},
            {"prompt": "Puzzle 7: Print  Hello  three times using a loop.",
             "starter": 'for i in range(3):\n    print("Hello")', "expect": "Hello\nHello\nHello"},
            {"prompt": "Puzzle 8: Print the numbers  0  to  5  using a loop.",
             "starter": "for i in range(6):\n    print(i)", "expect": "0\n1\n2\n3\n4\n5"},
            {"prompt": "Puzzle 9: Print  Jump  four times using a loop.",
             "starter": 'for i in range(4):\n    print("Jump")', "expect": "Jump\nJump\nJump\nJump"},
            {"prompt": "Puzzle 10: Print  1 2 3 4 5  using  range(1, 6).",
             "starter": "for n in range(1, 6):\n    print(n)", "expect": "1\n2\n3\n4\n5"},
            {"prompt": "Puzzle 11: Print  Star  two times using a loop.",
             "starter": 'for i in range(2):\n    print("Star")', "expect": "Star\nStar"},
            {"prompt": "Puzzle 12: Print  Loop  two times using a loop.",
             "starter": 'for i in range(2):\n    print("Loop")', "expect": "Loop\nLoop"},
        ],
    },
    {
        "title": "Range",
        "emoji": "🔢",
        "youtube": "https://www.youtube.com/watch?v=LGtB6zCtJGA&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=9",
        "theory": [
            "RANGE creates a SEQUENCE of numbers that you can loop through.",
            "It's perfect for for loops when you need to repeat something a set number of times.",
            "range(n) creates: 0, 1, 2, ... n-1  (starts at 0, goes up to n-1).",
            "range(start, end) creates: start, start+1, ... end-1  (from start to end-1).",
            "range(start, end, step) counts by STEP amounts (1, 3, 5, ...).",
            "Look at these examples 👇",
            "   for i in range(5):          →  loops 5 times: i = 0, 1, 2, 3, 4",
            "   for i in range(2, 5):       →  loops 3 times: i = 2, 3, 4",
            "   for i in range(0, 10, 2):  →  loops with step 2: i = 0, 2, 4, 6, 8",
            "   list(range(5))              →  creates a list: [0, 1, 2, 3, 4]",
            "Range is super useful for controlling exactly how many times a loop runs.",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Make a list  pets = [\"cat\", \"dog\"]  and print the first pet.",
             "starter": 'pets = ["cat", "dog"]\nprint(pets[0])', "expect": "cat"},
            {"prompt": "Puzzle 2: Print each color in  [\"red\", \"blue\"]  on its own line.",
             "starter": 'for c in ["red", "blue"]:\n    print(c)', "expect": "red\nblue"},
            {"prompt": "Puzzle 3: Make  nums = [1, 2, 3]  and print the first number.",
             "starter": "nums = [1, 2, 3]\nprint(nums[0])", "expect": "1"},
            {"prompt": "Puzzle 4: From  [\"apple\", \"banana\"]  print the SECOND fruit (index 1).",
             "starter": 'fruits = ["apple", "banana"]\nprint(fruits[1])', "expect": "banana"},
            {"prompt": "Puzzle 5: Print each number in  [1, 2, 3]  on its own line.",
             "starter": "for x in [1, 2, 3]:\n    print(x)", "expect": "1\n2\n3"},
            {"prompt": "Puzzle 6: From  [\"green\", \"yellow\"]  print the second color.",
             "starter": 'colors = ["green", "yellow"]\nprint(colors[1])', "expect": "yellow"},
            {"prompt": "Puzzle 7: Print how many things are in  [1, 2, 3, 4]  using  len().",
             "starter": "print(len([1, 2, 3, 4]))", "expect": "4"},
            {"prompt": "Puzzle 8: Make  animals = [\"fox\"]  and print the first animal.",
             "starter": 'animals = ["fox"]\nprint(animals[0])', "expect": "fox"},
            {"prompt": "Puzzle 9: Print each number in  [10, 20]  on its own line.",
             "starter": "for n in [10, 20]:\n    print(n)", "expect": "10\n20"},
            {"prompt": "Puzzle 10: From  [\"a\", \"b\", \"c\"]  print the THIRD one (index 2).",
             "starter": 'print(["a", "b", "c"][2])', "expect": "c"},
            {"prompt": "Puzzle 11: Make  fruits = [\"mango\", \"kiwi\"]  and print the first fruit.",
             "starter": 'fruits = ["mango", "kiwi"]\nprint(fruits[0])', "expect": "mango"},
            {"prompt": "Puzzle 12: Print each word in  [\"hi\", \"bye\"]  on its own line.",
             "starter": 'for w in ["hi", "bye"]:\n    print(w)', "expect": "hi\nbye"},
        ],
    },
    {
        "title": "Function Statements",
        "emoji": "🧩",
        "youtube": "https://www.youtube.com/watch?v=7eyiXO-B044&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=10",
        "theory": [
            "A FUNCTION is a reusable BLOCK OF CODE that does a specific task.",
            "Define a function using  def  keyword:  def function_name():",
            "The code INSIDE the function is INDENTED and runs only when you CALL it.",
            "To RUN (call) a function, write its name followed by ( ):  function_name()",
            "Functions let you avoid writing the same code over and over.",
            "Look at these examples 👇",
            '   def greet():\n       print("Hello, friend!")   →  defines the function',
            '   greet()                                  →  calls the function, shows: Hello, friend!',
            '   def draw_line():\n       print("-" * 10)\n   draw_line()\n   draw_line()  →  shows 2 lines',
            "Functions make code cleaner and easier to reuse.",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Make a function  hello  that prints  Hi there!  then call it.",
             "starter": 'def hello():\n    print("Hi there!")\n\nhello()', "expect": "Hi there!"},
            {"prompt": "Puzzle 2: Make a function  cheer  that prints  Yay!  and call it twice.",
             "starter": 'def cheer():\n    print("Yay!")\n\ncheer()\ncheer()', "expect": "Yay!\nYay!"},
            {"prompt": "Puzzle 3: Make a function  hi  that prints  Hello  and call it.",
             "starter": 'def hi():\n    print("Hello")\n\nhi()', "expect": "Hello"},
            {"prompt": "Puzzle 4: Make a function  bark  that prints  Woof  and call it.",
             "starter": 'def bark():\n    print("Woof")\n\nbark()', "expect": "Woof"},
            {"prompt": "Puzzle 5: Make a function  clap  that prints  Clap  and call it 3 times.",
             "starter": 'def clap():\n    print("Clap")\n\nclap()\nclap()\nclap()', "expect": "Clap\nClap\nClap"},
            {"prompt": "Puzzle 6: Make a function  add  that prints  2 + 3  and call it.",
             "starter": 'def add():\n    print(2 + 3)\n\nadd()', "expect": "5"},
            {"prompt": "Puzzle 7: Make a function  star  that prints  star  and call it.",
             "starter": 'def star():\n    print("star")\n\nstar()', "expect": "star"},
            {"prompt": "Puzzle 8: Make a function  sing  that prints  La  and call it twice.",
             "starter": 'def sing():\n    print("La")\n\nsing()\nsing()', "expect": "La\nLa"},
            {"prompt": "Puzzle 9: Make a function  greet  that prints  Hi Sam  and call it.",
             "starter": 'def greet():\n    print("Hi Sam")\n\ngreet()', "expect": "Hi Sam"},
            {"prompt": "Puzzle 10: Make a function  count  that prints  1  then  2,  and call it.",
             "starter": 'def count():\n    print(1)\n    print(2)\n\ncount()', "expect": "1\n2"},
            {"prompt": "Puzzle 11: Make a function  wave  that prints  Bye!  and call it.",
             "starter": 'def wave():\n    print("Bye!")\n\nwave()', "expect": "Bye!"},
            {"prompt": "Puzzle 12: Make a function  myname  that prints your name, and call it.",
             "starter": 'def myname():\n    print("Sam")\n\nmyname()', "expect_any": True},
        ],
    },
    {
        "title": "Write Functions",
        "emoji": "✍️",
        "youtube": "https://www.youtube.com/watch?v=QT-MlfIBWnI&list=PLIQId4LTxIpAHNNJ24YruAhx8HFlovUSK&index=11",
        "theory": [
            "Now you'll write FUNCTIONS with PARAMETERS — inputs that the function uses.",
            "A parameter is a VALUE passed INTO a function when you call it.",
            "Format:   def function_name(parameter):\n                use parameter here",
            "Call it:   function_name(value)   →  passes value into the function",
            "Functions can have MULTIPLE parameters separated by commas.",
            "Look at these examples 👇",
            '   def greet(name):\n       print("Hello, " + name)\n   greet("Alice")  →  Hello, Alice',
            '   def add(a, b):\n       print(a + b)\n   add(3, 5)  →  8',
            '   def multiply(x, y):\n       return x * y\n   result = multiply(4, 6)  →  result is 24',
            "Functions with parameters are SUPER powerful — they let you write flexible, reusable code!",
        ],
        "puzzles": [
            {"prompt": "Puzzle 1: Print  1 2 3 4 5  (each on its own line) with a loop.",
             "starter": "for n in range(1, 6):\n    print(n)", "expect": "1\n2\n3\n4\n5"},
            {"prompt": "Puzzle 2: Loop 1 to 5. Print each number, then print  High five!",
             "starter": 'for n in range(1, 6):\n    print(n)\nprint("High five!")',
             "expect": "1\n2\n3\n4\n5\nHigh five!"},
            {"prompt": "Puzzle 3: Print  Go  three times with a loop.",
             "starter": 'for i in range(3):\n    print("Go")', "expect": "Go\nGo\nGo"},
            {"prompt": "Puzzle 4: Count  1 2 3  with a loop.",
             "starter": "for n in range(1, 4):\n    print(n)", "expect": "1\n2\n3"},
            {"prompt": "Puzzle 5: Print  Ready  Set  Go  on three lines.",
             "starter": 'print("Ready")\nprint("Set")\nprint("Go")', "expect": "Ready\nSet\nGo"},
            {"prompt": "Puzzle 6: Loop 1 to 5 printing each number, then print  Done.",
             "starter": 'for n in range(1, 6):\n    print(n)\nprint("Done")',
             "expect": "1\n2\n3\n4\n5\nDone"},
            {"prompt": "Puzzle 7: score is 10. If  score > 5,  print  Winner.",
             "starter": 'score = 10\nif score > 5:\n    print("Winner")', "expect": "Winner"},
            {"prompt": "Puzzle 8: Print a star  *  three times with a loop.",
             "starter": 'for i in range(3):\n    print("*")', "expect": "*\n*\n*"},
            {"prompt": "Puzzle 9: Blast off! Print  5 4 3 2 1  each on its own line.",
             "starter": "print(5)\nprint(4)\nprint(3)\nprint(2)\nprint(1)", "expect": "5\n4\n3\n2\n1"},
            {"prompt": "Puzzle 10: Put your hero name in  hero  and print it.",
             "starter": 'hero = "Zoom"\nprint(hero)', "expect_any": True},
            {"prompt": "Puzzle 11: Loop 1 to 5 printing each number, then print  Win!",
             "starter": 'for n in range(1, 6):\n    print(n)\nprint("Win!")',
             "expect": "1\n2\n3\n4\n5\nWin!"},
            {"prompt": "Puzzle 12: Print  GAME OVER  to finish the game.",
             "starter": 'print("GAME OVER")', "expect": "GAME OVER"},
        ],
    },
]


# ===================================================================
#  ADVENTURE MODE  —  write Python to move a hero in a game world
# ===================================================================
GRID = 6  # 6 x 6 tiles

# Each level: hero start (x, y, facing), objects, mission text, tools,
# starter code, and a check(engine) that returns True when solved.
ADV_LEVELS = [
    {
        "id": "A1", "title": "First Steps", "emoji": "🦘",
        "mission": ["Walk the hero to the flag 🚩.",
                    "Use  hero.move_right(3)  to hop 3 tiles to the right."],
        "tools": ["move_right(n)", "move_left(n)"],
        "start": (0, 5, "right"), "trees": [], "gems": [], "walls": [],
        "flag": (3, 5),
        "starter": "hero.move_right(3)",
        "check": lambda e: (e.x, e.y) == e.flag,
    },
    {
        "id": "A2", "title": "Turn & Walk", "emoji": "🧭",
        "mission": ["The flag is up high! 🚩",
                    "Go right, then up. Try  hero.move_up(3)."],
        "tools": ["move_right(n)", "move_up(n)"],
        "start": (0, 5, "right"), "trees": [], "gems": [], "walls": [],
        "flag": (3, 2),
        "starter": "hero.move_right(3)\nhero.move_up(3)",
        "check": lambda e: (e.x, e.y) == e.flag,
    },
    {
        "id": "A3", "title": "Loop the Path", "emoji": "🔁",
        "mission": ["The flag is 5 tiles away. 🚩",
                    "Don't type move 5 times — use a loop!",
                    "for i in range(5):",
                    "    hero.move_right(1)"],
        "tools": ["move_right(n)", "for i in range(n):"],
        "start": (0, 5, "right"), "trees": [], "gems": [], "walls": [],
        "flag": (5, 5),
        "starter": "for i in range(5):\n    hero.move_right(1)",
        "check": lambda e: (e.x, e.y) == e.flag,
    },
    {
        "id": "A4", "title": "Chop the Tree", "emoji": "🪓",
        "mission": ["A tree 🌳 blocks the path!",
                    "You are facing it. Use  hero.chop()  first,",
                    "then walk to the flag 🚩."],
        "tools": ["chop()", "move_right(n)"],
        "start": (0, 5, "right"), "trees": [(1, 5)], "gems": [], "walls": [],
        "flag": (4, 5),
        "starter": "hero.chop()\nhero.move_right(4)",
        "check": lambda e: (e.x, e.y) == e.flag and len(e.trees) == 0,
    },
    {
        "id": "A5", "title": "Grab the Gem", "emoji": "💎",
        "mission": ["Reach the gem 💎 and pick it up.",
                    "Walk onto its tile, then  hero.pickup()."],
        "tools": ["move_right(n)", "move_up(n)", "pickup()"],
        "start": (0, 5, "right"), "trees": [], "gems": [(3, 3)], "walls": [],
        "flag": None,
        "starter": "hero.move_right(3)\nhero.move_up(2)\nhero.pickup()",
        "check": lambda e: e.collected >= 1,
    },
    {
        "id": "A6", "title": "If Blocked, Jump", "emoji": "🔀",
        "mission": ["Is a tree ahead? Only chop IF it is.",
                    "if hero.tree_ahead():",
                    "    hero.chop()",
                    "then walk to the flag 🚩."],
        "tools": ["tree_ahead()", "chop()", "if:", "move_right(n)"],
        "start": (0, 5, "right"), "trees": [(1, 5)], "gems": [], "walls": [],
        "flag": (3, 5),
        "starter": "if hero.tree_ahead():\n    hero.chop()\nhero.move_right(3)",
        "check": lambda e: (e.x, e.y) == e.flag and len(e.trees) == 0,
    },
    {
        "id": "A7", "title": "Count the Coins", "emoji": "🪙",
        "mission": ["Collect all 3 gems 💎 in a row.",
                    "Walk a step and pickup, again and again.",
                    "A loop makes it easy!"],
        "tools": ["move_right(n)", "pickup()", "for i in range(n):"],
        "start": (0, 5, "right"), "trees": [], "gems": [(1, 5), (2, 5), (3, 5)],
        "walls": [], "flag": None,
        "starter": "for i in range(3):\n    hero.move_right(1)\n    hero.pickup()",
        "check": lambda e: e.collected >= 3,
    },
    {
        "id": "A8", "title": "Paint a Picture", "emoji": "🎨",
        "mission": ["Paint a red stripe of 3 tiles! 🎨",
                    'Use  hero.paint("red")  then move and paint again.'],
        "tools": ['paint("red")', "move_right(n)"],
        "start": (0, 5, "right"), "trees": [], "gems": [], "walls": [],
        "flag": None,
        "starter": ('hero.paint("red")\n'
                    'hero.move_right(1)\nhero.paint("red")\n'
                    'hero.move_right(1)\nhero.paint("red")'),
        "check": lambda e: sum(1 for c in e.painted.values() if c == "red") >= 3,
    },
    {
        "id": "A9", "title": "Draw a Square", "emoji": "🟦",
        "mission": ["Put the pen down and drive in a square!",
                    "hero.pen_down()",
                    "for i in range(4):",
                    "    hero.forward(2)",
                    "    hero.turn_right()"],
        "tools": ["pen_down()", "forward(n)", "turn_right()", "for i in range(n):"],
        "start": (1, 1, "right"), "trees": [], "gems": [], "walls": [],
        "flag": None,
        "starter": ("hero.pen_down()\nfor i in range(4):\n"
                    "    hero.forward(2)\n    hero.turn_right()"),
        "check": lambda e: len(e.painted) >= 8,
    },
    {
        "id": "A10", "title": "Maze Run", "emoji": "🧱",
        "mission": ["Walls 🧱 block the way. Find the open path!",
                    "Go down the left side, then across the bottom."],
        "tools": ["move_down(n)", "move_right(n)"],
        "start": (0, 0, "down"),
        "trees": [], "gems": [],
        "walls": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                  (2, 2), (3, 2), (3, 3), (3, 4), (4, 4)],
        "flag": (5, 5),
        "starter": "hero.move_down(5)\nhero.move_right(5)",
        "check": lambda e: (e.x, e.y) == e.flag,
    },
    {
        "id": "A11", "title": "Boss: Treasure Hunt", "emoji": "🏆",
        "mission": ["The big one! Chop the tree 🌳, grab BOTH gems 💎💎,",
                    "then stand on the flag 🚩. Use everything you know!"],
        "tools": ["chop()", "move_right(n)", "move_up(n)", "pickup()"],
        "start": (0, 5, "right"), "trees": [(1, 5)],
        "gems": [(3, 5), (3, 2)], "walls": [], "flag": (5, 2),
        "starter": ("hero.chop()\nhero.move_right(3)\nhero.pickup()\n"
                    "hero.move_up(3)\nhero.pickup()\nhero.move_right(2)"),
        "check": lambda e: (e.x, e.y) == e.flag and e.collected >= 2 and len(e.trees) == 0,
    },

    # ---------------- SPACE WORLD 🚀 ----------------
    {
        "id": "S1", "title": "Blast Off", "emoji": "🚀", "theme": "space",
        "world": "🚀 SPACE WORLD",
        "mission": ["Fly the rocket 🚀 to the planet 🪐.",
                    "Use  hero.move_right(4)."],
        "tools": ["move_right(n)"],
        "start": (0, 5, "right"), "trees": [], "gems": [], "walls": [],
        "flag": (4, 5),
        "starter": "hero.move_right(4)",
        "check": lambda e: (e.x, e.y) == e.flag,
    },
    {
        "id": "S2", "title": "Catch a Star", "emoji": "⭐", "theme": "space",
        "world": "🚀 SPACE WORLD",
        "mission": ["Fly up to the star ⭐ and grab it.",
                    "Go right, then up, then  hero.pickup()."],
        "tools": ["move_right(n)", "move_up(n)", "pickup()"],
        "start": (0, 5, "right"), "trees": [], "gems": [(5, 0)], "walls": [],
        "flag": None,
        "starter": "hero.move_right(5)\nhero.move_up(5)\nhero.pickup()",
        "check": lambda e: e.collected >= 1,
    },
    {
        "id": "S3", "title": "Asteroid Field", "emoji": "☄️", "theme": "space",
        "world": "🚀 SPACE WORLD",
        "mission": ["An asteroid ☄️ blocks the way!",
                    "Blast it with  hero.chop()  then fly to the planet 🪐."],
        "tools": ["chop()", "move_right(n)"],
        "start": (0, 5, "right"), "trees": [(1, 5)], "gems": [], "walls": [],
        "flag": (3, 5),
        "starter": "hero.chop()\nhero.move_right(3)",
        "check": lambda e: (e.x, e.y) == e.flag and len(e.trees) == 0,
    },
    {
        "id": "S4", "title": "Collect 3 Stars", "emoji": "✨", "theme": "space",
        "world": "🚀 SPACE WORLD",
        "mission": ["Scoop up all 3 stars ⭐ in a row using a loop!"],
        "tools": ["move_right(n)", "pickup()", "for i in range(n):"],
        "start": (0, 5, "right"), "trees": [], "gems": [(1, 5), (2, 5), (3, 5)],
        "walls": [], "flag": None,
        "starter": "for i in range(3):\n    hero.move_right(1)\n    hero.pickup()",
        "check": lambda e: e.collected >= 3,
    },
    {
        "id": "S5", "title": "Comet Trail", "emoji": "🌠", "theme": "space",
        "world": "🚀 SPACE WORLD",
        "mission": ["Leave a glowing comet trail across space! 🌠",
                    "hero.pen_down()  then  hero.forward(5)."],
        "tools": ["pen_down()", "forward(n)"],
        "start": (5, 5, "left"), "trees": [], "gems": [], "walls": [],
        "flag": None,
        "starter": "hero.pen_down()\nhero.forward(5)",
        "check": lambda e: len(e.painted) >= 5,
    },
    {
        "id": "S6", "title": "Boss: Space Rescue", "emoji": "🛸", "theme": "space",
        "world": "🚀 SPACE WORLD",
        "mission": ["Final mission! Blast the asteroid ☄️, collect BOTH stars ⭐⭐,",
                    "then land on the planet 🪐. You can do it!"],
        "tools": ["chop()", "move_right(n)", "move_up(n)", "pickup()"],
        "start": (0, 5, "right"), "trees": [(1, 5)],
        "gems": [(3, 5), (3, 1)], "walls": [], "flag": (5, 1),
        "starter": ("hero.chop()\nhero.move_right(3)\nhero.pickup()\n"
                    "hero.move_up(4)\nhero.pickup()\nhero.move_right(2)"),
        "check": lambda e: (e.x, e.y) == e.flag and e.collected >= 2 and len(e.trees) == 0,
    },
]

# Sprite + color themes for each world
THEMES = {
    "forest": {"hero": "🦘", "tree": "🌳", "gem": "💎", "flag": "🚩",
               "bg1": "#a8d65c", "bg2": "#9fce54", "wall": "#6b5b47",
               "grid": "#8fbf4f"},
    "space":  {"hero": "🚀", "tree": "☄️", "gem": "⭐", "flag": "🪐",
               "bg1": "#241d47", "bg2": "#2c2456", "wall": "#555069",
               "grid": "#3a3168"},
}

TOTAL_PUZZLES = sum(len(c["puzzles"]) for c in CHAPTERS)
TOTAL_ADV = len(ADV_LEVELS)
TOTAL_TASKS = TOTAL_PUZZLES + TOTAL_ADV

# A friendly "what to do" hint for each chapter (NOT the answer).
CHAPTER_HINTS = [
    'Use print() to show things on the screen. Put text in quotes " ". print("Hello") shows Hello',
    'A STRING is text in quotes. You can join strings with + sign. "Hello" + " " + "World" joins them.',
    "NUMBERS don't need quotes. Use  +  -  *  /  for math. print(5 + 3) shows the answer.",
    "A VARIABLE stores a value. Use  name = value  to create it. Use the name (no quotes) to show it.",
    "A LIST holds many items in [ ]. Count starts at 0. Use list[0] for first item.",
    "A BOOLEAN is True or False. Use  ==  !=  >  <  to compare and get True/False.",
    "IF STATEMENT makes decisions. If condition is True, run the code. Indent the code inside if.",
    "FOR LOOP repeats code. Use  for i in range(n):  to repeat n times. Indent the repeated code.",
    "RANGE makes a sequence of numbers.  range(5)  makes 0,1,2,3,4.  range(2,5)  makes 2,3,4.",
    "FUNCTION is reusable code. Use  def name():  to define it. Use  name()  to call it.",
    "FUNCTION PARAMETERS are inputs. def greet(name) takes a name. greet('Alice') passes 'Alice' to it.",
]


# Quick multiple-choice questions to refresh each chapter (shown in the Hint pop-up).
# "a" is the index of the correct option.
CHAPTER_QUIZ = [
    [  # 1 Hello / print
        {"q": "Which keyword SHOWS something on the screen?",
         "opts": ["print", "show", "say"], "a": 0},
        {"q": "What do we put around words we print?",
         "opts": ['quotes " "', "stars *", "nothing"], "a": 0},
    ],
    [  # 2 Print & Play
        {"q": "Each  print  starts a…", "opts": ["new line", "new game", "new box"], "a": 0},
        {"q": "Do numbers need quotes?", "opts": ["No", "Yes", "Always"], "a": 0},
    ],
    [  # 3 Variables
        {"q": "Which sign makes a variable box?", "opts": ["=", "+", "?"], "a": 0},
        {"q": "age = 8  puts 8 in a box called…", "opts": ["age", "8", "print"], "a": 0},
    ],
    [  # 4 Numbers & Math
        {"q": "Which sign means times (multiply)?", "opts": ["*", "x", "&"], "a": 0},
        {"q": "print(2 + 3)  shows…", "opts": ["5", "23", "2 + 3"], "a": 0},
    ],
    [  # 5 Strings
        {"q": "How do we glue two words together?", "opts": ["+", "-", "="], "a": 0},
        {"q": '"cat" + "dog"  makes…', "opts": ["catdog", "cat dog", "dogcat"], "a": 0},
    ],
    [  # 6 True / False
        {"q": "Which one checks if two things are the SAME?", "opts": ["==", "=", ">"], "a": 0},
        {"q": "print(5 > 3)  shows…", "opts": ["True", "False", "5"], "a": 0},
    ],
    [  # 7 If
        {"q": "What goes right after the  if  question?",
         "opts": [": (colon)", "; ", ". "], "a": 0},
        {"q": "The line under  if  must be…",
         "opts": ["indented (pushed in)", "in capitals", "in quotes"], "a": 0},
    ],
    [  # 8 Loops
        {"q": "Which keyword REPEATS things?", "opts": ["for", "again", "loop"], "a": 0},
        {"q": "range(3)  counts…", "opts": ["0 1 2", "1 2 3", "3 only"], "a": 0},
    ],
    [  # 9 Lists
        {"q": "Lists use which brackets?", "opts": ["[ ]", "( )", "{ }"], "a": 0},
        {"q": "The FIRST item in a list is number…", "opts": ["0", "1", "first"], "a": 0},
    ],
    [  # 10 Functions
        {"q": "Which keyword makes a function?", "opts": ["def", "fun", "make"], "a": 0},
        {"q": "How do you RUN a function called hello?",
         "opts": ["hello()", "run hello", "hello!"], "a": 0},
    ],
    [  # 11 Mini Game
        {"q": "range(1, 6)  counts…", "opts": ["1 2 3 4 5", "1 to 6", "0 to 6"], "a": 0},
        {"q": "if score > 5  runs the next line when it is…",
         "opts": ["True", "False", "big"], "a": 0},
    ],
]


# Command quiz questions for Adventure Mode (shown in its Hint pop-up).
ADV_QUIZ_BANK = {
    "move_right": {"q": "Which command moves the hero to the RIGHT?",
                   "opts": ["hero.move_right(2)", "hero.right()", "go_right(2)"], "a": 0},
    "move_left": {"q": "Which command moves the hero to the LEFT?",
                  "opts": ["hero.move_left(2)", "hero.left(2)", "move.left()"], "a": 0},
    "move_up": {"q": "Which command moves the hero UP?",
                "opts": ["hero.move_up(2)", "hero.up(2)", "up(2)"], "a": 0},
    "move_down": {"q": "Which command moves the hero DOWN?",
                  "opts": ["hero.move_down(2)", "hero.down(2)", "down(2)"], "a": 0},
    "pickup": {"q": "Which command picks up a gem or star?",
               "opts": ["hero.pickup()", "hero.grab()", "hero.take()"], "a": 0},
    "chop": {"q": "Which command chops a tree or blasts an asteroid?",
             "opts": ["hero.chop()", "hero.cut()", "hero.hit()"], "a": 0},
    "tree_ahead": {"q": "How do you check if something is blocking the way?",
                   "opts": ["if hero.tree_ahead():", "if blocked:", "check()"], "a": 0},
    "loop": {"q": "How do you repeat a move 3 times?",
             "opts": ["for i in range(3):", "repeat 3", "loop 3 times"], "a": 0},
    "pen_down": {"q": "Which command starts drawing a trail?",
                 "opts": ["hero.pen_down()", "hero.draw()", "pen.start()"], "a": 0},
    "forward": {"q": "Which command walks the hero forward?",
                "opts": ["hero.forward(2)", "hero.go(2)", "walk(2)"], "a": 0},
    "turn_right": {"q": "Which command turns the hero to the right?",
                   "opts": ["hero.turn_right()", "hero.turn()", "right.turn()"], "a": 0},
    "paint": {"q": "Which command paints the tile red?",
              "opts": ['hero.paint("red")', "hero.color(red)", "paint.red()"], "a": 0},
}


def adv_quiz_for(level):
    """Pick the quiz questions that match the commands this level uses."""
    text = " ".join(level["tools"]) + " " + level["starter"]
    order = ["move_right", "move_left", "move_up", "move_down", "pickup", "chop",
             "tree_ahead", "loop", "pen_down", "forward", "turn_right", "paint"]
    keys = {"loop": ("range(", "for "), "tree_ahead": ("tree_ahead",)}
    picked = []
    for k in order:
        needles = keys.get(k, (k,))
        if any(n in text for n in needles):
            picked.append(ADV_QUIZ_BANK[k])
    return picked[:3] if picked else [ADV_QUIZ_BANK["move_right"]]


def today_str():
    return date.today().strftime("%d %b %Y")


def solution_tips(sol):
    """Turn a reference solution into gentle 'tools you'll need' tips
    WITHOUT revealing the actual answer."""
    import re
    tips = []
    s = sol
    if "print(" in s:
        tips.append("• Use  print( ... )  to show something on the screen.")
    if "for " in s and "range(" in s:
        tips.append("• Repeat with a loop:  for i in range(n):  then indent the next line.")
    elif "for " in s:
        tips.append("• Loop over items:  for item in list:")
    if re.search(r"\bif\b", s):
        tips.append("• Make a choice with  if something:  then indent the next line.")
    if "def " in s:
        tips.append("• Make a command with  def name():  then call it by writing  name().")
    if "len(" in s:
        tips.append("• Count items with  len( ... ).")
    if "[" in s and "]" in s:
        tips.append("• Lists use square brackets, like  [1, 2, 3].  The first item is  [0].")
    if re.search(r"(?<![=<>!])=(?!=)", s):
        tips.append("• Make a box with  name = value.")
    if '"' in s and "+" in s:
        tips.append('• Glue words with  + . Keep quotes " " around each word.')
    elif any(op in s for op in ("+", "-", "*")):
        tips.append("• Do the math with  +  -  or  * .")
    if "==" in s or ">" in s or "<" in s:
        tips.append("• Compare with  >  <  or  ==  (the answer is True or False).")
    if not tips:
        tips.append("• Read the problem again and try it one step at a time.")
    # dedupe, keep order
    return "\n".join(dict.fromkeys(tips))

_DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
_LEFT = {"up": "left", "left": "down", "down": "right", "right": "up"}
_RIGHT = {"up": "right", "right": "down", "down": "left", "left": "up"}


class HeroError(Exception):
    pass


class HeroEngine:
    """The game-world hero. Kids' code calls these methods; every action
    records a frame so the world can be animated step-by-step afterwards."""

    def __init__(self, level):
        self.x, self.y, self.dir = level["start"]
        self.trees = set(tuple(t) for t in level["trees"])
        self.gems = set(tuple(g) for g in level["gems"])
        self.walls = set(tuple(w) for w in level["walls"])
        self.flag = tuple(level["flag"]) if level["flag"] else None
        self.collected = 0
        self.painted = {}
        self.pen = False
        self.pen_color = "#4cc9f0"
        self.frames = []
        self._snap()  # starting frame

    # ----- recording -----
    def _snap(self):
        self.frames.append({
            "x": self.x, "y": self.y, "dir": self.dir,
            "trees": set(self.trees), "gems": set(self.gems),
            "collected": self.collected, "painted": dict(self.painted),
        })

    def _blocked(self, x, y):
        return (not (0 <= x < GRID and 0 <= y < GRID)
                or (x, y) in self.walls or (x, y) in self.trees)

    def _step(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if self._blocked(nx, ny):
            return  # bump: stay put
        self.x, self.y = nx, ny
        if self.pen:
            self.painted[(self.x, self.y)] = self.pen_color
        self._snap()

    def _move(self, direction, n):
        dx, dy = _DIRS[direction]
        for _ in range(max(1, int(n))):
            self._step(dx, dy)

    # ----- movement (grid style) -----
    def move_right(self, n=1): self._move("right", n)
    def move_left(self, n=1):  self._move("left", n)
    def move_up(self, n=1):    self._move("up", n)
    def move_down(self, n=1):  self._move("down", n)

    # ----- facing / turtle style -----
    def face_up(self):    self.dir = "up";    self._snap()
    def face_down(self):  self.dir = "down";  self._snap()
    def face_left(self):  self.dir = "left";  self._snap()
    def face_right(self): self.dir = "right"; self._snap()

    def turn_left(self):  self.dir = _LEFT[self.dir];  self._snap()
    def turn_right(self): self.dir = _RIGHT[self.dir]; self._snap()

    def forward(self, n=1): self._move(self.dir, n)

    # ----- pen / painting -----
    def pen_down(self):
        self.pen = True
        self.painted[(self.x, self.y)] = self.pen_color
        self._snap()

    def pen_up(self):
        self.pen = False
        self._snap()

    def paint(self, color="red"):
        self.pen_color = color
        self.painted[(self.x, self.y)] = color
        self._snap()

    # ----- sensing & actions -----
    def tree_ahead(self):
        dx, dy = _DIRS[self.dir]
        return (self.x + dx, self.y + dy) in self.trees

    def chop(self):
        dx, dy = _DIRS[self.dir]
        target = (self.x + dx, self.y + dy)
        if target in self.trees:
            self.trees.discard(target)
        self._snap()

    def pickup(self):
        if (self.x, self.y) in self.gems:
            self.gems.discard((self.x, self.y))
            self.collected += 1
        self._snap()


def run_hero_code(code, level):
    """Run adventure code against a fresh engine. Returns (engine, error)."""
    engine = HeroEngine(level)
    safe_globals = {"__builtins__": __builtins__, "hero": engine}
    try:
        exec(code, safe_globals)
        return engine, None
    except Exception as e:
        return engine, f"{type(e).__name__}: {e}"


# ---------- Progress save/load ----------
def load_progress():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"stars": 0, "solved": [], "adv_solved": [],
                "name": "", "started": "", "last": ""}


def save_progress(data):
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


# ---------- Safe-ish code runner ----------
def run_user_code(code):
    """Run the kid's code, capture printed output. Returns (output, error)."""
    buf = io.StringIO()
    safe_globals = {"__builtins__": __builtins__}
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(code, safe_globals)
        return buf.getvalue(), None
    except Exception as e:
        return buf.getvalue(), f"{type(e).__name__}: {e}"


class PythonPals(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME + " — Learn to Code!")
        self.geometry("1000x680")
        self.minsize(860, 600)
        self.configure(bg=C["bg"])
        try:
            self.iconbitmap(_resource("app_icon.ico"))
        except Exception:
            pass

        self.progress = load_progress()
        self.progress.setdefault("adv_solved", [])
        self.mode = "lesson"
        self.ch_index = 0
        self.pz_index = 0
        self.adv_index = 0
        self._anim_job = None

        # Fonts
        self.f_title = tkfont.Font(family="Trebuchet MS", size=22, weight="bold")
        self.f_h2    = tkfont.Font(family="Trebuchet MS", size=17, weight="bold")
        self.f_body  = tkfont.Font(family="Trebuchet MS", size=13)
        self.f_bold  = tkfont.Font(family="Trebuchet MS", size=13, weight="bold")
        self.f_code  = tkfont.Font(family="Consolas", size=14)
        self.f_small = tkfont.Font(family="Trebuchet MS", size=11)

        self._build_titlebar()
        self._build_body()
        if self.progress.get("name"):
            self.show_home()
        else:
            self.show_welcome()

    # ---- Title bar ----
    def _build_titlebar(self):
        bar = tk.Frame(self, bg=C["grape"], height=56)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)
        tk.Label(bar, text="🐍  Python Pals", bg=C["grape"], fg="white",
                 font=self.f_title).pack(side="left", padx=18)
        home = tk.Label(bar, text="🏠 Home", bg="#5b3fd6", fg="white",
                        font=self.f_bold, padx=12, pady=4, cursor="hand2")
        home.pack(side="left", padx=4)
        home.bind("<Button-1>", lambda e: self.show_home())
        self.star_lbl = tk.Label(bar, text="", bg=C["sun"], fg="#5a3b00",
                                 font=self.f_bold, padx=14, pady=4)
        self.star_lbl.pack(side="right", padx=(6, 18))
        self.badge_lbl = tk.Label(bar, text="", bg="#2fa34a", fg="white",
                                  font=self.f_bold, padx=14, pady=4)
        self.badge_lbl.pack(side="right", padx=6)
        self.update_lbl = tk.Label(bar, text="🔄 Check for Updates", bg="#5b3fd6", fg="white",
                                   font=self.f_bold, padx=12, pady=4, cursor="hand2")
        self.update_lbl.pack(side="right", padx=6)
        self.update_lbl.bind("<Button-1>", lambda e: self.check_for_updates())
        self._refresh_stars()

    # ---- Updates ----
    def check_for_updates(self):
        if getattr(self, "_update_busy", False):
            return
        self._update_busy = True
        self.update_lbl.config(text="Checking...")
        threading.Thread(target=self._check_for_updates_worker, daemon=True).start()

    def _script_path(self, name):
        # scripts/ ships next to the installed exe (see installer/*.iss), not
        # inside PyInstaller's _MEIPASS temp extraction dir.
        base = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) \
            else os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, "scripts", name)

    def _run_update_script(self, extra_args=None):
        import subprocess
        args = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
                 "-File", self._script_path("update.ps1")]
        if extra_args:
            args.extend(extra_args)
        return subprocess.run(args, capture_output=True, text=True, timeout=30,
                               creationflags=subprocess.CREATE_NO_WINDOW)

    def _check_for_updates_worker(self):
        try:
            result = self._run_update_script(["-CheckOnly"])
            status = json.loads(result.stdout.strip()) if result.stdout.strip() else {}
            available = status.get("UpdateAvailable", False)
        except Exception:
            available = None
        self.after(0, lambda: self._on_update_check_done(available))

    def _on_update_check_done(self, available):
        self._update_busy = False
        if available is None:
            self.update_lbl.config(text="🔄 Check for Updates")
            return
        if not available:
            self.update_lbl.config(text="✅ Up to date")
            self.after(3000, lambda: self.update_lbl.config(text="🔄 Check for Updates"))
            return
        self.update_lbl.config(text="⬇ Update Now")
        self.update_lbl.unbind("<Button-1>")
        self.update_lbl.bind("<Button-1>", lambda e: self.apply_update())

    def apply_update(self):
        if getattr(self, "_update_busy", False):
            return
        self._update_busy = True
        self.update_lbl.unbind("<Button-1>")
        self.update_lbl.config(text="Updating...")
        threading.Thread(target=self._apply_update_worker, daemon=True).start()

    def _apply_update_worker(self):
        try:
            self._run_update_script()
            ok = True
        except Exception:
            ok = False
        self.after(0, lambda: self._on_update_applied(ok))

    def _on_update_applied(self, ok):
        self._update_busy = False
        self.update_lbl.bind("<Button-1>", lambda e: self.check_for_updates())
        self.update_lbl.config(
            text="✅ Updated! Restart to play" if ok else "❌ Update failed"
        )

    def _refresh_stars(self):
        self.star_lbl.config(text=f"⭐ {self.progress['stars']} stars")
        self.badge_lbl.config(text=f"🏅 {len(self.progress.get('adv_solved', []))} badges")

    # ---- Body: chapter rail + lesson ----
    def _build_body(self):
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True)

        # Left rail (scrollable)
        rail_wrap = tk.Frame(body, bg=C["bg"], width=234)
        rail_wrap.pack(side="left", fill="y")
        rail_wrap.pack_propagate(False)
        rail_canvas = tk.Canvas(rail_wrap, bg=C["bg"], highlightthickness=0, width=234)
        rail_sb = tk.Scrollbar(rail_wrap, orient="vertical", command=rail_canvas.yview)
        rail_canvas.configure(yscrollcommand=rail_sb.set)
        rail_sb.pack(side="right", fill="y")
        rail_canvas.pack(side="left", fill="both", expand=True)
        self.rail = tk.Frame(rail_canvas, bg=C["bg"])
        rail_win = rail_canvas.create_window((0, 0), window=self.rail, anchor="nw")
        self.rail.bind("<Configure>",
                       lambda e: rail_canvas.configure(scrollregion=rail_canvas.bbox("all")))
        rail_canvas.bind("<Configure>",
                         lambda e: rail_canvas.itemconfig(rail_win, width=e.width))

        def _rwheel(event):
            rail_canvas.yview_scroll(int(-event.delta / 120), "units")
        rail_canvas.bind("<Enter>", lambda e: rail_canvas.bind_all("<MouseWheel>", _rwheel))
        rail_canvas.bind("<Leave>", lambda e: rail_canvas.unbind_all("<MouseWheel>"))

        tk.Label(self.rail, text="CHAPTERS", bg=C["bg"], fg=C["muted"],
                 font=self.f_small).pack(anchor="w", padx=16, pady=(14, 6))
        self.chap_btns = []
        for i, ch in enumerate(CHAPTERS):
            b = tk.Label(self.rail, text=f"{ch['emoji']}  {i+1}. {ch['title']}",
                         bg=C["bg"], fg=C["ink"], font=self.f_bold, anchor="w",
                         padx=10, pady=6, cursor="hand2")
            b.pack(fill="x", pady=1)
            b.bind("<Button-1>", lambda e, idx=i: self.show_chapter(idx))
            self.chap_btns.append(b)

        self.adv_btns = []
        current_world = None
        for i, lv in enumerate(ADV_LEVELS):
            world = lv.get("world", "🌳 ADVENTURE MODE")
            if world != current_world:
                current_world = world
                color = "#2fa34a" if "SPACE" not in world else "#7b5cff"
                tk.Label(self.rail, text=world, bg=C["bg"], fg=color,
                         font=self.f_small).pack(anchor="w", padx=8, pady=(12, 4))
            b = tk.Label(self.rail, text=f"{lv['emoji']}  {lv['id']} {lv['title']}",
                         bg=C["bg"], fg=C["ink"], font=self.f_bold, anchor="w",
                         padx=10, pady=6, cursor="hand2")
            b.pack(fill="x", pady=1)
            b.bind("<Button-1>", lambda e, idx=i: self.show_adventure(idx))
            self.adv_btns.append(b)

        # Right lesson area
        self.main = tk.Frame(body, bg=C["panel"])
        self.main.pack(side="left", fill="both", expand=True, padx=(0, 0))

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    def _stop_anim(self):
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None

    # ---- Completion stats ----
    def _stats(self):
        done_pz = len(set(self.progress.get("solved", [])))
        done_adv = len(set(self.progress.get("adv_solved", [])))
        done = done_pz + done_adv
        pct = round(done / TOTAL_TASKS * 100) if TOTAL_TASKS else 0
        return done_pz, done_adv, done, pct

    # ---- Welcome / name screen ----
    def show_welcome(self):
        self._stop_anim()
        self.mode = "welcome"
        self._highlight_rail()
        self._clear_main()
        wrap = tk.Frame(self.main, bg=C["panel"])
        wrap.pack(fill="both", expand=True)
        box = tk.Frame(wrap, bg=C["panel"])
        box.place(relx=0.5, rely=0.42, anchor="center")

        tk.Label(box, text="🐍", bg=C["panel"], font=("Segoe UI Emoji", 64)).pack()
        tk.Label(box, text="Welcome to Python Pals!", bg=C["panel"], fg=C["grape"],
                 font=self.f_title).pack(pady=(4, 2))
        tk.Label(box, text="What is your name, coder?", bg=C["panel"], fg=C["ink"],
                 font=self.f_h2).pack(pady=(6, 10))

        self.name_entry = tk.Entry(box, font=("Trebuchet MS", 20), width=18,
                                   justify="center", bg="#f4eefe", fg=C["ink"],
                                   relief="flat", highlightthickness=3,
                                   highlightbackground=C["grape"],
                                   highlightcolor=C["grape"])
        self.name_entry.pack(ipady=8)
        self.name_entry.insert(0, self.progress.get("name", ""))
        self.name_entry.focus_set()
        self.name_entry.bind("<Return>", lambda e: self._submit_name())

        self._btn(box, "Let's Go!  🚀", C["mint"], "#053",
                  self._submit_name).pack(pady=18)

    def _submit_name(self):
        name = self.name_entry.get().strip() or "Coder"
        self.progress["name"] = name
        if not self.progress.get("started"):
            self.progress["started"] = today_str()
        self.progress["last"] = today_str()
        save_progress(self.progress)
        self.show_home()

    # ---- Home / progress summary ----
    def show_home(self):
        self._stop_anim()
        self.mode = "home"
        self.progress["last"] = today_str()
        if not self.progress.get("started"):
            self.progress["started"] = today_str()
        save_progress(self.progress)
        self._highlight_rail()
        outer = self._scrollable_page()
        name = self.progress.get("name") or "Coder"
        done_pz, done_adv, done, pct = self._stats()

        tk.Label(outer, text=f"Hi {name}! 👋", bg=C["panel"], fg=C["grape"],
                 font=self.f_title).pack(anchor="w")
        tk.Label(outer, text="Here is your coding progress:", bg=C["panel"],
                 fg=C["muted"], font=self.f_body).pack(anchor="w", pady=(0, 12))

        # Progress summary card
        card = tk.Frame(outer, bg="#f4eefe", highlightbackground=C["grape"],
                        highlightthickness=3)
        card.pack(fill="x")
        row = tk.Frame(card, bg="#f4eefe")
        row.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(row, text="📊 Progress Summary", bg="#f4eefe", fg=C["ink"],
                 font=self.f_h2).pack(side="left")
        tk.Label(row, text=f"{pct}%", bg="#f4eefe", fg=C["grape"],
                 font=("Trebuchet MS", 34, "bold")).pack(side="right")

        # Big progress bar
        barbg = tk.Frame(card, bg="#e3d5f7", height=26)
        barbg.pack(fill="x", padx=16, pady=(2, 6))
        barbg.pack_propagate(False)
        fill = tk.Frame(barbg, bg=C["mint"] if pct >= 100 else C["grape"])
        fill.place(relx=0, rely=0, relwidth=max(0.02, pct / 100), relheight=1)
        tk.Label(fill if pct >= 12 else barbg, text=f"{done} / {TOTAL_TASKS} done",
                 bg=fill["bg"] if pct >= 12 else "#e3d5f7",
                 fg="white" if pct >= 12 else C["muted"],
                 font=self.f_small).place(relx=0.5, rely=0.5, anchor="center")

        # Date + counters grid
        info = tk.Frame(card, bg="#f4eefe")
        info.pack(fill="x", padx=16, pady=(6, 14))
        cells = [
            ("📅 Started", self.progress.get("started", today_str())),
            ("🕒 Today", today_str()),
            ("📘 Exercises", f"{done_pz} / {TOTAL_PUZZLES}"),
            ("🏅 Badges", f"{done_adv} / {TOTAL_ADV}"),
        ]
        for i, (lab, val) in enumerate(cells):
            cell = tk.Frame(info, bg="white", highlightbackground="#e3d5f7",
                            highlightthickness=2)
            cell.grid(row=0, column=i, padx=5, sticky="nsew")
            info.grid_columnconfigure(i, weight=1)
            tk.Label(cell, text=lab, bg="white", fg=C["muted"],
                     font=self.f_small).pack(anchor="w", padx=10, pady=(8, 0))
            tk.Label(cell, text=val, bg="white", fg=C["ink"],
                     font=self.f_bold).pack(anchor="w", padx=10, pady=(0, 8))

        if pct >= 100:
            tk.Label(outer, text="🎉 WOW! You finished everything! You are a Python star! 🌟",
                     bg=C["panel"], fg="#2fa34a", font=self.f_h2).pack(anchor="w", pady=(14, 0))

        # Action buttons
        btns = tk.Frame(outer, bg=C["panel"])
        btns.pack(anchor="w", pady=18)
        self._btn(btns, "▶ Continue Learning", C["grape"], "white",
                  self._continue_learning).pack(side="left")
        self._btn(btns, "🌳 Adventure Mode", "#2fa34a", "white",
                  lambda: self.show_adventure(self._first_unsolved_adv())).pack(side="left", padx=10)
        self._btn(btns, "✏️ Change Name", C["sun"], "#5a3b00",
                  self.show_welcome).pack(side="left")
        self._btn(btns, "🔄 Reset Progress", "#d32f2f", "white",
                  self.confirm_reset).pack(side="left", padx=10)

    def _first_unsolved_chapter(self):
        for i in range(len(CHAPTERS)):
            if not all(f"{i}-{p}" in self.progress.get("solved", [])
                       for p in range(len(CHAPTERS[i]["puzzles"]))):
                return i
        return 0

    def _first_unsolved_adv(self):
        done = self.progress.get("adv_solved", [])
        for i, lv in enumerate(ADV_LEVELS):
            if lv["id"] not in done:
                return i
        return 0

    def _continue_learning(self):
        self.show_chapter(self._first_unsolved_chapter())

    def confirm_reset(self):
        """Confirm before resetting all progress."""
        top = tk.Toplevel(self)
        top.title("Reset Progress")
        top.configure(bg=C["panel"])
        top.geometry("480x280")
        top.transient(self)
        try:
            top.iconbitmap(_resource("app_icon.ico"))
        except Exception:
            pass

        pad = tk.Frame(top, bg=C["panel"])
        pad.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(pad, text="⚠️ Are you sure?", bg=C["panel"], fg="#d32f2f",
                 font=self.f_title).pack(pady=(0, 10))
        tk.Label(pad, text="This will erase ALL your progress:",
                 bg=C["panel"], fg=C["ink"], font=self.f_bold).pack(anchor="w")
        tk.Label(pad, text="• All ⭐ stars will be gone\n"
                          "• All 🏅 badges will be gone\n"
                          "• You will go back to 0%",
                 bg=C["panel"], fg=C["muted"], font=self.f_body).pack(anchor="w", pady=(4, 12))

        tk.Label(pad, text="Your name and start date will stay.",
                 bg=C["panel"], fg=C["muted"], font=self.f_small).pack(anchor="w", pady=(8, 0))

        btns = tk.Frame(pad, bg=C["panel"])
        btns.pack(anchor="e", pady=(20, 0))
        self._btn(btns, "Cancel", C["line"], C["ink"], top.destroy).pack(side="left", padx=4)
        self._btn(btns, "Yes, reset", "#d32f2f", "white",
                  lambda: (self.reset_progress(), top.destroy())).pack(side="left")
        top.grab_set()

    def reset_progress(self):
        """Clear all solved exercises and badges, reset to 0%."""
        self.progress["solved"] = []
        self.progress["adv_solved"] = []
        self.progress["stars"] = 0
        self.progress["last"] = today_str()
        save_progress(self.progress)
        self._refresh_stars()
        self._highlight_rail()
        self.show_home()

    def _highlight_rail(self):
        for i, b in enumerate(self.chap_btns):
            solved_all = all(
                f"{i}-{p}" in self.progress["solved"]
                for p in range(len(CHAPTERS[i]["puzzles"]))
            )
            if self.mode == "lesson" and i == self.ch_index:
                b.config(bg=C["grape"], fg="white")
            elif solved_all:
                b.config(bg=C["mint"], fg="#053")
            else:
                b.config(bg=C["bg"], fg=C["ink"])
        adv_done = self.progress.get("adv_solved", [])
        unlocked = self.adventure_unlocked()
        for i, b in enumerate(self.adv_btns):
            lv = ADV_LEVELS[i]
            label = f"{lv['emoji']}  {lv['id']} {lv['title']}"
            if not unlocked:
                b.config(text="🔒 " + label, bg=C["bg"], fg="#b9aecb")
            elif self.mode == "adventure" and i == self.adv_index:
                b.config(text=label, bg="#2fa34a", fg="white")
            elif lv["id"] in adv_done:
                b.config(text=label, bg=C["mint"], fg="#053")
            else:
                b.config(text=label, bg=C["bg"], fg=C["ink"])

    # ---- Show a chapter ----
    def show_chapter(self, idx):
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        self.mode = "lesson"
        self.ch_index = idx
        self.pz_index = -1   # -1 = show the explanation screen first
        self._highlight_rail()
        self._render()

    def _scrollable_page(self):
        """Clear main and return an inner frame that scrolls (wheel + bar)."""
        self._clear_main()
        canvas = tk.Canvas(self.main, bg=C["panel"], highlightthickness=0)
        page_sb = tk.Scrollbar(self.main, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=page_sb.set)
        page_sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        holder = tk.Frame(canvas, bg=C["panel"])
        win = canvas.create_window((0, 0), window=holder, anchor="nw")

        def _fit(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(win, width=canvas.winfo_width())
        holder.bind("<Configure>", _fit)
        canvas.bind("<Configure>", _fit)

        def _wheel(event):
            canvas.yview_scroll(int(-event.delta / 120), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        outer = tk.Frame(holder, bg=C["panel"])
        outer.pack(fill="both", expand=True, padx=22, pady=18)
        return outer

    def _render(self):
        if self.pz_index < 0:
            self._render_intro()
        else:
            self._render_puzzle()

    # ---- Step 1: the explanation screen ("what is this all about?") ----
    def _render_intro(self):
        ch = CHAPTERS[self.ch_index]
        outer = self._scrollable_page()

        card = tk.Frame(outer, bg="#eaf7fe", highlightbackground=C["sky"],
                        highlightthickness=3)
        card.pack(fill="x")

        header = tk.Frame(card, bg="#eaf7fe")
        header.pack(fill="x", padx=12, pady=(10, 0))
        tk.Label(header, text="📖 LET'S LEARN", bg=C["sky"], fg="#023",
                 font=self.f_small, padx=8, pady=2).pack(side="left")
        if ch.get("youtube"):
            def open_youtube():
                import webbrowser
                try:
                    webbrowser.open(ch["youtube"])
                except Exception:
                    pass
            yt_btn = tk.Label(header, text="📺 Watch on YouTube", bg=C["sky"], fg="#023",
                             font=self.f_small, padx=8, pady=2, cursor="hand2")
            yt_btn.pack(side="right")
            yt_btn.bind("<Button-1>", lambda e: open_youtube())

        tk.Label(card, text=f"Chapter {self.ch_index+1}: {ch['title']} {ch['emoji']}",
                 bg="#eaf7fe", fg=C["ink"], font=self.f_title,
                 anchor="w", justify="left").pack(anchor="w", padx=12, pady=(4, 4))
        tk.Label(card, text="What is this all about?", bg="#eaf7fe", fg=C["grape"],
                 font=self.f_h2).pack(anchor="w", padx=12, pady=(2, 4))
        for line in ch["theory"]:
            tk.Label(card, text=line, bg="#eaf7fe", fg=C["ink"], font=self.f_body,
                     anchor="w", justify="left", wraplength=660).pack(
                     anchor="w", padx=12, pady=2)
        tk.Frame(card, bg="#eaf7fe", height=10).pack()

        tk.Label(outer, text=f"Ready? There are {len(ch['puzzles'])} puzzles. "
                 "You write the program yourself in the box — tap 💡 Hint if you get stuck!",
                 bg=C["panel"], fg=C["muted"], font=self.f_body,
                 wraplength=660, justify="left").pack(anchor="w", pady=(16, 8))
        self._btn(outer, "Start Puzzles →", C["mint"], "#053",
                  self.start_puzzles).pack(anchor="w", pady=4)

    def start_puzzles(self):
        self.pz_index = 0
        self._render()

    def review_intro(self):
        self.pz_index = -1
        self._render()

    # ---- Step 2: the puzzle screen (kid writes the program) ----
    def _render_puzzle(self):
        ch = CHAPTERS[self.ch_index]
        pz = ch["puzzles"][self.pz_index]
        outer = self._scrollable_page()

        # Compact reminder + "read again" link
        strip = tk.Frame(outer, bg="#eaf7fe", highlightbackground=C["sky"],
                         highlightthickness=2)
        strip.pack(fill="x")
        tk.Label(strip, text=f"📖 {ch['title']} {ch['emoji']}", bg="#eaf7fe",
                 fg=C["ink"], font=self.f_bold).pack(side="left", padx=10, pady=6)
        self._btn(strip, "Read explanation again", C["sky"], "#023",
                  self.review_intro).pack(side="right", padx=6, pady=4)

        # PRACTICE header
        head = tk.Frame(outer, bg=C["panel"])
        head.pack(fill="x", pady=(14, 4))
        tk.Label(head, text="🎮 YOUR TURN", bg=C["bubble"], fg="#5a0030",
                 font=self.f_small, padx=8, pady=2).pack(side="left")
        tk.Label(head, text=f"Puzzle {self.pz_index+1} of {len(ch['puzzles'])}",
                 bg=C["panel"], fg=C["muted"], font=self.f_small).pack(side="left", padx=10)

        tk.Label(outer, text=pz["prompt"], bg=C["panel"], fg=C["ink"],
                 font=self.f_bold, anchor="w", justify="left",
                 wraplength=660).pack(anchor="w", pady=(4, 6))
        tk.Label(outer, text="✍️ Write your program here, then press ▶ Run:",
                 bg=C["panel"], fg=C["muted"], font=self.f_small).pack(anchor="w")

        # Code editor — EMPTY so the child writes it themselves
        ed_wrap = tk.Frame(outer, bg=C["editor"])
        ed_wrap.pack(fill="x", pady=(2, 0))
        ed_y = tk.Scrollbar(ed_wrap, orient="vertical")
        ed_y.pack(side="right", fill="y")
        ed_x = tk.Scrollbar(ed_wrap, orient="horizontal")
        ed_x.pack(side="bottom", fill="x")
        self.editor = tk.Text(ed_wrap, height=7, font=self.f_code, bg=C["editor"],
                              fg=C["code"], insertbackground="white", bd=0,
                              padx=12, pady=10, wrap="none",
                              yscrollcommand=ed_y.set, xscrollcommand=ed_x.set)
        self.editor.pack(side="left", fill="both", expand=True)
        ed_y.config(command=self.editor.yview)
        ed_x.config(command=self.editor.xview)
        self.editor.focus_set()

        # Buttons
        btns = tk.Frame(outer, bg=C["panel"])
        btns.pack(fill="x", pady=12)
        self._btn(btns, "▶ Run my code", C["mint"], "#053", self.on_run).pack(side="left")
        self._btn(btns, "💡 Hint", C["sun"], "#5a3b00", self.show_hint).pack(side="left", padx=8)
        self._btn(btns, "🧹 Clear", C["line"], C["ink"], self.on_clear).pack(side="left")
        self._btn(btns, "⏭ Skip", C["line"], C["ink"], self.next_puzzle).pack(side="left", padx=8)
        self.next_btn = self._btn(btns, "Next →", C["grape"], "white", self.next_puzzle)
        self.next_btn.pack(side="right")

        # Output box (scrollable)
        out_wrap = tk.Frame(outer, bg="#f4fff9", highlightbackground=C["mint"],
                            highlightthickness=3)
        out_wrap.pack(fill="both", expand=True, pady=(2, 0))
        out_y = tk.Scrollbar(out_wrap, orient="vertical")
        out_y.pack(side="right", fill="y")
        self.out = tk.Text(out_wrap, font=self.f_code, bg="#f4fff9", fg=C["ink"],
                           bd=0, padx=12, pady=10, wrap="word", height=12,
                           state="disabled", yscrollcommand=out_y.set)
        self.out.pack(side="left", fill="both", expand=True)
        out_y.config(command=self.out.yview)
        self.out_wrap = out_wrap
        self._set_output("Write your program above, then press ▶ Run to see what it does!",
                         "#f4fff9", C["mint"])

    # ---- The Hint pop-up (explains the problem + a refresher quiz, NOT the answer) ----
    def show_hint(self):
        ch = CHAPTERS[self.ch_index]
        pz = ch["puzzles"][self.pz_index]
        top = tk.Toplevel(self)
        top.title("💡 Hint")
        top.configure(bg=C["panel"])
        top.geometry("560x620")
        top.transient(self)
        try:
            top.iconbitmap(_resource("app_icon.ico"))
        except Exception:
            pass

        # Scrollable body (there is a lot to show now)
        canvas = tk.Canvas(top, bg=C["panel"], highlightthickness=0)
        sb = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        pad = tk.Frame(canvas, bg=C["panel"])
        win = canvas.create_window((0, 0), window=pad, anchor="nw")
        pad.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.bind("<Enter>", lambda e: canvas.bind_all(
            "<MouseWheel>", lambda ev: canvas.yview_scroll(int(-ev.delta / 120), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        inner = tk.Frame(pad, bg=C["panel"])
        inner.pack(fill="both", expand=True, padx=18, pady=16)

        tk.Label(inner, text="💡 Here's a hint!", bg=C["panel"], fg=C["grape"],
                 font=self.f_title).pack(anchor="w")

        tk.Label(inner, text="THE PROBLEM", bg=C["panel"], fg=C["muted"],
                 font=self.f_small).pack(anchor="w", pady=(10, 0))
        tk.Label(inner, text=pz["prompt"], bg=C["panel"], fg=C["ink"], font=self.f_bold,
                 wraplength=500, justify="left").pack(anchor="w")

        tk.Label(inner, text="WHAT TO DO", bg=C["panel"], fg=C["muted"],
                 font=self.f_small).pack(anchor="w", pady=(12, 2))
        tk.Label(inner, text=CHAPTER_HINTS[self.ch_index], bg="#fff8e6", fg=C["ink"],
                 font=self.f_body, wraplength=496, justify="left",
                 padx=10, pady=8).pack(anchor="w", fill="x")

        tk.Label(inner, text="TOOLS YOU'LL NEED", bg=C["panel"], fg=C["muted"],
                 font=self.f_small).pack(anchor="w", pady=(12, 2))
        tk.Label(inner, text=solution_tips(pz["starter"]), bg="#eaf7fe", fg=C["ink"],
                 font=self.f_body, wraplength=496, justify="left",
                 padx=10, pady=8).pack(anchor="w", fill="x")

        # ---- Refresher quiz (multiple choice) ----
        tk.Label(inner, text="QUICK QUIZ — refresh your memory! 🧠", bg=C["panel"],
                 fg=C["grape"], font=self.f_bold).pack(anchor="w", pady=(16, 4))
        for quiz in CHAPTER_QUIZ[self.ch_index]:
            self._build_quiz(inner, quiz)

        tk.Label(inner, text="Now try writing it yourself — you can do it! 🌟\n"
                 "(This is a hint, not the answer.)", bg=C["panel"], fg="#2fa34a",
                 font=self.f_small, justify="left").pack(anchor="w", pady=(14, 0))

        self._btn(inner, "Got it! ✅", C["mint"], "#053",
                  top.destroy).pack(anchor="e", pady=(14, 0))
        top.grab_set()

    def _build_quiz(self, parent, quiz):
        """One multiple-choice question with instant tap-to-check feedback."""
        box = tk.Frame(parent, bg="white", highlightbackground="#e3d5f7",
                       highlightthickness=2)
        box.pack(fill="x", pady=6)
        tk.Label(box, text="❓ " + quiz["q"], bg="white", fg=C["ink"],
                 font=self.f_bold, wraplength=486, justify="left",
                 anchor="w").pack(anchor="w", padx=10, pady=(8, 4))
        correct = quiz["opts"][quiz["a"]]
        opts = list(quiz["opts"])
        random.shuffle(opts)
        result = tk.Label(box, text="", bg="white", font=self.f_small)

        def pick(val, lbl):
            if val == correct:
                lbl.config(bg=C["mint"], fg="#053")
                result.config(text="✅ Correct! Well done!", fg="#2a8a55")
                play_sound("good")
            else:
                lbl.config(bg="#ffd3e0", fg="#5a0030")
                result.config(text="❌ Not that one — try another!", fg="#b02a5b")
                play_sound("oops")

        row = tk.Frame(box, bg="white")
        row.pack(anchor="w", padx=10, pady=(0, 4), fill="x")
        for val in opts:
            lbl = tk.Label(row, text=val, bg="#f4eefe", fg=C["ink"],
                           font=("Consolas", 12, "bold"), padx=12, pady=6,
                           cursor="hand2", relief="flat")
            lbl.pack(side="left", padx=4, pady=2)
            lbl.bind("<Button-1>", lambda e, v=val, l=lbl: pick(v, l))
        result.pack(anchor="w", padx=10, pady=(0, 8))

    def _btn(self, parent, text, bg, fg, cmd):
        b = tk.Label(parent, text=text, bg=bg, fg=fg, font=self.f_bold,
                     padx=16, pady=8, cursor="hand2")
        b.bind("<Button-1>", lambda e: cmd())
        return b

    def _set_output(self, text, bg, border):
        self.out.config(state="normal", bg=bg)
        self.out.delete("1.0", "end")
        self.out.insert("1.0", text)
        self.out.config(state="disabled")
        self.out_wrap.config(bg=bg, highlightbackground=border)

    # ---- Actions ----
    def on_clear(self):
        self.editor.delete("1.0", "end")

    def on_run(self):
        code = self.editor.get("1.0", "end-1c")
        output, err = run_user_code(code)
        ch = CHAPTERS[self.ch_index]
        pz = ch["puzzles"][self.pz_index]

        if err:
            play_sound("oops")
            self._set_output(
                f"Oops! Little bug: {err}\n💡 Check your spelling and quotes, then try again!",
                "#fff0f4", C["bubble"])
            return

        shown = output if output.strip() else "(nothing printed yet)"
        got = output.strip().replace("\r\n", "\n")

        # Decide if correct
        if pz.get("expect_any"):
            correct = bool(got)
        else:
            correct = got == pz["expect"].strip()

        if correct:
            play_sound("good")
            key = f"{self.ch_index}-{self.pz_index}"
            first_time = key not in self.progress["solved"]
            if first_time:
                self.progress["solved"].append(key)
                self.progress["stars"] += 1
                save_progress(self.progress)
                self._refresh_stars()
                self._highlight_rail()
            star_msg = "🌟 +1 star!" if first_time else "🌟 Nice!"
            self._set_output(
                f"Output:\n{shown}\n\n✅ Great job! {star_msg}  Press Next → to keep going.",
                "#f0fff6", C["mint"])
        else:
            play_sound("oops")
            hint = "" if pz.get("expect_any") else f"\n🎯 We were hoping to see:\n{pz['expect']}"
            self._set_output(
                f"Output:\n{shown}\n\n🤏 Almost! Try again.{hint}",
                "#fffbe8", C["sun"])

    def next_puzzle(self):
        ch = CHAPTERS[self.ch_index]
        if self.pz_index + 1 < len(ch["puzzles"]):
            self.pz_index += 1
            self._render()
        elif self.ch_index + 1 < len(CHAPTERS):
            self.show_chapter(self.ch_index + 1)
        else:
            self._clear_main()
            done = tk.Frame(self.main, bg=C["panel"])
            done.pack(fill="both", expand=True)
            tk.Label(done, text="🎉🏆🎉", bg=C["panel"], font=("Trebuchet MS", 60)).pack(pady=(80, 10))
            tk.Label(done, text="You finished all 11 chapters!", bg=C["panel"],
                     fg=C["ink"], font=self.f_title).pack()
            tk.Label(done, text=f"You earned ⭐ {self.progress['stars']} stars. "
                                 "You are a real Python coder now!",
                     bg=C["panel"], fg=C["muted"], font=self.f_body).pack(pady=8)
            tk.Label(done, text="🌳 Now try ADVENTURE MODE — write code to move a hero!",
                     bg=C["panel"], fg="#2fa34a", font=self.f_bold).pack(pady=(6, 2))
            self._btn(done, "Start Adventure A1 →", "#2fa34a", "white",
                      lambda: self.show_adventure(0)).pack(pady=(8, 4))
            self._btn(done, "Start over from Chapter 1", C["grape"], "white",
                      lambda: self.show_chapter(0)).pack(pady=8)

    # ================= ADVENTURE MODE =================
    CELL = 62

    def _lesson_percent(self):
        done_pz = len(set(self.progress.get("solved", [])))
        return round(done_pz / TOTAL_PUZZLES * 100) if TOTAL_PUZZLES else 0

    def adventure_unlocked(self):
        return self._lesson_percent() >= 90

    def show_adventure(self, idx):
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        self.mode = "adventure"
        self.adv_index = idx
        self._highlight_rail()
        if not self.adventure_unlocked():
            self._render_adv_locked()
            return
        self.adv_level = ADV_LEVELS[idx]
        self._render_adventure()

    def _render_adv_locked(self):
        pct = self._lesson_percent()
        done_pz = len(set(self.progress.get("solved", [])))
        outer = self._scrollable_page()
        card = tk.Frame(outer, bg="#fff8e6", highlightbackground=C["sun"],
                        highlightthickness=3)
        card.pack(fill="x", pady=(10, 0))
        tk.Label(card, text="🔒", bg="#fff8e6", font=("Segoe UI Emoji", 60)).pack(pady=(16, 4))
        tk.Label(card, text="Adventure Mode is locked!", bg="#fff8e6", fg=C["ink"],
                 font=self.f_title).pack()
        tk.Label(card, text="Finish your lessons first to unlock the game worlds. 🌳🚀",
                 bg="#fff8e6", fg=C["muted"], font=self.f_body).pack(pady=(4, 2))
        tk.Label(card, text=f"You need 90% of lessons.  You are at {pct}%  "
                            f"({done_pz} / {TOTAL_PUZZLES} exercises).",
                 bg="#fff8e6", fg=C["grape"], font=self.f_h2).pack(pady=(8, 4))

        # progress bar
        barbg = tk.Frame(card, bg="#efe3d0", height=24, width=460)
        barbg.pack(pady=(4, 16))
        barbg.pack_propagate(False)
        fill = tk.Frame(barbg, bg=C["mint"] if pct >= 90 else C["sun"])
        fill.place(relx=0, rely=0, relwidth=max(0.02, min(pct, 100) / 100), relheight=1)

        self._btn(outer, "▶ Go to my Lessons", C["grape"], "white",
                  self._continue_learning).pack(anchor="center", pady=16)

    # ---- Adventure Hint pop-up (guides + quizzes, NOT the answer) ----
    def show_adv_hint(self):
        lv = self.adv_level
        top = tk.Toplevel(self)
        top.title("💡 Hint")
        top.configure(bg=C["panel"])
        top.geometry("560x620")
        top.transient(self)
        try:
            top.iconbitmap(_resource("app_icon.ico"))
        except Exception:
            pass
        canvas = tk.Canvas(top, bg=C["panel"], highlightthickness=0)
        sb = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        pad = tk.Frame(canvas, bg=C["panel"])
        win = canvas.create_window((0, 0), window=pad, anchor="nw")
        pad.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.bind("<Enter>", lambda e: canvas.bind_all(
            "<MouseWheel>", lambda ev: canvas.yview_scroll(int(-ev.delta / 120), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        inner = tk.Frame(pad, bg=C["panel"])
        inner.pack(fill="both", expand=True, padx=18, pady=16)

        tk.Label(inner, text="💡 Here's a hint!", bg=C["panel"], fg=C["grape"],
                 font=self.f_title).pack(anchor="w")

        tk.Label(inner, text="THE MISSION", bg=C["panel"], fg=C["muted"],
                 font=self.f_small).pack(anchor="w", pady=(10, 2))
        tk.Label(inner, text="\n".join(lv["mission"]), bg="#eafbe6", fg=C["ink"],
                 font=self.f_body, wraplength=496, justify="left",
                 padx=10, pady=8).pack(anchor="w", fill="x")

        tk.Label(inner, text="HOW TO THINK", bg=C["panel"], fg=C["muted"],
                 font=self.f_small).pack(anchor="w", pady=(12, 2))
        tk.Label(inner, text="• Look at the world. Where is the hero? Where is the goal?\n"
                 "• Plan each step, ONE command per line.\n"
                 "• Repeating a move? Use a loop:  for i in range(n):\n"
                 "• Something in the way? Use  hero.chop()  first.",
                 bg="#fff8e6", fg=C["ink"], font=self.f_body, wraplength=496,
                 justify="left", padx=10, pady=8).pack(anchor="w", fill="x")

        tk.Label(inner, text="COMMANDS YOU CAN USE", bg=C["panel"], fg=C["muted"],
                 font=self.f_small).pack(anchor="w", pady=(12, 2))
        toolrow = tk.Frame(inner, bg=C["panel"])
        toolrow.pack(anchor="w", fill="x")
        for t in lv["tools"]:
            tk.Label(toolrow, text=t, bg=C["sky"], fg="#023",
                     font=("Consolas", 11, "bold"), padx=8, pady=3).pack(
                     side="left", padx=3, pady=3)

        tk.Label(inner, text="QUICK QUIZ — do you know the commands? 🧠", bg=C["panel"],
                 fg=C["grape"], font=self.f_bold).pack(anchor="w", pady=(16, 4))
        for quiz in adv_quiz_for(lv):
            self._build_quiz(inner, quiz)

        tk.Label(inner, text="Now write your commands yourself — you can do it! 🌟\n"
                 "(This is a hint, not the answer.)", bg=C["panel"], fg="#2fa34a",
                 font=self.f_small, justify="left").pack(anchor="w", pady=(14, 0))
        self._btn(inner, "Got it! ✅", C["mint"], "#053",
                  top.destroy).pack(anchor="e", pady=(14, 0))
        top.grab_set()

    def _render_adventure(self):
        lv = self.adv_level
        outer = self._scrollable_page()

        # Mission card
        card = tk.Frame(outer, bg="#eafbe6", highlightbackground="#2fa34a",
                        highlightthickness=3)
        card.pack(fill="x")
        tk.Label(card, text=f"🎯 MISSION {lv['id']}", bg="#2fa34a", fg="white",
                 font=self.f_small).pack(anchor="w", padx=12, pady=(10, 0))
        tk.Label(card, text=f"{lv['title']} {lv['emoji']}", bg="#eafbe6", fg=C["ink"],
                 font=self.f_h2, anchor="w").pack(anchor="w", padx=12, pady=(2, 2))
        for line in lv["mission"]:
            tk.Label(card, text=line, bg="#eafbe6", fg=C["ink"], font=self.f_body,
                     anchor="w", justify="left", wraplength=640).pack(anchor="w", padx=12)
        tools = tk.Frame(card, bg="#eafbe6")
        tools.pack(anchor="w", padx=10, pady=8)
        tk.Label(tools, text="Commands you can use:", bg="#eafbe6", fg=C["muted"],
                 font=self.f_small).pack(side="left", padx=(2, 6))
        for t in lv["tools"]:
            tk.Label(tools, text=t, bg=C["sky"], fg="#023", font=("Consolas", 10, "bold"),
                     padx=7, pady=2).pack(side="left", padx=3)

        # Stage: world canvas + editor
        stage = tk.Frame(outer, bg=C["panel"])
        stage.pack(fill="x", pady=(14, 0))

        left = tk.Frame(stage, bg=C["panel"])
        left.pack(side="left", padx=(0, 14))
        size = GRID * self.CELL
        th = THEMES.get(lv.get("theme", "forest"), THEMES["forest"])
        self.world = tk.Canvas(left, width=size, height=size, bg=th["bg1"],
                               highlightthickness=3, highlightbackground=C["ink"])
        self.world.pack()
        self.world_cap = tk.Label(left, text="", bg=C["panel"], fg=C["muted"],
                                  font=self.f_small)
        self.world_cap.pack(pady=(6, 0))

        right = tk.Frame(stage, bg=C["panel"])
        right.pack(side="left", fill="both", expand=True)
        tk.Label(right, text="✍️ Write your commands here, then press ▶ Run:",
                 bg=C["panel"], fg=C["ink"], font=self.f_bold).pack(anchor="w")
        ed_wrap = tk.Frame(right, bg=C["editor"])
        ed_wrap.pack(fill="x", pady=(4, 0))
        ed_y = tk.Scrollbar(ed_wrap, orient="vertical")
        ed_y.pack(side="right", fill="y")
        self.editor = tk.Text(ed_wrap, height=9, font=self.f_code, bg=C["editor"],
                              fg=C["code"], insertbackground="white", bd=0,
                              padx=12, pady=10, wrap="none", yscrollcommand=ed_y.set)
        self.editor.pack(side="left", fill="both", expand=True)
        ed_y.config(command=self.editor.yview)
        self.editor.focus_set()   # EMPTY box — the child writes it themselves

        btns = tk.Frame(right, bg=C["panel"])
        btns.pack(fill="x", pady=12)
        self._btn(btns, "▶ Run", C["mint"], "#053", self.on_adv_run).pack(side="left")
        self._btn(btns, "💡 Hint", C["sun"], "#5a3b00",
                  self.show_adv_hint).pack(side="left", padx=8)
        self._btn(btns, "🧹 Clear", C["line"], C["ink"],
                  lambda: self.editor.delete("1.0", "end")).pack(side="left")
        if self.adv_index + 1 < len(ADV_LEVELS):
            self._btn(btns, "Next →", "#2fa34a", "white",
                      lambda: self.show_adventure(self.adv_index + 1)).pack(side="right")

        # Output
        out_wrap = tk.Frame(outer, bg="#f4fff9", highlightbackground=C["mint"],
                            highlightthickness=3)
        out_wrap.pack(fill="both", expand=True, pady=(4, 0))
        self.adv_out = tk.Label(out_wrap, text="Press ▶ Run to watch your hero move!",
                                bg="#f4fff9", fg=C["ink"], font=self.f_body, anchor="w",
                                justify="left", wraplength=700, padx=12, pady=10)
        self.adv_out.pack(fill="both", expand=True)
        self.adv_out_wrap = out_wrap

        # Draw the starting world
        start_engine = HeroEngine(lv)
        self._draw_world(start_engine.frames[0])

    def _draw_world(self, snap):
        c = self.world
        c.delete("all")
        cell = self.CELL
        lv = self.adv_level
        th = THEMES.get(lv.get("theme", "forest"), THEMES["forest"])
        walls = set(tuple(w) for w in lv["walls"])
        for gx in range(GRID):
            for gy in range(GRID):
                x0, y0 = gx * cell, gy * cell
                base = th["bg1"] if (gx + gy) % 2 == 0 else th["bg2"]
                if (gx, gy) in walls:
                    base = th["wall"]
                paint = snap["painted"].get((gx, gy))
                fill = paint if paint else base
                c.create_rectangle(x0, y0, x0 + cell, y0 + cell,
                                   fill=fill, outline=th["grid"])
        ef = ("Segoe UI Emoji", 26)
        if lv["flag"]:
            fx, fy = lv["flag"]
            c.create_text(fx * cell + cell / 2, fy * cell + cell / 2, text=th["flag"], font=ef)
        for (tx, ty) in snap["trees"]:
            c.create_text(tx * cell + cell / 2, ty * cell + cell / 2, text=th["tree"], font=ef)
        for (gx, gy) in snap["gems"]:
            c.create_text(gx * cell + cell / 2, gy * cell + cell / 2, text=th["gem"], font=ef)
        arrow = {"up": "⬆", "down": "⬇", "left": "⬅", "right": "➡"}[snap["dir"]]
        hx, hy = snap["x"], snap["y"]
        c.create_text(hx * cell + cell / 2, hy * cell + cell / 2, text=th["hero"], font=ef)
        c.create_text(hx * cell + cell - 10, hy * cell + 12, text=arrow,
                      font=("Segoe UI Emoji", 12))
        self.world_cap.config(text=f"Hero at ({hx},{hy}) · facing {snap['dir']}"
                                   f" · gems collected: {snap['collected']}")

    def on_adv_run(self):
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        code = self.editor.get("1.0", "end-1c")
        engine, err = run_hero_code(code, self.adv_level)
        if err:
            play_sound("oops")
            self._draw_world(engine.frames[0])
            self.adv_out.config(
                text=f"Oops! Little bug: {err}\n💡 Check your spelling and the ( ) brackets.",
                bg="#fff0f4")
            self.adv_out_wrap.config(bg="#fff0f4", highlightbackground=C["bubble"])
            return
        self._anim_frames = engine.frames
        self._anim_engine = engine
        self._animate(0)

    def _animate(self, i):
        if i < len(self._anim_frames):
            self._draw_world(self._anim_frames[i])
            self._anim_job = self.after(350, lambda: self._animate(i + 1))
            return
        self._anim_job = None
        engine = self._anim_engine
        if self.adv_level["check"](engine):
            play_sound("win")
            key = self.adv_level["id"]
            first = key not in self.progress["adv_solved"]
            if first:
                self.progress["adv_solved"].append(key)
                save_progress(self.progress)
                self._refresh_stars()
                self._highlight_rail()
            self.adv_out.config(
                text=f"🏅 MISSION COMPLETE! {'New badge earned!' if first else 'Nice!'}"
                     "  Press Next → for the next adventure.", bg="#f0fff6")
            self.adv_out_wrap.config(bg="#f0fff6", highlightbackground=C["mint"])
        else:
            play_sound("oops")
            self.adv_out.config(
                text="🤏 Not quite there yet! Look at where the hero stopped, "
                     "fix your code, and press ▶ Run again.", bg="#fffbe8")
            self.adv_out_wrap.config(bg="#fffbe8", highlightbackground=C["sun"])


if __name__ == "__main__":
    PythonPals().mainloop()
