# main.py
# Author: Andrew Kelton

import GUI as gui
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Cognitive ability levels
COGNITIVE_ABILITIES_STRING=["low", "medium", "high"]
LOW, MEDIUM, HIGH = 0, 1, 2

QUESTIONS=["1 + 1 = ?"]
ANSWERS=[2]
ANSWER_CHOICES=[[1,2,3,4]]

# question structure format
QUESTION1={
    "id": 0,
    "difficulty": LOW,
    "question": "1 + 1 = ?",
    "answer": 2,
    "answer choices": [1,2,3,4],
}
QUESTION2={
    "id": 4,
    "difficulty": HIGH,
    "question": "What is the next number in the sequence: 2, 6, 12, 20, 30, __.",
    "answer": 42,
    "answer choices": [42,40,21,43],
}
QUESTION3={
    "id": 2,
    "difficulty": MEDIUM,
    "question": "To be inferior to someone means?",
    "answer": "to be of lower status",
    "answer choices": ["to be of higher status","to be of lower status","to be poorer","to be equal to"],
}

# main
def main():
    project_gui = gui.GUI([QUESTION1, QUESTION2, QUESTION3]) # call game 
    print(project_gui.answers_list)

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

