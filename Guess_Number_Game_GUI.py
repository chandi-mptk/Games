from tkinter import (Tk, Text, END, Button, Entry, Label, StringVar)
from tkinter.messagebox import showerror, showinfo

from Guess_Number_Game import NumberGuessing


class GUI:
    def __init__(self, root):
        # Game Object
        self.number_guessing = None
        
        # Window Configuration
        self.root = root
        self.root.title("Guess Number Game")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.grab_set()
        self.root.focus_set()
        
        # Event Configuration
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.quit_game())
        self.root.bind('<Escape>', lambda event: self.quit_game())

        # Variables
        self.start_var = StringVar(value="1")
        self.end_var = StringVar(value="10")
        self.answer = StringVar()
                
        # Main Label
        self.main_label = Label(self.root, text="Welcome to Guess Number Game.", font=("Helvetica", 14))
        self.main_label.pack(padx=10, pady=10)

        # Game Instruction Area
        self.game_instruction_1 = Label(self.root, text=f"Select Start and End Numbers, from which the computer will Select a number")
        self.game_instruction_2 = Label(self.root, text=f"The Game is You have to guess the number.")
        self.game_instruction_3 = Label(self.root, text=f"Select Start and End numbers, Then press Start Game Button to Begin the Game.")
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
        self.start_label = Label(self.root, text="Start: ")
        self.start_entry =Entry(self.root, textvariable=self.start_var)
        self.end_label = Label(self.root, text="End: ")
        self.end_entry = Entry(self.root, textvariable=self.end_var)
        self.start_button = Button(self.root, text="Start Game", command=self.start_game)
        self.start_label.pack(padx=10, pady=5)
        self.start_entry.pack(padx=10, pady=5)
        self.end_label.pack(padx=10, pady=5)
        self.end_entry.pack(padx=10, pady=5)
        self.start_button.pack(padx=15, pady=15)

    # Remove Start Button
    def remove_start_button(self):
        self.start_label.destroy()
        self.start_entry.destroy()
        self.end_label.destroy()
        self.end_entry.destroy()
        self.start_button.destroy()

    def start_game(self):
        start, end = self.verify_range()
        showinfo("Guising", f"Computer is going to guess a Number between {start} and {end}, including both.")
        
        self.number_guessing = NumberGuessing(start, end)
        self.number_guessing.start_game()
        self.remove_start_button()
        self.create_answer_area()
        self.update_attempts()
        self.label_update(self.status_label, "Status: Waiting user to Enter Guess.")

    def update_attempts(self):
        attempts = self.number_guessing.attempts
        if attempts == 0:
            self.label_update(self.status_label, "Status: You Lost The game")
            self.label_update(self.attempt_label, "Attempt: 0", bg='red')
        elif attempts == 1:
            self.label_update(self.attempt_label, "Attempt: 1", bg='orange')
        elif attempts >= 2:
            self.label_update(self.attempt_label, f"Attempts: {attempts}", bg='green')
        

    def verify_range(self):
        try:
            start = int(self.start_var.get())
            end = int(self.end_var.get())
        except ValueError:
            showerror("Error", "You Enter Invalid Range. Loading Defaults")
            self.load_default_range()
            return 1, 10
        if start > end or end - start < 9:
            showerror("Error", "You Enter Invalid Range. Loading Defaults")
            return 1, 10
        return start, end

    def load_default_range(self):
        self.start_var.set("1")
        self.end_var.set("10")

    def label_update(self, label, new_text, bg="green", fg="white"):
        label.config(text=new_text, bg=bg, fg=fg)
        
    # Create Entry field for Answer
    def create_answer_area(self):
        self.answer_label = Label(self.root, text="Guess: ")
        self.answer_label.pack(padx=10, pady=10)
        self.answer_entry = Entry(self.root, textvariable=self.answer)
        self.answer_entry.pack(padx=10, pady=10)
        
        self.answer_entry.focus_set()
        self.answer_entry.bind("<Return>", self.check_answer)

        # Submit Button
        self.submit_button = Button(self.root, text="Submit", command=self.check_answer)
        self.submit_button.pack(padx=10, pady=10)

    # Remove answer area
    def remove_answer_area(self):
        self.answer_label.destroy()
        self.answer_entry.destroy()
        self.submit_button.destroy()


    def check_answer(self):
        if self.number_guessing.is_guess_valid(self.answer.get()):
            if self.number_guessing.is_guess_correct(self.answer.get()):
                self.label_update(self.status_label, "Status: You Won The game")
                self.label_update(self.attempt_label, "Attempt: 0", bg='green')
                showinfo("Won", "You won the Game.")
                self.remove_answer_area()
                self.create_start_button()
                self.number_guessing.reset_game()
            else:
                if self.number_guessing.is_attempts_left:
                    self.label_update(self.status_label, "Status: Waiting user to Enter Guess.")
                    self.update_attempts()
                else:
                    self.label_update(self.status_label, "Status: You Lost The game, Click Start to Play again.", bg='red')
                    self.label_update(self.attempt_label, "Attempt: 0", bg='red')
                    showerror("Lost", "You lost the Game.")
                    self.remove_answer_area()
                    self.create_start_button()
                    self.number_guessing.reset_game()
        self.answer.set("")


    def quit_game(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    gui = GUI(root)
    root.mainloop()