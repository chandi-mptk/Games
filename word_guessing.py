import sqlite3
from pathlib import Path
from random import choice
from string import ascii_uppercase


DB = "/home/nishanth/Desktop/GITHUB/Games/DATA/olamdb.db"

class WordGuessing:
    def __init__(self, db):
        
        # Check file Available
        if not Path(DB).is_file():
            print(f"File Not Found: {DB}")
            quit()
        self.db = db
        self.level = 0
        self.attempt = 0
        self.olam_data = None
        self.game_data = {}
        self.eng_word = ""
        self.eng_word_show = ""
        self.mal_word = ""
    
    def fetch_data(self):
        try:
            self.conn = sqlite3.connect(self.db)
            self.cursor = self.conn.cursor()
            
            # Select english and malayalam from olam table
            self.cursor.execute("SELECT english, malayalam FROM olam")
            self.olam_data = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
            return False
        return True
        
    def load_level(self, level):
        self.level = level
    
    def filter_data(self):
        try:
            # Iterate over olam_data
            for eng, mal in self.olam_data:
                eng = eng.strip().upper()
                # Check if eng contain other than ascii_uppercase
                if not all(c in ascii_uppercase for c in eng):
                    continue
                # eng not already added
                if eng in self.game_data.keys():
                    continue
                if len(eng) >= (self.level + 2):
                    self.game_data[eng] = mal
        except Exception as e:
            print(e)
            return False
        return True

    def start_game(self):
        self.eng_word = choice(list(self.game_data.keys()))
        eng_word_show = []
        for i, l in enumerate(self.eng_word):
            if i == 0:
                eng_word_show.append(l)
            elif i % (self.level + 1) != 0:
                eng_word_show.append('_')
            elif i % (self.level + 1) == 0:
                eng_word_show.append(l)
        
        self.eng_word_show = "".join(eng_word_show)
        self.mal_word = self.game_data[self.eng_word]
        self.attempt = self.attempt_calc
        
    def show_question(self):
        print(self.eng_word)
        return self.mal_word, self.eng_word_show
    
    def is_answer_ok(self, answer):
        self.attempt -= 1
        return answer.upper() == self.eng_word

    @property
    def attempt_calc(self):
        return max(self.eng_word_show.count('_') - 1, 1)

if __name__ == '__main__':
    
    word_guessing = WordGuessing(db=DB)
    
    # Select Game Level
    level = None
    while level is None:
        print("Select Game Difficulty Level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        level = input("Enter Your Choice: ")
        print()
        try:
            level = int(level)
            if level < 1 or level > 3:
                print("Error, Entered Level is invalid.")
                level = None
        except ValueError:
            print("Error, Entered Level is invalid.")
            level = None
        print()
    
    # Start Game
    if not word_guessing.fetch_data():
        print(f"File Loading Error.")
        quit()
    
    # Load Level
    word_guessing.load_level(level)

    # Filter Data
    if not word_guessing.filter_data():
        print("Data Filtering Error.")
        quit()
    print(f"Data Loaded:-\nTotal Data Available: {len(word_guessing.game_data)}")
    word_guessing.start_game()
    mal, eng_show = word_guessing.show_question()

    while word_guessing.attempt >=1:
        print()
        print(f"You have {word_guessing.attempt} attempts left.")
        print(f"English Word: {eng_show}")
        print(f"Malayalam Meaning: {mal}")
        eng_prediction = input("The English word: ")
        
        if len(eng_show) != len(eng_prediction):
            print("Error, Entered word length is not correct.")
            continue
        if not word_guessing.is_answer_ok(eng_prediction):
            if word_guessing.attempt <= 0:
                print("No Attempts Left.")
            print("Error, Entered word is not correct.")
            continue
        else:
            print(f"You guessed the word correctly.")
            break
        

