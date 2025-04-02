"""The heart of the game, includes: player movement, collision, and reactions to certain game pieces."""
__version__ = '04/02/2025'
__author__ = 'Kayla Cao'

import pygame
from config import *
from platforms import *
from sounds import *

class Player(pygame.sprite.Sprite):
    """The player!! The heart of the game!"""
    def __init__(self):
        """initialization"""
        super().__init__()

        self.sound_manager = SoundManager()

        # Load the entire sprite sheet
        sprite_sheet = pygame.image.load('images/player_sprite_sheet.png').convert_alpha()
        # Sprite dimensions in the original sheet

        #sprite positions
        self.idle_sprite = self.get_sprite_from_sheet(sprite_sheet, 0, 0, 75, 150)
        self.run_right_sprite = self.get_sprite_from_sheet(sprite_sheet, 0, 160, 110, 120)
        self.run_left_sprite = pygame.transform.flip(self.run_right_sprite, True, False)
        self.jump_sprite = self.get_sprite_from_sheet(sprite_sheet, 170, 0, 60, 140)

        self.width = 20
        self.height = 35

        #initial image
        self.image = pygame.transform.scale(self.idle_sprite, (self.width, self.height))
        self.rect = self.image.get_rect()

        self.level = None

        # movement
        self.default_gravity = 0.65  # Normal gravity
        self.wall_slide_gravity = 0.2  # Reduced gravity when sliding on wall
        self.gravity = self.default_gravity  # Current gravity

        self.h_speed = 0
        self.v_speed = 0
        self.max_h_speed = 6  # Horizontal movement speed
        self.jump_speed = -12  # Vertical jump speed

        # wall jumping
        self.wall_jump_h_speed = 3  # Increased push off wall
        self.wall_jump_v_speed = -12  # Vertical jump speed for wall jumps
        self.wall_direction = 0  # -1 for left wall, 1 for right wall
        self.can_wall_jump = False  # if your touching a wall, you can wall jump
        self.can_jump = False

        # Wall jump timer
        self.wall_jump_timer = 0
        self.wall_jump_duration = 10  # Frames to ignore horizontal input after wall jump

        # Score tracking
        self.score = 0
        self.gold_count = 0
        self.level_gold_count = [0, 0, 0]

        # Start with 3 lives
        self.initial_lives = 3
        self.lives = self.initial_lives

        # Initialize respawning attributes
        self.is_respawning = False
        self.respawn_timer = 0
        self.flash_duration = 60  # Flash for 60 frames (1 second at 60 FPS)

    def get_sprite_from_sheet(self, sheet, x, y, width, height):
        """Extract a specific sprite from a sprite sheet"""
        # Extract the sprite
        sprite = sheet.subsurface((x, y, width, height))

        return sprite

    def reset_lives(self):
        """Reset lives to initial value"""
        self.lives = self.initial_lives

    def collect_gold(self, gold, current_level_no):
        """ Collect gold and increase score """

        self.gold_count += 1

        if current_level_no == 0:
            self.level_gold_count[0] += 1
        elif current_level_no == 1:
            self.level_gold_count[1] += 1
        elif current_level_no == 2:
            self.level_gold_count[2] += 1

        self.sound_manager.play_gold_collect()  # play sound
        gold.kill()  # Remove gold from all sprite groups

    def update(self, current_level_no):
        """updates the player"""
        # Determine sprite based on movement and jump state
        if self.v_speed != 0:  # Jumping or falling
            self.image = pygame.transform.scale(self.jump_sprite, (self.width, self.height))
        elif self.h_speed > 0:
            self.image = pygame.transform.scale(self.run_right_sprite, (self.width, self.height))
        elif self.h_speed < 0:
            self.image = pygame.transform.scale(self.run_left_sprite, (self.width, self.height))
        else:
            self.image = pygame.transform.scale(self.idle_sprite, (self.width, self.height))

        # Reset jump flags at the beginning of each update
        self.can_jump = False
        # Don't reset wall jump here - we'll handle it after collision checks

        # Determine gravity and vertical speed based on wall sliding
        if self.can_wall_jump and self.v_speed > 0:
            # Sliding down a wall
            self.gravity = self.wall_slide_gravity
            # Cap the maximum vertical speed when sliding
            self.v_speed = min(self.v_speed, 2)  # Limit vertical speed to 2
        else:
            # Normal gravity
            self.gravity = self.default_gravity

        # Apply gravity
        self.v_speed += self.gravity

        # apply horizontal movement
        self.rect.x += self.h_speed

        # Reset wall jump state before checking for new wall collisions
        self.can_wall_jump = False

        # Check horizontal collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        # If there are any collisions, you can wall jump
        if block_hit_list:
            for block in block_hit_list:
                # Detect wall contact
                if self.h_speed > 0:  # going right
                    self.rect.right = block.rect.left
                    self.wall_direction = 1
                    self.can_wall_jump = True  # Set wall jump flag when hitting a wall
                elif self.h_speed < 0:  # going left
                    self.rect.left = block.rect.right
                    self.wall_direction = -1
                    self.can_wall_jump = True  # Set wall jump flag when hitting a wall

        # apply vertical movement
        self.rect.y += self.v_speed

        # Check vertical collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if len(block_hit_list) > 0:
            self.can_jump = True

        for block in block_hit_list:
            # Correct vertical position
            if self.v_speed > 0:  # Landing on a platform
                self.rect.bottom = block.rect.top
                self.v_speed = 0
                # Move with moving platforms
                if isinstance(block, MovingPlatform):  # if the block is a moving platform
                    if block.move_type == 'horizontal':  # if it is a horizontal moving platform
                        self.rect.x += block.speed
                    elif block.move_type == 'vertical':  # if it is a vertical moving platform
                        self.rect.y += block.speed

            elif self.v_speed < 0:  # Hitting platform from below
                self.rect.top = block.rect.bottom
                self.v_speed = 0

        # Check laser collision
        for laser in self.level.laser_list:
            if pygame.sprite.collide_rect(self, laser) and laser.is_active:
                self.caught()

        # Check spike collision
        if pygame.sprite.spritecollideany(self, self.level.spike_list):
            self.caught()

        # Check gold collision
        gold_hit = pygame.sprite.spritecollideany(self, self.level.gold_list)
        if gold_hit:
            self.collect_gold(gold_hit, current_level_no)

        # Check bouncepad collision
        bouncepad_hit = pygame.sprite.spritecollideany(self, self.level.bouncepad_list)
        if bouncepad_hit and self.v_speed > 0:  # Only bounce when falling onto the pad
            self.sound_manager.play_bouncepad() #play sound
            self.v_speed = bouncepad_hit.bounce_strength  # Apply bounce

        # Check enemy collision
        if pygame.sprite.spritecollideany(self, self.level.enemy_list):
            self.caught()

        # Screen boundary checks
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.v_speed = 0
            self.can_jump = True

        if self.rect.top < 0:
            self.rect.top = 0
            self.v_speed = 0

        # If respawning, completely stop movement and skip rest of update
        if self.is_respawning:
            # Flash the player (alternate visibility every few frames)
            self.respawn_timer += 1
            if self.respawn_timer % 10 < 5:  # Toggle every 5 frames
                self.image.set_alpha(128)  # Semi-transparent
            else:
                self.image.set_alpha(255)  # Fully visible

            # End the flashing effect after the duration
            if self.respawn_timer >= self.flash_duration:
                self.is_respawning = False
                self.image.set_alpha(255)  # Ensure player is fully visible

            # reset movement
            self.h_speed = 0
            self.v_speed = 0
            self.wall_jump_timer = 0
            self.can_jump = False
            self.can_wall_jump = False

        # Decrement wall jump timer if active
        if self.wall_jump_timer > 0:
            self.wall_jump_timer -= 1

    def jump(self):
        """lets player both jump and wall jump"""
        if self.can_wall_jump or self.can_jump:
            self.image = pygame.transform.scale(self.jump_sprite, (self.width, self.height))
        if self.can_wall_jump:
            # Wall jump - give a strong push away from the wall
            # Apply a horizontal impulse away from the wall
            self.h_speed = self.wall_jump_h_speed * -self.wall_direction  # Stronger push

            # Apply vertical jump velocity
            self.v_speed = self.wall_jump_v_speed

            # Start the wall jump timer to briefly ignore horizontal input
            self.wall_jump_timer = self.wall_jump_duration

            # Reset wall jump state
            self.can_wall_jump = False
        elif self.can_jump:
            self.v_speed = self.jump_speed

    def go_left(self):
        """ Move player left """
        self.h_speed = -self.max_h_speed
        self.image = pygame.transform.scale(self.run_left_sprite, (self.width, self.height))

    def go_right(self):
        """ Move player right """
        self.h_speed = self.max_h_speed
        self.image = pygame.transform.scale(self.run_right_sprite, (self.width, self.height))

    def stop(self):
        """ Stop horizontal movement when user lets go of keyboard"""
        self.h_speed = 0

    def caught(self):
        """ Reset player position when caught """
        self.sound_manager.play_lose_life() #play sound

        # Store the current world shift
        current_world_shift = self.level.world_shift

        # Reset all platforms and objects by shifting the world back to original position
        if current_world_shift != 0:
            self.level.shift_world(-current_world_shift)
            self.level.world_shift = 0

            # Reduce lives only if not already at 0
            if self.lives > 0:
                self.lives -= 1

            # Visual feedback - make player flash briefly
            self.is_respawning = True
            self.respawn_timer = 0

            # Reset movement
            self.h_speed = 0
            self.v_speed = 0

            # Reset states
            self.wall_direction = 0
            self.can_wall_jump = False
            self.can_jump = False

            # finding respawn location
            # Respawn on the first platform in the list
            if self.level.platform_list:
                first_platform = list(self.level.platform_list)[0]
                self.rect.bottom = first_platform.rect.top
                self.rect.x = first_platform.rect.x
            else:
                # Absolute fallback to default spawn if no platform found
                self.rect.x = 340
                self.rect.y = SCREEN_HEIGHT - self.rect.height

