from copy import deepcopy
import os
from random import randrange

class Game_Map:
    ACTION_COUNT = 5
    MOVE_NORTH = 0
    MOVE_SOUTH = 1
    MOVE_EAST = 2
    MOVE_WEST = 3
    PICK_UP_CAN = 4

    X = 0
    Y = 1
    MAP_FEATURES = 4
    FLOOR = 0
    WALL = 1
    CAN = 2
    ROBOT = 3
    map_features = {
        FLOOR : ' ',
        WALL : '#',
        CAN : 'o',
        ROBOT : '@'
    }

    PICK_UP_CAN_REWARD = 10
    PICK_UP_NOTHING_REWARD = -1
    HIT_WALL_REWARD = -5

    def __init__(self, map_size, can_count):
        self.map_size = map_size
        self.actual_map_size = self.map_size + 2
        self.can_count = can_count
        self.map = [['x' for i in range(self.actual_map_size)] for j in range(self.actual_map_size)]
#        print("initializing map...")
        self.build_map()
        self.robot_location = [randrange(self.map_size)+1,randrange(self.map_size)+1]
#        self.print_map()
#        print(self.robot_location)

    def get_sensor_data(s, direction):
        sensor_x = s.robot_location[s.X] + direction[s.X]
        sensor_y = s.robot_location[s.Y] + direction[s.Y]
        return s.map[sensor_x][sensor_y]

    def can_picked_up(s):
        s.map[s.robot_location[s.X]][s.robot_location[s.Y]] = s.FLOOR
        s.can_count -= 1

    def perform_action(s, action, direction):
        robot_x = s.robot_location[s.X]
        robot_y = s.robot_location[s.Y]
        reward = 0

        if (action == s.PICK_UP_CAN):
            if (s.map[robot_x][robot_y] == s.CAN):
                reward = s.PICK_UP_CAN_REWARD
                s.can_picked_up()
#                print("Can picked up")
            else:
                reward = s.PICK_UP_NOTHING_REWARD
#                print("Nothing picked up")
        elif (s.get_sensor_data(direction) == s.WALL):
            reward += s.HIT_WALL_REWARD
#            print("Ouch! Hit a wall!")
        else:
            s.robot_location[s.X] += direction[s.X]
            s.robot_location[s.Y] += direction[s.Y]
        return reward

    def build_map(self):
        for i in range(self.actual_map_size):
            self.map[i][0] = self.WALL
        for y in range(1, self.actual_map_size):
            self.map[0][y] = self.WALL
            for x in range(1, self.actual_map_size - 1):
                self.map[x][y] = self.FLOOR
            self.map[self.actual_map_size - 1][y] = self.WALL
        for i in range(self.actual_map_size):
            self.map[i][self.actual_map_size - 1] = self.WALL

        cans_placed = 0
        while (cans_placed < self.can_count):
            x = randrange(1, self.map_size)
            y = randrange(1, self.map_size)
            if (self.map[x][y] == self.FLOOR):
                self.map[x][y] = self.CAN
            cans_placed += 1
#        print(self.map)

    def print_map(s):
        os.system('cls')
        temp_map = deepcopy(s.map)
        temp_map[s.robot_location[s.X]][s.robot_location[s.Y]] = s.ROBOT
        for y in range(s.actual_map_size):
            for x in range(s.actual_map_size):
                map_object = temp_map[x][y]
                print(s.map_features[map_object], end='')
            print()
        


