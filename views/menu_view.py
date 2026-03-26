# menu_view.py
# Menu View for MineSweeper Game
# imports
import arcade
import settings


# Class Description: Main menu screen with difficulty selection
# Args: None
# Returns: None
# Notes: Handles the main menu interface and user interactions
class MenuView(arcade.View):
    """Main menu screen with difficulty selection"""
    # (*** Functions: __init__, get_button_positions, on_draw, draw_button, on_mouse_press, start_game***)

    # Description: Initialize the menu view
    # Args: self
    # Returns: None
    # Notes: Sets background color and button properties
    def __init__(self):
        super().__init__()
        arcade.set_background_color(settings.Background_Color_Menu)
        
        # Button properties
        self.button_width = 200
        self.button_height = 60
        self.button_spacing = 20



    
    # Description: Calculate button positions based on current window size
    # Args: self
    # Returns: tuple of arcade.LBWH objects representing button positions
    # Notes: Positions buttons centered horizontally and spaced vertically
    def get_button_positions(self):
        """Calculate button positions based on current window size"""
        center_x = self.window.width // 2
        start_y = self.window.height // 2 + 100
        
        # Define Button shape
        easy_button = arcade.LBWH(center_x - self.button_width//2, start_y, self.button_width, self.button_height)
        normal_button = arcade.LBWH(center_x - self.button_width//2, start_y - (self.button_height + self.button_spacing), self.button_width, self.button_height)
        expert_button = arcade.LBWH(center_x - self.button_width//2, start_y - 2*(self.button_height + self.button_spacing), self.button_width, self.button_height)
        
        
        return easy_button, normal_button, expert_button





    
    # Description: Render the menu screen
    # Args: self
    # Returns: None
    # Notes: Draws title and buttons
    def on_draw(self):
        """Render the menu screen"""
        self.clear()
        
        # Get current button positions
        easy_button, normal_button, expert_button = self.get_button_positions()
        
        # Draw title
        arcade.draw_text("🎮 MINESWEEPER", 
                        self.window.width // 2, self.window.height - 100,
                        arcade.color.WHITE, font_size=50, anchor_x="center")
        
        # Draw buttons
        self.draw_button(easy_button, "EASY", arcade.color.GREEN)
        self.draw_button(normal_button, "NORMAL", arcade.color.YELLOW) 
        self.draw_button(expert_button, "EXPERT", arcade.color.RED)
        
        # Draw difficulty info
        y_pos = 120
        arcade.draw_text("Easy: 10x10, 15 mines", self.window.width // 2, y_pos, 
                        arcade.color.WHITE, font_size=16, anchor_x="center")
        arcade.draw_text("Normal: 16x16, 30 mines", self.window.width // 2, y_pos - 25, 
                        arcade.color.WHITE, font_size=16, anchor_x="center")
        arcade.draw_text("Expert: 20x20, 40 mines", self.window.width // 2, y_pos - 50, 
                        arcade.color.WHITE, font_size=16, anchor_x="center")




    
    # Description: Draw a button with text
    # Args: self, button_rect (arcade.LBWH), text (str), color (arcade.Color)
    # Returns: None
    # Notes: Draws a filled rectangle with a border and centered text
    def draw_button(self, button_rect, text, color):
        """Draw a button with text"""
        # Draw button background
        arcade.draw_rect_filled(button_rect, color)
        
        # Draw button border  
        arcade.draw_rect_outline(button_rect, arcade.color.BLACK, 3)
        
        # Draw button text
        arcade.draw_text(text, button_rect.center_x, button_rect.center_y,
                        arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
    
    # Description: Handle mouse press events on the menu
    # Args: self, x (int), y (int), button (int), modifiers (int)
    # Returns: None
    # Notes: Detects clicks on difficulty buttons and starts the game
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle menu button clicks"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Get current button positions
            easy_button, normal_button, expert_button = self.get_button_positions()

            # Check which button was clicked
            if easy_button.point_in_rect((x, y)):
                self.start_game("EASY")
            elif normal_button.point_in_rect((x, y)):
                self.start_game("NORMAL")
            elif expert_button.point_in_rect((x, y)):
                self.start_game("EXPERT")

    # Description: Start the game with selected difficulty
    # Args: self, difficulty (str)
    # Returns: None
    # Notes: Switches to GameView with chosen difficulty
    def start_game(self, difficulty):
        """Start the game with selected difficulty"""
        from views.game_view import GameView
        game_view = GameView(difficulty)
        self.window.show_view(game_view)
