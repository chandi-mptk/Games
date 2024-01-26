
from random import randint
from math import ceil
import re


class NumberGuessing:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end
        self.guess = None
        self.attempts = self.calculate_attempts
    
    @property
    def calculate_attempts(self) -> int:
        attempts = ceil((self.end - self.start) * 0.05)
        if attempts < 3:
            return 3
        return attempts
    
    @property
    def is_attempts_left(self) -> bool:
        return self.attempts > 0
    
    def start_game(self) -> None:
        self.guess = randint(self.start, self.end)
        
    def is_guess_valid(self, guess) -> bool:
        try:
            guess = int(guess)
            self.attempts -= 1
            return True
        except ValueError:
            return False
        
    def is_guess_correct(self, guess):
        print(f"Guess: {self.guess}")
        return int(guess) == self.guess

    def reset_game(self):
        self.guess = None
        self.attempts = self.calculate_attempts


if __name__ == '__main__':

    # Get Number Range
    def get_range():
        number_range = input("Enter The Guessing Range (Default 1-10): ")
        if not number_range:
            return "1-10"
        return number_range
    
    # Get Guess
    def get_guess(start, end):
        guess = input(f"Enter Your guess Between {start} and {end} included both: ")
        return guess
    
    # Regex to check the format of number_range as number-number
    def is_valid_number_range(number_range):
        # Define the pattern for the desired format
        pattern = re.compile(r'^\d+-\d+$')
        return bool(pattern.match(number_range))

    number_range = None

    while number_range is None:
        number_range = get_range()
        # Using regex check the format of number_range as number-number
        if not is_valid_number_range(number_range):
            print("Error, Entered Number range is invalid.")
            number_range = None
            continue

        start, end = number_range.split('-')
        try:
            start = int(start)
            end = int(end)
            if start > end:
                print("Error, first value must be less than the second value Eg. 1-10")
                number_range = None
            elif end - start < 9:
                print("Error, Minimum difference must be 10 or greater.")
                number_range = None
        except ValueError:
            print("Error, Entered Number range is invalid.")
            number_range = None


    number_guessing = NumberGuessing(start=start, end=end)
    number_guessing.start_game()
    while number_guessing.is_attempts_left:
        guess = get_guess(start=number_guessing.start, end=number_guessing.end)
        if number_guessing.is_guess_valid(guess):
            if number_guessing.is_guess_correct(guess):
                print(f"You guessed the number Correct.{guess}")
                break
            else:
                print(f"You guessed the number {guess} is Not Correct.")
                print(f"You have {number_guessing.attempts} Attempts left.")
        else:
            print(f"Invalid Guess {guess}")



