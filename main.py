"""
Arcade MineSweeper Game
"""
import time
import arcade
import settings
from game.board import Board

# Constants
WINDOW_TITLE = "MineSweeper Arcade Game"


class MenuView(arcade.View):
    """Main menu screen with difficulty selection"""
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        
        # Button properties
        self.button_width = 200
        self.button_height = 60
        self.button_spacing = 20
        
        # Calculate button positions (we'll center them)
        center_x = self.window.width // 2
        start_y = self.window.height // 2 + 100
        
        # Button rectangles (Left, Bottom, Width, Height)
        self.easy_button = arcade.LBWH(center_x - self.button_width//2, start_y, self.button_width, self.button_height)
        self.normal_button = arcade.LBWH(center_x - self.button_width//2, start_y - (self.button_height + self.button_spacing), self.button_width, self.button_height)
        self.expert_button = arcade.LBWH(center_x - self.button_width//2, start_y - 2*(self.button_height + self.button_spacing), self.button_width, self.button_height)
        self.help_button = arcade.LBWH(center_x - self.button_width//2, start_y - 3*(self.button_height + self.button_spacing), self.button_width, self.button_height)
    
    def on_draw(self):
        """Render the menu screen"""
        self.clear()
        
        # Draw title
        arcade.draw_text("🎮 MINESWEEPER", 
                        self.window.width // 2, self.window.height - 100,
                        arcade.color.WHITE, font_size=50, anchor_x="center")
        
        # Draw buttons
        self.draw_button(self.easy_button, "EASY", arcade.color.GREEN)
        self.draw_button(self.normal_button, "NORMAL", arcade.color.YELLOW) 
        self.draw_button(self.expert_button, "EXPERT", arcade.color.RED)
        self.draw_button(self.help_button, "HELP", arcade.color.BLUE)
        
        # Draw difficulty info
        y_pos = 120
        arcade.draw_text("Easy: 10x10, 15 mines", self.window.width // 2, y_pos, 
                        arcade.color.WHITE, font_size=16, anchor_x="center")
        arcade.draw_text("Normal: 16x16, 30 mines", self.window.width // 2, y_pos - 25, 
                        arcade.color.WHITE, font_size=16, anchor_x="center")
        arcade.draw_text("Expert: 16x30, 99 mines", self.window.width // 2, y_pos - 50, 
                        arcade.color.WHITE, font_size=16, anchor_x="center")
    
    def draw_button(self, button_rect, text, color):
        """Draw a button with text"""
        # Draw button background
        arcade.draw_rect_filled(button_rect, color)
        
        # Draw button border  
        arcade.draw_rect_outline(button_rect, arcade.color.BLACK, 3)
        
        # Draw button text
        arcade.draw_text(text, button_rect.center_x, button_rect.center_y,
                        arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle menu button clicks"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.easy_button.point_in_rect((x, y)):
                self.start_game("EASY")
            elif self.normal_button.point_in_rect((x, y)):
                self.start_game("NORMAL")
            elif self.expert_button.point_in_rect((x, y)):
                self.start_game("EXPERT")
            elif self.help_button.point_in_rect((x, y)):
                self.show_help()
    
    def start_game(self, difficulty):
        """Start the game with selected difficulty"""
        game_view = GameView(difficulty)
        game_view.setup()
        self.window.show_view(game_view)
    
    def show_help(self):
        """Show help information"""
        print("🎯 HELP: Left-click to reveal cells. Avoid the mines!")
        print("💣 Numbers show how many mines are adjacent to that cell.")
        print("🏁 Goal: Reveal all safe cells without hitting any mines!")

class GameOverView(arcade.View):
    """Game over screen"""
    
    def __init__(self, won, elapsed_time=0):
        super().__init__()
        self.won = won
        self.elapsed_time = elapsed_time
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        """Render the game over screen"""
        self.clear()
        
        if self.won:
            message = "🎉 YOU WIN! 🎉"
            color = arcade.color.GREEN
            # Display completion time
            time_message = f"⏱️ Time: {self.elapsed_time} seconds"
        else:
            message = "💥 GAME OVER! 💥"
            color = arcade.color.RED
            time_message = ""
        
        arcade.draw_text(message, 
                        self.window.width // 2, self.window.height // 2,
                        color, font_size=50, anchor_x="center", anchor_y="center")
        
        # Show time for wins
        if self.won and self.elapsed_time > 0:
            arcade.draw_text(time_message, 
                            self.window.width // 2, self.window.height // 2 - 60,
                            arcade.color.YELLOW, font_size=30, anchor_x="center", anchor_y="center")
        
        arcade.draw_text("Press ESC to return to menu", 
                        self.window.width // 2, self.window.height // 2 - 100,
                        arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")
    
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if key == arcade.key.ESCAPE:
            # Return to menu
            menu_view = MenuView()
            self.window.show_view(menu_view)


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
                    game_over_view = GameOverView(won=False, elapsed_time=0)
                    self.window.show_view(game_over_view)
                elif isinstance(result, list) and result[0] == "You win!":
                    # Player has won - show win screen with elapsed time
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
            menu_view = MenuView()
            self.window.show_view(menu_view)
    def get_elapsed_time(self):
        """Get elapsed time since the start of the game in seconds."""
        return int(time.time() - self.start_time)



def main():
    """Main function"""
    # Create window and show menu first
    window = arcade.Window(settings.Screen_Width, settings.Screen_Height, WINDOW_TITLE, resizable=True)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()