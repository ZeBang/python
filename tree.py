import time
import random
import sys

# ---------- Color (ANSI) ----------
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
WHITE  = "\033[97m"
RESET  = "\033[0m"

USE_COLOR = True  # set False if your terminal shows weird symbols

def colorize(ch: str) -> str:
    if not USE_COLOR:
        return ch
    if ch == "^":   # star
        return YELLOW + ch + RESET
    if ch == "*":   # leaves
        return GREEN + ch + RESET
    if ch == "o":   # ornament
        return RED + ch + RESET
    if ch == "+":   # light
        return BLUE + ch + RESET
    if ch == "|":   # trunk
        return YELLOW + ch + RESET
    if ch in [".", "x"]:  # snow
        return WHITE + ch + RESET
    return ch

def clear_screen():
    # ANSI clear + move cursor to top-left (faster than os.system)
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

# ---------- Canvas / Tree params ----------
height = 12
rows = height + 6
cols = 2 * height + 12
snow_count = 60

# snowflakes: list of [x, y, char]
snowflakes = []
for _ in range(snow_count):
    x = random.randint(0, cols - 1)
    y = random.randint(0, rows - 1)
    ch = "." if random.random() < 0.7 else "x"
    snowflakes.append([x, y, ch])

def draw_tree_on(grid):
    cx = cols // 2

    # star
    sy = 1
    grid[sy][cx] = "^"

    # leaves
    top = 2
    for i in range(height):
        y = top + i
        half = i
        for x in range(cx - half, cx + half + 1):
            # decorations pattern (deterministic, stable)
            if (i + x) % 11 == 0:
                grid[y][x] = "o"
            elif (i + x) % 7 == 0:
                grid[y][x] = "+"
            else:
                grid[y][x] = "*"

    # trunk
    trunk_y = top + height
    for y in range(trunk_y, min(trunk_y + 3, rows - 1)):
        for x in range(cx - 1, cx + 2):
            grid[y][x] = "|"

def update_snowflakes():
    for flake in snowflakes:
        flake[1] += 1
        # slight drift
        if random.random() < 0.3:
            flake[0] += random.choice([-1, 0, 1])

        if flake[1] >= rows:
            flake[1] = 0
            flake[0] = random.randint(0, cols - 1)
            flake[2] = "." if random.random() < 0.7 else "x"

        # wrap x
        flake[0] %= cols

def draw_frame():
    # blank grid
    grid = [[" " for _ in range(cols)] for _ in range(rows)]

    # snow first (so tree can cover it)
    for x, y, ch in snowflakes:
        grid[y][x] = ch

    # tree on top
    draw_tree_on(grid)

    # render
    lines = []
    for r in grid:
        lines.append("".join(colorize(ch) for ch in r))
    return "\n".join(lines)

# ---------- Animation loop ----------
try:
    while True:
        clear_screen()
        print(draw_frame())
        print("\n" + RED + "Merry Christmas!" + RESET + "  🎄")
        update_snowflakes()
        time.sleep(0.12)
except KeyboardInterrupt:
    clear_screen()
    print("Stopped. Merry Christmas! 🎄")
