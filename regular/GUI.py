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

# general imports
from typing import List, Dict, Any
from random import sample
import time

# gui module import
import tkinter as tk
from tkinter import messagebox, simpledialog

# logging user interactions import
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# dictionary abbreviations of a question
ID="id"
QN="question"
AN="answer"
AC="answer choices"
DF="difficulty"

# indexes for variables in lists
INCORRECT=ID_=0
CORRECT=AN_=1
RS=2

# cognitive ability levels & their mapping
COGNITIVE_ABILITIES_STRING=["low", "medium", "high"]
LOW, MEDIUM, HIGH = 0, 1, 2
DIFF_MAP={
    COGNITIVE_ABILITIES_STRING[LOW]: LOW,
    COGNITIVE_ABILITIES_STRING[MEDIUM]: MEDIUM,
    COGNITIVE_ABILITIES_STRING[HIGH]: HIGH
}

# default font sizes
TITLE_FONT_SIZE=48
QUESTION_FONT_SIZE=24
BUTTON_FONT_SIZE=22


# GUI class
class GUI:

    def __init__(self, questions : List[Dict[str, Any]]):

        # create Tkinter object
        self.root=tk.Tk()
        self.root.withdraw() # hide main window

        # set initial values
        self.num_of_questions = len(questions)
        self.questions = questions
        self.current_question= self.score = self.correct_count = 0
        self.start_time = None
        self.possible_score = 0

        self.answers_list = [] # [[id,answ,res,diff, time],...]
        '''
            Example of an entry in answers_list

            answers_list[i] = {
                "id": question_id, 
                "selected_answer": selected_answer, 
                "result": result, 
                "difficulty": question[DF], 
                "time_taken": time_taken
            }
        '''

    def start_test(self) -> None:
        try:
            # welcome task
            self.__get_username()
            self.root.deiconify()

            # build ui components
            self.__build_main_ui()
            self.__build_menu_ui()
        except Exception as e:

            # menubar glitch, this ignores it
            if str(e).find("menu") != -1:
                return

            # print the error
            import tkinter.messagebox as msg
            msg.showerror("Error", f"Something went wrong:\n{e}")

            try:
                if hasattr(self, 'header_frame') and self.header_frame.winfo_exists():
                    self.header_frame.destroy()
                if hasattr(self, 'question_label') and self.question_label.winfo_exists():
                    self.question_label.destroy()
                if hasattr(self, 'button_grid_frame') and self.button_grid_frame.winfo_exists():
                    self.button_grid_frame.destroy()
                if self.root and self.root.winfo_exists():
                    self.root.destroy()
            except Exception as destroy_err:
                print(f"Error while cleaning up UI: {destroy_err}")
            
        
    # build the main ui
    def __build_main_ui(self) -> None:
        logging.debug("Building Main UI") # print debug

        self.root.title(f"{self.username.title()}'s Cognitive Test") # title
        self.root.geometry("800x600") # set size

        # header frame
        self.header_frame=tk.Frame(self.root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)

        # title
        self.label=tk.Label(
            self.header_frame, 
            text=f"{self.username.title()}'s Cognitive Test", 
            font=('Arial',TITLE_FONT_SIZE)
        )
        self.label.pack(padx=10,pady=10,side=tk.LEFT)

        # question count
        self.counter_label=tk.Label(self.header_frame, text="", font=('Arial', 14))
        self.counter_label.pack(padx=10,pady=10,side=tk.RIGHT)

        # question label
        self.question_label=tk.Label(
            self.root, 
            text="Welcome", 
            font=('Arial', QUESTION_FONT_SIZE),
            wraplength=700,
            justify="center"
        )
        self.question_label.pack(expand=True, fill="both", padx=10, pady=10)

        # button grid to answer questions
        self.button_grid = self.__ButtonGrid(self.root, self.__answer_selected)
        self.button_grid_frame = self.button_grid.buttonframe

        self.__load_question() # load the first question
 
        # close window
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.__on_closing(self.root))
        self.root.mainloop()

    # build the menu bar ui
    def __build_menu_ui(self) -> None:
        logging.debug("Building Menu UI") # print debug

        # menu bar configuration
        self.menubar=tk.Menu(self.root)

        # file menu configuration
        self.filemenu=tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.__on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close Without Question", command=self.__close_without_prompt)
        self.root.config(menu=self.menubar)

        # action bar configuration
        self.actionmenu=tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="Show Message", command=self.__show_message)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Action")

    # get username from user
    def __get_username(self) -> None:
        logging.debug("Collecting Username") # print debug

        self.username=None
        while not self.username or self.username == "":
            self.username=simpledialog.askstring("Welcome", "Enter your first name:")
        self.username=self.username.lower() # set to lowercase for easier access

        logging.info(f"User: {self.username} started test.")

    # load question into window
    def __load_question(self) -> None:
        self.start_time = time.time()
        
        # update question counter
        self.counter_label.config(text=f"Question {self.current_question + 1} of {self.num_of_questions}")

        # retrieve values
        self.current_question_dir = self.questions.pop(0)
        question_id = self.current_question_dir[ID] 
        question = self.current_question_dir[QN]
        choices = self.current_question_dir[AC]

        logging.debug(f"Loading Question ID {question_id}: {question}") # print debug

        # set question and answers
        self.question_label.config(text=question)
        self.button_grid.set_answers(choices)

    # callback function when a button in grid is pressed
    def __answer_selected(self, chosen_idx : int) -> None:
        end_time = time.time()
        time_taken = end_time - self.start_time

        question = self.current_question_dir 
        question_id = question[ID]

        selected_answer=self.button_grid.get_chosen_answer(chosen_idx) # collect answered value
        correct_answer =question[AN] # collect correct value

        logging.info(f"Question ID: {question_id}\tAnswered: '{selected_answer}'\tAnswer: '{correct_answer}'") # print debug

        self.possible_score += question[DF] + 1

        # user's answer correct
        if selected_answer == correct_answer:

            self.correct_count += 1        # increment correct count
            self.score += question[DF] + 1 # increase user's score
            self.answers_list.append({
                "id": question_id, 
                "selected_answer": selected_answer, 
                "result": CORRECT, 
                "difficulty": question[DF], 
                "time_taken": time_taken
            })
            messagebox.showinfo("Correct", "good job!")

        # user's answer incorrect
        else:

            # remove a point if difficulty is low
            if question[DF] == LOW:
                self.score -= 1
            
            self.answers_list.append({
                "id": question_id, 
                "selected_answer": selected_answer, 
                "result": INCORRECT, 
                "difficulty": question[DF], 
                "time_taken": time_taken
            })
            messagebox.showwarning("Incorrect", f"The correct answer was {correct_answer}.")
    
        self.current_question += 1 # increment current question count
        
        # more questions to complete
        if len(self.questions) > 0 and self.current_question < self.num_of_questions:
            self.__load_question() 
        
        # all questions have been completed
        else:
            messagebox.showinfo("Done!", "You have completed all questions!")
            self.__results_screen()

    # print message to terminal
    def __show_message(self) -> None:
        if self.check_state.get() == 0:
            print(self.textbox.get('1.0', tk.END)) # prints inputted message to terminal
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END)) # shows a messagebox

    # results screen when quiz finishes
    def __results_screen(self) -> None:
        self.root.destroy() # destroy quiz window 

        # create results window
        result_wdw = tk.Tk()
        result_wdw.title(f"{self.username.title()}'s Cognitive Ability Test Results") 
        result_wdw.geometry("800x600")
        label = tk.Label(
            result_wdw, 
            text="Thank you for completing the cognitive ability test!", 
            font=('Arial', QUESTION_FONT_SIZE)
        )
        label.pack(pady=20)

        # score labels
        correct_label = tk.Label(
            result_wdw, 
            text=f"{self.correct_count} / {self.num_of_questions} questions answered correctly!", 
            font=('Arial', BUTTON_FONT_SIZE)
        )
        correct_label.pack(pady=10)
        score_label = tk.Label(
            result_wdw, 
            text=f"Score: {self.score} / {self.possible_score}!", 
            font=('Arial', BUTTON_FONT_SIZE)
        )
        score_label.pack(pady=10)

        # close window
        result_wdw.protocol("WM_DELETE_WINDOW", lambda: self.__on_closing(result_wdw))
        result_wdw.mainloop()
        
    # exit GUI & close window
    def __on_closing(self, window) -> None:
        if messagebox.askyesno(title="Quit", message="Do you really want to quit?"):
            try:
                window.destroy()
            except Exception as e:
                logging.warning(f"Error: {e}")
    
    def __close_without_prompt(self) -> None:
        try:
            self.root.destroy()
        except Exception as e:
            logging.warning(f"Error: {e}")


    # ButtonGrid class for multiple choice questions
    class __ButtonGrid:
        
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
                self.buttonframe.grid_rowconfigure(i, weight=1, uniform="row") # size formatting

                for j in range(2):
                    self.buttonframe.grid_columnconfigure(j, weight=1, uniform="col") # size formatting
                    
                    # create button in grid
                    btn=tk.Button(
                        self.buttonframe,
                        text="",
                        font=('Arial', BUTTON_FONT_SIZE),
                        wraplength=150,
                        justify='center',
                        command=lambda idx=answer_idx: click_callback(idx)
                    )
                    btn.grid(row=i,column=j,sticky='nsew', padx=5, pady=5)
                    row.append(btn)
                    answer_idx += 1

                self.grid.append(row)
            
            # self.buttonframe.pack(fill=tk.X) # fill to edge's width
            self.buttonframe.pack(fill=tk.BOTH, expand=True)
            self.buttonframe.grid_propagate(False)

        # set the answers to button grid from a grouping of questions
        def set_answers(self, answers : list) -> None:
            logging.debug("Setting New Answers") # print debug

            random_answers = sample(answers, 4) # randomize answer choices

            # set respective answer choices in grid
            for i in range(2):
                for j in range(2):
                    self.grid[i][j].config(text=random_answers.pop(0))
        
        # return the answer choice's value
        def get_chosen_answer(self, answer_idx) -> any:
            return self.get_button_from_1d_idx(answer_idx).cget("text")
        
        # returns button from grid index chosen
        def get_button_from_1d_idx(self, idx) -> tk.Button:
            if idx == 0:
                return self.grid[0][0]
            elif idx == 1:
                return self.grid[0][1]
            elif idx == 2:
                return self.grid[1][0]
            elif idx == 3:
                return self.grid[1][1]
            else:
                return None
