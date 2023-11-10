# support functions for working with files

import pygame
from csv import reader
from os import walk


def import_csv_layout(path):
    layout = []

    with open(path) as level_layout:
        layout_table = reader(level_layout, delimiter=",")
        for row in layout_table:
            layout.append(list(row))

    return layout


def import_surfaces(path):
    surf_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)

    return surf_list
