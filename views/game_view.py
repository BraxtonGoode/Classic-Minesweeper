# game_view.py
# imports
import arcade
import settings
import time
from game.board import Board


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, difficulty="EXPERT", ):
        super().__init__()
        
        # Set difficulty using the proper settings function
        settings.set_difficulty(difficulty)
        self.difficulty = difficulty
        
        self.background_color = settings.Background_Color
        # Initialize the Board
        self.Board = Board()
        # start timer
        self.start_time = time.time()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Draw the board
        board_x = (self.window.width - settings.Total_width_Board) // 2
        board_y = (self.window.height - settings.Total_height_Board) // 2
        elapsed_time = self.get_elapsed_time()
        self.Board.draw(board_x, board_y, elapsed_time)   
        

    def on_mouse_press(self, x, y, button, modifiers):
        """Called when the user presses a mouse button."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Calculate board position (same calculation as in on_draw)
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
                               
                # Check if game is over
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
        
    
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if key == arcade.key.ESCAPE:
            # Return to menu
            from views.menu_view import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)
    def get_elapsed_time(self):
        """Get elapsed time since the start of the game in seconds."""
        return int(time.time() - self.start_time)