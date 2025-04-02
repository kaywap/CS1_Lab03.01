import pygame
from platforms import *

class Game():
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

        # How far this world has been scrolled up/down
        self.world_shift = 0
        self.game_limit = -1000

        # Array with width, height, x, and y of platform
        game = [
            [210, 30, 300, 600], #bottom starting platform
            [210, 30, 400, 400],
            [210, 30, 200, 300],
        ]

        # Go through the array above and add platforms
        for platform in game:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platforms
        # Vertical moving platform
        block = MovingPlatform(70, 40, move_type='vertical')
        block.rect.x = 100
        block.rect.y = 400
        block.boundary_top = 300
        block.boundary_bottom = 600
        block.change_y = 2  # Speed of vertical movement
        block.player = self.player
        block.game = self
        self.platform_list.add(block)

        # Horizontal moving platform
        block = MovingPlatform(70, 40, move_type='horizontal')
        block.rect.x = 300
        block.rect.y = 200
        block.boundary_left = 100
        block.boundary_right = 400
        block.change_x = 2  # Speed of horizontal movement
        block.player = self.player
        block.game = self
        self.platform_list.add(block)

    def update(self):
        """ Update everything in game."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything in game. """
        # Draw the background
        screen.fill((0, 0, 255)) #blue

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_y):
        """ When the user moves up/down and we need to scroll everything:
        """

        # Keep track of the shift amount
        self.world_shift += shift_y

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.y += shift_y