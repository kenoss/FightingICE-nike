import sys
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, get_field
import time
import subprocess

class Environment():
    actions = ["↖", "↑", "↗", "←", "→", "↙", "↓", "↘", "A", "B", "C", "_"]
    
    # Create the connection to the server
    def __init__(self):
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(port=4242), callback_server_parameters=CallbackServerParameters())
        self.manager = self.gateway.entry_point

        logo = '''
Welcome to

  ███████╗██╗ ██████╗ ██╗  ██╗████████╗██╗███╗   ██╗ ██████╗     ██╗ ██████╗███████╗
  ██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝██║████╗  ██║██╔════╝     ██║██╔════╝██╔════╝
  █████╗  ██║██║  ███╗███████║   ██║   ██║██╔██╗ ██║██║  ███╗    ██║██║     █████╗  
  ██╔══╝  ██║██║   ██║██╔══██║   ██║   ██║██║╚██╗██║██║   ██║    ██║██║     ██╔══╝  
  ██║     ██║╚██████╔╝██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝    ██║╚██████╗███████╗
  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝ ╚═════╝╚══════╝                                                                                
...the competitive deep reinforcement learning environment since 2013.
Powered by Prof. Ruck Thawonmas (Ritsumeikan University) 
        '''
        print(logo)

    def play(self, cls, opponent_cls=None, player_character="ZEN", opponent_character="GARNET", opponent_agent="GigaThunder"):
        self.reset()

        # Register custom AI with the engine. The name is needed later to select that agent.
        self.manager.registerAI(cls.__name__, cls(self))
        if opponent_cls is not None:
            if cls.__name__ != opponent_cls.__name__:
                self.manager.registerAI(opponent_cls.__name__, opponent_cls(self))
            opponent_agent=opponent_cls.__name__

        print("GAME START ▶")
        print("   (P1) %s/%s vs. (P2) %s/%s" % \
                  (cls.__name__, player_character, opponent_agent, opponent_character))
        GAME_NUM = 1

        # Create a game with the selected characters and AI
        # Possible default AIs are: MctsAi, GigaThunder
        # Characters: ZEN, GARNET
        game = self.manager.createGame(player_character, opponent_character, cls.__name__, opponent_agent, GAME_NUM)

        # Run a 3 match game
        try:
            self.manager.runGame(game)
            
        except KeyboardInterrupt:
            pass

        finally: 
            print("STOP ▮")
            # Close connection
            self.finalize()

    def finalize(self):
        self.gateway.close_callback_server()
        self.gateway.close()
        subprocess.call('ps aux | grep "java Main" | awk \'{print $2}\' | xargs kill', shell=True)
            
    def reset(self):
        print("Resetting game...")
        self.finalize()
        del self.gateway

        time.sleep(3)

        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(port=4242), callback_server_parameters=CallbackServerParameters())
        self.manager = self.gateway.entry_point
            
class Agent(object):
    def __init__(self, environment):
        self.environment = environment
        self.gateway = environment.gateway

    def close(self):
        pass

    def getInformation(self, frameData):
        # Getting the frame data of the current frame
        self.frameData = frameData
        self.cc.setFrameData(self.frameData, self.player)
    
    # please define this method when you use FightingICE version 3.20 or later
    def roundEnd(self, x, y, z):
        print("P1 HP:" % x)
        print("P2 HP:" % y)
        print("Cummrative Reward:" % x - y)
        #print(z)

    # please define this method when you use FightingICE version 4.00 or later
    def getScreenData(self, sd):
        pass

    def initialize(self, gameData, player):
        # Initializng the command center, the simulator and some other things
        self.inputKey = self.gateway.jvm.struct.Key()
        self.frameData = self.gateway.jvm.struct.FrameData()
        self.cc = self.gateway.jvm.aiinterface.CommandCenter()

        self.player = player
        self.gameData = gameData
        self.simulator = self.gameData.getSimulator()

        return 0

    def input(self):
        # Return the input for the current frame
        return self.inputKey
    
    def policy(self, state):
        pass 

    def sendCommand(self):
        pass 

    def processing(self):
        # Just compute the input for the current frame
        if self.frameData.getEmptyFlag() or self.frameData.getRemainingFramesNumber() <= 0:
                self.isGameJustStarted = True
                return

        # Just spam kick
        self.cc.setFrameData(self.frameData, self.player)
        distance = self.frameData.getDistanceX()
        my = self.frameData.getCharacter(self.player)
        energy = my.getEnergy()
        my_x = my.getX()
        my_state = my.getState()
        opp = self.frameData.getCharacter(not self.player)
        opp_x = opp.getX()
        opp_state = opp.getState()
        xDifference = my_x - opp_x
        if self.cc.getSkillFlag():
                self.inputKey = self.cc.getSkillKey()
                return
           
        self.inputKey.empty()
        self.cc.skillCancel()
        
        a = self.policy(self.frameData)
        dic = {
            "↙": "1", "↓": "2", "↘": "3",
            "←": "4",           "→": "6",
            "↖": "7", "↑": "8", "↗": "9"
        }
        if a is not None: 
            for k, v in dic.items(): a = a.replace(k, v)
            self.cc.commandCall(a)
        else:
            self.cc.commandCall("_")
        
        #self.sendCommand()
        
    # This part is mandatory
    class Java:
        implements = ["aiinterface.AIInterface"]
