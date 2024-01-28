from tkinter import (Tk, Text, END, Button, Entry, Label, StringVar, ttk)
from tkinter.messagebox import showerror, showinfo

from word_guessing import WordGuessing, DB


class GUI:
    def __init__(self, root):
        # Game Object
        self.word_prediction = WordGuessing(DB)
        if not self.word_prediction.fetch_data():
            showerror("Program Error", "Word Database Corrupt")
            self.quit_game()
        
        # Window Configuration
        self.root = root
        self.root.title("Word Prediction Game")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.grab_set()
        self.root.focus_set()
        
        # Event Configuration
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.quit_game())
        self.root.bind('<Escape>', lambda event: self.quit_game())

        # Variables
        self.answer = StringVar()
        self.attempts = 0
                
        # Main Label
        self.main_label = Label(self.root, text="Welcome to Word Prediction Game.", font=("Helvetica", 14))
        self.main_label.pack(padx=10, pady=10)

        # Game Instruction Area
        self.game_instruction_1 = Label(self.root, text=f"Select Difficulty Level of the Game, and Press Start Game.")
        self.game_instruction_2 = Label(self.root, text=f"Computer will Show The Malayalam Meaning of the word and show the word with missing letters.")
        self.game_instruction_3 = Label(self.root, text=f"You Have to predict the word from its Malayalam Meaning and Available Letters.")
        self.status_label = Label(self.root, text="Status: Waiting user to Begin Game.", bg='green', fg="white")
        self.attempt_label = Label(self.root, text="")
        self.game_instruction_1.pack(padx=10, pady=10)
        self.game_instruction_2.pack(padx=10, pady=10)
        self.game_instruction_3.pack(padx=10, pady=10)
        self.status_label.pack(padx=10, pady=10)
        self.attempt_label.pack(padx=10, pady=10)

        self.create_start_button()

    # Create Start Button
    def create_start_button(self):
        self.start_label = Label(self.root, text="Difficulty Level: ")
        self.level_combo =ttk.Combobox(state='readonly', values=["Level-1", "Level-2", "Level-3"])
        self.level_combo.set("Level-1")
        
        self.start_button = Button(self.root, text="Start Game", command=self.start_game)
        self.start_label.pack(padx=10, pady=5)
        self.level_combo.pack(padx=10, pady=5)
        self.start_button.pack(padx=15, pady=15)

    # Remove Start Button
    def remove_start_button(self):
        self.start_label.destroy()
        self.level_combo.destroy()
        self.start_button.destroy()

    def start_game(self):
        level = self.verify_level()
        # showinfo("Fetching Data", f"Computer Preparing Data")
        
        self.word_prediction.load_level(level=level)
        if not self.word_prediction.filter_data():
            showerror("Program Error", "Data Filtering Error")
            self.quit_game()

        self.word_prediction.start_game()
        
        self.remove_start_button()
        self.create_answer_area()
        self.attempts = self.word_prediction.attempt_calc
        self.label_update(self.status_label, "Status: Waiting user to Enter Guess.")
        self.label_update(self.attempt_label, f"Attempt: {self.attempts}", bg='green')
        

    def verify_level(self):
        level = self.level_combo.get()
        if level == "Level-1":
            return 1
        elif level == "Level-2":
            return 2
        elif level == "Level-3":
            return 3
        else:
            return 0

    def label_update(self, label, new_text, bg="green", fg="white"):
        label.config(text=new_text, bg=bg, fg=fg)
        
    # Create Entry field for Answer
    def create_answer_area(self):
        mal, eng = self.word_prediction.show_question()
        self.meaning_label = Label(self.root, text=f"Word Meaning: {mal}", font=("Helvetica", 14))
        self.word_label = Label(self.root, text=f"Word: {eng}", font=("Helvetica", 14))
        self.meaning_label.pack(padx=10, pady=10)
        self.word_label.pack(padx=10, pady=10)
        self.answer_entry = Entry(self.root, textvariable=self.answer)
        self.answer_entry.pack(padx=10, pady=10)
        
        self.answer_entry.focus_set()
        self.answer_entry.bind("<Return>", self.check_answer)

        # Submit Button
        self.submit_button = Button(self.root, text="Submit", command=self.check_answer)
        self.submit_button.pack(padx=10, pady=10)

    # Remove answer area
    def remove_answer_area(self):
        bg = self.root.cget("background")
        self.label_update(self.attempt_label, "", bg=bg)
        self.meaning_label.destroy()
        self.word_label.destroy()
        self.answer_entry.destroy()
        self.submit_button.destroy()


    def check_answer(self, event=None):
        if self.word_prediction.is_answer_ok(self.answer.get()):
            self.label_update(self.status_label, "Status: You Won The game")
            self.label_update(self.attempt_label, "Attempt: 0", bg='green')
            showinfo("Won", "Your Answer is Correct.")
            self.remove_answer_area()
            self.create_start_button()
        else:
            if self.word_prediction.attempt >= 1:
                self.label_update(self.status_label, "Status: Try again.")
                attempt = self.word_prediction.attempt
                if attempt == 1:
                    bg = 'red'
                elif attempt == 2:
                    bg = 'orange'
                else:
                    bg = 'green'
                self.label_update(self.attempt_label, f"Attempt: {self.word_prediction.attempt}", bg=bg)
            else:
                self.label_update(self.status_label, "Status: You Lost The game, Click Start to Play again.", bg='red')
                self.label_update(self.attempt_label, "Attempt: 0", bg='red')
                showerror("Lost", "You lost the Game.")
                self.remove_answer_area()
                self.create_start_button()
                self.word_prediction.reset_game()
        self.answer.set("")


    def quit_game(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    gui = GUI(root)
    root.mainloop()