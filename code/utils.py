# support functions for working with files

import pygame
from csv import reader
from os import walk
from os.path import dirname, abspath


# path to csv file
def import_csv_layout(path) -> list:
    layout = []

    with open(path) as level_layout:
        layout_table = reader(level_layout, delimiter=",")
        for row in layout_table:
            layout.append(list(row))

    return layout


# better import
def import_layouts(level_name, layers) -> dict:
    layouts = {}

    for layer in layers:
        layouts[layer] = import_csv_layout(
            get_parent_dir() + f"/levels/{level_name}/{level_name}_{layer}.csv"
        )

    return layouts


# path to the folder containing sprites
def import_surfaces(path) -> list:
    surf_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)

    return surf_list


# path to the sprite
def import_surface(path):
    surf = pygame.image.load(path).convert_alpha()
    return surf


# path to the folder with the mask, mask file name without extension
def import_mask(path, name):
    full_path = path + name + ".png"
    mask = pygame.mask.from_surface(pygame.image.load(full_path).convert_alpha())
    return mask


# path to the folder with the ysort
def import_ysort(path):
    full_path = path + "ysort.png"
    ysort = pygame.image.load(full_path).convert_alpha().get_rect()

    return ysort


def get_parent_dir(path=__file__) -> str:
    return dirname(dirname(abspath(path)))
