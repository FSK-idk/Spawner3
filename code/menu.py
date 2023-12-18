import sys
import pygame_widgets
import webbrowser
from tile import *
from pygame_widgets.slider import Slider


class Menu:
    start_menu_active = True
    pause_menu_active = False
    settings_active = False
    developers_menu_active = False

    volume = 100

    pygame.font.init()
    small_font = pygame.font.SysFont('Corbel', 35)

    settings_screen = pygame.Surface((Config.WIDTH, Config.HEIGHT))
    settings_screen.fill('Green')

    slider = Slider(settings_screen,
                    Config.WIDTH // 2 - 200,
                    Config.HEIGHT // 2,
                    400,
                    20,
                    min=0,
                    max=100,
                    step=1
                    )

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

        for event in pygame.event.get():
            if button_continue_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                return False
            if button_settings_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                Menu.settings_active = True
            if button_quit_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                Menu.start_menu_active = True

        screen.blit(pause_menu, (0, 0))

        pygame.display.update()

        return True

    @staticmethod
    def start_menu(screen) -> bool:
        # background = pygame.image.load('../graphics/gui/background/background.png')
        button_play = pygame.image.load('../graphics/gui/buttons/play.png')
        button_settings = pygame.image.load('../graphics/gui/buttons/settings.png')
        button_developers = pygame.image.load('../graphics/gui/buttons/settings.png')
        button_quit = pygame.image.load('../graphics/gui/buttons/quit.png')

        button_play_rect = button_play.get_rect(
            center=(Config.WIDTH / 2, Config.HEIGHT / 2)
        )
        button_settings_rect = button_settings.get_rect(
            center=(Config.WIDTH / 2, Config.HEIGHT / 6 * 3.67)
        )
        button_developers_rect = button_developers.get_rect(
            center=(Config.WIDTH / 2, Config.HEIGHT / 4 * 2.87)
        )
        button_quit_rect = button_quit.get_rect(
            center=(Config.WIDTH / 2, Config.HEIGHT / 4 * 3.3)
        )

        main_menu = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        main_menu.fill('Green')

        font = pygame.font.Font(None, 72)
        text = font.render("Spawner3", True, 'Black')
        text_rect = text.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 3))
        main_menu.blit(text, text_rect)

        main_menu.blit(button_play, button_play_rect)
        main_menu.blit(button_settings, button_settings_rect)
        main_menu.blit(button_developers, button_developers_rect)
        main_menu.blit(button_quit, button_quit_rect)

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if button_play_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                return False
            if button_settings_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                Menu.settings_active = True
            if button_developers_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                Menu.developers_menu_active = True
            if button_quit_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
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

        for event in pygame.event.get():
            if button_quit_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                Menu.settings_active = False

        pygame_widgets.update(pygame.event.get())

        screen.blit(Menu.settings_screen, (0, 0))

        pygame.display.update()

    @staticmethod
    def developers(screen):
        button_quit = pygame.image.load('../graphics/gui/buttons/quit.png')

        profile1 = pygame.image.load('../graphics/gui/profile/profile1.png')
        profile2 = pygame.image.load('../graphics/gui/profile/profile2.png')
        profile3 = pygame.image.load('../graphics/gui/profile/profile3.png')
        profile4 = pygame.image.load('../graphics/gui/profile/profile4.png')

        profile1_rect = profile1.get_rect()
        profile1_rect.x = Config.WIDTH / 10
        profile1_rect.y = Config.WIDTH / 9

        profile2_rect = profile2.get_rect()
        profile2_rect.x = Config.WIDTH / 3.2
        profile2_rect.y = Config.WIDTH / 9

        profile3_rect = profile3.get_rect()
        profile3_rect.x = Config.WIDTH / 1.9
        profile3_rect.y = Config.WIDTH / 9

        profile4_rect = profile4.get_rect()
        profile4_rect.x = Config.WIDTH / 1.35
        profile4_rect.y = Config.WIDTH / 9

        button_quit_rect = button_quit.get_rect(
            center=(Config.WIDTH / 2, Config.HEIGHT / 6 * 4)
        )

        font = pygame.font.Font(None, 50)
        small_font = pygame.font.Font(None, 35)

        text = font.render('Разработчики:', True, 'Black')
        text_rect = text.get_rect(center=(Config.WIDTH / 2, Config.HEIGHT / 8))

        name_text1 = small_font.render('Симанков Александр', True, 'Black')
        name_text1_rect = name_text1.get_rect()
        name_text1_rect.x = Config.WIDTH / 10
        name_text1_rect.y = Config.WIDTH / 3.2

        name_text2 = small_font.render('Рыбкин Владимир', True, 'Black')
        name_text2_rect = name_text1.get_rect()
        name_text2_rect.x = Config.WIDTH / 3.2
        name_text2_rect.y = Config.WIDTH / 3.2

        name_text3 = small_font.render('Верхов Владимир', True, 'Black')
        name_text3_rect = name_text1.get_rect()
        name_text3_rect.x = Config.WIDTH / 1.9
        name_text3_rect.y = Config.WIDTH / 3.2

        name_text4 = small_font.render('Можаров Дмитрий', True, 'Black')
        name_text4_rect = name_text1.get_rect()
        name_text4_rect.x = Config.WIDTH / 1.35
        name_text4_rect.y = Config.WIDTH / 3.2

        developers_menu = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        developers_menu.fill('Green')

        developers_menu.blit(button_quit, button_quit_rect)
        developers_menu.blit(text, text_rect)

        developers_menu.blit(name_text1, name_text1_rect)
        developers_menu.blit(name_text2, name_text2_rect)
        developers_menu.blit(name_text3, name_text3_rect)
        developers_menu.blit(name_text4, name_text4_rect)

        developers_menu.blit(profile1, profile1_rect)
        developers_menu.blit(profile2, profile2_rect)
        developers_menu.blit(profile3, profile3_rect)
        developers_menu.blit(profile4, profile4_rect)

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if button_quit_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                Menu.developers_menu_active = False

            if profile1_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                webbrowser.open_new('https://github.com/Fotlex')
            if profile2_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                webbrowser.open_new('https://github.com/FSK-idk')
            if profile3_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                webbrowser.open_new('https://github.com/verhovv')
            if profile4_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
                webbrowser.open_new('https://github.com/dmitry416')

        screen.blit(developers_menu, (0, 0))

        pygame.display.update()
