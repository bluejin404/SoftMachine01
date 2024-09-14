import os
import gym
from gym import spaces
import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import math
import pylab

env_name = "bipedal_robot-v0"
xml_path = 'bipedal_robot.xml'
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0
scores, episodes = [], []
_overlay = {}

def add_overlay(gridpos, text1, text2):
    if gridpos not in _overlay:
        _overlay[gridpos] = ["", ""]
    _overlay[gridpos][0] += text1 + "\n"
    _overlay[gridpos][1] += text2 + "\n"

def create_overlay(model, data, episode, total_return):
    topleft = mj.mjtGridPos.mjGRID_TOPLEFT
    topright = mj.mjtGridPos.mjGRID_TOPRIGHT
    bottomleft = mj.mjtGridPos.mjGRID_BOTTOMLEFT
    bottomright = mj.mjtGridPos.mjGRID_BOTTOMRIGHT
    add_overlay(bottomleft, "episode", str(episode) ,)
    add_overlay(bottomleft, "Time", '%.2f' % data.time,)
    add_overlay(bottomleft, "reward", '%.2f' % total_return,)

def init_controller(model,data):
    pass

def controller(model, data):
    pass

def keyboard(window, key, scancode, act, mods):
    if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
        mj.mj_resetData(model, data)
        mj.mj_forward(model, data)

def mouse_button(window, button, act, mods):
    global button_left
    global button_middle
    global button_right

    button_left = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
    button_middle = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
    button_right = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)
    glfw.get_cursor_pos(window)

def mouse_move(window, xpos, ypos):
    global lastx
    global lasty
    global button_left
    global button_middle
    global button_right
    dx = xpos - lastx
    dy = ypos - lasty
    lastx = xpos
    lasty = ypos

    if (not button_left) and (not button_middle) and (not button_right):
        return

    width, height = glfw.get_window_size(window)

    PRESS_LEFT_SHIFT = glfw.get_key(
        window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
    PRESS_RIGHT_SHIFT = glfw.get_key(
        window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
    mod_shift = (PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT)

    if button_right:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_MOVE_H
        else:
            action = mj.mjtMouse.mjMOUSE_MOVE_V
    elif button_left:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H
        else:
            action = mj.mjtMouse.mjMOUSE_ROTATE_V
    else:
        action = mj.mjtMouse.mjMOUSE_ZOOM

    mj.mjv_moveCamera(model, action, dx/height,
                      dy/height, scene, cam)

def scroll(window, xoffset, yoffset):
    action = mj.mjtMouse.mjMOUSE_ZOOM
    mj.mjv_moveCamera(model, action, 0.0, -0.05 *
                      yoffset, scene, cam)

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname + "/" + xml_path)
xml_path = abspath

model = mj.MjModel.from_xml_path(xml_path)  
data = mj.MjData(model)
cam = mj.MjvCamera()                    
opt = mj.MjvOption()                    

init_controller(model,data)
mj.set_mjcb_control(controller)

glfw.init()
window = glfw.create_window(1200, 900, env_name, None, None)
glfw.make_context_current(window)
glfw.swap_interval(1)
mj.mjv_defaultCamera(cam)
mj.mjv_defaultOption(opt)
glfw.set_key_callback(window, keyboard)
glfw.set_cursor_pos_callback(window, mouse_move)
glfw.set_mouse_button_callback(window, mouse_button)
glfw.set_scroll_callback(window, scroll)
scene = mj.MjvScene(model, maxgeom=10000)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)
cam.azimuth = 90
cam.elevation = -30
cam.distance =  3
cam.lookat =np.array([0.0 , 0 , 0])

