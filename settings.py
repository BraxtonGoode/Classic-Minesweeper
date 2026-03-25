# settings.py
# The main settings file for MineSweeper Game

# imports
import arcade

"""
    Main Design Settings for MineSweeper Game

"""

# Background color
Background_Color_Game = arcade.csscolor.LIGHT_GRAY
Background_Color_Menu = arcade.csscolor.DARK_BLUE

# Difficulty settings
DIFFICULTIES = {
    "EASY": {
        "rows": 10,
        "columns": 10,
        "mines": 15,
        "ui_height": 45
    },
    "NORMAL": {
        "rows": 16, 
        "columns": 16,
        "mines": 30,
        "ui_height": 45
    },
    "EXPERT": {
        "rows": 20,
        "columns": 20,  
        "mines": 40,
        "ui_height": 45
    }
}

# Starting/default difficulty (used only for initial setup)
STARTING_DIFFICULTY = "EXPERT"
SELECTED_DIFFICULTY = STARTING_DIFFICULTY  

# Constants for the game settings - initialize with starting values
Rows = DIFFICULTIES[STARTING_DIFFICULTY]["rows"]
Columns = DIFFICULTIES[STARTING_DIFFICULTY]["columns"]
Mines = DIFFICULTIES[STARTING_DIFFICULTY]["mines"]
UI_Height = DIFFICULTIES[STARTING_DIFFICULTY]["ui_height"]


# Description: Update the selected difficulty and recalculate all derived settings
# Args: difficulty (str) - New difficulty level ("EASY", "NORMAL", "EXPERT")
# Returns: None
# Notes: Modifies global settings based on selected difficulty
def set_difficulty(difficulty):
    """Update the selected difficulty and recalculate all derived settings"""
    global SELECTED_DIFFICULTY, Rows, Columns, Mines, UI_Height
    global Total_width_Board, Total_height_Board, Screen_Width, Screen_Height
    
    SELECTED_DIFFICULTY = difficulty
    
    # Recalculate all settings based on new difficulty
    Rows = DIFFICULTIES[SELECTED_DIFFICULTY]["rows"]
    Columns = DIFFICULTIES[SELECTED_DIFFICULTY]["columns"]
    Mines = DIFFICULTIES[SELECTED_DIFFICULTY]["mines"]
    UI_Height = DIFFICULTIES[SELECTED_DIFFICULTY]["ui_height"]
    
    # Recalculate derived settings
    Total_width_Board = Columns * Tile_Size
    Total_height_Board = (Rows * Tile_Size) + UI_Height
    Screen_Width = Total_width_Board + 100
    Screen_Height = Total_height_Board + 100



# Dimensions for tiles and total board size
Tile_Size = 36
Total_width_Board = Columns * Tile_Size
Total_height_Board = (Rows * Tile_Size) + UI_Height

# Screen dimensions
Screen_Width = Total_width_Board + 100
Screen_Height = Total_height_Board + 100

# Dimensions for Menu
Menu_Height = 300
Menu_Width = 400