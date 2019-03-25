import sys
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, get_field
import time
import subprocess

from .simulator import Simulator


def _message_with_frame(string):
    print()
    print('=' * 100)
    print(string)
    print('=' * 100)
    print()


class Environment():
    actions = ["↖", "↑", "↗", "←", "→", "↙", "↓", "↘", "A", "B", "C", "_"]

    # Create the connection to the server
    def __init__(self):
        self._port = 4242
        self._simulator = Simulator(self._port)
        self._gateway = None
        self._manager = None

        self._reset()

    def _finalize(self):
        if self._gateway:
            self._gateway.close_callback_server()
            self._gateway.close()
            del self._gateway
            self._gateway = None
            self._manager = None

        self._simulator.kill()

    def _reset(self):
        _message_with_frame('Environment reconnect...')
        self._finalize()
        self._simulator.connect()
        self._gateway = JavaGateway(gateway_parameters=GatewayParameters(port=self._port), callback_server_parameters=CallbackServerParameters())
        self._manager = self._gateway.entry_point
        _message_with_frame('Environment reconnect... done')

    def play(self, cls, opponent_cls=None, player_character="ZEN", opponent_character="GARNET", opponent_agent="GigaThunder"):
        # Register custom AI with the engine. The name is needed later to select that agent.
        self._manager.registerAI(cls.__name__, cls(self))
        if opponent_cls is not None:
            if cls.__name__ != opponent_cls.__name__:
                self._manager.registerAI(opponent_cls.__name__, opponent_cls(self))
            opponent_agent = opponent_cls.__name__

        print("GAME START ▶")
        print("   (P1) %s/%s vs. (P2) %s/%s" %
              (cls.__name__, player_character, opponent_agent, opponent_character))
        GAME_NUM = 1

        # Create a game with the selected characters and AI
        # Possible default AIs are: MctsAi, GigaThunder
        # Characters: ZEN, GARNET
        game = self._manager.createGame(player_character, opponent_character, cls.__name__, opponent_agent, GAME_NUM)

        # Run a 3 match game
        try:
            self._manager.runGame(game)

        except KeyboardInterrupt:
            pass

        finally:
            print("STOP ▮")
            # Close connection
            self._finalize()


class Agent(object):
    def __init__(self, environment):
        self._environment = environment
        self._gateway = environment._gateway

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
        # print(z)

    # please define this method when you use FightingICE version 4.00 or later
    def getScreenData(self, sd):
        pass

    def initialize(self, gameData, player):
        # Initializng the command center, the simulator and some other things
        self.inputKey = self._gateway.jvm.struct.Key()
        self.frameData = self._gateway.jvm.struct.FrameData()
        self.cc = self._gateway.jvm.aiinterface.CommandCenter()

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
            for k, v in dic.items():
                a = a.replace(k, v)
            self.cc.commandCall(a)
        else:
            self.cc.commandCall("_")

        # self.sendCommand()

    def roundEnd(self, x, y, z):
        print(x)
        print(y)
        print(z)

    # This part is mandatory
    class Java:
        implements = ["aiinterface.AIInterface"]
