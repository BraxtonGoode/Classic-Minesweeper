# game_view.py
# Game View for MineSweeper Game

# imports
import arcade
import settings
import time
from game.board import Board

# Class Description: Main game view where the Minesweeper board is displayed and interacted with.
# Args: difficulty (str) - The difficulty level for the game ("EASY", "NORMAL", "EXPERT")
# Returns: None
# Notes: Handles the main game interface, user interactions, and game logic.
class GameView(arcade.View):
    """
    Main application class.
    """

    # (*** Functions: __init__, on_draw, on_mouse_press, game_result, on_key_press, get_elapsed_time ***)

    # Description: Initialize the game view
    # Args: self, default difficulty level (str)
    # Returns: None
    # Notes: Sets up the game board and initializes the timer
    def __init__(self, difficulty="EXPERT", ):
        super().__init__()        
        settings.set_difficulty(difficulty)
        self.difficulty = difficulty        
        self.background_color = settings.Background_Color_Game
        # Initialize the Board
        self.Board = Board()
        # start timer
        self.start_time = time.time()

    # Description: Render the game screen
    # Args: self
    # Returns: None
    # Notes: Draws the game board and elapsed time
    def on_draw(self):
        """Render the screen."""
        self.clear()
        # Draw the board
        board_x = (self.window.width - settings.Total_width_Board) // 2
        board_y = (self.window.height - settings.Total_height_Board) // 2
        elapsed_time = self.get_elapsed_time()
        self.Board.draw_board(board_x, board_y, elapsed_time)   


    # Description: Handle mouse press events
    # Args: self, x (int), y (int), button (int), modifiers (int)
    # Returns: None
    # Notes: Determines which cell was clicked and updates the board accordingly
    def on_mouse_press(self, x, y, button, modifiers):
        """Called when the user presses a mouse button."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Calculate board position
            board_x = (self.window.width - settings.Total_width_Board) // 2
            board_y = (self.window.height - settings.Total_height_Board) // 2
            
            # Convert pixel coordinates to grid coordinates
            col = int((x - board_x) // settings.Tile_Size)
            row = int((y - board_y) // settings.Tile_Size)
            
            # Check if click is within the game grid (not UI area)
            if (0 <= col < settings.Columns and 
                0 <= row < settings.Rows):
                print(f"Clicked cell ({row}, {col})")
                # Tell the board to reveal this cell and check result
                result = self.Board.reveal_cell(row, col, self.get_elapsed_time())
                self.game_result(result)    
            else:
                print("Clicked outside game area")
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            # calculate board position
            board_x = (self.window.width - settings.Total_width_Board) // 2
            board_y = (self.window.height - settings.Total_height_Board) // 2
            # Convert pixel coordinates to grid coordinates
            col = int((x - board_x) // settings.Tile_Size)
            row = int((y - board_y) // settings.Tile_Size)
            # Check if click is within the game grid (not UI area)
            if (0 <= col < settings.Columns and
                0 <= row < settings.Rows):
                print(f"Right-clicked cell ({row}, {col})")
                # Toggle flag on the cell
                self.Board.toggle_flag(row, col)

    # Description: Handle game result (win/loss)
    # Args: self, result (list or str) - The result of the last action ("mine_hit", ["You win!", "Time: X seconds"])
    # Returns: None
    # Notes: Shows the appropriate game over screen based on the result
    def game_result(self, result):
        """Handle game result (win/loss)"""
        if result == "mine_hit":
            # Game over - show loss screen
            from views.game_over_view import GameOverView
            game_over_view = GameOverView(won=False, elapsed_time=0)
            self.window.show_view(game_over_view)
        elif isinstance(result, list) and result[0] == "You win!":
            # Player has won - show win screen with elapsed time
            from views.game_over_view import GameOverView
            elapsed_time = self.get_elapsed_time()
            game_over_view = GameOverView(won=True, elapsed_time=elapsed_time)
            self.window.show_view(game_over_view)
        
    # Description: Handle ESC key presses
    # Args: self, key (int), modifiers (int)
    # Returns: None
    # Notes: Returns to the main menu when the ESC key is pressed
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if key == arcade.key.ESCAPE:
            # Return to menu
            from views.menu_view import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)


    # Description: Get elapsed time since the start of the game
    # Args: self
    # Returns: int - Elapsed time in seconds
    # Notes: Calculates the time difference between the current time and the start time
    def get_elapsed_time(self):
        """Get elapsed time since the start of the game in seconds."""
        return int(time.time() - self.start_time)