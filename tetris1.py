import curses
import random
import time
 
# Tetromino shapes
TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}
 
# Rotate clockwise
def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]
 
# Game constants
WIDTH, HEIGHT = 10, 20
TICK = 0.5  # Initial drop speed in seconds
 
def draw_board(stdscr, board, score, level):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Score: {score}  Level: {level}")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if board[y][x]:
                stdscr.addstr(y + 1, x * 2, "[]")
            else:
                stdscr.addstr(y + 1, x * 2, "  ")
    stdscr.border()
    stdscr.refresh()
 
def collision(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= WIDTH:
                    return True
                if y + off_y >= HEIGHT:
                    return True
                if board[y + off_y][x + off_x]:
                    return True
    return False
 
def merge(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + off_y][x + off_x] = 1
 
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = HEIGHT - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [0 for _ in range(WIDTH)])
    return new_board, cleared
 
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(50)
 
    board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    current = random.choice(list(TETROMINOS.values()))
    current_pos = [WIDTH // 2 - len(current[0]) // 2, 0]
    score = 0
    level = 1
    lines_cleared = 0
    last_tick = time.time()
 
    while True:
        now = time.time()
        key = stdscr.getch()
 
        dx = 0
        rotate_flag = False
        quit_flag = False
 
        if key == curses.KEY_LEFT:
            dx = -1
        elif key == curses.KEY_RIGHT:
            dx = 1
        elif key == ord('z'):
            rotate_flag = True
        elif key == ord('q'):
            quit_flag = True
 
        if quit_flag:
            break
 
        new_pos = [current_pos[0] + dx, current_pos[1]]
        if not collision(board, current, new_pos):
            current_pos = new_pos
 
        if rotate_flag:
            rotated = rotate(current)
            if not collision(board, rotated, current_pos):
                current = rotated
 
        if now - last_tick > max(0.1, TICK - level * 0.05):
            last_tick = now
            new_pos = [current_pos[0], current_pos[1] + 1]
            if not collision(board, current, new_pos):
                current_pos = new_pos
            else:
                merge(board, current, current_pos)
                board, cleared = clear_lines(board)
                score += cleared * 100
                lines_cleared += cleared
                level = lines_cleared // 10 + 1
                current = random.choice(list(TETROMINOS.values()))
                current_pos = [WIDTH // 2 - len(current[0]) // 2, 0]
                if collision(board, current, current_pos):
                    draw_board(stdscr, board, score, level)
                    stdscr.addstr(HEIGHT // 2, WIDTH, " GAME OVER ")
                    stdscr.refresh()
                    stdscr.nodelay(False)
                    stdscr.getch()
                    break
 
        temp_board = [row[:] for row in board]
        for y, row in enumerate(current):
            for x, cell in enumerate(row):
                if cell:
                    temp_board[y + current_pos[1]][x + current_pos[0]] = 1
        draw_board(stdscr, temp_board, score, level)
 
curses.wrapper(main)
