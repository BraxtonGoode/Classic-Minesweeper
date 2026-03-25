# game_over_view.py
# imports
import arcade
from views.menu_view import MenuView

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