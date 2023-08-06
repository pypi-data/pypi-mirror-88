import os
import random
from random import randint

import pygame

from gym_cabworld.envs.cab_model import Cab
from gym_cabworld.envs.game import Game
from gym_cabworld.envs.map_model import Map
from gym_cabworld.envs.passenger_model import Passenger

screen_width = 1000
screen_height = 1000
number_passengers = 3
number_cabs = 2

random.seed(0)


class MultiAgentGame(Game):
    def __init__(self, game_mode):
        """
        Multi agent world
        """
        pygame.init()
        pygame.display.set_caption("Cabworld-v3")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.number_cabs = number_cabs

        dirname = os.path.dirname(__file__)
        self.img_path = os.path.join(dirname, "..", "images")
        data_path = os.path.join(dirname, "..", "data")

        if game_mode < 4:
            img = "map_gen.png"
        else:
            img = "small_map_gen.png"

        self.map = Map(
            os.path.join(self.img_path, img), screen_width, game_mode, data_path
        )
        self.grid_size = self.map.get_grid_size()

        for _ in range(number_passengers):
            self.add_passenger()

        self.cabs = []
        for _ in range(number_cabs):
            random_pos = self.map.get_random_pos_on_map()
            cab = Cab(
                os.path.join(self.img_path, "cab.png"),
                self.map,
                random_pos,
                self.grid_size,
            )
            self.cabs.append(cab)

        self.game_speed = 60
        self.mode = 0

    def action(self, actions):
        """ "
        Execute action on cab
        @param actions: action to perform
        """
        assert len(actions) == len(self.cabs)
        for cab, action in zip(self.cabs, actions):
            cab.rewards = 0
            if action == 0:
                cab.move_forward()
            if action == 1:
                cab.turn_left()
            elif action == 2:
                cab.turn_right()
            elif action == 3:
                cab.pick_up_passenger()
            elif action == 4:
                cab.drop_off_passenger()
            cab.update()

    def evaluate(self):
        """ "
        Evaluate rewards
        @return reward
        """
        return [cab.rewards for cab in self.cabs]

    def is_done(self):
        """ "
        Check if all passengers have reached their destination
        @return bool
        """
        return self.map.all_passengers_reached_dest()

    def observe(self):
        """ "
        Observe environment
        @return state of environment
        """
        observations = []
        for cab in self.cabs:
            # Possible actions
            r1, r2, r3 = cab.radars
            pick_up = cab.pick_up_possible
            drop_off = cab.drop_off_possible
            # own position
            pos_x, pos_y = cab.pos
            state = [r1, r2, r3, pick_up, drop_off, round(pos_x), round(pos_y)]
            for passenger in cab.next_passengers:
                pass_x, pass_y = passenger.pos
                dest_x, dest_y = passenger.destination
                state.append(pass_x)
                state.append(pass_y)
                state.append(dest_x)
                state.append(dest_y)
            observations.append(self.normalise(state))
        return observations

    def view(self):
        """ "
        Render environment using Pygame
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.mode += 1
                    self.mode = self.mode % 3

        self.screen.blit(self.map.map_img, (0, 0))
        if self.mode == 1:
            self.screen.fill((0, 0, 0))

        for cab in self.cabs:
            cab.check_radar()
            cab.draw(self.screen)

        self.map.draw_passengers(self.screen)
        pygame.display.flip()
        self.clock.tick(self.game_speed)
