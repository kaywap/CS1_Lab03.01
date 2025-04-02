"""Sound manager that manages all the sounds you hear in the game. """
_version__ = '04/02/2025'
__author__ = 'Kayla Cao'

import pygame

class SoundManager:
    """Manages your sounds"""
    def __init__(self):
        """initialization"""
        # Initialize pygame mixer
        pygame.mixer.init()

        # Load sounds (make sure to have these sound files in a 'sounds' folder)
        try:
            self.bouncepad_sound = pygame.mixer.Sound("sounds/bouncepad.wav")
            self.game_lost_sound = pygame.mixer.Sound("sounds/game_lost.wav")
            self.game_won_sound = pygame.mixer.Sound("sounds/game_won.wav")
            self.gold_collect_sound = pygame.mixer.Sound("sounds/gold_collect.wav")
            self.level_completed_sound = pygame.mixer.Sound("sounds/level_completed.wav")
            self.lose_life_sound = pygame.mixer.Sound("sounds/lose_life.wav")

            # Background music
            self.bg_music = pygame.mixer.Sound('sounds/bg_music.wav')
            self.bg_music_funny = pygame.mixer.Sound('sounds/bg_music_funny.wav') #for funny background music
            self.bg_music_funny.set_volume(0.3)

        except Exception as e:
            print(f"Error loading sounds: {e}")

    def play_bouncepad(self):
        """play boing sound"""
        self.bouncepad_sound.play()

    def play_game_lost(self):
        """plays game over sound"""
        self.game_lost_sound.play()

    def play_game_won(self):
        """plays woo! sound"""
        self.game_won_sound.play()

    def play_gold_collect(self):
        """plays collection sound"""
        self.gold_collect_sound.play()

    def play_level_completed(self):
        """plays level completed sound"""
        self.level_completed_sound.play()

    def play_lose_life(self):
        """plays oof sound"""
        self.lose_life_sound.play()

    def play_bg_music(self):
        """plays video game background music"""
        self.bg_music.play(loops=-1) #play forever

    def stop_bg_music(self):
        """stops video game background music"""
        self.bg_music.stop()

    def play_bg_music_funny(self):
        """plays funny background music"""
        self.bg_music_funny.play(loops=-1) #play forever

    def stop_bg_music_funny(self):
        """stops funny background music"""
        self.bg_music_funny.stop()