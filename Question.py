# Question.py
# Author: Andrew Kelton

from sklearn.tree import DecisionTreeClassifier

# Cognitive ability levels
COGNITIVE_ABILITIES_STRING=["low", "medium", "high"]
LOW=0
MEDIUM=1
HIGH=2

# Question Class
class Question:
    def __init__(self, question_id : int, difficulty : int, question : str, answer : any, answer_choices : list):
        self.question_id=question_id
        self.difficulty=difficulty 
        self.question=question
        self.answers=answer
        self.answer_choices=answer_choices
