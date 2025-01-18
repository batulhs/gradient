import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 400
GRID_SIZE = 4
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
PADDING = 10

# Colors
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

BACKGROUND_COLOR = (187, 173, 160)
TEXT_COLOR = (119, 110, 101)

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("2048")
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.font = pygame.font.Font(None, 36)
        self.add_new_tile()
        self.add_new_tile()
        
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                x = j * CELL_SIZE + PADDING
                y = i * CELL_SIZE + PADDING
                width = CELL_SIZE - 2 * PADDING
                pygame.draw.rect(self.screen, COLORS.get(value, COLORS[0]), 
                               (x, y, width, width), border_radius=5)
                
                if value != 0:
                    text = self.font.render(str(value), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(x + width/2, y + width/2))
                    self.screen.blit(text, text_rect)
        
        pygame.display.flip()

    def move(self, direction):
        original_grid = self.grid.copy()

        if direction in ['LEFT', 'RIGHT']:
            for i in range(GRID_SIZE):
                row = list(self.grid[i])
                if direction == 'RIGHT':
                    row = row[::-1]
                
                # Remove zeros and compact the row
                row = [x for x in row if x != 0]
                
                # Merge similar numbers
                j = 0
                while j < len(row) - 1:
                    if row[j] == row[j + 1]:
                        row[j] *= 2
                        row.pop(j + 1)
                    j += 1
                
                # Add zeros to maintain grid size
                row.extend([0] * (GRID_SIZE - len(row)))
                
                if direction == 'RIGHT':
                    row = row[::-1]
                
                self.grid[i] = row

        elif direction in ['UP', 'DOWN']:
            for j in range(GRID_SIZE):
                col = list(self.grid[:, j])
                if direction == 'DOWN':
                    col = col[::-1]
                
                # Remove zeros and compact the column
                col = [x for x in col if x != 0]
                
                # Merge similar numbers
                i = 0
                while i < len(col) - 1:
                    if col[i] == col[i + 1]:
                        col[i] *= 2
                        col.pop(i + 1)
                    i += 1
                
                # Add zeros to maintain grid size
                col.extend([0] * (GRID_SIZE - len(col)))
                
                if direction == 'DOWN':
                    col = col[::-1]
                
                self.grid[:, j] = col

        if not np.array_equal(original_grid, self.grid):
            self.add_new_tile()

    def game_over(self):
        # Check if any moves are possible
        if 0 in self.grid:  # If there are empty cells
            return False
        
        # Check for possible merges horizontally and vertically
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE-1):
                if self.grid[i][j] == self.grid[i][j+1] or self.grid[j][i] == self.grid[j+1][i]:
                    return False
        return True

def main():
    game = Game2048()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move('LEFT')
                elif event.key == pygame.K_RIGHT:
                    game.move('RIGHT')
                elif event.key == pygame.K_UP:
                    game.move('UP')
                elif event.key == pygame.K_DOWN:
                    game.move('DOWN')
        
        game.draw()
        
        if game.game_over():
            print("Game Over!")
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
