# main.py
# Author: Andrew Kelton

# import my gui
import GUI_tree as gui

# import DT modules
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import pandas as pd
import json

class QuestionNode: 

    def __init__(self, question_data, correct_child=None, incorrect_child=None):
        self.question_data = question_data  # dict with question info
        self.correct_child = correct_child
        self.incorrect_child = incorrect_child

def load_tree_from_dict(data):
    if data is None:
        return None
    question_data = data["question_data"]
    correct_child = load_tree_from_dict(data.get("correct_child"))
    incorrect_child = load_tree_from_dict(data.get("incorrect_child"))
    return QuestionNode(question_data, correct_child, incorrect_child)

def load_tree_from_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return load_tree_from_dict(data)


# main
def main():

    root_node = load_tree_from_file("questions-tree.json")
    app = gui.GUI(root_node)

#     # create df from results
#     if 1 == 0:
#         df = pd.DataFram(project_gui.answers_list, columns=["question_id", "selected_answer", "result", "difficulty"])
#         X = df["question_id", "selected_answer", "result", "difficulty"]
#         y = df['''cognitive ability levels''']
# 
#         # split data
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# 
#         # train model
#         clf = DecisionTreeClassifier()
#         clf.fit(X_train, y_train)
#         y_pred = clf.predict(X_test)
#         
#         print(classification_report(y_test, y_pred, target_names=COGNITIVE_ABILITIES_STRING))



if __name__ == '__main__':
    main()

