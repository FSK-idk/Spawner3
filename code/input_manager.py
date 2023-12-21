import pygame


class InputManager:
    interact = [pygame.K_e]

    pause = [pygame.K_ESCAPE]
    contin = [pygame.K_SPACE]

    go_right = [pygame.K_RIGHT, pygame.K_d]
    go_left = [pygame.K_LEFT, pygame.K_a]
    go_up = [pygame.K_UP, pygame.K_w]
    go_down = [pygame.K_DOWN, pygame.K_s]

    events = []

    @staticmethod
    def is_pressed(codes: list[int]) -> bool:
        keys = pygame.key.get_pressed()
        return any(map(lambda key: keys[key], codes))

    @staticmethod
    def get_event(type: int) -> pygame.event.Event:
        for event in InputManager.events:
            if event.type == type:
                return event
        return None
