import pygame

from utils import get_parent_dir

UPDATE_STATE = pygame.USEREVENT + 1
UPDATE_GAMEPLAY_STATE = pygame.USEREVENT + 2

pygame.font.init()


class GameData:
    project_folder = get_parent_dir()
    tile_size = 32

    # wood - stone
    woodcutter_upgrade = [(20, 0), (500, 600), (900, 1000)]
    miner_upgrade = [(10, 10), (600, 500), (1000, 900)]
    cats_upgrade = [(800, 800), (1500, 1500)]

    wood_gain = [1, 20, 50, 100]
    stone_gain = [1, 20, 50, 100]

    # npc
    mesenev_phrases = [
        "ХАХАХА! Программирование",
        "9 программистов не могут родить одного ребенка за месяц",
        "Надо же было спавнер на расте написать!",
        "Я люблю своих учеников",
        "Кто не сдаст 16 задач на хаскеле - в бан!",
        "Да мне все равно, я на доске программирую!",
        "Вопрос не придумали? Двойка Вам за пару"
    ]

    # level updates
    update_list = []
    is_update_all_sprites = False
    is_update_background = False

    # fonts
    font_lana150 = pygame.font.Font(
        project_folder + "/graphics/font/LanaPixel.ttf", 150)

    font_lana50 = pygame.font.Font(
        project_folder + "/graphics/font/LanaPixel.ttf", 50)

    font_lana30 = pygame.font.Font(
        project_folder + "/graphics/font/LanaPixel.ttf", 30)

    font_lana11 = pygame.font.Font(
        project_folder + "/graphics/font/LanaPixel.ttf", 11)

    font_mago16 = pygame.font.Font(
        project_folder + "/graphics/font/mago2.ttf", 16)
