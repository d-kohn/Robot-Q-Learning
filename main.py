from game_map import Game_Map
from robot import Robot
from time import sleep

MAP_SIZE = 10
CAN_COUNT = 20
EPISODES = 20000
STEPS = 200
EPSILON = 0.1
EPSILON_DECREASE_FREQ = 100
EPSILON_DECREASE_RATE = EPSILON / (EPISODES/EPSILON_DECREASE_FREQ)
ETA = 0.2
DISCOUNT = 0.9
REPORT_FREQUENCY = 50
Q_TABLE_FILE = "q-table.txt"
REPORT_FILE = "reports.txt"
SCORES_FILE = "scores.csv"

scores = []
score_set = []
highest_score = 0

#gm = Game_Map(MAP_SIZE, CAN_COUNT)
epsilon = EPSILON
robby = Robot()
for episodes in range(1, EPISODES+1):
    gm = Game_Map(MAP_SIZE, CAN_COUNT)
    robby.check_sensors(gm)
    for steps in range(1, STEPS+1):
        action = robby.choose_action(epsilon)
        reward = robby.perform_action(action, gm)
#        print(f'Step: {steps}  Reward: {reward}')
        robby.check_sensors(gm)
        robby.update_q_table(reward, ETA, DISCOUNT)
#        if (steps % REPORT_FREQUENCY == 0):
#            print(f'Step: {steps}  Score: {robby.get_score()}')
    score = robby.get_score()
    if (score > highest_score):
        highest_score = score
    score_set.append(score)
    if (episodes % EPSILON_DECREASE_FREQ == 0):
        EPSILON -= EPSILON_DECREASE_RATE
    if (episodes % REPORT_FREQUENCY == 0):
        avg = sum(score_set) / REPORT_FREQUENCY
        score_set = []
        print(f'Episode: {episodes}  Highest Score: {highest_score}  Last 50 Avg Score: {avg}  Epsilon: {EPSILON}')    
        robby.output_q_table(Q_TABLE_FILE)
        with open(SCORES_FILE, "a") as f:
            f.write(f'{episodes},{robby.get_score()}\n')
        f.close()
    robby.reset()

gm = Game_Map(MAP_SIZE, 50)
robby.check_sensors(gm)
for steps in range(1, STEPS+1):
    gm.print_map()
    action = robby.choose_action(0)
    reward = robby.perform_action(action, gm)
    robby.check_sensors(gm)
    robby.update_q_table(reward, ETA, DISCOUNT)
    sleep(0.1)
score = robby.get_score()
print(f'Final Score: {score}  Epsilon: 0')    




