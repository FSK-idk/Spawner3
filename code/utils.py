# support functions for working with files

import pygame
from csv import reader
from os import walk
from os.path import dirname, abspath
from collections import defaultdict


def import_csv_layout(path):
    layout = []

    with open(path) as level_layout:
        layout_table = reader(level_layout, delimiter=",")
        for row in layout_table:
            layout.append(list(row))

    return layout


def import_layouts(level_name, layers):
    layouts = {}

    for layer in layers:
        layouts[layer] = import_csv_layout(
            get_parent_dir() + f"/levels/{level_name}/{level_name}_{layer}.csv"
        )

    return layouts


def import_surfaces(path):
    surf_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)

    return surf_list


def get_parent_dir(path=__file__):
    return dirname(dirname(abspath(path)))
