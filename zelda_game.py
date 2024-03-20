import pygame
import sys
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Zelda-like Game")

# Load character image
character_image = pygame.image.load("character.png")
character_rect = character_image.get_rect()
character_rect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)

# Load enemy image
enemy_image = pygame.image.load("enemy.png")
enemy_rect = enemy_image.get_rect()
enemy_rect.center = (random.randint(0, WINDOW_SIZE[0]), random.randint(0, WINDOW_SIZE[1]))

# Load music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop the music indefinitely

clock = pygame.time.Clock()

# Define the world
class Area:
    def __init__(self, name, description, exits=None):
        self.name = name
        self.description = description
        self.exits = exits if exits else {}

# Define the areas
areas = {
    "cave": Area("Cave", "You are in a dark cave.", {"east": "forest"}),
    "forest": Area("Forest", "You are in a forest. You can hear birds chirping.", {"west": "cave", "south": "field"}),
    "field": Area("Field", "You are in an open field with tall grass.", {"north": "forest", "east": "courtyard"}),
    "courtyard": Area("Courtyard", "You are in a castle courtyard. It's deserted.", {"west": "field"})
}

# Set starting area
current_area = areas["cave"]

# Define the Enemy class
class Enemy:
    def __init__(self, image, speed):
        self.image = image
        self.rect = image.get_rect()
        self.speed = speed

    def move_towards(self, target_rect):
        dx = target_rect.x - self.rect.x
        dy = target_rect.y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            dx = dx / dist
            dy = dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

# Create the enemy with a higher speed
enemy = Enemy(enemy_image, speed=4)


# Variable to track player's health
player_health = 100

# Variable to track whether the character is being attacked
attacked = False

# Variable to track game over state
game_over = False

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            character_rect.x += 5
        if keys[pygame.K_UP]:
            character_rect.y -= 5
        if keys[pygame.K_DOWN]:
            character_rect.y += 5

        # Move the enemy towards the player
        enemy.move_towards(character_rect)

        # Clear the screen
        screen.fill(WHITE)

        # Display the current area description
        font = pygame.font.Font(None, 36)
        text = font.render(current_area.description, True, WHITE)
        screen.blit(text, (20, 20))

        # Draw the character and enemy
        screen.blit(character_image, character_rect)
        screen.blit(enemy.image, enemy.rect)

        # Draw the enemy title above the enemy
        enemy_title = font.render("Enemy", True, RED)
        enemy_title_rect = enemy_title.get_rect(midtop=(enemy.rect.centerx, enemy.rect.top - 10))
        screen.blit(enemy_title, enemy_title_rect)

        # Check for collision with the enemy
        if character_rect.colliderect(enemy.rect):
            # If the player collides with the enemy, decrease player's health
            player_health -= 10
            attacked = True
            if player_health <= 0:
                game_over = True
        else:
            attacked = False

        # If the character is being attacked, display "help"
        if attacked:
            help_text = font.render("Help!", True, RED)
            screen.blit(help_text, (character_rect.centerx - 20, character_rect.centery - 50))

        # Draw player health
        health_text = font.render(f"Health: {player_health}", True, RED)
        screen.blit(health_text, (20, WINDOW_SIZE[1] - 40))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

# Game over screen
screen.fill(BLACK)
game_over_font = pygame.font.Font(None, 64)
game_over_text = game_over_font.render("Game Over - You Lose", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
screen.blit(game_over_text, game_over_rect)
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

pygame.quit()
sys.exit()
