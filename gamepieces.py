"""Creating obstacle and game piece classes that the player can use/dodge"""
__version__ = '04/02/2025'
__author__ = 'Kayla Cao'

import pygame

class GamePiece(pygame.sprite.Sprite):
    """Parent class for all game pieces"""
    def __init__(self, x, y, width, height, color):
        '''initialization'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Laser(GamePiece):
    """class for a laser that flashes on and off"""
    def __init__(self, x, y, width, height, active_duration=60, inactive_duration=60):
        '''initialization'''
        # Bright red when active
        super().__init__(x, y, width, height, color=(255, 0, 0))

        # Additional laser-specific attributes
        self.active_image = pygame.Surface([width, height])
        self.active_image.fill((255, 0, 0))

        self.inactive_image = pygame.Surface([width, height])
        self.inactive_image.fill((25, 0, 0))

        self.active_duration = active_duration
        self.inactive_duration = inactive_duration
        self.timer = 0
        self.is_active = True

    def update(self):
        '''updates the laer'''
        self.timer += 1

        if self.is_active and self.timer > self.active_duration:
            self.is_active = False
            self.timer = 0
            self.image = self.inactive_image

        elif not self.is_active and self.timer > self.inactive_duration:
            self.is_active = True
            self.timer = 0
            self.image = self.active_image

class Spike(GamePiece):
    """class for a spike"""
    def __init__(self, x, y, width, height, orientation='up'):
        """initialization"""
        # Gray color for spikes
        super().__init__(x, y, width, height, color=(100, 100, 100))

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
    """class for a spike that attaches to moving platforms"""
    def __init__(self, platform, orientation='up', width=None, height=20):
        '''initialization'''

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

class Gold(GamePiece):
    """class for a collectible gold piece"""
    def __init__(self, x, y, width, height):
        """initialization"""
        super().__init__(x, y, width, height, color=(255, 215, 0))

class Bouncepad(GamePiece):
    """class for a bouncepad"""
    def __init__(self, x, y, width, height, bounce_strength=-18):
        """initialization"""
        super().__init__(x, y, width, height, color=(255, 0, 225))
        self.bounce_strength = bounce_strength

class Enemy(GamePiece):
    """class for an enemy that moves in a specified boundary"""
    def __init__(self, x, y, width, height, boundary1, boundary2, speed, move_type):
        """initialization"""
        super().__init__(x, y, width, height, color=(0, 0, 255))

        self.move_type = move_type
        self.speed = speed
        self.top_boundary = min(boundary1, boundary2)
        self.bottom_boundary = max(boundary1, boundary2)
        self.left_boundary = min(boundary1, boundary2)
        self.right_boundary = max(boundary1, boundary2)

        self.player = None
        self.level = None

    def update(self):
        """updates the enemy"""
        if self.move_type == 'horizontal':
            self.rect.x += self.speed
            cur_pos = self.rect.x - self.level.world_shift
            if cur_pos <= self.left_boundary or cur_pos >= self.right_boundary:
                self.speed *= -1

        elif self.move_type == 'vertical':
            self.rect.y += self.speed
            if self.rect.top <= self.top_boundary or self.rect.bottom >= self.bottom_boundary:
                self.speed *= -1