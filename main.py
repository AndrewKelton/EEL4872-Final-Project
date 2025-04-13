# main.py
# Author: Andrew Kelton

# import my gui
import GUI as gui

# import DT modules
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# import pandas as pd
import numpy as np
import json
import sys

# dummy training data, or control data
dummy_X = [
    [10, gui.LOW, 4.0],
    [10, gui.MEDIUM, 4.0],
    [10, gui.HIGH, 4.0],

    [0, gui.LOW, 4.0],
    [0, gui.MEDIUM, 4.0],
    [0, gui.HIGH, 4.0]
]
# result of answer
dummy_y = [
    "medium",  # correct LOW fast → not low, not high
    "high",    # correct MED fast → high potential
    "high",    # correct HIGH fast → high

    "low",     # wrong LOW
    "low",     # wrong MED
    "medium"   # wrong HIGH → tried hard, but maybe not lowest
]

def compute_weighted_correct(is_correct : int, time_taken : float) -> int:
    if is_correct:
        return 10 if time_taken < 6 else 7 if time_taken < 10 else 5 
    return 0

def read_json(file_name : str):
    '''reads and returns contents of json file'''
    with open(file_name, "r") as jf:
        return json.load(jf)

def get_questions(file_name : str):
    ''' Read questions from JSON file and returns
        a triple of lists containing low-high questions.
    '''

    data = read_json(file_name)

    # convert difficulties to ints
    for ability, question_list in data.items():
        for q in question_list:
            q["difficulty"]=gui.DIFF_MAP[q["difficulty"]]

    return data["low"], data["medium"], data["high"]


def get_answers_to_X_y(folder_path: str = "data"):
    ''' 
        Reads answers from previous tests in data folder and 
        turns them to the true value to label y. Returns
        tuple of prepared X, y training data set for model.
    '''
    import os 

    X, y = [], []

    # loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            try:
                data = read_json(file_path)

                # read and append answer data
                for answer in data:
                    try:
                        result = compute_weighted_correct(int(answer['result']), float(answer['time_taken']))
                        difficulty = int(answer['difficulty'])
                        time_taken_logged = np.log(float(answer['time_taken']) + 1) # normalize time with log
                        # predicted_difficulty = str(answer['predicted_difficulty'])

                        # assign label based on actual performance, not prediction
                        if result == gui.CORRECT and difficulty >= gui.MEDIUM:
                            label = "high"
                        elif result == gui.CORRECT:
                            label = "medium"
                        else:
                            label = "low"

                        X.append([result, difficulty, time_taken_logged])
                        y.append(label)

                    except (KeyError, ValueError, TypeError) as e:
                        print(f"Skipping bad entry in {filename}: {e}")
            
            except Exception as e:
                print(f"Error: {e}, Reading: {file_path}", sys.stderr)

    return X, y

# main
def main():

    # read questions from json file
    low_questions, medium_questions, high_questions = get_questions("questions.json")

    X_train, y_train=[], []
    if len(sys.argv) > 1:
        print('reading file')
        ''' If there is any command line input, read and prepare 
            previous answers from previous tests in 'data/'. This 
            will be our training data to train the Decision Tree.
        '''
        X_train, y_train = get_answers_to_X_y()

    # normalize control data and extend training set
    dummy_X_logged = [[compute_weighted_correct(x[0], x[2]), x[1], np.log(x[2] + 1)] for x in dummy_X]
    X_train.extend(dummy_X_logged)
    y_train.extend(dummy_y)
    
    model=DecisionTreeClassifier(class_weight="balanced")
    # evaluate the model
    if len(X_train) >= 5:  # only evaluate if we have enough samples
        X_train_split, X_test, y_train_split, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
        # model = DecisionTreeClassifier()
        model.fit(X_train_split, y_train_split)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # save classification metrics
        with open("training_predictions.log", "w") as log:
            log.write("\t\t\t\t\t\t--- Classification Report ---\n")
            log.write(classification_report(y_test, y_pred))

        print("--------------------------------")
        print(f"   Model Test Accuracy: {accuracy:.2f}")
        print("--------------------------------")

    else:
        print("-------------------------------------------------------------")
        print("Not enough data to evaluate accuracy, training with full set.")
        print("-------------------------------------------------------------")
        # 
        # # model = DecisionTreeClassifier()
        # model.fit(X_train, y_train)
    
    # initialize and train the model
    # model=DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # initialize GUI and start test
    project_gui = gui.GUI(low_questions,
                          medium_questions, 
                          high_questions, 
                          model)
    project_gui.start_test()

    # save answers and predictions to JSON file if answers exists
    if not project_gui.answers_list is None and len(project_gui.answers_list) > 0:
        if project_gui.determined: # only save if cognitive ability is determined
            file_name = 'data/' + project_gui.username.lower() + '_answers.json'
            with open(file_name, 'w') as out_jf:
                json.dump(project_gui.answers_list, out_jf, indent=4)


if __name__ == '__main__':
    main()
