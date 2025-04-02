"""Creates each level and updates all sprites for world shifting"""
__version__ = '04/02/2025'
__author__ = 'Kayla Cao'

import pygame
from platforms import *
from gamepieces import *

class Level(object):
    """Parent class for all levels"""
    def __init__(self, player):
        """initialization"""

        # Player completes level by moving left past this point
        self.level_limit = -500  # Default value, will be overridden by specific levels

        # How far this world has been scrolled left/right
        self.world_shift = 0

        self.player = player

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.laser_list = pygame.sprite.Group()
        self.spike_list = pygame.sprite.Group()
        self.gold_list = pygame.sprite.Group()
        self.bouncepad_list = pygame.sprite.Group()

        self.font = pygame.font.Font(None, 24)  # Default font and size
        self.text_list = []


        # Background image
        self.background = None

    def update(self):
        """ Update everything in the level."""
        self.platform_list.update()
        self.enemy_list.update()
        for laser in self.laser_list:
            laser.update()
        self.spike_list.update()
        self.gold_list.update()
        self.bouncepad_list.update()

    def add_text(self, text, x, y, color=(240,240,240)):
        """Add text to be drawn in the level"""
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(x=x, y=y)
        self.text_list.append((text_surf, text_rect))

    def draw(self, screen):
        """Draw everything on this level. """
        screen.fill((100, 125, 150))  # Dark bluish-gray room color

        # Draw all the sprite lists
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.laser_list.draw(screen)
        self.spike_list.draw(screen)
        self.gold_list.draw(screen)
        self.bouncepad_list.draw(screen)

        # Draw level texts
        for text_surf, text_rect in self.text_list:
            screen.blit(text_surf, text_rect)

    def shift_world(self, shift_x):
        """ When the user moves left/right, we need to scroll everything"""
        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        # Shift obstacle groups
        for laser in self.laser_list:
            laser.rect.x += shift_x

        for spike in self.spike_list:
            spike.rect.x += shift_x

        for gold in self.gold_list:
            gold.rect.x += shift_x

        for bouncepad in self.bouncepad_list:
            bouncepad.rect.x += shift_x

        new_text_list = []
        for text_surf, text_rect in self.text_list:
            text_rect.x += shift_x
            new_text_list.append((text_surf, text_rect))

        self.text_list = new_text_list

class Level_01(Level):
    """ Level 01! The easiest level with tutorial text to help you along """
    def __init__(self, player):
        """initialization"""
        super().__init__(player)

        #text
        self.add_text("Arrow keys or", -50, 460)
        self.add_text("WASD to move", -50, 489)
        self.add_text("Nothing here.", -290, 300)
        self.add_text("Ooh bouncy!", 175, 425)
        self.add_text("Yummy gold bits!", 100, 300)
        self.add_text("Blue for bad guy,", 240, 540)
        self.add_text("gray for g-bad guy", 305, 560)
        self.add_text("This guy moves!", 320, 190)
        self.add_text("Hold right and press jump:", 450, 75)
        self.add_text("Wall Jump!!", 850, 200)
        self.add_text("Go right ------------------------------------------------------------------------------------------------------------------->", 1000, 300)

        #width, length, x, y
        level = [
            # Floating platforms
            [250, 30, 50, 570],  # Left lower platform
            [30, 140, 300, 380],  # left wall
            [100, 30, 400, 350],  # Mid platform
            [30, 300, 500, 310], # left middle wall
            [30, 350, 590, 250],  # right middle wall
            [30, 170, 700, 100],  # Right upper wall
            [150, 600, -300, 0],  # far left barrier wall
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)

        # Spikes
        spike1 = Spike(200, 540, 50, 30)
        spike2 = Spike(400, 575, 100, 25) #under mid platform
        spike3 = Spike(500, 290, 30, 20) #spike on left middle wall
        spike4 = Spike(530, 570, 60, 30) #spike between mid walls
        spike5 = Spike(700, 80, 30, 20) #spike on right upper wall


        self.spike_list.add(spike1, spike2, spike3, spike4, spike5)

        # Gold
        gold1 = Gold(240, 250, 20, 20)
        gold2 = Gold(460, 400, 20, 20)
        gold3 = Gold(450, 320, 20, 20)
        gold4 = Gold(600, 230, 20, 20)

        self.gold_list.add(gold1, gold2, gold3, gold4)

        # Bouncepads
        bouncepad1 = Bouncepad(200, 500, 100, 20, bounce_strength=-18)
        bouncepad2 = Bouncepad(620, 250, 80, 20, bounce_strength=-13)

        self.bouncepad_list.add(bouncepad1, bouncepad2)

        # Enemies
        enemy1 = Enemy(
            x=340,  # x position
            y=300,  # y position
            width=30,  # width
            height=30,  # height
            boundary1=300,  # top boundary (lower y value)
            boundary2=545,  # bottom boundary (higher y value)
            speed=3,  # movement speed
            move_type="vertical"
        )
        enemy1.level = self
        enemy1.player = self.player
        self.enemy_list.add(enemy1)

        # Add a moving platform
        moving_platform = MovingPlatform(
            x=300,           # x position
            y=250,           # y position
            width=100,       # width
            height=20,       # height
            boundary1=300,   # left/top boundary
            boundary2=450,   # right/bottom boundary
            speed = 3,
            move_type="horizontal"
        )
        moving_platform.player = self.player
        moving_platform.level = self
        self.platform_list.add(moving_platform)

