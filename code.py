import sys
import math

agent_list = dict() #global

class Agent():
    """
    A class used to represent an Agent

    Attributes
    ----------
    agent_id : int
       Unique identifier for this agent
    shoot_cooldown : int
       Number of turns between each of this agent's shots
    optimal_range : int
        Maximum manhattan distance for greatest damage output
    soaking_power : int
        Damage output within optimal conditions
    splash_bombs : int
        Number of splash bombs this can throw this game
    x : int
        X coordinate (0 is leftmost)
    y : int
        Y coordinate (0 is uppermost)

    Methods
    -------
    locate (x,y)
        Set actual position for the agent.
    nextTo(enemies: list[Agent]) -> int
        return the ID of the closest enemy to him.
    distance(enemy: Agent) -> float
        calculate the distance between a enemy and you
    shoot(enemy : Agent) -> int
        answer to the benefit to shoot to the enemy at that
        range or cooldown. it returns:
            1 : if it is inside the optimal range and don't have cooldown.
            0 : is out of range, can shoot with halved damage.
           -1 : the distance is the double of the optimal range.
    """
    def __init__(self,agent_id, player, shoot_cooldown, optimal_range, soaking_power, splash_bombs):
        self.agent_id       = agent_id
        self.player         = player
        self.shoot_cooldown = shoot_cooldown
        self.optimal_range  = optimal_range
        self.soaking_power  = soaking_power
        self.splash_bombs   = splash_bombs
        self.x              = None
        self.y              = None

    def __str__(self):
        return f"{self.agent_id} ({self.x},{self.y}) wet: {self.wetness}"


    def locate(x:int,y:int):
        """ set actual position for the agent.
        x : int
            X coordinate (0 is leftmost)
        y : int
            Y coordinate (0 is uppermost)
        """
        self.x = x
        self.y = y

    def distance(enemy: Agent) -> float :
        """calculate the distance between a enemy and you """
        return math.sqrt(pow(self.x-enemy.x,2) + pow(self.y-enemy.y,2))


    def shoot(enemy : Agent) -> int:
        """answer to the benefit to shoot to the enemy at that range or cooldown. it returns:
            1 : if it is inside the optimal range and don't have cooldown.
            0 : is out of range, can shoot with halved damage.
           -1 : the distance is the double of the optimal range.
        """
        dist = self.distance(enemy)
        if dist < optimal_range: return 1
        elif  dist < 2*optimal_range : return 0
        else: return -1

    def nextTo() -> int:
        """return the ID of the closest enemy to him."""
        closeid   = None
        closedist = None

        for a in list(agent_list.values()):
            if a.player != self.player:
                temp = self.distance(en)
                if temp < closedist:
                    closedist = temp
                    closeid = en.agent_id
        return closeid

my_id = int(input()) # My player id (0 or 1)
agent_data_count = int(input())  # Total number of agents in the game
myAgents  = []

for i in range(agent_data_count):
    # agent_id:       Unique identifier for this agent
    # player:         Player id of this agent
    # shoot_cooldown: Number of turns between each of this agent's shots
    # optimal_range:  Maximum manhattan distance for greatest damage output
    # soaking_power:  Damage output within optimal conditions
    # splash_bombs:   Number of splash bombs this can throw this game
    agent_id, player, shoot_cooldown, optimal_range, soaking_power, splash_bombs = [int(j) for j in input().split()]
    agent_list.append(Agent(agent_id,player, shoot_cooldown, optimal_range, soaking_power, splash_bombs))
    if player == my_id:
        myAgents.append(agent_id)

# width: Width of the game map
# height: Height of the game map
width, height = [int(i) for i in input().split()]
mapa = [[0 for j in range(width)] for i in range(height)]
for i in range(height):
    inputs = input().split()
    for j in range(width):
        # x: X coordinate, 0 is left edge
        # y: Y coordinate, 0 is top edge
        x = int(inputs[3*j])
        y = int(inputs[3*j+1])
        tile_type = int(inputs[3*j+2])

# game loop
while True:
    agent_count = int(input())  # Total number of agents still in the game
    for i in range(agent_count):
        # cooldown: Number of turns before this agent can shoot
        # wetness: Damage (0-100) this agent has taken
        agent_id, x, y, cooldown, splash_bombs, wetness = [int(j) for j in input().split()]

    my_agent_count = int(input())  # Number of alive agents controlled by you
    for i in range(my_agent_count):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)


        # One line per agent: <agentId>;<action1;action2;...> actions are "MOVE x y | SHOOT id | THROW x y | HUNKER_DOWN | MESSAGE text"
        #print("HUNKER_DOWN")
        print("MOVE 6 1")
