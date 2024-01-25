from data.save_data import save_data
from core.utils import import_surfaces


class AnimationComponent():
    def __init__(self, folder) -> None:
        # animation
        self.frame_rate = 2
        self.frame_index = 0
        self.root_animation_images = import_surfaces(
            folder + "animation/")
        self.animation_images = self.root_animation_images.copy()

    def animate(self) -> None:
        animations = self.animation_images

        # change frame index
        self.frame_index += self.frame_rate / save_data.fps
        if self.frame_index >= len(animations):
            self.frame_index = 0

        self.image = animations[int(self.frame_index)]
