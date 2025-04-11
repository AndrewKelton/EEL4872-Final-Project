# GUI.py
# Author: Andrew Kelton

''' 
User Interface for EEL 4872 Final Project
  * Working prototype gaming system that identifies the 
    depth of cognitive ability of an individual.
  * Contains: 
    - GUI
    - knowledge base of questions
    - decision tree approach
    - internal scoring system based on answers and questions provided

'''

import pandas as pd

import tkinter as tk
from tkinter import messagebox, simpledialog

from typing import List, Dict, Any

# for logging user interactions
from random import randint, sample
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ID="id"
QN="question"
AN="answer"
AC="answer choices"
DF="difficulty"


# GUI class
class GUI:

    def __init__(self, questions : List[Dict[str, Any]]):

        # set initial values
        self.num_of_questions = len(questions)
        self.questions = questions
        self.correct_count = 0
        self.current_question = 0

        # create Tkinter object
        self.root=tk.Tk()
        self.root.withdraw() # hide main window

        # welcome task
        self.get_username()
        self.root.deiconify()

        # build ui components
        self.build_menu_ui()
        self.build_main_ui()

    # build the main ui
    def build_main_ui(self) -> None:
        logging.debug("Building Main UI")

        # title
        self.root.title(f"{self.username.title()}'s Test")

        # heading
        self.label=tk.Label(self.root, text=f"{self.username.title()}'s Test", font=('Arial',18))
        self.label.pack(padx=10,pady=10)

        # question label
        self.question_label=tk.Label(self.root, text="Welcome", font=('Arial', 16))
        self.question_label.pack(padx=10, pady=10)

        # button grid to answer questions
        self.button_grid = self.ButtonGrid(self.root, self.answer_selected)
        self.button_grid_frame = self.button_grid.buttonframe

        # load the first question
        self.load_question(self.current_question)

        # exit the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    # build the menu bar ui
    def build_menu_ui(self) -> None:
        logging.debug("Building Menu UI")

        # menu bar configuration
        self.menubar=tk.Menu(self.root)

        # file menu configuration
        self.filemenu=tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close Without Question", command=exit)
        self.root.config(menu=self.menubar)

        # action bar configuration
        self.actionmenu=tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="Show Message", command=self.show_message)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Action")

     # get username from user
    def get_username(self) -> None:
        logging.debug("Collecting Username")

        self.username=None
        while not self.username or self.username == "":
            self.username=simpledialog.askstring("Welcome", "Enter your first name:")
        self.username=self.username.lower() # set to lowercase for easier access

        logging.info(f"User: {self.username} started test.")

    # load question into window
    def load_question(self, idx : int) -> None:

        # retrieve values
        question_dir = self.questions[idx]
        question_id = question_dir[ID] 
        question = question_dir[QN]
        choices = question_dir[AC]

        logging.debug(f"Loading Question ID {question_id}: {question}") 

        # set question and answers
        self.question_label.config(text=question)
        self.button_grid.set_answers(choices)

    # callback function when a button in grid is pressed
    def answer_selected(self, current_idx : int, chosen_idx : int) -> None:
        question_id = self.questions[current_idx][ID]
        logging.debug(f"Question ID {question_id} has been answered")

        selected_answer=self.button_grid.get_chosen_answer(chosen_idx) # collect answered value
        correct_answer=self.questions[current_idx][AN]                 # collect correct value

        if selected_answer == correct_answer:
            logging.info(f"Question ID {question_id}: Correct")
            self.correct_count += 1
            messagebox.showinfo("Correct", "nice one!")
        else:
            logging.info(f"Question ID {question_id}: Incorrect")
            messagebox.showwarning("Incorrect", f"The correct answer was {correct_answer}.")
        


        self.current_question += 1 # move to next question
        
        if self.current_question < self.num_of_questions:

            # more questions to complete
            self.load_question(self.current_question) 
        else:

            # all questions have been answered
            messagebox.showinfo("Done!", "You have completed all questions!")
            self.root.destroy()

    # print message to terminal
    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get('1.0', tk.END)) # prints inputted message to terminal
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END)) # shows a messagebox

    # exit GUI & close window
    def on_closing(self) -> None:
        if messagebox.askyesno(title="Quit", message="Do you really want to quit?"):
            self.root.destroy()

    # ButtonGrid class for multiple choice questions
    class ButtonGrid:
        
        def __init__(self, root, click_callback):

            # create buttonframe
            self.buttonframe=tk.Frame(root)
            self.buttonframe.columnconfigure(0, weight=1)
            self.buttonframe.columnconfigure(1, weight=1)

            # create button 2x2 grid
            self.grid =[]
            answer_idx=0
            for i in range(2):
                row = []
                for j in range(2):
                    btn=tk.Button(
                        self.buttonframe,
                        text="",
                        font=('Arial', 10),
                        command=lambda idx=answer_idx: click_callback(0, idx)
                    )
                    btn.grid(row=i,column=j,sticky=tk.W+tk.E)
                    row.append(btn)
                    answer_idx += 1
                self.grid.append(row)
            
            self.buttonframe.pack(fill=tk.X) # fill to edge's width

        # set the answers to button grid from a grouping of questions
        def set_answers(self, answers : list) -> None:
            logging.debug("Setting New Answers")

            random_answers = sample(answers, 4) # randomize answer choices
            answ_idx=0

            # set respective answer choices in grid
            for i in range(2):
                for j in range(2):
                    self.grid[i][j].config(text=random_answers[answ_idx])
                    answ_idx+=1
        
        # return the answer choice's value
        def get_chosen_answer(self, answer_idx) -> any:
            return self.get_button_from_1d_idx(answer_idx).cget("text")
        
        # returns button from grid index chosen
        def get_button_from_1d_idx(self, idx) -> tk.Button:
            if idx == 0:
                return self.grid[0][0]
            if idx == 1:
                return self.grid[0][1]
            if idx == 2:
                return self.grid[1][0]
            if idx == 3:
                return self.grid[1][1]
