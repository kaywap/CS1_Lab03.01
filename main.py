"""Very Fun Platformer Game - Players must navigate platforms, avoid enemies, collect gold, and finish as fast as possible to maximize their score."""
__version__ = '04/02/2025'
__author__ = 'Kayla Cao'

#my flint sessions:
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/8340eb75-2369-4bc4-8d51-840fae452640
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/e77caa16-99e2-4454-bde9-cb1849f0afa1
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/282cf138-fa4a-4cf7-bc3c-827c162eff97
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/67720e26-1e5f-44d9-872b-8356aa962f62
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/ed75331f-f465-4c72-a1ec-321ee4fa665e
# https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/edf741da-42b4-4ad0-910e-b6e65b43c061

import pygame
from player import *
from levels import *
from config import *
from HighScore import *
from game_over_sequence import *
from sounds import *

def load_scores():
    """Loads high scores from file, creates file if it doesn't exist"""
    try:
        with open("scores.txt", "r") as f:
            scores = []
            for line in f:
                temp = line.split()
                if len(temp) >= 2:  # Make sure we have both initials and score
                    scores.append(HighScore(temp[0], int(temp[1])))
        scores.sort(reverse=True)
        return scores[:5]  # Limit to top 5 scores
    except FileNotFoundError:
        with open("scores.txt", "w") as f:
            pass
        return []

def draw_game_info(screen, player, current_level_no, font, high_score):
    """Renders game information on the screen during the game"""

    # High score display
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(high_score_text, (10, 10))

    # Level display
    level_text = font.render(f"Level: {current_level_no + 1}", True, (255, 255, 255))
    screen.blit(level_text, (10, 40))

    # Lives display
    lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 70))

    # Gold display
    gold_text = font.render(f"Gold: {player.gold_count}", True, (255, 255, 255))
    screen.blit(gold_text, (10, 100))

    # Remaining gold display (you'll need to modify this to track remaining gold)
    remaining_gold = len(player.level.gold_list)
    gold_text = font.render(f"Gold Left: {remaining_gold}", True, (255, 215, 0))
    screen.blit(gold_text, (10, 130))

    # Time display
    current_time = (pygame.time.get_ticks()) / 1000
    time_text = font.render(f"Time: {current_time:.1f}s", True, (255, 255, 255))
    screen.blit(time_text, (10, 160))

def calculate_game_score(level_start_times, level_end_times, player):
    """Calculates the game score based on the completion time and the amount of gold collected"""
    total_score = 0

    # Time-based scoring tiers (in seconds)
    TIME_SCORING_TIERS = [
        (15, 1000),   # If level completed in 15 seconds or less, 1000 points
        (30, 800),    # If level completed in 30 seconds or less, 800 points
        (45, 600),    # If level completed in 45 seconds or less, 600 points
        (60, 300),    # If level completed in 60 seconds or less, 400 points
        (float('inf'), 100)  # Any time beyond 60 seconds, 200 points
    ]

    # Total gold pieces per level
    level_total_gold = [4, 4, 4]  # Total gold pieces in each level

    for i in range(len(level_start_times)): # 3 levels
        if i < len(level_end_times): # Check if level was actually completed
            level_ticks = level_end_times[i] - level_start_times[i]
            level_time_seconds = level_ticks / 1000.0

            # Time score
            time_score = 0
            for max_time, points in TIME_SCORING_TIERS:
                if level_time_seconds <= max_time:
                    time_score = points
                    break

            # Gold score
            gold_score = player.gold_count * 250 #per gold

            # Full level gold bonus
            if player.level_gold_count[i] == level_total_gold[i]:
                gold_score += 500 #full level bonus
                #debug
                '''print(f"FULL level GOLD COLLECTION BONUS: +{500}")'''

            # Combine scores for this level
            level_total = time_score + gold_score

            total_score += level_total

            # Debugging print
            '''
            print(f"Level {i+1}:")
            print(f"  Time: {level_time_seconds:.2f} seconds")
            print(f"  Time Score: {time_score}")
            print(f"  Gold Count: {player.gold_count}")
            print(f"  Gold Score: {gold_score}")
            print(f"  Level Total: {level_total}")
            '''

    # Full game gold bonus
    if sum(player.level_gold_count) == sum(level_total_gold):
        total_score += 2000 #full game bonus
        #debug
        '''print(f"FULL GAME GOLD COLLECTION BONUS: +{2000}")'''

    print(f"Total Score: {total_score}")
    return int(total_score)

