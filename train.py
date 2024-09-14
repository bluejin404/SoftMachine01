import gym
import os
from datetime import datetime
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from bipedal_robot.envs import bipedal_robot_env

render = True
env_name = 'bipedal_robot-v0'
start_time = datetime.now().replace(microsecond=0)

env = gym.make(env_name)
env.settings(rend = render, train = True)
vec_env = DummyVecEnv([lambda: env])
vec_env = VecNormalize(vec_env, norm_obs=True, norm_reward=True, clip_obs=10.)
model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=400_000)

log_dir = "PPO_trained_model"
if not os.path.exists(log_dir):
        os.makedirs(log_dir)
log_dir = log_dir + '/' + env_name+ '/'
if not os.path.exists(log_dir):
        os.makedirs(log_dir)

model.save(log_dir + "ppo_" + env_name)
stats_path = os.path.join(log_dir, "vec_normalize.pkl")
vec_env.save(stats_path)

print("modelsaved at" + log_dir)

end_time = datetime.now().replace(microsecond=0)

print("--------------------------------------------------------------------------------------------")
print("Started training at : ", start_time)
print("Finished training at : ", end_time)
print("Total training time : ", end_time - start_time)
print("--------------------------------------------------------------------------------------------")