class Level_02(Level):
    """Level 02! Getting a little harder!"""
    def __init__(self, player):
        """initialization"""
        # Call the parent constructor
        super().__init__(player)

        self.add_text("Lasers are bad when red", 350, 375)
        self.add_text("Hold against the wall:", 900, 100)
        self.add_text("Wall", 1060, 280)
        self.add_text("Slide!", 1040, 310)
        self.add_text("Go right again -->", 1400, 380)
        self.add_text("Fun fact:", 1400, 420)
        self.add_text("press 1 and 2 to switch background music", 1400, 440)
        self.add_text(" and press 3 to mute.", 1400, 460)

        # width length x y
        level = [
            [170, 30, 500, 570],  # Lower platform
            [100, 20, 570, 440],  # under laser
            [100, 20, 570, 400],  # over laser
            [30, 200, 930, 400],  # wall connecting to middle platform
            [150, 30, 780, 400],  # Mid platform
            [30, 450, 1000, 200],  # wall with spike
            [30, 540, 1100, 0],  # mid right wall
            [30, 450, 1200, 150],  # right wall
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)

        # Add lasers
        laser1 = Laser(500, 420, 230, 20, active_duration=40, inactive_duration=40)
        self.laser_list.add(laser1)

        # Add spikes
        spike1 = Spike(640, 550, 30, 20)

        spike2 = Spike(830, 570, 30, 30)
        spike3 = Spike(860, 570, 30, 30)
        spike4 = Spike(890, 570, 30, 30)


        spike5 = Spike(960, 570, 40, 30)
        spike6 = Spike(1000, 180, 30, 20)

        spike7 = Spike(1080, 330, 20, 30, "left")
        spike8 = Spike(1080, 360, 20, 30, "left")
        spike9 = Spike(1030, 570, 20, 30, "right")
        spike10 = Spike(1030, 540, 20, 30, "right")

        spike11 = Spike(1100, 540, 30, 20, "down")

        spike12 = Spike(1180, 570, 20, 30, "left")
        spike13 = Spike(1180, 540, 20, 30, "left")

        spike14 = Spike(1130, 360, 10, 30, "right")

        spike15 = Spike(1200, 130, 30, 20)

        self.spike_list.add(spike1, spike2, spike3, spike4, spike5, spike6, spike7, spike8, spike9, spike10, spike11, spike12, spike13, spike14, spike15)

        # Add gold
        gold1 = Gold(600, 350, 20, 20)

        gold2 = Gold(900, 440, 20, 20)

        gold3 = Gold(930, 250, 20, 20)
        gold4 = Gold(1200, 40, 20, 20)
        self.gold_list.add(gold1, gold2, gold3, gold4)

        # Add moving platform
        moving_platform = MovingPlatform(
            x=800,  # x position
            y=350,  # y position
            width=100,  # width
            height=30,  # height
            boundary1=730,  # left boundary
            boundary2=860,  # right boundary
            speed=3,
            move_type="horizontal"
        )
        moving_platform.player = self.player
        moving_platform.level = self
        self.platform_list.add(moving_platform)

        # Bouncepads
        bouncepad1 = Bouncepad(670, 570, 60, 30, bounce_strength=-18)

        self.bouncepad_list.add(bouncepad1)

        # Add enemy
        enemy1 = Enemy(
            x=800,  # x position
            y=220,  # y position
            width=30,  # width
            height=30,  # height
            boundary1=700,  # left/top boundary
            boundary2=900,  # right/bottom boundary
            speed=3,  # movement speed
            move_type="horizontal"
        )
        enemy1.level = self
        enemy1.player = self.player
        self.enemy_list.add(enemy1)

