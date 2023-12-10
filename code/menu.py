import sys
import pygame
from settings import *
from tile import *
from player import Player


class Menu:
    start_menu_active = True

    pygame.font.init()
    small_font = pygame.font.SysFont('Corbel', 35)

    @staticmethod
    def show(screen):
        button_quit = pygame.image.load('C:/Users/kudro/'
                                        'PycharmProjects/Spawner3/graphics/sprites/buttons/quit.png')
        button_continue = pygame.image.load('C:/Users/kudro/'
                                            'PycharmProjects/Spawner3/graphics/sprites/buttons/continue.png')
        button_settings = pygame.image.load('C:/Users/kudro/'
                                            'PycharmProjects/Spawner3/graphics/sprites/buttons/settings.png')

        button_continue_rect = button_continue.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 2))
        button_settings_rect = button_settings.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 6 * 3.75))
        button_quit_rect = button_quit.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 4 * 3))

        pause_menu = pygame.Surface((Config.WIDTH, Config.HEIGHT))

        pause_menu.fill("black")
        pause_menu.set_alpha(225)

        pause_menu.blit(button_continue, button_continue_rect)
        pause_menu.blit(button_settings, button_settings_rect)
        pause_menu.blit(button_quit, button_quit_rect)

        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        if button_continue_rect.collidepoint(mouse) and pressed[0]:
            return False
        if button_quit_rect.collidepoint(mouse) and pressed[0]:
            sys.exit()

        screen.blit(pause_menu, (0, 0))

        pygame.display.update()

        return True

    @staticmethod
    def start_menu(screen):
        # background = pygame.image.load('C:/Users/kudro/'
        #                                 'PycharmProjects/Spawner3/graphics/sprites/background/background.png')
        button_play = pygame.image.load('C:/Users/kudro/'
                                        'PycharmProjects/Spawner3/graphics/sprites/buttons/play.png')
        button_settings = pygame.image.load('C:/Users/kudro/'
                                            'PycharmProjects/Spawner3/graphics/sprites/buttons/settings.png')
        button_quit = pygame.image.load('C:/Users/kudro/'
                                        'PycharmProjects/Spawner3/graphics/sprites/buttons/quit.png')

        button_play_rect = button_play.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 2))
        button_settings_rect = button_settings.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 6 * 3.75))
        button_quit_rect = button_quit.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 4 * 3))

        main_menu = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        main_menu.fill('Green')

        font = pygame.font.Font(None, 72)
        text = font.render("Spawner3", True, 'Black')
        text_rect = text.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 3))
        main_menu.blit(text, text_rect)

        main_menu.blit(button_play, button_play_rect)
        main_menu.blit(button_settings, button_settings_rect)
        main_menu.blit(button_quit, button_quit_rect)

        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        if button_play_rect.collidepoint(mouse) and pressed[0]:
            return False
        if button_settings_rect.collidepoint(mouse) and pressed[0]:
            pass
        if button_quit_rect.collidepoint(mouse) and pressed[0]:
            sys.exit()

        screen.blit(main_menu, (0, 0))

        pygame.display.update()

        return True

    @staticmethod
    def settings(screen):
        pass