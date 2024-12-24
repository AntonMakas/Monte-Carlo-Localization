import pygame
import sys
from game import main

pygame.init()

WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monte Carlo Localization - Menu")

font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 48)

input_boxes = {
    "landmarks": {"rect": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 200, 200, 50), "text": "", "active": False},
    "motion_noise": {"rect": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50), "text": "", "active": False},
    "sensor_noise": {"rect": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50), "text": "", "active": False},
}
input_color_active = BLUE
input_color_inactive = GRAY

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, button_rect)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

def start_game():
    try:
        num_landmarks = int(input_boxes["landmarks"]["text"]) if input_boxes["landmarks"]["text"].isdigit() else 2
        motion_noise = float(input_boxes["motion_noise"]["text"]) if input_boxes["motion_noise"]["text"] else 5.0
        sensor_noise = float(input_boxes["sensor_noise"]["text"]) if input_boxes["sensor_noise"]["text"] else 10.5
        main(num_landmarks, motion_noise, sensor_noise)  # Pass inputs to the game
    except ValueError:
        pass

def quit_game():
    pygame.quit()
    sys.exit()

def menu():
    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Input box logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, box in input_boxes.items():
                    box["active"] = box["rect"].collidepoint(event.pos)
                for key, box in input_boxes.items():
                    box["color"] = input_color_active if box["active"] else input_color_inactive

            if event.type == pygame.KEYDOWN:
                for key, box in input_boxes.items():
                    if box["active"]:
                        if event.key == pygame.K_RETURN:
                            start_game()
                        elif event.key == pygame.K_BACKSPACE:
                            box["text"] = box["text"][:-1]
                        else:
                            box["text"] += event.unicode

        # Draw input boxes and labels
        for i, (key, box) in enumerate(input_boxes.items()):
            pygame.draw.rect(screen, input_color_active if box["active"] else input_color_inactive, box["rect"], border_radius=5)
            text_surface = input_font.render(box["text"], True, BLACK)
            screen.blit(text_surface, (box["rect"].x + 10, box["rect"].y + 10))
            box["rect"].w = max(200, text_surface.get_width() + 20)

        labels = [
            "Enter number of landmarks:",
            "Enter motion noise (float):",
            "Enter sensor noise (float):",
        ]
        for i, label in enumerate(labels):
            label_surface = font.render(label, True, BLACK)
            screen.blit(label_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 250 + i * 100))

        draw_button("Start Game", WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50, GRAY, BLUE, start_game)
        draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 250, 200, 50, GRAY, RED, quit_game)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu()
