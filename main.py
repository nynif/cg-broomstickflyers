import sys
import math
import random

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
        self.dir = math.atan2(vy,vx) * 180 / math.pi
#Dans le cas ou je marque à droite
#L'opp est derrière moi si abs(angle) > 90 
#L'opp est devant moi si abs(angle) < 90 

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
op_x_goal = 0
my_x_goal = 16000
angle_lim = 135
if my_team_id == 1:
    op_x_goal = 16000
    my_x_goal = 0
    angle_lim = 45

dist_max = 25000
#Distance à partir de laquelle on va tirer sur les bludgers
dist_min_bludger = 3000

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
   
def distance_between_entities(entity_a: Entitie, entity_b: Entitie):
    return distance(entity_a.x, entity_a.y, entity_b.x, entity_b.y)

def direction_between_entities(entity_a: Entitie, entity_b: Entitie):
    return math.atan2(entity_b.y-entity_a.y,entity_b.x-entity_a.x) * 180 / math.pi

def is_entitie_after(entity_a: Entitie, entity_b: Entitie, angle_state0 = 90, angle_state1 = 90):
    direction = direction_between_entities(entity_a, entity_b)
    ret = True
    if my_team_id == 0 and abs(direction) < angle_state1:
        ret = False
    if my_team_id == 1 and abs(direction) > angle_state0:
        ret = False
    return ret

def MAGIC_OBLIVIATE(my_wizard, p_bludgers, my_magic):
    tmp_action = ""
    for i_bludger, act_bludger in enumerate(p_bludgers):
        if distance_between_entities(my_wizard, act_bludger) < dist_min_bludger:
            if my_magic > 5:
                tmp_action = "OBLIVIATE " + str(act_bludger.entity_id) + " OBLIVIATE"
                my_magic -= 5 
    return tmp_action, my_magic

#Lancer un flipendo si un adversaire est proche de moi sauf si ça l'envoi vers ses buts
def MAGIC_FLIPENDO_IF_NEAR(my_wizard, p_op_wizards, my_magic):
    tmp_action = ""
    for i_opwiz, op_wiz in enumerate(p_op_wizards):
        dir_op = direction_between_entities(my_wizard, op_wiz)
        if (abs(dir_op)<135 and abs(dir_op)<45) and distance_between_entities(op_wiz, my_wizard) < 3000 and my_magic > 20:
            tmp_action = "FLIPENDO " + str(op_wiz.entity_id) + " FLIPENDO"
            my_magic -= 20
    return tmp_action, my_magic

def MAGIC_ACCIO(p_snaffles, p_snaffles_already_target, my_magic):
    tmp_action = ""
    for i, snaffle in enumerate(p_snaffles):
        if (snaffle.entity_id not in p_snaffles_already_target) and distance_between_entities(actual_wizard, snaffle) > 6000 and my_magic > 15:
            tmp_action = "ACCIO " + str(snaffle.entity_id) + " ACCIO"
            my_magic -= 15
    return tmp_action, my_magic

def MAGIC_ACCIO_PERFECT(my_wizard, p_snaffles, my_magic):    
    tmp_action = ""
    # Il faut que la ligne entre le wizard et le snaffle termine vers les buts

    # Il faut que le snaffle soit à bonne distance pour que 6 tours l'amene à moi
    # Si le snaffle est immobile la distance est environ de 6100
    for i, snaffle in enumerate(p_snaffles):
        if is_entitie_after(my_wizard, snaffle, 45, 125) and distance_between_entities(my_wizard, snaffle) > 3500 and distance_between_entities(my_wizard, snaffle) < 7000 and my_magic > 15:
            tmp_action = "ACCIO " + str(snaffle.entity_id) + " ACCIOPERFECT"
            my_magic -= 15
    return tmp_action, my_magic

