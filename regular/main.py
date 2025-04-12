# main.py
# Author: Andrew Kelton

# import my gui
import GUI as gui

# import DT modules
from sklearn.tree import DecisionTreeClassifier

# import pandas as pd
import numpy as np
import json

# main
def main():

    # read questions from json
    with open("questions.json", "r") as qf:
        questions = json.load(qf)

        # convert difficulties to ints
        for ability, question_list in questions.items():
            for q in question_list: 
                q["difficulty"]=gui.DIFF_MAP[q["difficulty"]]
    
    # questions split by cognitive ability level
    low_questions=questions["low"]
    medium_questions = questions["medium"]
    high_questions = questions["high"]

    # dummy training data 
    dummy_X = [
        # [correct ? 1 : 0, question difficulty, time_took]
        [1, gui.LOW, 5.0],
        [0, gui.LOW, 10.0],
        [1, gui.MEDIUM, 7.5],
        [0, gui.MEDIUM, 12.0],
        [1, gui.HIGH, 3.0],
        [0, gui.HIGH, 15.0]
    ]

    # result of answer
    dummy_y = [
        "medium",
        "low",
        "high",
        "low",
        "high",
        "medium"
    ]

    ''' Log transform the training data to reduce impact 
        of quick answers, but incorrect results.
    '''
    dummy_X_log_transformed = [[x[0], x[1], np.log(x[2] + 1)] for x in dummy_X]

    # initialize and train the model
    model=DecisionTreeClassifier()
    model.fit(dummy_X_log_transformed, dummy_y)

    # initialize GUI and start test
    project_gui = gui.GUI(low_questions, medium_questions, high_questions, model)
    project_gui.start_test()

    # save results to json file
    with open('user_answers.json', 'w') as out_jf:
        json.dump(project_gui.answers_list, out_jf, indent=4)

if __name__ == '__main__':
    main()