def main():
    """The main loop"""
    pygame.init()

    # Initialize sound manager
    sound_manager = SoundManager()

    sound_manager.play_bg_music()
    music = 0

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Very Fun Platformer Game")

    player = Player()
    level_list = [Level_01(player), Level_02(player), Level_03(player)]

    current_level_no = 0  # change number to debug certain level

    current_level = level_list[current_level_no]
    player.level = current_level

    # Initial player placement
    if current_level.platform_list:
        first_platform = list(current_level.platform_list)[0]
        player.rect.bottom = first_platform.rect.top
        player.rect.x = first_platform.rect.x
    else:
        player.rect.x = 340
        player.rect.y = SCREEN_HEIGHT - player.rect.height

    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)

    scores = load_scores()
    if scores:
        high_score = scores[0].score
    else:
        high_score = 0

    done = False
    game_over = False
    clock = pygame.time.Clock()

    # Track level start times and gold
    level_start_times = [pygame.time.get_ticks()]
    level_gold_count = [0] * len(level_list)  # Initialize with zeros for each level
    level_end_times = []

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and music != 1:
                    sound_manager.stop_bg_music_funny()
                    sound_manager.play_bg_music()
                    music = 1
                if event.key == pygame.K_2 and music != 2:
                    sound_manager.stop_bg_music()
                    sound_manager.play_bg_music_funny()
                    music = 2
                if event.key == pygame.K_3 and music != 3:
                    sound_manager.stop_bg_music()
                    sound_manager.stop_bg_music_funny()
                    music = 3

            if not game_over:
                if event.type == pygame.KEYDOWN and not player.is_respawning:
                    if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        player.jump()

        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if player.wall_jump_timer <= 0 and not player.is_respawning:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    player.go_left()
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    player.go_right()
                else:
                    player.stop()

            # Update game state
            active_sprite_list.update(current_level_no)
            current_level.update()

            if player.rect.right >= WORLD_SHIFT_RIGHT_BOUNDARY:
                diff = player.rect.right - WORLD_SHIFT_RIGHT_BOUNDARY
                player.rect.right = WORLD_SHIFT_RIGHT_BOUNDARY
                current_level.shift_world(-diff)

            if player.rect.left <= WORLD_SHIFT_LEFT_BOUNDARY:
                diff = WORLD_SHIFT_LEFT_BOUNDARY - player.rect.left
                player.rect.left = WORLD_SHIFT_LEFT_BOUNDARY
                current_level.shift_world(diff)

            # Level progression
            current_position = player.rect.x + current_level.world_shift
            if current_position < current_level.level_limit:
                if current_level_no < len(level_list) - 1:
                    sound_manager.play_level_completed()
                    # Record end time for current level
                    level_end_times.append(pygame.time.get_ticks())

                    # Move to next level
                    current_level_no += 1
                    current_level = level_list[current_level_no]
                    player.level = current_level

                    # Reset world shift
                    current_level.world_shift = 0

                    # Reset player position
                    if current_level.platform_list:
                        first_platform = list(current_level.platform_list)[0]
                        player.rect.bottom = first_platform.rect.top
                        player.rect.x = first_platform.rect.x

                    # Trigger respawning effect for level transition
                    player.is_respawning = True
                    player.respawn_timer = 0

                    # Track new level start time
                    level_start_times.append(pygame.time.get_ticks())

                else:
                    # Player has completed all levels
                    current_level_no += 1
                    level_end_times.append(pygame.time.get_ticks())
                    game_over = True

            # Track gold collection per level
            gold_hit = pygame.sprite.spritecollideany(player, current_level.gold_list)
            if gold_hit:
                # Check if this specific gold piece hasn't been collected before
                if gold_hit in current_level.gold_list:
                    # Increment the gold count for the current level
                    level_gold_count[current_level_no] += 1
                    # Remove the gold piece from the level's gold list
                    current_level.gold_list.remove(gold_hit)

                # Collect the gold (this will play sound and remove the gold from all sprite groups)
                player.collect_gold(gold_hit, current_level_no)

            # Game over check
            if player.lives <= 0:
                game_over = True

        if game_over:
            #debug code
            ''' 
            print(f"Debug - Final level_gold_count: {player.level_gold_count}")
            print("Debug = Final gold_count:", player.gold_count)
            '''

            # Calculate final score
            final_score = calculate_game_score(
                level_start_times,
                level_end_times,
                player
            )

            font = pygame.font.Font(None, 74)

            # Game over and high score flow
            game_over_screen(screen, font, final_score, current_level_no, high_score)
            pygame.display.flip()
            pygame.time.wait(1000)  # Pause briefly to show game over screen

            # Handle user input for name
            user_input_result = user_input(screen, font, final_score, scores, current_level_no, high_score)

            # Show high scores screen
            highscores_screen(screen, font, final_score, scores)

            # Exit the game
            done = True

            pygame.display.flip()

        # Drawing
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        font = pygame.font.Font(None, 36)
        draw_game_info(screen, player, current_level_no, font, high_score)

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()