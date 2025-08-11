import pygame
import sys
import random

# --- Configuration ---
# Screen settings
WIDTH, HEIGHT = 1920, 1080
FPS = 30

# Colors
BACKGROUND_COLOR = (0, 0, 0)      # Black
FONT_COLOR = (0, 255, 70)          # Green
HEAD_COLOR = (200, 255, 220)       # Light green for the first character

# Font settings
FONT_SIZE = 20

# Animation settings
MIN_SPEED = 2
MAX_SPEED = 10
MIN_STREAM_LENGTH = 10
MAX_STREAM_LENGTH = 30

# Characters to use in the animation (Katakana, numbers, symbols)
CHARACTERS = "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズヅブプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789"

class Stream:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(MIN_SPEED, MAX_SPEED)
        self.symbols = []
        self.total_symbols = random.randint(MIN_STREAM_LENGTH, MAX_STREAM_LENGTH)
        self.is_active = True

    def generate_symbols(self, y):
        self.y = y
        self.symbols = []
        for i in range(self.total_symbols):
            symbol = {
                'char': random.choice(CHARACTERS),
                'pos': [self.x, y - i * FONT_SIZE],
                'first': i == 0
            }
            self.symbols.append(symbol)

    def update_and_draw(self, screen, font):
        self.y += self.speed
        if self.y > HEIGHT + self.total_symbols * FONT_SIZE:
            self.is_active = False

        for i, symbol in enumerate(self.symbols):
            symbol['pos'][1] = self.y - i * FONT_SIZE

            if 0 < symbol['pos'][1] < HEIGHT:
                color = HEAD_COLOR if symbol['first'] else FONT_COLOR
                text_surface = font.render(symbol['char'], True, color)
                screen.blit(text_surface, symbol['pos'])

            # Randomly change characters
            if random.random() > 0.98:
                symbol['char'] = random.choice(CHARACTERS)


def run_screensaver():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Matrix Screensaver")
    clock = pygame.time.Clock()

    pygame.mouse.set_visible(False)

    try:
        font = pygame.font.Font(None, FONT_SIZE)
    except pygame.error:
        font = pygame.font.SysFont('arial', FONT_SIZE)


    streams = [Stream(x, random.uniform(-1000, 0)) for x in range(0, WIDTH, FONT_SIZE)]
    for stream in streams:
        stream.generate_symbols(stream.y)

    running = True
    while running:
        for event in pygame.event.get():
            # Any key press or mouse movement will exit the screensaver
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for stream in streams:
            stream.update_and_draw(screen, font)
            if not stream.is_active:
                stream.is_active = True
                stream.generate_symbols(random.uniform(-1000, 0))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Windows screensavers are called with command-line arguments.
    # /s: Run the screensaver.
    # /p <HWND>: Show a preview of the screensaver.
    # /c: Show the configuration dialog.

    # We only implement the /s (run) mode.
    # No arguments or /s will run the screensaver.
    # Other arguments will do nothing.

    if len(sys.argv) > 1:
        if sys.argv[1].lower().strip() == "/s":
            run_screensaver()
    else:
        run_screensaver()
