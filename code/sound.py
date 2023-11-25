import pygame
import json

class Soundbar:
    def __init__(self, user_settings: dict):
        self.mute_status: bool = False

        self.user_settings = user_settings
        # main sounds
        self.start_window_bg_music = pygame.mixer.Sound('../audio/happy_adveture.mp3')
        self.start_window_bg_music.set_volume(0.8)

        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
        self.level_bg_music_status: bool = False
        self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')
        self.overworld_bg_music_status: bool = False

        # effects sounds
        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
        self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')

        # activating user setting
        self.set_settings(self.user_settings)

    def __change_mute_status(self):
        if self.mute_status:
            self.mute_status = False
        else:
            self.mute_status = True

    def change_mute_mode(self):
        self.__change_mute_status()
        if self.mute_status:
            self.level_bg_music.stop()
            self.overworld_bg_music.stop()

        else:
            if self.level_bg_music_status:
                self.level_bg_music.play(loops=-1)
            elif self.overworld_bg_music_status:
                self.overworld_bg_music.play(loops=-1)

    def set_settings(self, user_setting: dict):
        self.level_bg_music.stop()
        self.overworld_bg_music.stop()

        self.level_bg_music.set_volume(user_setting['bg_music_volume'])
        self.overworld_bg_music.set_volume(user_setting['bg_music_volume'])

        self.coin_sound.set_volume(user_setting['effects_sound_volume'])
        self.stomp_sound.set_volume(user_setting['effects_sound_volume'])
        self.jump_sound.set_volume(user_setting['effects_sound_volume'])
        self.hit_sound.set_volume(user_setting['effects_sound_volume'])

    def set_to_standard_settings(self):
        with open('../code/settings_data.json', 'r') as file:
            data = json.load(file)
            default_data = data['default_settings']
            self.level_bg_music_volume = default_data['level_bg_sound_level']
            self.overworld_bg_music_volume = default_data['overworld_bg_sound_level']
            self.effects_sound_volume = default_data['effects_sound_volume']

    def play_overworld_bg_music(self):
        if not self.mute_status:
            self.level_bg_music_status = False
            self.level_bg_music.stop()

            self.overworld_bg_music_status = True
            self.overworld_bg_music.play(loops=-1)
        else:
            self.level_bg_music_status = False

            self.overworld_bg_music_status = True

    def play_level_bg_music(self):
        if not self.mute_status:
            self.overworld_bg_music_status = False
            self.overworld_bg_music.stop()

            self.level_bg_music_status = True
            self.level_bg_music.play(loops=-1)
        else:
            self.overworld_bg_music_status = False

            self.level_bg_music_status = True


    def play_effect_sound(self, effect: str):
        if not self.mute_status:
            if effect == 'coin_sound':
                self.coin_sound.play()
            elif effect == 'stomp_sound':
                self.stomp_sound.play()
            elif effect == 'jump_sound':
                self.jump_sound.play()
            elif effect == 'hit_sound':
                self.hit_sound.play()