def ACTION_MOVE_ATT(my_wizard, p_snaffles, p_snaffles_already_target):
    tmp_action = ""
    target_x = 8000
    target_y = random.randint(2500, 4500)
    target_d = dist_max #plus grand distance possible
    target_id = ""

    for i, actual_snaffle in enumerate(p_snaffles):
        d = distance(my_wizard.x, my_wizard.y, actual_snaffle.x, actual_snaffle.y)

        if ((actual_snaffle.entity_id not in p_snaffles_already_target) or len(p_snaffles) < 2) and (d < target_d):
            target_x = actual_snaffle.x
            target_y = actual_snaffle.y
            target_d = d
            target_id = actual_snaffle.entity_id
                    
    p_snaffles_already_target.append(target_id)
    tmp_action = "MOVE " + str(target_x) + ' ' + str(target_y) + " 150"
                
    return tmp_action, p_snaffles_already_target 

def ACTION_MOVE_DEF(my_wizard, p_snaffles, p_snaffles_already_target):
    target_x = abs(op_x_goal - 300)
    target_y = random.randint(2100, 5200)
    target_y = random.randint(2500, 4500)
    target_d = dist_max #plus grand distance possible
    target_id = ""

    for i, actual_snaffle in enumerate(p_snaffles):
        d = distance(my_wizard.x, my_wizard.y, actual_snaffle.x, actual_snaffle.y)
        if ((actual_snaffle.entity_id not in p_snaffles_already_target) or len(p_snaffles) < 2) and (d < target_d):
            target_x = actual_snaffle.x
            target_y = actual_snaffle.y
            target_d = d
            target_id = actual_snaffle.entity_id
                    
    p_snaffles_already_target.append(target_id)
    tmp_action = "MOVE " + str(target_x) + ' ' + str(target_y) + " 150"
                
    return tmp_action, p_snaffles_already_target 

def ACTION_THROW():
    tmp_action = "THROW "+ str(my_x_goal) + " " + str(random.randint(2500, 4500)) + " 500"
    return tmp_action


# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    entities = int(input())  # number of entities still in game
 
    action_att, action_def, snaffles_already_target, l_entities = "", "", [], []
    total_score = my_score + opponent_score

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
    op_wizards  = list(filter(lambda ent: ent.entity_type == "OPPONENT_WIZARD", l_entities))
    snaffles    = list(filter(lambda ent: ent.entity_type == "SNAFFLE", l_entities))
    bludgers    = list(filter(lambda ent: ent.entity_type == "BLUDGER", l_entities))

    for i_wiz, actual_wizard in enumerate(wizards):

        #Au debut de la partie il faut aller vite, éviter les bludgers 
        if action_att == "" and total_score < 2:
            action_att, my_magic = MAGIC_OBLIVIATE(actual_wizard, bludgers, my_magic)

        #Si on est proche d'un enemi, on lance un flipendo de manière aléatoire 25% 
        #if action_att == "" and total_score > 2 and random.randint(0, 4) == 1:
        #    action_att, my_magic = MAGIC_FLIPENDO_IF_NEAR(actual_wizard, op_wizards, my_magic)
        
        if action_att == "":
            action_att, my_magic = MAGIC_ACCIO_PERFECT(actual_wizard, snaffles, my_magic)

        # MODE ATTAQUE
        if i_wiz % 2 == 0:
            if action_att == "":

                # if wizard is NOT holding a Snaffle, Move to the targeted snaffle
                if actual_wizard.state != 1:
                    action_att, snaffles_already_target = ACTION_MOVE_ATT(actual_wizard, snaffles, snaffles_already_target)

                # if wizard hold a Snaffle, THROW it in the middle of the goal
                else:
                    action_att = ACTION_THROW()
        
            print(action_att)
            action_att = ""

        #MODE DEFENSE
        # Le defenseur reste dans sa moité de terrain
        else:
    
            #if action_def == "":
            #    action_def, my_magic= MAGIC_ACCIO(snaffles, snaffles_already_target, my_magic)
                
            if action_def == "":
                
                # if wizard is NOT holding a Snaffle, Move to the closest snaffle
                if actual_wizard.state != 1:
                    action_def, snaffles_already_target = ACTION_MOVE_DEF(actual_wizard, snaffles, snaffles_already_target)

                # if wizard hold a Snaffle, THROW it in the middle of the goal
                else:
                    action_def = ACTION_THROW()
            
            print(action_def)
            action_def = "" 

        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        # print("debug", l_wizards[i].entity_type, file=sys.stderr, flush=True)