# Compile with Python3 3.8+
# Required files: main.py, robot.py, map.py
from game_map import Game_Map
from robot import Robot
from time import sleep

MAP_SIZE = 10
CAN_COUNT = 20
EPISODES = 5000
STEPS = 200
EPSILON = 0.1
EPSILON_DECREASE_FREQ = 50
EPSILON_DECREASE_RATE = (EPSILON / (EPISODES/EPSILON_DECREASE_FREQ)) * 2
LEARNING_RATE = 0.2
DISCOUNT = 0.9
REPORT_FREQUENCY = 100
Q_TABLE_FILE = "q-table.txt"
REPORT_FILE = "reports.txt"
SCORES_FILE = "scores.csv"

#Run a vizualization of the final Q-Table
def test_q_table(robby):
    gm = Game_Map(MAP_SIZE, CAN_COUNT*2)
    for steps in range(1, STEPS+1):
        robby.check_sensors(gm)
        gm.print_map()
        action = robby.choose_action(0)
        reward = robby.perform_action(action, gm)
        sleep(0.05)
    score = robby.get_score()
    print(f'Final Score: {score}  Epsilon: 0')

score_set = []
highest_score = 0
epsilon = EPSILON
robby = Robot()
#test_q_table(robby)

for episodes in range(1, EPISODES+1):
    gm = Game_Map(MAP_SIZE, CAN_COUNT)
    robby.check_sensors(gm)
    for steps in range(1, STEPS+1):
        action = robby.choose_action(epsilon)
        reward = robby.perform_action(action, gm)
        robby.check_sensors(gm)
        robby.update_q_table(reward, LEARNING_RATE, DISCOUNT)
    score = robby.get_score()
    if (score > highest_score):
        highest_score = score
    score_set.append(score)
    if (episodes % EPSILON_DECREASE_FREQ == 0 and epsilon != 0):
        epsilon -= EPSILON_DECREASE_RATE
        if (epsilon < 0):
            epsilon = 0
    if (episodes % REPORT_FREQUENCY == 0):
        avg = sum(score_set) / REPORT_FREQUENCY
        score_set = []
        print(f'Episode: {episodes}  Highest Score: {highest_score}  Last 50 Avg Score: {avg}  Epsilon: {epsilon}')    
        robby.output_q_table(Q_TABLE_FILE)
        with open(SCORES_FILE, "a") as f:
            f.write(f'{episodes},{score},{avg}\n')
        f.close()
    robby.reset()

test_q_table(robby)

    




