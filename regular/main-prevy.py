# main.py
# Author: Andrew Kelton

# import my gui
import GUI as gui

# import DT modules
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import pandas as pd
import json

# main
def main():

    # read questions from json
    with open("questions.json", "r") as qf:
        questions = json.load(qf)

        # convert difficulties to ints
        for q in questions: 
            q["difficulty"]=gui.DIFF_MAP[q["difficulty"]]
    
    # questions split by cognitive ability level
    low_questions=questions["low"]
    medium_questions = questions["medium"]
    high_questions = questions["high"]

    project_gui = gui.GUI(questions)
    project_gui.start_test()
    print(project_gui.answers_list)
    print("SCORE:", project_gui.score)


if __name__ == '__main__':
    main()

