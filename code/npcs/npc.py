import pygame

from random import choice
from core.utils import import_surfaces, import_ysort, import_mask
from npcs.cost_bubble import CostBubble
from npcs.text_cloud import TextCloud
from data.game_data import GameData
from data.save_data import save_data
from components.animation_component import AnimationComponent


class NPC(pygame.sprite.Sprite, AnimationComponent):
    def __init__(self, npc_groups: list, subgroups: list,
                 path: str, pos: (int, int), type: str) -> None:
        """
        Args:
            subgroups: groups to show bubble and cloud
            path: path to the NPC folder
        """
        pygame.sprite.Sprite.__init__(self, npc_groups)
        self.folder = path
        self.type = type
        self.position = pos

        # image
        self.root_image = import_surfaces(self.folder + "animation/")[0]
        self.image = self.root_image
        self.rect = self.image.get_rect(midbottom=self.position)

        # sort
        self.ysort = import_ysort(self.folder + "ysort.png")
        self.ysort.midtop = self.rect.midtop

        # collision
        self.mask = import_mask(self.folder + "mask.png")
        self.interact_mask = import_mask(self.folder + "interact_mask.png")

        # bubble and cloud
        self.subgroups = subgroups

        self.is_show_bubble = False
        self.cost_bubble = None
        self.text_cloud = None

        # cooldown
        self.cooldown = 2000
        self.start_time = 0
        self.is_interact = False

        # animation
        AnimationComponent.__init__(self, self.folder)
        self.frame_rate = 6

    def collide(self, show: bool) -> None:
        if self.type != "mesenev":
            if self.is_show_bubble == False and show:
                if ((self.type == "woodcutter" and save_data.tree_level == 3)
                    or (self.type == "miner" and save_data.rock_level == 3)
                        or (self.type == "laptop" and save_data.cats_level == 2)):
                    return

                self.cost_bubble = CostBubble(
                    self.subgroups, (
                        self.rect.left + self.root_image.get_size()[0] // 2,
                        self.rect.top),
                    self.type)

                self.is_show_bubble = True
                GameData.update_list.append(self.cost_bubble)

            elif self.is_show_bubble == True and not show:
                self.cost_bubble.kill()
                self.is_show_bubble = False

        if self.type == "mesenev" and self.text_cloud:
            self.text_cloud.run()

    def interact(self) -> None:
        current_time = pygame.time.get_ticks()

        if not self.is_interact:
            self.is_interact = True
            self.start_time = pygame.time.get_ticks()

            # interact
            if self.type == "woodcutter" and save_data.tree_level < 3:
                wood, stone = GameData.woodcutter_upgrade[save_data.tree_level]
                if (save_data.wood_amount >= wood
                        and save_data.stone_amount >= stone):
                    save_data.wood_amount -= wood
                    save_data.stone_amount -= stone
                    save_data.tree_level += 1

                    self.collide(False)
                    GameData.is_update_all_sprites = True

            if self.type == "miner" and save_data.rock_level < 3:
                wood, stone = GameData.miner_upgrade[save_data.rock_level]
                if (save_data.wood_amount >= wood
                        and save_data.stone_amount >= stone):
                    save_data.wood_amount -= wood
                    save_data.stone_amount -= stone
                    save_data.rock_level += 1

                    self.collide(False)
                    GameData.is_update_all_sprites = True

            if self.type == "laptop" and save_data.cats_level < 2:
                wood, stone = GameData.cats_upgrade[save_data.cats_level]
                if (save_data.wood_amount >= wood
                        and save_data.stone_amount >= stone):
                    save_data.wood_amount -= wood
                    save_data.stone_amount -= stone
                    save_data.cats_level += 1

                    self.collide(False)
                    GameData.is_update_background = True
                    GameData.is_update_all_sprites = True

            if self.type == "mesenev":
                if self.text_cloud:
                    self.text_cloud.kill()

                self.text_cloud = TextCloud(
                    choice(GameData.mesenev_phrases),
                    self.subgroups, (
                        self.rect.left + self.root_image.get_size()[0] // 2,
                        self.rect.top))

        if (self.is_interact
                and current_time - self.start_time >= self.cooldown):
            self.is_interact = False

    def update(self) -> None:
        self.animate()
