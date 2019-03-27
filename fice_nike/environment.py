from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters

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
        self.gateway = None
        self.manager = None

        self._reset()

    def _finalize(self):
        if self.gateway:
            self.gateway.close_callback_server()
            self.gateway.close()
            del self.gateway
            self.gateway = None
            self.manager = None

        self._simulator.kill()

    def _reset(self):
        _message_with_frame('Environment reconnect...')
        self._finalize()
        self._simulator.connect()
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(port=self._port), callback_server_parameters=CallbackServerParameters())
        self.manager = self.gateway.entry_point
        _message_with_frame('Environment reconnect... done')

    def play(self, cls, opponent_cls=None, player_character="ZEN", opponent_character="GARNET", opponent_agent="GigaThunder"):
        # Register custom AI with the engine. The name is needed later to select that agent.
        self.manager.registerAI(cls.__name__, cls(self))
        if opponent_cls is not None:
            if cls.__name__ != opponent_cls.__name__:
                self.manager.registerAI(opponent_cls.__name__, opponent_cls(self))
            opponent_agent = opponent_cls.__name__

        print("GAME START ▶")
        print("   (P1) %s/%s vs. (P2) %s/%s" %
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
            self._finalize()
