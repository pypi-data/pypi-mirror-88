"""Module containing the Game class."""

from .player import Player

class Game:
    """Represents the larger game structure for Yahtzee.

    Manages tracking and advancing global turns as well as initiating end-of-game scoring calculations. 
    Creating a game will create instances of the Player object according to the specified number of players passed to the constructor.
    
    Attributes:
        players (list): A list of Player object instances, one for each participant. The player_name attribute is set to "P{index_in_players_list}" which can be used to distinguish players.
        remaining_turns (int): Global turn tracker.
        current_player (Player): The player who is currently rolling dice/scoring.
        num_players (int): Number of players in the game. 
        winner (Player): Player who wins the game.
        tie (boolean): True if game ends in a tie - in this case, winner attribute will remain none.
    """

    def __init__(self, num_players):
        """Class constructor.
        
        Args:
            num_players (int): Number of palyers in the game.
        """
        self.players = [Player("P" + str(i)) for i in range(num_players)]
        self.remaining_turns = 13
        self.current_player = self.players[0]
        self.num_players = num_players

    def next_player(self):
        """Advances to the next player and moves to the next global turn when the last player is detected.
        
        Once the 13th turn is completed, this method will automatically calculate the final scores and
        return a list containing the winner(s) Player object(s).
        """
        if self.players.index(self.current_player) == self.num_players - 1:
            self.remaining_turns -= 1
            self.current_player = self.players[0]
            if self.remaining_turns == 0:
                return self._end_game()
        else:
            self.current_player = self.players[self.players.index(self.current_player) + 1]
            return []

    def print_status(self):
        """Prints out the current moment-in-time status of the game."""
        print("Turns Remaining: ", self.remaining_turns)
        print("Current player:", self.current_player.player_name)
        print("\n")
        for player in self.players:
            print(player.player_name + "'s scorecard:")
            player.print_scorecard()

    def _end_game(self):
        """Computes final scores for each player and prints the results.
        
        Returns a list with the winner(s). If there is a tie, the list will contain all players who had the highest score.
        Otherwise the list will contain only the winner, in position 0.
        """
        final_scores = []
        for player in self.players:
            player.calculate_final_score()
            final_scores.append(player.score)
        return [player for player in self.players if player.score == max(final_scores)]

