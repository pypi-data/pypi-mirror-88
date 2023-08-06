from gym.envs.registration import register

register(
    id="Cabworld-v0",
    entry_point="gym_cabworld.envs:CustomEnv0",
    max_episode_steps=3000,
)

register(
    id="Cabworld-v1",
    entry_point="gym_cabworld.envs:CustomEnv1",
    max_episode_steps=3000,
)

register(
    id="Cabworld-v2",
    entry_point="gym_cabworld.envs:CustomEnv2",
    max_episode_steps=3000,
)

register(
    id="Cabworld-v3",
    entry_point="gym_cabworld.envs:MarlEnv",
    max_episode_steps=3000,
)

register(
    id="Cabworld-v4",
    entry_point="gym_cabworld.envs:CustomEnv4",
    max_episode_steps=3000,
)

register(
    id="Cabworld-v5",
    entry_point="gym_cabworld.envs:CustomEnv5",
    max_episode_steps=3000,
)

register(
    id="Cabworld-v6",
    entry_point="gym_cabworld.envs:CustomEnv6",
    max_episode_steps=3000,
)

register(
    id="Cabworld-v7",
    entry_point="gym_cabworld.envs:MarlEnv2",
    max_episode_steps=3000,
)
