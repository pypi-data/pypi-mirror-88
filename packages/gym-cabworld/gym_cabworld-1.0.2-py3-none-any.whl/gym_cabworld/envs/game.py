import os
from random import randint
import random

import pygame

from gym_cabworld.envs.cab_model import Cab
from gym_cabworld.envs.map_model import Map
from gym_cabworld.envs.passenger_model import Passenger

screen_width = 1000
screen_height = 1000
number_passengers = 2
respawn_rate = 500


class Game:
    def __init__(self, game_mode):
        """
        Create Pygame with map, cab, passenger
        """
        pygame.init()
        pygame.display.set_caption("Cabworld-v" + str(game_mode))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        pygame.time.get_ticks()

        dirname = os.path.dirname(__file__)
        self.img_path = os.path.join(dirname, "..", "images")
        data_path = os.path.join(dirname, "..", "data")
        self.game_mode = game_mode

        if game_mode < 4:
            img = "map_gen.png"
        else:
            img = "small_map_gen.png"

        self.map = Map(
            os.path.join(self.img_path, img), screen_width, game_mode, data_path
        )
        self.grid_size = self.map.get_grid_size()

        if (game_mode % 4) == 0:
            self.add_passenger()
            cab_pos = [int(1.5 * self.grid_size), int(1.5 * self.grid_size)]

        elif (game_mode % 4) == 1:
            for _ in range(3):
                self.add_passenger()
            cab_pos = [int(1.5 * self.grid_size), int(1.5 * self.grid_size)]

        elif (game_mode % 4) == 2:
            for _ in range(3):
                self.add_passenger()
            cab_pos = self.map.get_random_pos_on_map()

        self.cab = Cab(
            os.path.join(self.img_path, "cab.png"), self.map, cab_pos, self.grid_size
        )
        self.game_speed = 60
        self.mode = 0
        self.steps = 0

    def add_passenger(self):
        """ "
        Add passenger with random position and destination on map
        """
        random_pos = self.map.get_random_pos_on_map()
        random_dest = self.map.get_random_pos_on_map()
        img = "person_" + str(randint(1, 3)) + ".png"
        passenger = Passenger(
            os.path.join(self.img_path, img),
            self.map,
            random_pos,
            0,
            random_dest,
            self.grid_size,
        )
        self.map.add_passenger(passenger)

    def action(self, action):
        """ "
        Execute action on cab
        @param action: action to perform
        """
        # reset rewards
        self.cab.rewards = 0

        if action == 0:
            self.cab.move_forward()
        if action == 1:
            self.cab.turn_left()
        elif action == 2:
            self.cab.turn_right()
        elif action == 3:
            self.cab.pick_up_passenger()
        elif action == 4:
            self.cab.drop_off_passenger()

        self.cab.update()
        self.steps += 1

        if (respawn_rate % self.steps) == 0:
            self.add_passenger()

    def evaluate(self):
        """ "
        Evaluate rewards
        @return reward
        """
        return self.cab.rewards

    def is_done(self):
        """ "
        Check if all passengers have reached their destination
        @return bool
        """
        return self.map.all_passengers_reached_dest()

    def normalise(self, state):
        """ "
        Normalise state
        @param state
        @return normalised state
        """
        features = []
        for i in range(5):
            if state[i] == 1:
                features.append(1)
            else:
                features.append(-1)
        for j in range(5, len(state)):
            features.append(state[j] / (screen_width - int(1.5 * self.grid_size)))

        # fill up the state if not enough passengers
        for _ in range(len(state), 19):
            features.append(-1)
        return tuple(features)

    def observe(self):
        """ "
        Observe environment
        @return state of environment
        """
        # Possible actions
        r1, r2, r3 = self.cab.radars
        pick_up = self.cab.pick_up_possible
        drop_off = self.cab.drop_off_possible
        # own position
        pos_x, pos_y = self.cab.pos
        state = [r1, r2, r3, pick_up, drop_off, round(pos_x), round(pos_y)]
        for passenger in self.cab.next_passengers:
            pass_x, pass_y = passenger.pos
            dest_x, dest_y = passenger.destination
            state.append(pass_x)
            state.append(pass_y)
            state.append(dest_x)
            state.append(dest_y)
        return self.normalise(state)

    def view(self):
        """
        Render environment using Pygame
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.blit(self.map.map_img, (0, 0))
        if self.mode == 1:
            self.screen.fill((0, 0, 0))

        self.cab.check_radar()
        self.cab.draw(self.screen)
        self.map.draw_passengers(self.screen)

        pygame.display.flip()
        self.clock.tick(self.game_speed)
