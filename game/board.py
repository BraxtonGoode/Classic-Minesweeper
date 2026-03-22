# board.py
# imports
import arcade
import settings
import random

# Board class
class Board:
    # This class is responsible for designing the game board
    # Initialization of the board
    def __init__(self):
        """Initialize the board with mines and covered cells."""
        # Create empty 2D array (all False = no mines initially)
        self.mines = [[False for _ in range(settings.Columns)] 
                      for _ in range(settings.Rows)]
        self.coverd = [[True for _ in range(settings.Columns)]
                        for _ in range(settings.Rows)]
        self.bomb_texture = arcade.load_texture("assets/images/Bomb_Image_32x32.png")
        self.flags = [[False for _ in range(settings.Columns)]
                      for _ in range(settings.Rows)]
        self.flag_texture = arcade.load_texture("assets/images/Red_flag_Image_32x32.png")
        
        # Place mines randomly
        self.generate_mines()


    def generate_mines(self):
        """Randomly place mines on the board."""
        mines_placed = 0
        while mines_placed < settings.Mines:
            row = random.randint(0, settings.Rows - 1)
            col = random.randint(0, settings.Columns - 1)
            if not self.mines[row][col]:
                self.mines[row][col] = True
                mines_placed += 1

    def reveal_cell(self, row, col, elapsed_time):
        """Reveal a specific cell by removing its cover. Returns game status."""
        # Check bounds first
        if not (0 <= row < settings.Rows and 
                0 <= col < settings.Columns):
            return "out_of_bounds"  # Out of bounds, do nothing
        
        # Prevent revealing flagged cells - just ignore the click
        if self.flags[row][col]:
            return "flagged"  # Do nothing, keep the flag
            
        if not self.coverd[row][col]:
            return "already_revealed"  # Already revealed, do nothing
        
        self.coverd[row][col] = False
        print(f"Revealed cell at ({row}, {col})")

        if self.mines[row][col]:
            print("Boom! Hit a mine!")
            return "mine_hit"  # Return game over status
            
        adjacent_count = self.count_adjacent_mines(row, col)
        if adjacent_count > 0:
            print(f"Cell ({row}, {col}) has {adjacent_count} adjacent mines.")
        else:
            print(f"Cell ({row}, {col}) has no adjacent mines.")
            directions = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1),          (0, 1),
                            (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions:
                self.reveal_cell(row + dr, col + dc, elapsed_time)

        if all(not self.coverd[r][c] or self.mines[r][c]
               for r in range(settings.Rows)
               for c in range(settings.Columns)):
            print("All safe cells revealed! You win!")
            win = ["You win!", f"Time: {elapsed_time} seconds"]
            return win
        
        return "safe"  # Return safe status





    def count_adjacent_mines(self, row, col):
        """Count the number of mines adjacent to the given cell."""
        count = 0
        for dr in [-1, 0, 1]:  # row offset
            for dc in [-1, 0, 1]:  # column offset  
                if dr == 0 and dc == 0:  # Skip center cell
                    continue
                
                # Calculate neighbor position
                neighbor_row = row + dr
                neighbor_col = col + dc
                
                # Check if neighbor is within bounds AND has a mine
                if (0 <= neighbor_row < settings.Rows and
                    0 <= neighbor_col < settings.Columns and
                    self.mines[neighbor_row][neighbor_col]):
                    count += 1
        
        return count

    # Draws the board grid and UI area
    def draw(self, board_x, board_y, elapsed_time):
        """Draw the game board at the specified position."""
        # Draw the board outline
        arcade.draw_lbwh_rectangle_outline(
            board_x,
            board_y,
            settings.Total_width_Board,
            settings.Total_height_Board,
            arcade.color.BLACK,
            2,
        )
        # seperating line between grid and UI area
        arcade.draw_line(
            board_x,
            board_y + settings.Rows * settings.Tile_Size,
            board_x + settings.Total_width_Board,
            board_y + settings.Rows * settings.Tile_Size,
            arcade.color.BLACK,
            2,
        )
        # Draw horizontal lines
        for row in range(1, settings.Rows):
            arcade.draw_line(
                board_x,
                board_y + row * settings.Tile_Size,
                board_x + settings.Total_width_Board,
                board_y + row * settings.Tile_Size,
                arcade.color.BLACK,
                2,
            )
        # Draw vertical lines
        for col in range(1, settings.Columns):
            arcade.draw_line(
                board_x + col * settings.Tile_Size,
                board_y,
                board_x + col * settings.Tile_Size,
                board_y + settings.Rows * settings.Tile_Size,
                arcade.color.BLACK,
                2,
            )
        # Draw Cell covers
        for row in range(settings.Rows):
            for col in range(settings.Columns):
                if self.coverd[row][col]:  # If the cell is covered
                    # Calculate the bottom-left corner of this cell
                    cell_x = board_x + (col * settings.Tile_Size)
                    cell_y = board_y + (row * settings.Tile_Size)
                    
                    # Draw gray cover
                    arcade.draw_lbwh_rectangle_filled(
                        cell_x + 2, cell_y + 2,  # Leave 2px border
                        settings.Tile_Size - 4, settings.Tile_Size - 4,  # 4px smaller total
                        arcade.color.DARK_GRAY
                    )
                else:  # Cell is revealed - show what's underneath
                    cell_x = board_x + (col * settings.Tile_Size)
                    cell_y = board_y + (row * settings.Tile_Size)
                    if self.mines[row][col]:
                        # Draw the bomb texture
                        rect = arcade.LBWH(
                            cell_x + 2, cell_y + 2,
                            settings.Tile_Size - 4, settings.Tile_Size - 4
                        )
                        arcade.draw_texture_rect(self.bomb_texture,rect)
                    else:
                        adjacent_count = self.count_adjacent_mines(row, col)
                        if adjacent_count > 0:
                            # Draw the number of adjacent mines
                            arcade.draw_text(
                                str(adjacent_count),
                                cell_x + settings.Tile_Size / 2,
                                cell_y + settings.Tile_Size / 2,
                                arcade.color.BLACK,
                                font_size=20,
                                anchor_x="center",
                                anchor_y="center"
                            )
                # added flag drawing
                if self.flags[row][col]:
                    cell_x = board_x + (col * settings.Tile_Size)
                    cell_y = board_y + (row * settings.Tile_Size)
                    # Draw a simple flag (red triangle)
                    # Draw the flag texture
                    rect = arcade.LBWH(
                        cell_x + 2, cell_y + 2,
                        settings.Tile_Size - 4, settings.Tile_Size - 4
                    )
                    arcade.draw_texture_rect(self.flag_texture,rect)
        # design UI area
        ui_y = board_y + settings.Rows * settings.Tile_Size

        flag_count = self.get_flag_count()
        arcade.draw_text(
            f"Flags: {flag_count} / {settings.Mines}",
            board_x + 10,
            ui_y + (settings.UI_Height // 2),
            arcade.color.BLACK,
            font_size=20,
            anchor_y="center"
        )
        # Timer (right side) - you'll need to pass this from GameView
        arcade.draw_text(f"⏱️ Time: {elapsed_time}s", 
                        board_x + settings.Total_width_Board - 150, ui_y + 10,
                        arcade.color.BLACK, font_size=18)


    def toggle_flag(self, row, col):
        """Toggle a flag on a specific cell."""
        if not (0 <= row < settings.Rows and 
                0 <= col < settings.Columns):
            return  # Out of bounds, do nothing
        if not self.coverd[row][col]:
            return  # Can't flag an already revealed cell
        
        self.flags[row][col] = not self.flags[row][col]
        if self.flags[row][col]:
            print(f"Flagged cell at ({row}, {col})")
        else:
            print(f"Unflagged cell at ({row}, {col})")
    def get_flag_count(self):
        """Return the total number of flags currently placed on the board."""
        flag_count = 0
        for row in range(settings.Rows):
            for col in range(settings.Columns):
                if self.flags[row][col]:
                    flag_count += 1
        return flag_count