class Level_03(Level):
    """Level 03! THE ULTIMATE TEST"""
    def __init__(self, player):
        """initialization"""
        super().__init__(player)

        # width length x y
        level = [
            [50, 30, 50, 570],  # Left lower platform 1
            [50, 30, 150, 570],  # Left lower platform 2
            [50, 30, 250, 570],  # Left lower platform 3
            [100, 30, 350, 570],  # Left lower platform 4
            [350, 20, 50, 380],  # above spike
            [15, 500, 450, 100],  # wall connecting bottom and top platform
            [400, 20, 50, 250],  # above the above spike
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)

        # lasers
        laser1 = Laser(100, 270, 20, 110, active_duration=15, inactive_duration=45)
        laser2 = Laser(200, 270, 20, 110, active_duration=20, inactive_duration=60)
        laser3 = Laser(300, 270, 20, 110, active_duration=15, inactive_duration=45)
        self.laser_list.add(laser1, laser2, laser3)

        #spikes
        spike1 = Spike(50, 400, 250, 20, "down") #change this one later so it is a row of spikes
        spike2 = Spike(100, 230, 40, 20)
        spike3 = Spike(200, 230, 40, 20)
        spike4 = Spike(300, 230, 40, 20)
        spike5 = Spike(400, 230, 40, 20)
        spike6 = Spike(480, 580, 700, 20)
        self.spike_list.add(spike1, spike2, spike3, spike4, spike5, spike6)

        # gold
        gold1 = Gold(350, 400, 20, 20)
        gold2 = Gold(350, 320, 20, 20)
        gold3 = Gold(25, 75, 20, 20)
        gold4 = Gold(470, 550, 20, 20)
        self.gold_list.add(gold1, gold2, gold3, gold4)

        # moving platforms
        moving_platform1 = MovingPlatform(
            x=0,           # x position
            y=300,           # y position
            width=40,       # width
            height=20,       # height
            boundary1=200,   # top boundary
            boundary2=450,   # bottom boundary
            speed=3,
            move_type="vertical"
        )

        moving_platform2 = MovingPlatform(
            x=530,  # x position
            y=150,  # y position
            width=70,  # width
            height=30,  # height
            boundary1=150,  # top boundary
            boundary2=500,  # bottom boundary
            speed=4,
            move_type="vertical"
        )

        moving_platform3 = MovingPlatform(
            x=600,  # x position
            y=300,  # y position
            width=50,  # width
            height=30,  # height
            boundary1=600,  # left boundary
            boundary2=750,  # right boundary
            speed=2,
            move_type="horizontal"
        )

        moving_platform4 = MovingPlatform(
            x=850,  # x position
            y=200,  # y position
            width=80,  # width
            height=30,  # height
            boundary1=200,  # top boundary
            boundary2=500,  # bottom boundary
            speed=3,
            move_type="vertical"
        )

        # Create moving spikes
        moving_spike1 = MovingSpike(moving_platform1, orientation='down')
        moving_spike2 = MovingSpike(moving_platform2, orientation='down')
        moving_spike3 = MovingSpike(moving_platform3, orientation='right', width=20)
        moving_spike4 = MovingSpike(moving_platform4, orientation='down')

        # Setup platforms
        for p in (moving_platform1, moving_platform2, moving_platform3, moving_platform4):
            p.player = self.player
            p.level = self
            self.platform_list.add(p)

        # Add moving spikes to spike list
        self.spike_list.add(moving_spike1, moving_spike2, moving_spike3, moving_spike4)

        #bouncepads
        bouncepad1 = Bouncepad(100, 570, 50, 30, bounce_strength=-15)
        bouncepad2 = Bouncepad(200, 570, 50, 30, bounce_strength=-15)
        bouncepad3 = Bouncepad(300, 570, 50, 30, bounce_strength=-15)

        self.bouncepad_list.add(bouncepad1, bouncepad2, bouncepad3)

        # Add enemies
        enemy1 = Enemy(
            x=50,  # x position
            y=100,  # y position
            width=30,  # width
            height=30,  # height
            boundary1=50,  # left boundary
            boundary2=400,  # right boundary
            speed=3,  # movement speed
            move_type="horizontal"
        )

        enemy1.level = self
        enemy1.player = self.player
        self.enemy_list.add(enemy1)