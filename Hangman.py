import tkinter as tk
import random
from tkinter import messagebox

# Word list of fruits and vegetables
word_list = [
    "apple", "banana", "carrot", "grape", "melon", "onion", "peach", "tomato", 
    "lemon", "mango", "kiwi", "cherry", "beet", "olive", "berry", "pear", "plum"
]

# Function to get a random word from the word list
def get_random_word(word_list):
    return random.choice([word for word in word_list if len(word) <= 6]).upper()

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman - Fruits & Vegetables Edition")

        # Set window size to 500x600 pixels
        self.root.geometry("500x600")

        # Center the window on the screen
        self.center_window()

        # Track the score (reset on close)
        self.score = 0
        
        # Title screen setup
        self.title_screen = tk.Frame(self.root, bg="pale green")
        self.title_screen.pack(fill="both", expand=True)

        title_label = tk.Label(self.title_screen, text="Welcome to Hangman!", font=("Lucida Consolefont", 24), bg="pale green")
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.title_screen, text="Guess the Fruit or Vegetable", font=("Lucida Consolefont", 18), bg="pale green")
        subtitle_label.pack(pady=10)
        
        start_button = tk.Button(self.title_screen, text="Start Game", command=self.start_game, font=("Lucida Consolefont", 16))
        start_button.pack(pady=20)

        self.canvas = None  # Hangman canvas will be created later

    def center_window(self):
        """Center the window on the screen."""
        window_width = 500
        window_height = 600

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_game(self):
        # Hide title screen and start the game
        self.title_screen.pack_forget()
        
        # Initialize game variables
        self.word = get_random_word(word_list)
        self.correct_guesses = set()
        self.guessed_letters = set()
        self.attempts_left = 6  # Starting with 6 total incorrect attempts
        
        # Game screen UI elements
        self.game_screen = tk.Frame(self.root)
        self.game_screen.pack(fill="both", expand=True)

        # Display score in the top-right corner
        self.score_label = tk.Label(self.game_screen, text=f"Score: {self.score}", font=("Lucida Consolefont", 14), anchor='e')
        self.score_label.pack(side='top', anchor='ne', padx=10)  # Pack it to the top-right corner

        # Hangman drawing canvas
        self.canvas = tk.Canvas(self.game_screen, width=200, height=200)
        self.canvas.pack(pady=20)
        self.draw_hangman(0)  # Start with the scaffold

        # Word display label
        self.word_label = tk.Label(self.game_screen, text=self.display_word_progress(), font=("Lucida Consolefont", 18))
        self.word_label.pack(pady=20)
        
        self.guess_label = tk.Label(self.game_screen, text="Guess a letter:", font=("Lucida Consolefont", 14))
        self.guess_label.pack()
        
        self.guess_entry = tk.Entry(self.game_screen, font=("Lucida Consolefont", 14))
        self.guess_entry.pack()

        # Add the submit button to process the guess
        self.submit_button = tk.Button(self.game_screen, text="Submit", command=self.process_guess, font=("Lucida Consolefont", 14))
        self.submit_button.pack(pady=10)

        self.attempts_label = tk.Label(self.game_screen, text=f"Attempts left: {self.attempts_left}", font=("Lucida Consolefont", 14))
        self.attempts_label.pack(pady=10)
        
        self.guessed_letters_label = tk.Label(self.game_screen, text="Guessed letters: ", font=("Lucida Consolefont", 14))
        self.guessed_letters_label.pack()

    def display_word_progress(self):
        return ' '.join([letter if letter in self.correct_guesses else '_' for letter in self.word])

    def draw_hangman(self, incorrect_attempts):
        """Draw parts of the hangman based on the number of incorrect attempts."""
        self.canvas.delete("all")  # Clear the canvas first
        # Draw the base structure (Scaffold drawn from the start)
        self.canvas.create_line(20, 180, 180, 180, width=3)  # Base
        self.canvas.create_line(100, 180, 100, 20, width=3)   # Vertical pole
        self.canvas.create_line(100, 20, 150, 20, width=3)    # Horizontal pole
        self.canvas.create_line(150, 20, 150, 40, width=3)    # Rope

        # Draw parts of the hangman based on wrong attempts (head, body, arms, legs)
        if incorrect_attempts > 0:
            self.canvas.create_oval(130, 40, 170, 80, width=3)  # Head
        if incorrect_attempts > 1:
            self.canvas.create_line(150, 80, 150, 130, width=3)  # Body
        if incorrect_attempts > 2:
            self.canvas.create_line(150, 90, 130, 110, width=3)  # Left arm
        if incorrect_attempts > 3:
            self.canvas.create_line(150, 90, 170, 110, width=3)  # Right arm
        if incorrect_attempts > 4:
            self.canvas.create_line(150, 130, 130, 160, width=3)  # Left leg
        if incorrect_attempts > 5:
            self.canvas.create_line(150, 130, 170, 160, width=3)  # Right leg

    def process_guess(self):
        guess = self.guess_entry.get().upper()
        self.guess_entry.delete(0, tk.END)
        
        # Validate guess
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid input", "Please enter a single letter.")
            return
        
        if guess in self.guessed_letters:
            messagebox.showwarning("Already guessed", f"You already guessed the letter '{guess}'.")
            return
        
        self.guessed_letters.add(guess)
        self.guessed_letters_label.config(text=f"Guessed letters: {', '.join(self.guessed_letters)}")
        
        if guess in self.word:
            self.correct_guesses.add(guess)
            self.word_label.config(text=self.display_word_progress())
            
            # Check if the player has guessed the word
            if set(self.word) == self.correct_guesses:
                messagebox.showinfo("Congratulations!", f"You've guessed the word: {self.word}")
                self.score += 1  # Increment score
                self.score_label.config(text=f"Score: {self.score}")
                self.reset_game()
        else:
            self.attempts_left -= 1
            self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
            self.draw_hangman(6 - self.attempts_left)  # Update hangman drawing
            
            if self.attempts_left == 0:
                messagebox.showerror("Game Over", f"You're out of attempts! The word was: {self.word}")
                self.reset_game()

    def reset_game(self):
        # Reset game state
        self.word = get_random_word(word_list)
        self.correct_guesses = set()
        self.guessed_letters = set()
        self.attempts_left = 6

        # Reset UI elements
        self.word_label.config(text=self.display_word_progress())
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.guessed_letters_label.config(text="Guessed letters: ")
        self.draw_hangman(0)  # Clear hangman drawing


if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
