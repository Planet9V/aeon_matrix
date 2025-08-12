import pygame
import sys
import random
import math

# --- Configuration ---
# Screen settings
WIDTH, HEIGHT = 1920, 1080
FPS = 30

# --- THEMES ---
# Select a theme: "Matrix", "Cyberpunk", "Monochrome", "Rainbow"
COLOR_MODE = "Matrix"

THEMES = {
    "Matrix": {
        "BACKGROUND": (0, 0, 0),
        "FONT_COLOR": (0, 255, 70),
        "HEAD_COLOR": (200, 255, 220)
    },
    "Cyberpunk": {
        "BACKGROUND": (25, 25, 112), # Midnight Blue
        "FONT_COLOR": (255, 105, 180), # Hot Pink
        "HEAD_COLOR": (0, 255, 255)   # Aqua
    },
    "Monochrome": {
        "BACKGROUND": (0, 0, 0),
        "FONT_COLOR": (150, 150, 150), # Gray
        "HEAD_COLOR": (255, 255, 255)   # White
    },
    "Rainbow": { # Special mode, handled in code
        "BACKGROUND": (0, 0, 0)
    }
}

# Set colors based on selected theme
BACKGROUND_COLOR = THEMES[COLOR_MODE]["BACKGROUND"]
FONT_COLOR = THEMES[COLOR_MODE].get("FONT_COLOR") # .get() for rainbow
HEAD_COLOR = THEMES[COLOR_MODE].get("HEAD_COLOR")

# Font settings
FONT_SIZE = 20

# Animation settings
MIN_SPEED = 2
MAX_SPEED = 10
MIN_STREAM_LENGTH = 10
MAX_STREAM_LENGTH = 30

# --- CHARACTER SETS ---
# Select a character set: "Katakana", "Binary", "Hex"
CHARACTER_SET_MODE = "Katakana"

CHARACTER_SETS = {
    "Katakana": "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズヅブプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789",
    "Binary": "01",
    "Hex": "0123456789ABCDEF"
}

CHARACTERS = CHARACTER_SETS[CHARACTER_SET_MODE]


# Glitch Effects
GLITCH_CHANCE = 0.01  # Chance for a character to flash
GLITCH_COLOR = (255, 255, 255) # White
SPEED_BURST_CHANCE = 0.005 # Chance for a stream to have a speed burst

# Wind Drift
WIND_ENABLED = True
WIND_STRENGTH = 5  # How far the streams drift
WIND_FREQUENCY = 0.01 # How fast the streams sway

# Mouse Ripple
MOUSE_RIPPLE_ENABLED = True
MOUSE_RIPPLE_RADIUS = 100 # The radius of the ripple effect
MOUSE_RIPPLE_BRIGHTNESS = 100 # How much brighter the streams get

class Stream:
    def __init__(self, x, y):
        self.original_x = x
        self.x = x
        self.y = y
        self.speed = random.uniform(MIN_SPEED, MAX_SPEED)
        self.symbols = []
        self.total_symbols = random.randint(MIN_STREAM_LENGTH, MAX_STREAM_LENGTH)
        self.is_active = True

        # Handle Rainbow mode
        if COLOR_MODE == "Rainbow":
            self.font_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.head_color = (min(self.font_color[0] + 100, 255), min(self.font_color[1] + 100, 255), min(self.font_color[2] + 100, 255))
        else:
            self.font_color = FONT_COLOR
            self.head_color = HEAD_COLOR


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

    def update_and_draw(self, screen, font, time, mouse_pos):
        # Wind drift
        if WIND_ENABLED:
            self.x = self.original_x + math.sin(time * WIND_FREQUENCY + self.original_x) * WIND_STRENGTH

        # Speed burst glitch
        if random.random() < SPEED_BURST_CHANCE:
            self.y += random.randint(50, 150)
        else:
            self.y += self.speed

        if self.y > HEIGHT + self.total_symbols * FONT_SIZE:
            self.is_active = False

        for i, symbol in enumerate(self.symbols):
            symbol['pos'][0] = self.x
            symbol['pos'][1] = self.y - i * FONT_SIZE

            if 0 < symbol['pos'][1] < HEIGHT:
                # Base color
                color = self.head_color if symbol['first'] else self.font_color

                # Mouse ripple effect
                if MOUSE_RIPPLE_ENABLED and mouse_pos:
                    distance = abs(self.x - mouse_pos[0])
                    if distance < MOUSE_RIPPLE_RADIUS:
                        # Calculate brightness factor (1.0 at center, 0.0 at edge)
                        brightness_factor = (MOUSE_RIPPLE_RADIUS - distance) / MOUSE_RIPPLE_RADIUS
                        brighten_amount = int(MOUSE_RIPPLE_BRIGHTNESS * brightness_factor)

                        # Apply brightness
                        color = (
                            min(color[0] + brighten_amount, 255),
                            min(color[1] + brighten_amount, 255),
                            min(color[2] + brighten_amount, 255)
                        )

                # Character flash glitch (overrides other effects)
                if random.random() < GLITCH_CHANCE:
                    color = GLITCH_COLOR

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

    time = 0
    running = True
    while running:
        for event in pygame.event.get():
            # Any key press or mouse movement will exit the screensaver
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
                running = False

        mouse_pos = pygame.mouse.get_pos() if MOUSE_RIPPLE_ENABLED else None

        screen.fill(BACKGROUND_COLOR)

        for stream in streams:
            stream.update_and_draw(screen, font, time, mouse_pos)
            if not stream.is_active:
                stream.is_active = True
                stream.generate_symbols(random.uniform(-1000, 0))

        pygame.display.flip()
        clock.tick(FPS)
        time += 1

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower().strip() == "/s":
            run_screensaver()
    else:
        run_screensaver()
