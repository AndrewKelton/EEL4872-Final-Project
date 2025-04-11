# main.py
# Author: Andrew Kelton

import tkinter as tk
import GUI as gui

# Cognitive ability levels
COGNITIVE_ABILITIES_STRING=["low", "medium", "high"]
LOW=0
MEDIUM=1
HIGH=2

QUESTIONS=["1 + 1 = ?"]
ANSWERS=[2]
ANSWER_CHOICES=[[1,2,3,4]]

# question structure format
QUESTION={
    "id": 0,
    "difficulty": LOW,
    "question": "1 + 1 = ?",
    "answer": 2,
    "answer choices": [1,2,3,4],
}

# main
def main():
    project_gui = gui.GUI([QUESTION])


if __name__ == '__main__':
    main()

