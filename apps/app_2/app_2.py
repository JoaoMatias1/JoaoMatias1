import pygame
import math
import sys
from datetime import datetime

def run(screen):
    # Adjusted for 480x320 resolution
    CLOCK_RADIUS = 140
    CENTER = (screen.get_width() // 2, screen.get_height() // 2)
    DATE_POS = (CENTER[0], CENTER[1] + 80)  # Position for the date, slightly below center
    BACK_BUTTON_POS = (40, 40)  # Position for the back button
    BACK_BUTTON_RADIUS = 20  # Radius for the back button

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Hand thickness and lengths adjusted
    HAND_THICKNESS = {'hour': 8, 'minute': 5, 'second': 3}
    HAND_LENGTH = {'hour': 60, 'minute': 90, 'second': 110}

    # Font sizes adjusted
    FONT_SIZE = 24
    DATE_FONT_SIZE = 20
    font = pygame.font.Font(None, FONT_SIZE)
    date_font = pygame.font.Font(None, DATE_FONT_SIZE)

    # Load back button and background images
    back_button_image_path = './apps/app_2/back.png'
    back_button_image = pygame.image.load(back_button_image_path)
    back_button_image = pygame.transform.scale(back_button_image, (2 * BACK_BUTTON_RADIUS, 2 * BACK_BUTTON_RADIUS))

    background_image_path = './apps/app_2/background.jpg'
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    def draw_hand(angle, length, thickness, color):
        angle = math.radians(450 - angle)
        end_x = CENTER[0] + length * math.cos(angle)
        end_y = CENTER[1] - length * math.sin(angle)
        pygame.draw.line(screen, color, CENTER, (int(end_x), int(end_y)), thickness)

    def draw_clock_numbers_and_dots():
        for num in range(1, 13):
            angle = math.radians(450 - (num * 30))
            x = CENTER[0] + (CLOCK_RADIUS - 20) * math.cos(angle)
            y = CENTER[1] - (CLOCK_RADIUS - 20) * math.sin(angle)
            if num in [12, 3, 6, 9]:
                text = font.render(str(num), True, WHITE)
                text_rect = text.get_rect(center=(int(x), int(y)))
                screen.blit(text, text_rect)
            else:
                pygame.draw.circle(screen, WHITE, (int(x), int(y)), 3)

    def draw_date():
        today = datetime.now()
        date_str = today.strftime("%A, %B %d")  # E.g., "Monday, April 22"
        text = date_font.render(date_str, True, WHITE)
        text_rect = text.get_rect(center=DATE_POS)
        screen.blit(text, text_rect)

    def draw_back_button():
        top_left = (BACK_BUTTON_POS[0] - BACK_BUTTON_RADIUS, BACK_BUTTON_POS[1] - BACK_BUTTON_RADIUS)
        screen.blit(back_button_image, top_left)

    def draw_clock():
        screen.blit(background_image, (0, 0))
        pygame.draw.circle(screen, WHITE, CENTER, CLOCK_RADIUS, 2)
        pygame.draw.circle(screen, WHITE, CENTER, 4)

        now = datetime.now()
        hour_angle = (now.hour % 12) / 12 * 360 + (now.minute / 60) * 30
        minute_angle = now.minute / 60 * 360 + now.second / 60 * 6
        second_angle = now.second / 60 * 360

        draw_hand(hour_angle, HAND_LENGTH['hour'], HAND_THICKNESS['hour'], WHITE)
        draw_hand(minute_angle, HAND_LENGTH['minute'], HAND_THICKNESS['minute'], WHITE)
        draw_hand(second_angle, HAND_LENGTH['second'], HAND_THICKNESS['second'], RED)
        draw_clock_numbers_and_dots()
        draw_date()
        draw_back_button()

        pygame.display.flip()

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if math.hypot(event.pos[0] - BACK_BUTTON_POS[0], event.pos[1] - BACK_BUTTON_POS[1]) <= BACK_BUTTON_RADIUS:
                    return  # Return to the home screen if back button is clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Return to the home screen on ESC key

        draw_clock()
        clock.tick(60)

# Main entry point
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("Clock App")
    run(screen)