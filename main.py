import sys
import math

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.
class Entitie:
    def __init__(self, entity_id, entity_type, x, y, vx, vy, state):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = state
        self.is_target = False

def distance(x1, y1, x2, y2):
    return ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
   
my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
goal = "THROW 16000 3750 500"
if my_team_id == 1:
    goal = "THROW 0 3750 500"

# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    entities = int(input())  # number of entities still in game

    l_entities = []
    for i in range(entities):
        inputs = input().split()
        entity_id = int(inputs[0])  # entity identifier
        entity_type = inputs[1]  # "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        x = int(inputs[2])  # position
        y = int(inputs[3])  # position
        vx = int(inputs[4])  # velocity
        vy = int(inputs[5])  # velocity
        state = int(inputs[6])  # 1 if the wizard is holding a Snaffle, 0 otherwise
        
        new_ent = Entitie(entity_id, entity_type, x, y ,vx, vy, state)
        l_entities.append(new_ent)

    wizards     = list(filter(lambda ent: ent.entity_type == "WIZARD", l_entities))
    snaffles    = list(filter(lambda ent: ent.entity_type == "SNAFFLE", l_entities))

    snaffles_already_target = []
    for i in range(len(wizards)):
        actual_wizard = wizards[i]
        
        target_x = 8000
        target_y = 3750
        target_d = 270000000
        target_id = ""
        # if wizard is NOT holding a Snaffle, Move to the closest snaffle
        if actual_wizard.state != 1:

            # Find the closest Snaffle
            for j in range(len(snaffles)):
                actual_snaffle = snaffles[j]
                actual_snaffle.is_target = False

                d = distance(actual_wizard.x, actual_wizard.y, actual_snaffle.x, actual_snaffle.y)

                if (actual_snaffle.entity_id not in snaffles_already_target) and (d < target_d):
                    target_x = actual_snaffle.x
                    target_y = actual_snaffle.y
                    target_d = d
                    target_id = actual_snaffle.entity_id
            
            snaffles_already_target.append(target_id)
            print(actual_wizard.entity_id, "target snaffle", target_id, file=sys.stderr, flush=True)
            print("MOVE", target_x, target_y, "150")

        # if wizard hold a Snaffle, THROW it in the middle of the goal
        else:
            print(goal)
       

        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        # print("debug", l_wizards[i].entity_type, file=sys.stderr, flush=True)
