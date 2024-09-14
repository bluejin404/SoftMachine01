from gym.envs.registration import register

register(
    id='bipedal_robot-v0',
    entry_point='bipedal_robot.envs:BipedalRobot',
)