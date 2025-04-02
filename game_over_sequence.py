"""Functions associated with what happens after the game ends"""
__version__ = '04/02/2025'
__author__ = 'Kayla Cao'

import pygame
from HighScore import HighScore
from config import *
from sounds import *


def draw_text(screen, text, font, color, center_pos):
    """Helper function to draw text with proper rendering"""
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=center_pos)
    screen.blit(text_surf, text_rect)
    return text_rect

def game_over_screen(screen, font, score, level_completed, high_score):
    """Displays game over screen with statistics."""

    # Create a surface to draw on
    screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_surface.fill((0, 0, 0))  # Black background

    # Game Over text
    game_over_font = pygame.font.Font(None, 100)
    if level_completed >= 3:
        game_over_text = game_over_font.render('YOU FINISHED', True, (255, 0, 0))
    else:
        game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
    screen_surface.blit(game_over_text, game_over_rect)

    # Detailed stats font
    stats_font = pygame.font.Font(None, 50)

    # Score text
    score_text = stats_font.render(f'Final Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen_surface.blit(score_text, score_rect)

    # Level completed text
    level_text = stats_font.render(f'Levels Completed: {level_completed}', True, (255, 255, 255))
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen_surface.blit(level_text, level_rect)

    # High score comparison
    if score > high_score:
        high_score_text = stats_font.render(f'NEW HIGH SCORE! Previous: {high_score}', True, (0, 255, 0))
    else:
        high_score_text = stats_font.render(f'High Score: {high_score}', True, (255, 255, 255))

    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen_surface.blit(high_score_text, high_score_rect)

    # Instructions
    instruction_font = pygame.font.Font(None, 40)
    enter_text = instruction_font.render('Press ENTER to save score', True, (0, 255, 0))
    esc_text = instruction_font.render('Press ESC to skip', True, (255, 0, 0))

    enter_rect = enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    esc_rect = esc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

    screen_surface.blit(enter_text, enter_rect)
    screen_surface.blit(esc_text, esc_rect)

    screen.blit(screen_surface, (0, 0))
    pygame.display.flip()

def user_input(screen, font, score, scores, level_completed, high_score):
    """Handle user input for name entry"""
    user = ""
    clock = pygame.time.Clock()

    # Create a persistent surface
    input_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    input_surface.fill((0, 0, 0))

    # Render static elements
    game_over_screen(screen, font, score, level_completed, high_score)

    sound_manager = SoundManager()
    if level_completed >= 3:
        sound_manager.play_game_won()
    else:
        sound_manager.play_game_lost()

    while True:
        clock.tick(10)  # Limit frame rate

        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user:
                    try:
                        scores.append(HighScore(user, score))
                        scores.sort(reverse=True)
                        with open('scores.txt', 'w') as f:
                            f.write('\n'.join(str(s) for s in scores))
                        return user
                    except Exception as e:
                        print(f"Error saving score: {e}")
                        return None
                elif event.key == pygame.K_BACKSPACE and user:
                    user = user[:-1]
                elif len(user) < 3 and event.unicode.isalpha():
                    user += event.unicode.upper()

        # Name entry text
        name_font = pygame.font.Font(None, 50)
        name_text = name_font.render(f'Enter 3 letters: {user}', True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

        # Recreate the surface to avoid flickering
        screen.blit(input_surface, (0, 0))
        game_over_screen(screen, font, score, level_completed, high_score)
        screen.blit(name_text, name_rect)

        pygame.display.flip()

def highscores_screen(screen, font, score, scores):
    """Display high scores screen"""
    smaller_font = pygame.font.Font(None, 50)

    while True:
        screen.fill((0, 0, 0))
        # Title
        draw_text(screen, 'HIGH SCORES', font, (255, 255, 0),
                  (SCREEN_WIDTH // 2, 100))

        # High scores with increased spacing
        for i, highscore in enumerate(scores[:5]):
            color = (255, 255, 0) if highscore.score == score else (255, 255, 255)
            draw_text(screen, f"{i + 1}. {str(highscore)}", smaller_font,
                      color, (SCREEN_WIDTH // 2, 200 + (i * 70)))

        # Exit instruction
        draw_text(screen, 'Press ESC to exit', smaller_font, (255, 0, 0),
                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return True