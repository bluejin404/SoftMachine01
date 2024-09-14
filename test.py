import gym
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from bipedal_robot.envs import bipedal_robot_env

env_name = 'bipedal_robot-v0'

log_dir = "PPO_trained_model"
if not os.path.exists(log_dir):
        os.makedirs(log_dir)
log_dir = log_dir + '/' + env_name+ '/'
stats_path = os.path.join(log_dir, "vec_normalize.pkl")

env = gym.make(env_name)
env.settings(rend = True, train = False)
vec_env = DummyVecEnv([lambda: env])
vec_env = VecNormalize.load(stats_path, vec_env)
vec_env.training = False
vec_env.norm_reward = False

model = PPO.load(log_dir + "ppo_" + env_name, env=vec_env)
obs = vec_env.reset()
for _ in range(10000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)