import pygame

from csv import reader
from os import walk
from os.path import dirname, abspath


def import_csv_layout(path: str) -> list:
    """
    Args:
        path: path to a .csv file with the extension
    """
    layout = []

    with open(path) as level_layout:
        layout_table = reader(level_layout, delimiter=",")
        for row in layout_table:
            layout.append(list(row))

    return layout


def import_layouts(level_name: str, layers: str) -> dict:
    layouts = {}

    for layer in layers:
        layouts[layer] = import_csv_layout(
            get_parent_dir() + f"/levels/{level_name}/{level_name}_{layer}.csv"
        )

    return layouts


def import_surfaces(path: str) -> list:
    """
    Args:
        path: path to the folder where the images are stored
    """
    surf_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)

    return surf_list


def import_surface(path: str) -> pygame.Surface:
    """
    Args:
        path: path to the image with extension
    """
    surf = pygame.image.load(path).convert_alpha()
    return surf


def import_mask(path: str) -> pygame.Surface:
    """
    Args:
        path: path to the image with extension
    """
    mask = pygame.mask.from_surface(
        pygame.image.load(path).convert_alpha())
    return mask


def import_ysort(path: str) -> pygame.rect.Rect:
    """
    Args:
        path: path to the image with extension
    """
    ysort = pygame.image.load(path).convert_alpha().get_rect()

    return ysort


def get_parent_dir(path: str = __file__) -> str:
    """
    Args:
        path: path to the file whose folder is needed

    """
    return dirname(dirname(abspath(path)))
