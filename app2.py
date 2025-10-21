import pygame
import random

# Define constants for the game grid and display
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Colors (R, G, B)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0),    # Z
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0
        self.color = random.choice(COLORS)

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)


def create_grid(locked):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (j, i), color in locked.items():
        if i >= 0:
            grid[i][j] = color
    return grid


def convert_shape_format(piece):
    positions = []
    format = piece.image()
    for i, row in enumerate(format):
        for j, val in enumerate(row):
            if val:
                positions.append((piece.x + j, piece.y + i))
    return positions


def valid_space(piece, grid):
    accepted = [[(j, i) for j in range(COLS) if grid[i][j] == BLACK] for i in range(ROWS)]
    accepted = [j for sub in accepted for j in sub]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    return any(y < 1 for (x, y) in positions)


def clear_rows(grid, locked):
    cleared = 0
    for i in range(ROWS - 1, -1, -1):
        if BLACK not in grid[i]:
            cleared += 1
            del_row = i
            for j in range(COLS):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue
    if cleared > 0:
        # shift rows down
        for key in sorted(list(locked), key=lambda x: x[1])[
            ::-1]:
            x, y = key
            if y < del_row:
                color = locked.pop(key)
                locked[(x, y + cleared)] = color
    return cleared


def get_shape():
    shape = random.choice(SHAPES)
    # Convert shape layout into rotations
    rotations = []
    for _ in range(4):
        rotations.append(shape)
        shape = [list(row) for row in zip(*shape[::-1])]
    return rotations


def draw_grid(surface, grid):
    for i in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        for j in range(COLS):
            pygame.draw.line(surface, GRAY, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))
            pygame.draw.rect(surface, grid[i][j], (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_window(surface, grid, score=0):
    surface.fill(BLACK)
    draw_grid(surface, grid)
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', True, (255,255,255))
    surface.blit(label, (10, 10))


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Piece(COLS//2 - 2, 0, get_shape())
    next_piece = Piece(COLS//2 - 2, 0, get_shape())
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = Piece(COLS//2 - 2, 0, get_shape())
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
            if check_lost(locked_positions):
                run = False

        draw_window(win, grid, score)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
