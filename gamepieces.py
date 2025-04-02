# creating obstacle and game piece classes that the player can use/dodge

__version__ = '04/02/2025'
__author__ = 'Kayla Cao'

import pygame
import random

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, active_duration=60, inactive_duration=60):
        super().__init__()

        # Laser surface (vertical)
        self.active_image = pygame.Surface([width, height])
        self.active_image.fill((255, 0, 0))  # Bright red when active

        self.inactive_image = pygame.Surface([width, height])
        self.inactive_image.fill((25, 0, 0))  # Dark red when inactive

        # Initial state
        self.image = self.active_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Timing parameters
        self.active_duration = active_duration  # Frames active
        self.inactive_duration = inactive_duration  # Frames inactive
        self.timer = 0
        self.is_active = True

    def update(self):
        # Increment timer
        self.timer += 1

        # Toggle between active and inactive states
        if self.is_active and self.timer > self.active_duration:
            # Switch to inactive
            self.is_active = False
            self.timer = 0
            self.image = self.inactive_image

        elif not self.is_active and self.timer > self.inactive_duration:
            # Switch to active
            self.is_active = True
            self.timer = 0
            self.image = self.active_image


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, orientation='up'):
        super().__init__()

        # Create a surface with per-pixel alpha (transparency)
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)

        # Define spike points based on orientation
        if orientation == 'up':
            points = [
                (0, height),  # Bottom left
                (width // 2, 0),  # Top middle
                (width, height)  # Bottom right
            ]
        elif orientation == 'down':
            points = [
                (0, 0),  # Top left
                (width // 2, height),  # Bottom middle
                (width, 0)  # Top right
            ]
        elif orientation == 'left':
            points = [
                (width, height),  # Bottom right
                (0, height // 2),  # Middle left
                (width, 0)  # Top right
            ]
        elif orientation == 'right':
            points = [
                (0, 0),  # Top left
                (width, height // 2),  # Middle right
                (0, height)  # Bottom left
            ]
        else:
            # Default to up orientation
            points = [
                (0, height),  # Bottom left
                (width // 2, 0),  # Top middle
                (width, height)  # Bottom right
            ]

        # Draw the triangle on the surface
        pygame.draw.polygon(self.image, (100, 100, 100), points)

        # Set up the rectangle for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MovingSpike(Spike):
    def __init__(self, platform, orientation='up', width=None, height=20):
        """
        Create a spike that moves with a specific platform

        :param platform: The platform this spike will be attached to
        :param orientation: 'up', 'down', 'left', or 'right'
        :param width: Width of the spike. Defaults to platform width if not specified
        :param height: Height of the spike
        """
        # Use platform width if no width specified
        if width is None:
            width = platform.rect.width

        # Call parent Spike constructor with initial position
        super().__init__(platform.rect.x, platform.rect.y, width, height, orientation)

        # Store reference to parent platform
        self.platform = platform
        self.orientation = orientation

    def update(self):
        """Update spike position based on parent platform's movement"""
        # Position based on platform and orientation
        if self.orientation == 'up':
            self.rect.bottom = self.platform.rect.top
            self.rect.centerx = self.platform.rect.centerx
        elif self.orientation == 'down':
            self.rect.top = self.platform.rect.bottom
            self.rect.centerx = self.platform.rect.centerx
        elif self.orientation == 'left':
            self.rect.right = self.platform.rect.left
            self.rect.centery = self.platform.rect.centery
        elif self.orientation == 'right':
            self.rect.left = self.platform.rect.right
            self.rect.centery = self.platform.rect.centery


class Gold(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 215, 0))  # Gold color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bouncepad(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bounce_strength=-18):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 0, 225))  # Bright pink color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bounce_strength = bounce_strength  # How high the player bounces


class Enemy(pygame.sprite.Sprite):
    """ Enemy that patrols a certain area. If you touch it, you lose a life """

    def __init__(self, x, y, width, height, boundary1, boundary2, speed, move_type):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 255))  # Blue color for enemies
        self.rect = self.image.get_rect()

        self.move_type = move_type
        self.speed = speed

        # For vertical movement
        self.top_boundary = min(boundary1, boundary2)
        self.bottom_boundary = max(boundary1, boundary2)

        # For horizontal movement
        self.left_boundary = min(boundary1, boundary2)
        self.right_boundary = max(boundary1, boundary2)

        self.player = None
        self.level = None
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """ Move the enemy """
        if self.move_type == 'horizontal':
            # Move left/right
            self.rect.x += self.speed

            # Check boundaries considering world shift
            cur_pos = self.rect.x - self.level.world_shift
            if cur_pos <= self.left_boundary or cur_pos >= self.right_boundary:
                self.speed *= -1

        elif self.move_type == 'vertical':
            # Move up/down
            self.rect.y += self.speed

            # Check the boundaries and see if we need to reverse direction
            if self.rect.top <= self.top_boundary or self.rect.bottom >= self.bottom_boundary:
                self.speed *= -1