"""
    def processing(self):
        # First we check whether we are at the end of the round
        if self.frameData.getEmptyFlag() or self.frameData.getRemainingFramesNumber() <= 0:
            self.isGameJustStarted = True
            return
        if not self.isGameJustStarted:
            # Simulate the delay and look ahead 2 frames. The simulator class exists already in FightingICE
            self.frameData = self.simulator.simulate(self.frameData, self.player, None, None, 17)
            #You can pass actions to the simulator by writing as follows:
            #actions = self.gateway.jvm.java.util.ArrayDeque()
            #actions.add(self.gateway.jvm.enumerate.Action.STAND_A)
            #self.frameData = self.simulator.simulate(self.frameData, self.player, actions, actions, 17)
        else:
            # If the game just started, no point on simulating
            self.isGameJustStarted = False
        self.cc.setFrameData(self.frameData, self.player)
        distance = self.frameData.getDistanceX()
        my = self.frameData.getCharacter(self.player)
        energy = my.getEnergy()
        my_x = my.getX()
        my_state = my.getState()
        opp = self.frameData.getCharacter(not self.player)
        opp_x = opp.getX()
        opp_state = opp.getState()
        xDifference = my_x - opp_x
        if self.cc.getSkillFlag():
            # If there is a previous "command" still in execution, then keep doing it
            self.inputKey = self.cc.getSkillKey()
            return
        # We empty the keys and cancel skill just in case
        self.inputKey.empty()
        self.cc.skillCancel()
        
        self.policy(my, opp, distance)
        self.sendCommand()
"""
        
"""
    def processing(self):
         # First we check whether we are at the end of the round
        if self.frameData.getEmptyFlag() or self.frameData.getRemainingFramesNumber() <= 0:
            self.isGameJustStarted = True
            return
        if not self.isGameJustStarted:
            # Simulate the delay and look ahead 2 frames. The simulator class exists already in FightingICE
            self.frameData = self.simulator.simulate(self.frameData, self.player, None, None, 17)
            #You can pass actions to the simulator by writing as follows:
            #actions = self.gateway.jvm.java.util.ArrayDeque()
            #actions.add(self.gateway.jvm.enumerate.Action.STAND_A)
            #self.frameData = self.simulator.simulate(self.frameData, self.player, actions, actions, 17)
        else:
            # If the game just started, no point on simulating
            self.isGameJustStarted = False
        self.cc.setFrameData(self.frameData, self.player)

        distance = self.frameData.getDistanceX()
        my = self.frameData.getCharacter(self.player)
        energy = my.getEnergy()
        my_x = my.getX()
        my_state = my.getState()
        opp = self.frameData.getCharacter(not self.player)
        opp_x = opp.getX()
        opp_state = opp.getState()
        xDifference = my_x - opp_x
        
        if self.cc.getSkillFlag():
                self.inputKey = self.cc.getSkillKey()
                return

        
        self.inputKey.empty()
        self.cc.skillCancel()
       
        self.policy(my, opp, distance)
        self.sendCommand()          
"""
