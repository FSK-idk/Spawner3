import sys
import pygame
from settings import *
from support import *
from tile import *
from player import Player


class Menu:
    pygame.font.init()
    smallfont = pygame.font.SysFont('Corbel', 35)

    @staticmethod
    def show(screen):
        text_quit = Menu.smallfont.render('quit', True, "Black")
        text_continue = Menu.smallfont.render("continue", True, "Black")

        text_quit_rect = text_quit.get_rect(center=(WIDTH / 2, HEIGHT / 4 * 3))

        text_continue_rect = text_continue.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        pause_menu = pygame.Surface((WIDTH, HEIGHT),)
        #pause_panel = pygame.Surface((WIDTH / 2, HEIGHT / 2), 4)
        #pause_panel.fill("white")
        pause_menu.fill("black")
        pause_menu.set_alpha(150)

        button_quit = pygame.Surface((text_quit.get_rect().width, text_quit.get_rect().height))
        button_continue = pygame.Surface((text_continue.get_rect().width, text_continue.get_rect().height))

        #rect_width, rect_height = 600, 600
        #rect_x = (WIDTH - rect_width) // 2
        #rect_y = (HEIGHT - rect_height) // 2
        #pygame.draw.rect(screen, "white", (rect_x, rect_y, rect_width, rect_height))

        button_quit.fill("Grey")
        button_continue.fill("Grey")

        button_quit.blit(text_quit, (0, 0))
        button_continue.blit(text_continue, (0, 0))

        pause_menu.blit(button_quit, text_quit_rect)
        pause_menu.blit(button_continue, text_continue_rect)

        #pause_panel.blit(button_quit, text_quit_rect)
        #pause_panel.blit(button_continue, text_continue_rect)

        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        if text_quit_rect.collidepoint(mouse) and pressed[0]:
            sys.exit()

        if text_continue_rect.collidepoint(mouse) and pressed[0]:
            return False

        screen.blit(pause_menu, (0, 0))
        #screen.blit(pause_panel, (0, 0))

        pygame.display.update()
        return True
