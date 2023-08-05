import random

class RandomNumberGame:

    def __init__(self):
        
        """ Guess my number game class. The player has to guess a random number between 1 and 100 with as few attempts as possible.
        
             Attributes: 
                 None
                 """

        self.solution = random.randint(1,100)


    def play_a_game():

        """Function to start a game. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.

        Args:
            None

        Returns:
            Messages
            """

        new_game = RandomNumberGame()
        new_game.is_solution()


    def take_a_guess(self):

         """Function to request and receive a guess from the player.

         Args:
             None

         Returns:
             None
             """

         try:
             self.guess = int(input("Guess a number between 1 and 100:- "))
         except ValueError:
             print("You're input is not an integer.")


    def is_solution(self):

        """Function to check, if the guess is right (then the end of the game is reached) or to give a hint, if not.

        Args:
            None

        Returns:
            Messages
            """

        self.attempts = 0
        while self.attempts < 100:
            self.attempts += 1
            self.take_a_guess()
            if self.guess == self.solution:
                print("You won! Number of tries: ", self.attempts)
                break
            elif self.guess < self.solution:
                print("No, the number must be higher")
            else:
                print("No, the number must be smaller")





