from __future__ import annotations
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
        self.wetness        = None

    def __str__(self) -> str:
        return f'{self.agent_id} ({self.x},{self.y}) wet:{self.wetness}'


    def update(self, x:int, y:int, cooldown:int, splash_bombs:int, wetness:int) -> None:
        """ update info for each turn.
        x : int
            X coordinate (0 is leftmost)
        y : int
            Y coordinate (0 is uppermost)
        cooldown : int
            number of turns left until this agent can shoot again
        splash_bombs : int
            current amount of splash bombs available to this agent
        wetness : int
            current wetness of the age
        """
        self.x = x
        self.y = y
        self.cooldown = cooldown
        self.splash_bombs= splash_bombs
        self.wetness = wetness

    def distance(self,enemy:Agent)->float:
        """calculate the distance between a enemy and you """
        return math.sqrt(pow(self.x - enemy.x ,2) + pow(self.y-enemy.y,2))


    def optimalPosition(self,enemy:Agent)->(int,int):
        """Calculate the correct position to attack specified enemy
        Attributes
        ----------
        enemy : Agent
            the agent that we want attack.

        Returns
        -------
        nx : int
            new position on the x-axis
        ny : int
            new position on the y-axis

        """
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        distancia = math.hypot(dx,dy)

        if distancia <= self.optimal_range:
            #Is already in the optimal range
            return self.x, self.y

        #redux the distance to be at the optimal distance
        factor = (distancia - self.optimal_range)/distancia
        nx = self.x + dx * factor
        ny = self.y + dy * factor
        return nx, ny


    def shoot(self,enemy):
        """answer to the benefit to shoot to the enemy at that range or cooldown.
        it returns:
            1 : if it is inside the optimal range and don't have cooldown.
            0 : is out of range, can shoot with halved damage.
           -1 : the distance is the double of the optimal range.
        """
        dist = self.distance(enemy)
        if dist < optimal_range: return 1
        elif  dist < 2*optimal_range : return 0
        else: return -1

    def nextTo(self) -> int:
        """return the ID of the closest enemy to him."""
        closeid   = None
        wetness   = 0
        closedist = None

        for a in list(agent_list.values()):
            if a.player != self.player:
                temp = self.distance(a)
                if closedist is None or temp < closedist  or (temp == closedist and a.wetness>wetness):
                    closedist = temp
                    closeid = a.agent_id
                    wetness = a.wetness

        return closeid

    def wettest(self):
        """search the wettest agent from the other player
        """
        wet = 0
        enemyID = 0
        for ag in agent_list.values():
            if ag.player != self.player and ag.wetness > wet:
                wet = ag.wetness
                enemyID = ag.agent_id

        return enemyID

my_id = int(input()) # My player id (0 or 1)
agent_data_count = int(input())  # Total number of agents in the game
myAgents  = []

print("Our agents:", file=sys.stderr, flush=True)
for i in range(agent_data_count):
    # agent_id:       Unique identifier for this agent
    # player:         Player id of this agent
    # shoot_cooldown: Number of turns between each of this agent's shots
    # optimal_range:  Maximum manhattan distance for greatest damage output
    # soaking_power:  Damage output within optimal conditions
    # splash_bombs:   Number of splash bombs this can throw this game
    agent_id, player, shoot_cooldown, optimal_range, soaking_power, splash_bombs = [int(j) for j in input().split()]

    agent_list[agent_id] = Agent(agent_id,player, shoot_cooldown, optimal_range, soaking_power, splash_bombs)

    if player == my_id:
        myAgents.append(agent_id)
        print(myAgents[-1], file=sys.stderr, flush=True)

print("Enemies:", file=sys.stderr, flush=True)
for a in agent_list.values():
    print(myAgents[-1], file=sys.stderr, flush=True)

    
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

        #mapa[y,x] = tile_type

# game loop
while True:
    oldlist = list(agent_list.keys())
    agent_count = int(input())  # Total number of agents still in the game
    for i in range(agent_count):
        # cooldown: Number of turns before this agent can shoot
        # wetness: Damage (0-100) this agent has taken
        agent_id, x, y, cooldown, splash_bombs, wetness = [int(j) for j in input().split()]


        print(f'{agent_id} wet:{wetness}.', file=sys.stderr, flush=True)

        oldlist.remove(agent_id)

        #update list
        agent_list[agent_id].update(x, y, cooldown, splash_bombs, wetness)
        # update & delete bañados
    for i in oldlist:
        del agent_list[i]
        if i in myAgents: myAgents.remove(i)
        print(f'agente {i} eliminado.', file=sys.stderr, flush=True)


    my_agent_count = int(input())  # Number of alive agents controlled by you
    for i in range(my_agent_count):

        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # One line per agent: <agentId>;<action1;action2;...> actions are "MOVE x y | SHOOT id | THROW x y | HUNKER_DOWN | MESSAGE text"
        #print("HUNKER_DOWN")
        respuesta = f'{myAgents[i]};'
        actualAgent = agent_list[myAgents[i]]
        closest = agent_list[actualAgent.nextTo()]
        #closest = agent_list[actualAgent.wettest()]
        if not actualAgent.shoot(closest):
            nx,ny = actualAgent.optimalPosition(closest)
            respuesta += f'MOVE {nx} {ny};'

        respuesta += f'SHOOT {closest.agent_id}'

        print(respuesta)