class BipedalRobot(gym.Env):

    def __init__(self):
        self.action_space = spaces.Box(low=-1, high=1, shape=(6, ), dtype="float32") #set action space size, range
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(25,), dtype="float32") ##set observation space size, range
        self.done = False
        self.episode = 0
        self.train = False
        self.rend = True
        self.total_return = 0
        self.score_avg = 0

        self.sum_zpos_reward = 0
        self.sum_xvel_reward = 0
        self.sum_zvel_penalty = 0
        self.sum_tilt_penalty = 0
        self.life_time_reward = 0
        self.sum_life_time_reward = 0
        self.sum_torque_penalty = 0

        self.xvel_timestamp = [0, 0, 0, 0, 0]

    def step(self, action):
        self.xvel_timestamp[4] = self.xvel_timestamp[3]
        self.xvel_timestamp[3] = self.xvel_timestamp[2]
        self.xvel_timestamp[2] = self.xvel_timestamp[1]
        self.xvel_timestamp[1] = self.xvel_timestamp[0]
        self.xvel_timestamp[0] = -1 * data.qvel[1]

        for i in range(6):
            data.ctrl[i] = action[i] #set action
        time_prev = data.time
        while (data.time - time_prev < 1.0/60.0):
            mj.mj_step(model, data)
        state1 = [data.qpos[i] for i in range(13)]
        state2 = [data.qvel[i] for i in range(12)]
        state = state1 + state2

        if data.qpos[2] > 0.225:
            zpos_reward = 10
        else :
            zpos_reward = 1 / 2 * (abs(data.qpos[2] - 0.225) + 0.1)

        if sum(self.xvel_timestamp)/5 > 0.67:
            xvel_reward = 10
        else :
            xvel_reward = 10 * sum(self.xvel_timestamp)/5

        zvel_penalty = - 2 * abs(data.qvel[2])
        tilt_penalty = - 1 * abs(1 - data.qpos[3])
        torque_penalty = 0

        for i in range(6, 12):
            torque_penalty += -0.1 * abs(data.qfrc_actuator[i])

        self.sum_zpos_reward += zpos_reward
        self.sum_xvel_reward += xvel_reward
        self.sum_zvel_penalty += zvel_penalty
        self.sum_tilt_penalty += tilt_penalty
        self.sum_torque_penalty += torque_penalty

        self.life_time_reward += 0.002
        self.sum_life_time_reward += self.life_time_reward

        reward = zpos_reward + xvel_reward + zvel_penalty + torque_penalty

        self.total_return  = self.total_return + reward
        if self.rend == True:
            create_overlay(model,data, self.episode, self.total_return)
            viewport_width, viewport_height = glfw.get_framebuffer_size(window)
            viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)
            mj.mjv_updateScene(model, data, opt, None, cam,
            mj.mjtCatBit.mjCAT_ALL.value, scene)
            mj.mjr_render(viewport, scene, context)
            for gridpos, [t1, t2] in _overlay.items():
                mj.mjr_overlay(
                    mj.mjtFontScale.mjFONTSCALE_150, gridpos, viewport, t1, t2, context)
            glfw.swap_buffers(window)
            glfw.poll_events()
        if data.time >= 10: #end episode

            self.done = True
            self.plot(self.train)
            self.episode = self.episode + 1
            print(
                f"zpos_reward: {self.sum_zpos_reward:.2f}, xvel_reward: {self.sum_xvel_reward:.2f}, zvel_penalty: {self.sum_zvel_penalty:.2f}, torque_penalty: {self.sum_torque_penalty}, time: {data.time:.2f}")
        elif abs(data.qpos[2]) <= 0.15: #end episode

            self.done = True
            self.plot(self.train)
            self.episode = self.episode + 1
            print(
                f"zpos_reward: {self.sum_zpos_reward:.2f}, xvel_reward: {self.sum_xvel_reward:.2f}, zvel_penalty: {self.sum_zvel_penalty:.2f}, torque_penalty: {self.sum_torque_penalty}, time: {data.time:.2f}")
        _overlay.clear()
        return state, reward, self.done, {}
    
    def settings(self, rend, train):
        self.train = train
        self.rend = rend
        if self.rend == False:
            glfw.terminate()

    def reset(self):
        self.total_return = 0
        self.done = False
        mj.mj_resetData(model, data)
        mj.mj_forward(model, data)
        for i in range(6):
            data.ctrl[i] = 0
        state1 = [data.qpos[i] for i in range(13)]
        state2 = [data.qvel[i] for i in range(12)]
        state = state1 + state2

        self.sum_zpos_reward = 0
        self.sum_xvel_reward = 0
        self.sum_zvel_penalty = 0
        self.sum_tilt_penalty = 0
        self.life_time_reward = 0
        self.sum_life_time_reward = 0
        self.sum_torque_penalty = 0
        self.xvel_timestamp = [0, 0, 0, 0, 0]

        return state

    def plot(self, enable): #plot score graph
        if enable == True:
            self.score_avg = 0.9 * self.score_avg + 0.1 * self.total_return if self.episode != 0 else self.total_return 
            scores.append(self.score_avg)
            episodes.append(self.episode)
            pylab.plot(episodes, scores, 'b')
            pylab.xlabel("episode")
            pylab.ylabel("average score")
            pylab.savefig("PPO_reward.png")