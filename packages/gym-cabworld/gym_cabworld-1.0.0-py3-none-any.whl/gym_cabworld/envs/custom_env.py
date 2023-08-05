import gym
import numpy as np
from gym import spaces

from gym_cabworld.envs.game import Game
from gym_cabworld.envs.game_multi_agent import MultiAgentGame


class CustomEnv(gym.Env):
    def __init__(self, mode):
        """
        Create OpenAiGym with Pygame
        """
        self.mode = mode
        self.pygame = Game(self.mode)
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), np.array(
            [1, 1, 1, 1, 1, 1000, 1000, 1000, 1000, 1000, 1000]), dtype=np.int)

    def reset(self):
        """
        Reset Game
        """
        del self.pygame
        self.pygame = Game(self.mode)
        obs = self.pygame.observe()
        return obs

    def step(self, actions):
        """
        Execute one step in environment
        """
        self.pygame.action(actions)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        """
        Render PyGame
        """
        self.pygame.view()


class CustomEnv0(CustomEnv):
    def __init__(self):
        """
        Partial Dynamic: Fixed cab and three random passengers
        """
        super().__init__(0)


class CustomEnv1(CustomEnv):
    def __init__(self):
        """
        Partial Dynamic: Fixed cab and three random passengers
        """
        super().__init__(1)


class CustomEnv2(CustomEnv):
    def __init__(self):
        """
        Partial Dynamic: Fixed cab and three random passengers
        """
        super().__init__(2)


class MarlEnv(CustomEnv):
    def __init__(self):
        """
        Multi Agent with 2 random cabs and 3 random passengers
        """
        self.pygame = MultiAgentGame(3)
        number_cabs = self.pygame.number_cabs
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * number_cabs), np.array(
            [1, 1, 1, 1, 1, 1000, 1000, 1000, 1000, 1000, 1000] * number_cabs), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = MultiAgentGame(3)
        obs = self.pygame.observe()
        return obs


class CustomEnv4(CustomEnv):
    def __init__(self):
        """
        Partial Dynamic: Fixed cab and three random passengers
        """
        super().__init__(4)


class CustomEnv5(CustomEnv):
    def __init__(self):
        """
        Partial Dynamic: Fixed cab and three random passengers
        """
        super().__init__(5)


class CustomEnv6(CustomEnv):
    def __init__(self):
        """
        Partial Dynamic: Fixed cab and three random passengers
        """
        super().__init__(6)


class MarlEnv2(CustomEnv):
    def __init__(self):
        """
        Multi Agent with 2 random cabs and 3 random passengers
        """
        self.pygame = MultiAgentGame(7)
        number_cabs = self.pygame.number_cabs
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * number_cabs), np.array(
            [1, 1, 1, 1, 1, 1000, 1000, 1000, 1000, 1000, 1000] * number_cabs), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = MultiAgentGame(7)
        obs = self.pygame.observe()
        return obs
