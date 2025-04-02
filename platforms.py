"""Creating platform classes that the player stands on"""
__version__ = '04/02/2025'
__author__ = 'Kayla Cao'

import pygame

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor."""
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((0, 225, 0)) #green

        self.rect = self.image.get_rect()

class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """

    def __init__(self, x, y, width, height, boundary1, boundary2, speed, move_type):
        """initialization"""
        super().__init__(width, height)
        self.move_type = move_type
        self.speed = speed

        # Vertical boundaries
        self.top_boundary = min(boundary1, boundary2)
        self.bottom_boundary = max(boundary1, boundary2)

        # Horizontal boundaries
        self.left_boundary = min(boundary1, boundary2)
        self.right_boundary = max(boundary1, boundary2)

        self.player = None
        self.level = None
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """ Move the platform. """
        if self.move_type == 'horizontal':
            # Move left/right
            self.rect.x += self.speed

            # See if we hit the player
            hit = pygame.sprite.collide_rect(self, self.player)
            if hit:
                if self.speed < 0:
                    self.player.rect.right = self.rect.left
                else:
                    self.player.rect.left = self.rect.right

            # Check horizontal boundaries
            cur_pos = self.rect.x - self.level.world_shift
            if cur_pos < self.left_boundary or cur_pos > self.right_boundary:
                self.speed *= -1

        elif self.move_type == 'vertical':
            # Move up/down
            self.rect.y += self.speed

            # See if we hit the player
            hit = pygame.sprite.collide_rect(self, self.player)
            if hit:
                if self.speed < 0:
                    # Platform moving up
                    self.player.rect.bottom = self.rect.top
                else:
                    # Platform moving down
                    self.player.rect.top = self.rect.bottom

            # Check vertical boundaries
            if self.rect.bottom > self.bottom_boundary or self.rect.top < self.top_boundary:
                self.speed *= -1
