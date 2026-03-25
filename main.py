"""
Arcade MineSweeper Game
"""
# imports
import arcade
import settings
from views.menu_view import MenuView

# Constants
WINDOW_TITLE = "MineSweeper Arcade Game"

# Description: Main entry point for the MineSweeper game using Arcade library.
# Args: None
# Returns: None
# Notes: Initializes the game window and shows the main menu.
def main():
    """Main function"""
    # Create window and show main menu first
    window = arcade.Window(settings.Screen_Width, settings.Screen_Height, WINDOW_TITLE, resizable=True)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()