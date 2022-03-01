from copy import deepcopy
from random import random, randrange, randint

class Robot:
    ACTION_COUNT = 5
    MOVE_NORTH = 0
    MOVE_SOUTH = 1
    MOVE_EAST = 2
    MOVE_WEST = 3
    PICK_UP_CAN = 4

    SENSOR_STATES = 3
    FLOOR = 0
    WALL = 1
    CAN = 2

    SENSOR_COUNT = 5
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    CURRENT = 4
    direction = {
        NORTH : [0,-1],
        EAST : [1,0],
        SOUTH : [0,1],
        WEST : [-1,0],
        CURRENT : [0,0]
    }

    def __init__(self):       
        self.sensor_data = [0]*5
        self.q_table = {}
        self.build_q_table()
        self.current_state = ()
        self.prev_state = ()
        self.prev_action = -1
        self.score = 0

    def reset(s):
        s.sensor_data = [0]*5
        s.current_state = ()
        s.prev_state = ()
        s.prev_action = -1
        s.score = 0

    def get_score(s):
        return s.score

    def get_q_table(s):
        return s.q_table

    def check_sensors(s, game_map):
        for sensor in s.direction:
            s.sensor_data[sensor] = game_map.get_sensor_data(s.direction[sensor])
            s.current_state = tuple(s.sensor_data)
#        print(s.sensor_data)

    def check_sensor(s, sensor, game_map):
        return game_map.get_sensor_data(s.direction[sensor])

    def choose_action(s, epsilon):
        s.q_table[0,0,0,0,0] = [0,0,0,0,0]
        cur_state = s.q_table[s.current_state]
        # Do random action
        if (1 - epsilon < random()):
            return randrange(s.ACTION_COUNT)
        # Do greedy action
        else:
            best_actions = [0]
            for action in range(1, s.ACTION_COUNT):
                if (int(cur_state[action]*1000) > int(cur_state[best_actions[0]]*1000)):
                    best_actions = [action]
                elif (int(cur_state[action]*1000) == int(cur_state[best_actions[0]]*1000)):
                    best_actions.append(action)   
        
            if (len(best_actions) == 1):
                return best_actions[0]
            else:
                index = randrange(len(best_actions))
                return best_actions[index]

    def perform_action(s, action, game_map):
        reward = game_map.perform_action(action, s.direction[action])
        s.prev_state = s.current_state
        s.prev_action = action
        s.score += reward
        return reward
        
    def assess_reward(s, action, game_map):
        if (action == s.PICK_UP_CAN):
            if (s.sensor_data[s.CURRENT] == s.CAN):
                (s.q_table[s.current_state])[s.PICK_UP_CAN] = s.PICK_UP_CAN_REWARD
                s.score += s.PICK_UP_CAN_REWARD
                game_map.can_picked_up()
            else:
                (s.q_table[s.current_state])[s.PICK_UP_CAN] = s.PICK_UP_NOTHING_REWARD
                s.score += s.PICK_UP_NOTHING_REWARD
        elif (s.sensor_data[action] == s.WALL):
            (s.q_table[s.current_state])[action] = s.PICK_UP_NOTHING_REWARD
            s.score += s.PICK_UP_NOTHING_REWARD

    def update_q_table(s, reward, eta, discount):
        cur_state = s.q_table[s.current_state]
        prev_state = s.q_table[s.prev_state]
        current_state_max_reward = 0

        for action in range(s.ACTION_COUNT):
            if (cur_state[action] > current_state_max_reward):
                current_state_max_reward = cur_state[action]
        
        (s.q_table[s.prev_state])[s.prev_action] = prev_state[s.prev_action] + eta * (reward + discount * current_state_max_reward - prev_state[s.prev_action])
#        print(s.q_table[s.prev_state])

    def build_q_table(s):
        for north in range(s.SENSOR_STATES):
            for east in range(s.SENSOR_STATES):
                for south in range(s.SENSOR_STATES):
                    for west in range(s.SENSOR_STATES):
                        for current in range(s.SENSOR_STATES):
                            state_action = tuple([north, east, south, west, current])
                            s.q_table[state_action] = [0]*5
#                            print(f"{state_action}: {s.q_table[state_action]}")

    def output_q_table(s, file):
        with open(file, "w") as f:
            for state in s.q_table:
                f.write(f'{state}\n')
                f.write(f'{s.q_table[state]}\n')
        f.close()
