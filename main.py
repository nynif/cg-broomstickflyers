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

masse_snaffle = 0.5
friction_snaffle = 0.75

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
op_x_goal = 0
my_x_goal = 16000
if my_team_id == 1:
    op_x_goal = 16000
    my_x_goal = 0

dist_max = 25000
#Distance à partir de laquelle on va tirer sur les bludgers
dist_min_bludger = 4500

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
   
def distance_between_entities(entity_a: Entitie, entity_b: Entitie):
    return distance(entity_a.x, entity_a.y, entity_b.x, entity_b.y)

def direction_between_entities(entity_a: Entitie, entity_b: Entitie):
    return math.atan2(entity_b.y-entity_a.y,entity_b.x-entity_a.x) * 180 / math.pi

def norme(vx, vy):
    return math.sqrt(vx*vx+vy*vy)

def get_affine(entity_a: Entitie, entity_b: Entitie):
    a = 0
    if entity_b.x != entity_a.x :
        a = (entity_b.y - entity_a.y)/(entity_b.x - entity_a.x)

    b = entity_a.y - a*entity_a.x
    return a,b

def affine_get_y_from_x(a,b,x):
    return a*x+b

def affine_get_x_from_y(a,b,y):
    if a != 0:
        return (y-b)/a
    else:
        return 0

def is_a_before_b(entity_a: Entitie, entity_b: Entitie):
    to_ret = False
    if (my_team_id == 0 and entity_a.x<entity_b.x) or (my_team_id == 1 and entity_a.x>entity_b.x):
        to_ret = True
    return to_ret

def y_impact_is_in_goal(y_impact):
    return y_impact > 1950 and y_impact < 5950

def will_goal(entity_a: Entitie, entity_b: Entitie, accio= False):
    a,b = get_affine(entity_a, entity_b)
    y_impact = affine_get_y_from_x(a,b, my_x_goal)

    return y_impact_is_in_goal(y_impact) and is_a_before_b(entity_a, entity_b) 

def accio_goal(entity_a: Entitie, entity_b: Entitie):
    a, b = get_affine(entity_a, entity_b)
    y_impact = affine_get_y_from_x(a,b, my_x_goal)

    if y_impact_is_in_goal(y_impact) and is_a_before_b(entity_a, entity_b) == False:
        return True

    return False

def new_vect(wizard: Entitie, snaffle: Entitie):
    previous_norme   = norme(snaffle.vx, snaffle.vy)
    # print(snaffle.vx, snaffle.vy, previous_norme)

    dist_ab = distance_between_entities(wizard, snaffle)

    pousse  = (distance_between_entities(wizard, snaffle) / 1000) ** 2

    vx_add_norm = (wizard.x-snaffle.x)/dist_ab
    vy_add_norm = (wizard.y-snaffle.y)/dist_ab
    
    new_snaffle = snaffle 
    new_snaffle.vx = round((snaffle.vx + vx_add_norm*pousse/masse_snaffle)*friction_snaffle)
    new_snaffle.vy = round((snaffle.vy + vy_add_norm*pousse/masse_snaffle)*friction_snaffle)
    new_snaffle.x = round(snaffle.x+  new_snaffle.vx)
    new_snaffle.y = round(snaffle.y+new_snaffle.vy)

    return new_snaffle

def will_catch_with_accio(wizard: Entitie, snaffle: Entitie):

    will_catch_with_accio = False
    init_snaffle = snaffle
    for i in range(6):
        snaffle=  new_vect(wizard, snaffle)
        if will_catch_with_accio == False and distance_between_entities(wizard, snaffle) < 1600:
            will_catch_with_accio = True
    
    if will_catch_with_accio == False:
        for i in range(6):
            init_snaffle=  new_vect(wizard, snaffle)
            print("loop", init_snaffle.vx, init_snaffle.vy, distance_between_entities(wizard, init_snaffle), file=sys.stderr, flush=True)


    return will_catch_with_accio


def MAGIC_OBLIVIATE(my_wizard, p_bludgers, my_magic):
    tmp_action = ""
    for i_bludger, act_bludger in enumerate(p_bludgers):
        if distance_between_entities(my_wizard, act_bludger) < dist_min_bludger:
            if my_magic > 5:
                tmp_action = "OBLIVIATE " + str(act_bludger.entity_id) + " OBLIVIATE"
                my_magic -= 5 
    return tmp_action, my_magic

def MAGIC_ACCIO(p_snaffles, p_snaffles_already_target, my_magic):
    tmp_action = ""
    for i, snaffle in enumerate(p_snaffles):
        if (snaffle.entity_id not in p_snaffles_already_target) and distance_between_entities(actual_wizard, snaffle) > 6000 and my_magic > 15:
            tmp_action = "ACCIO " + str(snaffle.entity_id) + " ACCIO"
            my_magic -= 15
    return tmp_action, my_magic

#TODO: regler correctement la distance afin que la balle ne soit pas capturer par le soricer, sinon la vitesse est réduite
def MAGIC_ACCIO_PERFECT(my_wizard, p_snaffles, my_magic):    
    tmp_action = ""
    for i, snaffle in enumerate(p_snaffles):
        dist =  distance_between_entities(my_wizard, snaffle) 
        if dist > 2500 and dist < 6500 and accio_goal(my_wizard, snaffle):
            if will_catch_with_accio(my_wizard, snaffle) == False and my_magic > 15:
                tmp_action = "ACCIO " + str(snaffle.entity_id) + " ACCIOPERFECT"
                my_magic -= 15
    return tmp_action, my_magic

