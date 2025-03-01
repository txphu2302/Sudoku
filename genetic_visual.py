import pygame
import pygame_widgets
from pygame_widgets.button import Button
import sys
from genetic import genetic_algorithm

# Colors and dimensions
WIDTH, HEIGHT = 500, 675
GRID_SIZE = 9
INC = WIDTH // GRID_SIZE

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Genetic Algorithm Sudoku Solver")
a_font = pygame.font.SysFont("times", 30, "bold")

# Initial puzzle (easy mode)
grid = [
    [4, 1, 0, 2, 7, 0, 8, 0, 5],
    [0, 8, 5, 1, 4, 6, 0, 9, 7],
    [0, 7, 0, 5, 8, 0, 0, 4, 0],
    [9, 2, 7, 4, 5, 1, 3, 8, 6],
    [5, 3, 8, 6, 9, 7, 4, 1, 2],
    [1, 6, 4, 3, 2, 8, 7, 5, 9],
    [8, 5, 2, 7, 0, 4, 9, 0, 0],
    [0, 9, 0, 8, 0, 2, 5, 7, 4],
    [7, 4, 0, 9, 6, 5, 0, 2, 8],
]

# New: global mode variable (1: Easy, 2: Average, 3: Hard)
current_mode = 1

# New: Render mode instructions.
def draw_modes():
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    screen.blit(TitleFont.render("Game Settings", True, (0, 0, 0)), (15, 505))
    screen.blit(AttributeFont.render("C: Clear", True, (0, 0, 0)), (30, 530))
    screen.blit(TitleFont.render("Modes", True, (0, 0, 0)), (15, 555))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (30, 580))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (30, 605)) 
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (30, 630))

# Updated: set_grid_mode now updates current_mode.
def set_grid_mode(mode):
    global grid, current_mode
    current_mode = mode
    if mode == 0:  # Clear grid
        grid = [[0]*9 for _ in range(9)]
    elif mode == 1:  # Easy mode
        grid = [
            [4, 1, 0, 2, 7, 0, 8, 0, 5],
            [0, 8, 5, 1, 4, 6, 0, 9, 7],
            [0, 7, 0, 5, 8, 0, 0, 4, 0],
            [9, 2, 7, 4, 5, 1, 3, 8, 6],
            [5, 3, 8, 6, 9, 7, 4, 1, 2],
            [1, 6, 4, 3, 2, 8, 7, 5, 9],
            [8, 5, 2, 7, 0, 4, 9, 0, 0],
            [0, 9, 0, 8, 0, 2, 5, 7, 4],
            [7, 4, 0, 9, 6, 5, 0, 2, 8],
        ]
    elif mode == 2:  # Average mode
        grid = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7],
        ]
    elif mode == 3:  # Hard mode
        grid = [
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0],
        ]

def draw_grid(current_grid):
    # Clear screen
    screen.fill((255, 255, 255))
    # Draw sudoku cells and numbers
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = current_grid[i][j]
            if value != 0:
                pygame.draw.rect(screen, (204, 102, 153), (j * INC, i * INC, INC + 1, INC + 1))
                text = a_font.render(str(value), True, (0, 0, 0))
                screen.blit(text, (j * INC + 15, i * INC + 10))
    # Draw grid lines
    for i in range(GRID_SIZE + 1):
        width_line = 10 if i % 3 == 0 else 5
        pygame.draw.line(screen, (0, 0, 0), (0, i * INC), (WIDTH, i * INC), width_line)
        pygame.draw.line(screen, (0, 0, 0), (i * INC, 0), (i * INC, WIDTH), width_line)

def update_display():
    draw_grid(grid)
    draw_modes()
    pygame_widgets.update(pygame.event.get())
    pygame.display.update()

# New: Backtracking solver functions
def is_value_valid(m, i, j, val):
    # Check row and column
    for k in range(9):
        if m[i][k] == val or m[k][j] == val:
            return False
    # Check block
    bi, bj = 3 * (i // 3), 3 * (j // 3)
    for x in range(bi, bi+3):
        for y in range(bj, bj+3):
            if m[x][y] == val:
                return False
    return True

def update_grid(candidate):
    global grid
    grid = candidate
    update_display()
    pygame.time.delay(30)

def DisplayMessage(message, interval, color):
    # Render the message and pause for a given interval
    text = a_font.render(message, True, color)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(interval)
    update_display()

def solve_puzzle():
    global grid, current_mode
    solved = genetic_algorithm(grid, population_size=500, generations=1000, mutation_rate=0.05, display_callback=update_grid)
    if solved:
        grid = solved
        DisplayMessage("Successful", 2000, (0, 255, 0))

def main():
    global grid
    clock = pygame.time.Clock()
    # Create "Solve" button.
    solve_button = Button(
        screen, 350, 600, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=solve_puzzle
    )
    
    running = True
    while running:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            # New: Handle key events for mode selection.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    set_grid_mode(0)
                elif event.key == pygame.K_e:
                    set_grid_mode(1)
                elif event.key == pygame.K_a:
                    set_grid_mode(2)
                elif event.key == pygame.K_h:
                    set_grid_mode(3)
        update_display()
    pygame.quit()

if __name__ == '__main__':
    main()
