# Camel case is necesarry...


from .action import Action


class AgentBase:
    THRESHOLD_FRAME_COUNT_FOR_THE_CASE_SIMULATOR_BROKEN = 30

    def __init__(self, environment):
        self.environment = environment
        self.gateway = environment.gateway

        self._skill_flag_continue_count = 0

    def close(self):
        pass

    def getInformation(self, frameData):
        # Getting the frame data of the current frame
        self.frameData = frameData
        self.cc.setFrameData(self.frameData, self.player)

    # please define this method when you use FightingICE version 3.20 or later
    def roundEnd(self, x, y, z):
        print(f"P1 HP: {x}")
        print(f"P2 HP: {y}")
        print(f"Cummrative Reward: {x - y}")
        # print(z)

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
        '''
        Args:
            state:
                Frame data.  See method `processing`.

        Returns:
            input_keys: [Action] or Action
        '''
        raise NotImplementedError()

    # def sendCommand(self):
    #     pass

    def processing(self):
        import inspect; import os; frame = inspect.currentframe(); print(f"DEBUG: {os.path.basename(frame.f_code.co_filename)}: {frame.f_lineno}: {self.__class__.__name__}.{frame.f_code.co_name}: called")
        try:
            self._processing()
        except Exception as e:
            import sys
            import traceback
            print(traceback.format_exception(*sys.exc_info()))
            print(traceback.format_tb(e.__traceback__))

    def _processing(self):
        # First we check whether we are at the end of the round
        if self.frameData.getEmptyFlag() or self.frameData.getRemainingFramesNumber() <= 0:
            self.isGameJustStarted = True
            return
        if not self.isGameJustStarted:
            # Simulate the delay and look ahead 2 frames. The simulator class exists already in FightingICE
            self.frameData = self.simulator.simulate(self.frameData, self.player, None, None, 17)
            # You can pass actions to the simulator by writing as follows:
            # actions = self.gateway.jvm.java.util.ArrayDeque()
            # actions.add(self.gateway.jvm.enumerate.Action.STAND_A)
            # self.frameData = self.simulator.simulate(self.frameData, self.player, actions, actions, 17)
        else:
            # If the game just started, no point on simulating
            self.isGameJustStarted = False

        self.cc.setFrameData(self.frameData, self.player)

        if self.cc.getSkillFlag():
            self._skill_flag_continue_count += 1

            # If there is a previous "command" still in execution, then keep doing it
            self.inputKey = self.cc.getSkillKey()

            # The case simulator seems to be broken.
            if self._skill_flag_continue_count >= self.THRESHOLD_FRAME_COUNT_FOR_THE_CASE_SIMULATOR_BROKEN:
                print('=' * 100)
                print('ERROR: self._skill_flag_continue_count >= self.THRESHOLD_FRAME_COUNT_FOR_THE_CASE_SIMULATOR_BROKEN')
                print('=' * 100)
                self.cc.skillCancel()
        else:
            self._skill_flag_continue_count = 0

            # We empty the keys and cancel skill just in case
            # self.inputKey.empty()
            # self.cc.skillCancel()

            inputs = self.policy(self.frameData)

            if inputs is None:
                xs = [Action.NEUTRAL]
            elif type(inputs) is not list:
                assert inputs in Action
                xs = [inputs]
            else:
                xs = inputs

            command = ' '.join([x.value for x in xs])
            print(command)
            self.cc.commandCall(command)

    # def processing(self):
    #     # Just compute the input for the current frame
    #     if self.frameData.getEmptyFlag() or self.frameData.getRemainingFramesNumber() <= 0:
    #         self.isGameJustStarted = True
    #         return

    #     # Just spam kick
    #     self.cc.setFrameData(self.frameData, self.player)
    #     # distance = self.frameData.getDistanceX()
    #     # my = self.frameData.getCharacter(self.player)
    #     # energy = my.getEnergy()
    #     # my_x = my.getX()
    #     # my_state = my.getState()
    #     # opp = self.frameData.getCharacter(not self.player)
    #     # opp_x = opp.getX()
    #     # opp_state = opp.getState()
    #     # xDifference = my_x - opp_x
    #     if self.cc.getSkillFlag():
    #         self.inputKey = self.cc.getSkillKey()
    #         return

    #     self.inputKey.empty()
    #     self.cc.skillCancel()

    #     a = self.policy(self.frameData)
    #     dic = {
    #         "↙": "1", "↓": "2", "↘": "3",
    #         "←": "4",           "→": "6",
    #         "↖": "7", "↑": "8", "↗": "9"
    #     }
    #     if a is not None:
    #         for k, v in dic.items():
    #             a = a.replace(k, v)
    #         self.cc.commandCall(a)
    #     else:
    #         self.cc.commandCall("_")

    #     # self.sendCommand()

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
