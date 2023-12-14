import sys
from tile import *
import pygame_widgets
from pygame_widgets.slider import Slider


class Menu:
    start_menu_active = True
    pause_menu_active = False
    settings_active = False

    timer = 0
    clock = pygame.time.Clock()

    volume = 100

    pygame.font.init()
    small_font = pygame.font.SysFont('Corbel', 35)

    settings_screen = pygame.Surface((Config.WIDTH, Config.HEIGHT))
    settings_screen.fill('Green')

    slider = Slider(settings_screen, Config.WIDTH // 2 - 200, Config.HEIGHT // 2,
                    400, 20, min=0, max=100, step=1)

    @staticmethod
    def pause_menu(screen) -> bool:
        button_quit = pygame.image.load('../graphics/gui/buttons/quit.png')
        button_continue = pygame.image.load('../graphics/gui/buttons/continue.png')
        button_settings = pygame.image.load('../graphics/gui/buttons/settings.png')

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
        if button_settings_rect.collidepoint(mouse) and pressed[0]:
            Menu.settings_active = True
        if button_quit_rect.collidepoint(mouse) and pressed[0]:
            sys.exit()

        screen.blit(pause_menu, (0, 0))

        pygame.display.update()

        return True

    @staticmethod
    def start_menu(screen) -> bool:
        # background = pygame.image.load('../graphics/gui/background/background.png')
        button_play = pygame.image.load('../graphics/gui/buttons/play.png')
        button_settings = pygame.image.load('../graphics/gui/buttons/settings.png')
        button_quit = pygame.image.load('../graphics/gui/buttons/quit.png')

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
            Menu.settings_active = True
        if button_quit_rect.collidepoint(mouse) and pressed[0]:
            sys.exit()

        screen.blit(main_menu, (0, 0))

        pygame.display.update()

        return True

    @staticmethod
    def settings(screen) -> None:
        Menu.volume = Menu.slider.getValue()
        Menu.settings_screen.fill('Green')
        # background = pygame.image.load('../graphics/gui/background/background.png')
        button_quit = pygame.image.load('../graphics/gui/buttons/quit.png')

        font = pygame.font.Font(None, 50)
        text = font.render('Звук:', True, 'Black')
        text_rect = text.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 3))
        Menu.settings_screen.blit(text, text_rect)

        volume_level = font.render(f'{Menu.volume}%', True, 'Black')
        Menu.settings_screen.blit(volume_level, (Config.WIDTH / 2.13, Config.HEIGHT / 2.5))

        button_quit_rect = button_quit.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 6 * 4))
        Menu.settings_screen.blit(button_quit, button_quit_rect)

        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        if button_quit_rect.collidepoint(mouse) and pressed[0]:
            Menu.settings_active = False

        pygame_widgets.update(pygame.event.get())

        screen.blit(Menu.settings_screen, (0, 0))

        pygame.display.update()