def MAGIC_PETRIFICUS(my_wizard, p_snaffles, my_magic):
    tmp_action = ""
    for i, snaffle in enumerate(p_snaffles):
        if abs(op_x_goal-snaffle.x) < 3000 and my_magic > 10:
            tmp_action = "PETRIFICUS " + str(snaffle.entity_id) + " PETRIFICUS"
            my_magic -= 10
            print('PETRIFICUS ON ', snaffle.entity_id, file=sys.stderr, flush=True)


    return tmp_action, my_magic


def MAGIC_FLIPENDO_PERFECT(my_wizard, p_snaffles, my_magic):
    tmp_action = ""
    for i, snaffle in enumerate(p_snaffles):
        if will_goal(my_wizard, snaffle) and distance_between_entities(my_wizard, snaffle) < 6000 and my_magic > 20:
            tmp_action = "FLIPENDO " + str(snaffle.entity_id) + " FLIPENDOPERFECT"
            my_magic -= 20
    return tmp_action, my_magic

#TODO: ne pas utiliser de magie sur une balles qui est déjà target 

def ACTION_MOVE_ATT(my_wizard, p_snaffles, p_snaffles_already_target, total_score):
    tmp_action = ""
    target_x = 8000
    target_y = random.randint(2500, 4500)
    target_d = dist_max #plus grand distance possible
    target_id = ""
    att_area = 10000

    for i, actual_snaffle in enumerate(p_snaffles):
        d = distance_between_entities(my_wizard, actual_snaffle)

        if ((actual_snaffle.entity_id not in p_snaffles_already_target) or len(p_snaffles) < 2) and (d < target_d):
            target_x = actual_snaffle.x
            target_y = actual_snaffle.y
            target_d = d
            target_id = actual_snaffle.entity_id
                    
    p_snaffles_already_target.append(target_id)
    print(my_wizard.entity_id, 'target', target_id, file=sys.stderr, flush=True)
    tmp_action = "MOVE " + str(target_x) + ' ' + str(target_y) + " 150"
                
    return tmp_action, p_snaffles_already_target 

def ACTION_MOVE_DEF(my_wizard, p_snaffles, p_snaffles_already_target):
    target_x = abs(op_x_goal - 300)
    target_y = random.randint(2500, 4500)
    target_d = dist_max #plus grand distance possible
    target_id = ""

    for i, actual_snaffle in enumerate(p_snaffles):
        d = abs(actual_snaffle.x-op_x_goal) #distance_between_entities(my_wizard, actual_snaffle)
        if ((actual_snaffle.entity_id not in p_snaffles_already_target) or len(p_snaffles) < 2) and (d < target_d):
#            if (my_team_id == 0 and actual_snaffle.x < def_area) or (my_team_id == 1 and actual_snaffle.x > def_area):  
            target_x = actual_snaffle.x
            target_y = actual_snaffle.y
            target_d = d
            target_id = actual_snaffle.entity_id
                    
    p_snaffles_already_target.append(target_id)
    print(my_wizard.entity_id, 'target', target_id, file=sys.stderr, flush=True)
    tmp_action = "MOVE " + str(target_x) + ' ' + str(target_y) + " 150 DEFENSE"
                
    return tmp_action, p_snaffles_already_target 

def ACTION_THROW():
    tmp_action = "THROW "+ str(my_x_goal) + " " + str(random.randint(3000, 4500)) + " 500"
    return tmp_action


# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    entities = int(input())  # number of entities still in game
 
    action, snaffles_already_target, l_entities = "", [], []
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

        # MODE ATTAQUE
        if True: #i_wiz % 2 == 0:

            if action == "":
                action, my_magic = MAGIC_FLIPENDO_PERFECT(actual_wizard, snaffles, my_magic)

           # if action == "":
           #     action, my_magic = MAGIC_PETRIFICUS(actual_wizard, snaffles, my_magic)
            

            if action == "":
                action, my_magic = MAGIC_ACCIO_PERFECT(actual_wizard, snaffles, my_magic)          

            if action == "":
                # if wizard is NOT holding a Snaffle, Move to the targeted snaffle
                if actual_wizard.state != 1:
                    action, snaffles_already_target = ACTION_MOVE_ATT(actual_wizard, snaffles, snaffles_already_target, total_score)

                # if wizard hold a Snaffle, THROW it in the middle of the goal
                else:
                    action = ACTION_THROW()
    
        #MODE DEFENSE
        # Le defenseur reste dans sa moité de terrain
        else:

            if action == "":
                action, my_magic = MAGIC_FLIPENDO_PERFECT(actual_wizard, snaffles, my_magic)

            if action == "":
                action, my_magic = MAGIC_PETRIFICUS(actual_wizard, snaffles, my_magic)
    
            if action == "":
                
                # if wizard is NOT holding a Snaffle, Move to the closest snaffle
                if actual_wizard.state != 1:
                    action, snaffles_already_target = ACTION_MOVE_DEF(actual_wizard, snaffles, snaffles_already_target)

                # if wizard hold a Snaffle, THROW it in the middle of the goal
                else:
                    action = ACTION_THROW()
            
        print(action)
        action = "" 

        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        # print("debug", l_wizards[i].entity_type, file=sys.stderr, flush=True)